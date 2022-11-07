import asyncio
import threading

import cv2
import numpy as np

import PROTOCOL as p
from queue import Queue
from Assignment import Assignment, DetectResult, getDumpFromObject
from DeployServer.ServerInfo import ServerInfo
from Model import FPS


class GlobalServer:
    def __init__(self, ip: str, port: int):
        self.globalServer = None
        self.ip = ip
        self.port = port
        self.Servers = dict()
        self.Clients = list()

        self.RequestQueue = Queue()
        self.assignerStatus = False
        self.assigner = threading.Thread(target=self.assignManager)
        self.assignIndex = 0
        self.assignDone = dict()

    async def run_server(self) -> None:
        self.globalServer = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with self.globalServer:
            await self.globalServer.serve_forever()

    # ==============================[ Main ]=================================

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client_addr = writer.get_extra_info('peernamwre')
        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
        msg = data.decode().split(p.TASK_SPLIT)

        if msg[0] == p.DEPLOY_SERVER_LOGIN:
            msg_result = self.addDeployServer(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.DEPLOY_SERVER_LOGIN_SUCCESS:
                await self.serverHandler(reader=reader, writer=writer)

        elif msg[0] == p.CLIENT_LOGIN:
            msg_result = self.addClient(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.CLIENT_LOGIN_SUCCESS:
                await self.clientHandler(reader=reader, writer=writer)

        elif msg[0] == p.CLIENT_RASPBERRY_LOGIN:
            msg_result = self.addClient(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.CLIENT_LOGIN_SUCCESS:
                await self.clientHandler(reader=reader, writer=writer, isRaspberry=True)

        writer.close()

    async def serverHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        server_addr = writer.get_extra_info('peername')

        try:
            while True:
                if self.isServerExist(server_addr) is False:
                    break

                serverInfo: ServerInfo = self.getServerInfo(server_addr)
                if serverInfo is None:
                    break

                # Server is Not Assigned work
                if serverInfo.isAssigned() is False:
                    continue

                # server is Assigned work
                assignment: Assignment = serverInfo.getAssign()
                bytes_img: bytes = assignment.getDump_Images()

                writer.write(bytes_img)
                await writer.drain()

                DetectResult_Dump: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                assignment.setDetectResult_FromDump(bytes_result=DetectResult_Dump)

                self.assignServer_Complete(server_ip=server_addr)

        except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
            self.delDeployServer(server_ip=server_addr)
            await writer.drain()
            writer.close()
            await writer.wait_closed()

        self.delDeployServer(server_ip=server_addr)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def clientHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                            isRaspberry=False) -> None:
        client_addr = writer.get_extra_info('peername')

        while True:
            try:
                recv_imgs = list()
                for i in FPS:
                    try:
                        bytes_img: bytes = await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE),
                                                                  p.TIME_OUT)
                        cv_img: np.ndarray = cv2.imdecode(bytes_img, flags=1)
                        recv_imgs.append(cv_img)

                    except asyncio.TimeoutError:
                        pass

                np_imgs: np.ndarray = np.array(recv_imgs)
                new_assignment = Assignment(client_ip=client_addr, images=np_imgs)
                self.EnQueue(new_assignment)

                while True:
                    if self.isClient_AssignComplete(client_ip=client_addr) is True:
                        break

                completed_assign: Assignment = self.getClient_AssignComplete(client_ip=client_addr)

                if completed_assign is None:
                    bytes_result: bytes = p.CLIENT_ASSIGN_FAIL

                else:
                    detectResult: DetectResult = completed_assign.getDetectResult()
                    if detectResult is None:
                        bytes_result: bytes = p.CLIENT_ASSIGN_FAIL
                    else:

                        if detectResult.getComplete():
                            if isRaspberry:
                                bytes_result: bytes = getDumpFromObject(detectResult)
                            else:
                                bytes_result: bytes = detectResult.toString().encode()
                        else:
                            bytes_result: bytes = p.CLIENT_ASSIGN_FAIL

                writer.write(bytes_result)
                await writer.drain()

            except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
                self.delClient(ip=client_addr)
                break

    # ==========================[ AssignManager ]============================
    def assignManager(self):
        while self.assignerStatus:
            while not self.isQueueEmpty():
                assignment: Assignment = self.DeQueue()
                client_ip = assignment.getClient_IP()

                if len(self.Servers.keys()) == 0:
                    self.assignDone[client_ip] = assignment

                self.assignIndex %= (len(self.Servers.keys()) + 1)
                serverDictKey: str = list(self.Servers.keys())[self.assignIndex]
                assignServer: ServerInfo = self.getServerInfo(serverDictKey)

                if assignServer is None:
                    continue

                assignServer.setAssign(assignment=assignment)

    def startManager(self):
        if self.assignerStatus is True:
            self.stopManager()
        self.assignerStatus = True
        self.assigner.start()

    def stopManager(self):
        self.assignerStatus = False

    def isManagerActive(self):
        return self.assignerStatus

    # ==============================[ QUEUE ]=================================

    def EnQueue(self, assign: Assignment) -> bool:
        if self.isQueueFull() is True:
            return False
        self.RequestQueue.put(assign)
        return True

    def DeQueue(self) -> Assignment or None:
        if self.isQueueEmpty():
            return None
        return self.RequestQueue.get()

    def isQueueEmpty(self):
        return self.RequestQueue.empty()

    def isQueueFull(self):
        return self.RequestQueue.full()

    # ============================[ ASSIGNMENT ]==============================

    def assignServer(self, server_ip: str, assignment: Assignment) -> bool:
        if self.isServerAssigned(server_ip=server_ip) is True:
            return False

        server: ServerInfo = self.Servers[server_ip]
        server.setAssign(assignment=assignment)
        return True

    def assignServer_Complete(self, server_ip: str):
        if self.isServerExist(ip=server_ip) is False:
            return

        serverinfo: ServerInfo = self.getServerInfo(ip=server_ip)
        assign_done: Assignment = serverinfo.getAssign()
        request_client_ip: str = assign_done.getClient_IP()

        self.assignDone[request_client_ip] = assign_done
        serverinfo.delAssign()

    def isServerAssigned(self, server_ip: str) -> bool:
        if self.isServerExist(ip=server_ip) is False:
            return False

        serverinfo: ServerInfo = self.getServerInfo(ip=server_ip)
        return serverinfo.isAssigned()

    def isClient_AssignComplete(self, client_ip: str):
        if client_ip in self.assignDone.keys():
            return True
        return False

    def getClient_AssignComplete(self, client_ip: str) -> Assignment or None:
        if client_ip in self.assignDone.keys():
            result: Assignment = self.assignDone[client_ip]
            del self.assignDone[client_ip]
            return result
        return None

    # ==============================[ SERVER ]================================

    def addDeployServer(self, ip: str) -> str:
        if self.isServerExist(ip):
            return p.DEPLOY_SERVER_LOGIN_FAIL
        self.Servers[ip] = ServerInfo(server_ip=ip)
        return p.DEPLOY_SERVER_LOGIN_SUCCESS

    def delDeployServer(self, server_ip: str) -> None:
        if self.isServerExist(ip=server_ip) is False:
            return

        serverinfo: ServerInfo = self.getServerInfo(ip=server_ip)
        if serverinfo.isAssigned() is True:
            self.assignServer_Complete(server_ip=server_ip)

        del self.Servers[server_ip]

    def isServerExist(self, ip: str) -> bool:
        if ip in self.Servers.keys():
            return True
        return False

    def getServerInfo(self, ip: str) -> ServerInfo or None:
        if self.isServerExist(ip) is True:
            return self.Servers[ip]
        return None

    # ==============================[ CLIENT ]================================

    def addClient(self, ip: str) -> str:
        if ip in self.Clients:
            return p.CLIENT_LOGIN_FAIL
        self.Clients.append(ip)
        _ = self.getClient_AssignComplete(ip)
        return p.CLIENT_LOGIN_SUCCESS

    def delClient(self, ip: str) -> None:
        if ip in self.Clients:
            self.Clients.remove(ip)
            _ = self.getClient_AssignComplete(ip)

    def isClientExist(self, ip: str) -> bool:
        return ip in self.Clients


if __name__ == "__main__":
    print('        [ OSS Buddy Project ]       '.center(75))
    print('')
    ip = input("[Deploy Server] 호스트 IP 를 입력하세요 (ex 192.168.0.1) : ")
    port = int(input("[Deploy Server] 호스트 PORT 를 입력하세요 (ex 8877) : ", ))
    GlobalServer(ip=ip, port=port)
