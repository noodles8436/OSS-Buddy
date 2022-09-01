import asyncio
import UserManager
import PROTOCOL as p


class Server:

    def __init__(self):
        self.ip = "localhost"
        self.port = 7777
        self.packetSize = 1024
        self.userMgr = UserManager.UserManager()

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data: bytes = await reader.read(self.packetSize)
        msg = data.decode().split(p.TASK_SPLIT)

        if msg[0] == p.USER_REGISTER:  # User Register
            if len(msg) == 4:
                msg_result = self.userMgr.userRegister(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_REGISTER_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

        elif msg[0] == p.USER_LOGIN:  # User Login
            if len(msg) == 4:
                msg_result = self.userMgr.userLogin(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_LOGIN_CLIENT_ERR

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.USER_LOGIN_SUCCESS:
                await self.userHandler(reader=reader, writer=writer, userName=msg[1],
                                       userPhone=msg[2], userMac=msg[3])

        elif msg[0] == "20":  # Bus Driver Login
            pass

        elif msg[0] == "21":  # Bus Driver Login
            pass

        elif msg[0] == "30":  # Raspberry PI InfoProvider Connection
            pass

        elif msg[0] == "40":  # Raspberry PI Detector Connection
            pass

        writer.close()

    async def userHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                          userName: str, userPhone: str, userMac: str):
        peername = writer.get_extra_info('peername')
        print(f"[SERVER] {peername} is connected!")
        while True:
            # 클라이언트 위치 확인
            while self.userMgr.getUserLocation(mac_add=userMac) is None:
                await asyncio.sleep(p.LOCATION_SEARCH_TERM)
                connectCheck = await self.connectionCheck(reader=reader, writer=writer)
                if connectCheck is False:
                    msg_result = p.KICK_USER
                    writer.write(msg_result.encode())
                    await writer.drain()
                    print(f"[SERVER] {peername} is disconnected!")
                    return

            msg_result = p.USER_LOCATION_FIND_SUCCESS
            writer.write(msg_result.encode())
            await writer.drain()

            # 클라이언트 위치 이후 처리
            while self.userMgr.getUserLocation(mac_add=userMac) is not None:
                # 예약, 취소 명령 받기
                data = await reader.read(p.SERVER_PACKET_SIZE)
                msg = data.decode().split(p.TASK_SPLIT)

                if msg[0] == p.USER_BUS_CAN_RESERVATION:
                    if len(msg) == 2:
                        msg_result = self.busCheck(userMac=userMac, routeNo=msg[1])
                    else:
                        msg_result = p.USER_BUS_CAN_RESERVATION_NO

                    writer.write(msg_result.encode())
                    await writer.drain()

                elif msg[0] == p.USER_BUS_RESERVATION_CONFIRM:
                    if len(msg) == 2:
                        msg_result = self.busReservation(userMac=userMac, routeNo=msg[1])
                    else:
                        msg_result = p.USER_BUS_RESERVATION_CONFIRM_FAIL

                    writer.write(msg_result.encode())
                    await writer.drain()

                    if msg_result == p.USER_BUS_RESERVATION_CONFIRM_SUCCESS:
                        while True:
                            try:
                                data: bytes = await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE),
                                                                     p.BUS_REALTIME_SEARCH_TERM)
                                isCancel = data.decode().split(p.TASK_SPLIT)[0]
                                if isCancel == p.USER_BUS_CANCEL:
                                    msg_result = self.busCancel(userMac=userMac)
                                    writer.write(msg_result.encode())
                                    await writer.drain()
                                    break

                            except asyncio.TimeoutError:
                                if self.isBusAlarmTime() is True:
                                    self.AlarmUser(userMac=userMac)
                                    break

            # 클라이언트 위치 확인 안됨
            msg_result = p.USER_LOCATION_FIND_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

    async def connectionCheck(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        msg = p.CONNECTION_CHECK
        writer.write(msg.encode())
        await writer.drain()

        try:
            await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE), timeout=p.TIMEOUT_SEC)
        except asyncio.TimeoutError:
            return False

        return True

    async def run_server(self) -> None:
        server = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with server:
            await server.serve_forever()

    def busCheck(self, userMac: str, routeNo: str) -> str:
        pass

    def busReservation(self, userMac: str, routeNo: str) -> str:
        pass

    def busCancel(self, userMac: str) -> str:
        pass

    def isBusReserved(self) -> bool:
        pass

    def isBusAlarmTime(self, userMac: str):
        pass

    def AlarmUser(self, userMac: str):
        pass


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run_server())
