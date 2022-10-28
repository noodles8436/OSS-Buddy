import asyncio
import threading
import PROTOCOL as p
from queue import Queue


class GlobalServer:
    def __init__(self, ip: str, port: int):
        self.globalServer = None
        self.ip = ip
        self.port = port
        self.Servers = list()
        self.RequestQueue = Queue()
        self.assignor = threading.Thread(target=self.assignManager)
        self.assignIndex = 0

    async def run_server(self) -> None:
        self.globalServer = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with self.globalServer:
            await self.globalServer.serve_forever()

    # ==============================[ Main ]=================================

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:

        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
        msg = data.decode().split(p.TASK_SPLIT)

        client_addr = writer.get_extra_info('peername')

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

        writer.close()

    async def serverHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        pass

    async def clientHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        pass

    # ==========================[ AssignManager ]============================
    def assignManager(self):
        pass

    def startManager(self):
        pass

    def stopManager(self):
        pass

    # ==============================[ QUEUE ]=================================

    def addQueue(self):
        pass

    def delQueue(self):
        pass

    # ============================[ ASSIGNMENT ]==============================

    def assignServer(self):
        pass

    def assignComplete(self):
        pass

    def isServerAssigned(self):
        pass

    # ==============================[ SERVER ]================================

    def addDeployServer(self, ip: str) -> str:
        pass

    def delDeployServer(self, ip: str) -> str:
        pass

    def isServerExist(self, ip: str) -> bool:
        pass

    # ==============================[ CLIENT ]================================

    def addClient(self, ip: str) -> str:
        return p.CLIENT_LOGIN_SUCCESS

    def delClient(self, ip: str) -> str:
        pass

    def isClientExist(self, ip: str) -> bool:
        return False
