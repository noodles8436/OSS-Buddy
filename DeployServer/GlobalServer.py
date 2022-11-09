import asyncio
import sys
import threading

import cv2
import numpy as np

import PROTOCOL as p
from queue import Queue
from Assignment import Assignment, DetectResult, getDumpFromObject, loadDataFromDump
from ServerInfo import ServerInfo
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
        self.assignIndex = 0
        self.assignDone = dict()
        self.assigner = threading.Thread(target=self.assignManager)
        self.startManager()

    async def run_server(self) -> None:
        self.globalServer = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with self.globalServer:
            await self.globalServer.serve_forever()

    # ==============================[ Main ]=================================

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client_addr = writer.get_extra_info('peername')
        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
        msg = data.decode().split(p.TASK_SPLIT)

        print('ACCESS : ', client_addr)

        if msg[0] == p.DEPLOY_SERVER_LOGIN:
            msg_result = self.addDeployServer(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.DEPLOY_SERVER_LOGIN_SUCCESS:
                print('Deploy Server login Success!')
                await self.serverHandler(reader=reader, writer=writer)
            else:
                print('Deploy Server login Failed...')

        elif msg[0] == p.CLIENT_LOGIN:
            msg_result = self.addClient(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.CLIENT_LOGIN_SUCCESS:
                print('App Client login Success!')
                await self.clientHandler(reader=reader, writer=writer)
            else:
                print('App Client login Failed...')

        elif msg[0] == p.CLIENT_RASPBERRY_LOGIN:
            msg_result = self.addClient(client_addr)

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.CLIENT_LOGIN_SUCCESS:
                print('Raspberry PI login Success!')
                await self.clientHandler(reader=reader, writer=writer, isRaspberry=True)
            else:
                print('Raspberry PI login Failed...')

        writer.close()

    async def serverHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        server_addr = writer.get_extra_info('peername')

        try:
            while True:
                if self.isServerExist(server_addr) is False:
                    print(server_addr, ' Server is Logout!')
                    break

                serverInfo: ServerInfo = self.getServerInfo(server_addr)
                if serverInfo is None:
                    print(server_addr, ' There is No Server INFO ')
                    break

                print(server_addr, ' Wait Work...')
                # Server is Not Assigned work
                if serverInfo.isAssigned() is False:
                    await asyncio.sleep(1)
                    continue

                # server is Assigned work
                print(server_addr, ' server is Assigned! ')
                assignment: Assignment = serverInfo.getAssign()
                bytes_img: bytes = assignment.getDump_Images()

                writer.write(bytes_img)
                await writer.drain()

                DetectResult_Dump: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                assignment.setDetectResult_FromDump(bytes_result=DetectResult_Dump)

                detectResult: DetectResult = assignment.getDetectResult()
                print(detectResult.getResult_Understanding())

                self.assignServer_Complete(server_ip=server_addr)

        except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
            self.delDeployServer(server_ip=server_addr)
            return

        self.delDeployServer(server_ip=server_addr)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return

    async def clientHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                            isRaspberry=False) -> None:
        client_addr = writer.get_extra_info('peername')
        while True:
            try:
                if isRaspberry:
                    print(client_addr, 'Try To Read Images')
                    bytes_imgs: bytes = bytes()
                    while True:
                        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                        bytes_imgs += data
                        if len(data) < p.SERVER_PACKET_SIZE:
                            break

                    print(client_addr, 'Image Readed!')
                    print(sys.getsizeof(bytes_imgs))
                    np_imgs: np.ndarray = loadDataFromDump(bytes_imgs)
                    print(client_addr, 'image shapes : ', np_imgs.shape)

                else:
                    recv_imgs = list()
                    print(client_addr, 'Try To Read Images')
                    for i in range(FPS):
                        try:
                            bytes_img: bytes = bytes()
                            print(client_addr, 'Try To Read Image')
                            while True:
                                data: bytes = await asyncio.wait_for(reader.read(), p.TIME_OUT)
                                bytes_img += data
                                if len(data) < p.SERVER_PACKET_SIZE:
                                    break

                            cv_img: np.ndarray = cv2.imdecode(bytes_img, cv2.IMREAD_COLOR)
                            recv_imgs.append(cv_img)

                        except asyncio.TimeoutError:
                            self.delClient(client_addr)
                    np_imgs: np.ndarray = np.array(recv_imgs)
                    print(client_addr, 'image shapes : ', np_imgs.shape)

                new_assignment = Assignment(client_ip=client_addr, images=np_imgs)
                self.EnQueue(new_assignment)

                print(client_addr, 'Waiting until work done...')
                while True:
                    if self.isClient_AssignComplete(client_ip=client_addr) is True:
                        break
                    await asyncio.sleep(1)
                print(client_addr, 'Work Done!')

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
                                bytes_result: bytes = str(detectResult.getCanSitCnt()).encode()
                        else:
                            bytes_result: bytes = p.CLIENT_ASSIGN_FAIL

                writer.write(bytes_result)
                await writer.drain()

            except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError) as e:
                self.delClient(ip=client_addr)
                print('Connection Error')
                break

            except Exception as e:
                self.delClient(ip=client_addr)
                print(str(e))
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                break

    # ==========================[ AssignManager ]============================
    def assignManager(self):
        while self.assignerStatus:
            while not self.isQueueEmpty():
                print('[Assign Manager] NEW WORK Detected!')
                assignment: Assignment = self.DeQueue()
                client_ip = assignment.getClient_IP()
                print('[Assign Manager] NEW WORK from', client_ip)

                if len(self.Servers.keys()) == 0:
                    print('[Assign Manager] There is no available servers..')
                    self.assignDone[client_ip] = assignment
                    continue

                self.assignIndex %= len(self.Servers.keys())
                serverDictKey: str = list(self.Servers.keys())[self.assignIndex]
                assignServer: ServerInfo = self.getServerInfo(serverDictKey)

                print('[Assign Manager] Target Server -> ', serverDictKey, assignServer)

                if assignServer is None:
                    continue

                assignServer.setAssign(assignment=assignment)
                print('[Assign Manager] Assigned!')

                self.assignIndex += 1

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
        self.Servers.__delitem__(server_ip)
        print(' Server is Logout! : ', server_ip)

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
        print(ip, ' Client Logout ')

    def isClientExist(self, ip: str) -> bool:
        return ip in self.Clients


if __name__ == "__main__":
    print('        [ OSS Buddy Project ]       '.center(75))
    print('')
    ip = input("[Deploy Server] 호스트 IP 를 입력하세요 (ex 192.168.0.1) : ")
    port = int(input("[Deploy Server] 호스트 PORT 를 입력하세요 (ex 8877) : ", ))
    globalServer = GlobalServer(ip=ip, port=port)
    asyncio.run(globalServer.run_server())
