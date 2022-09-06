import asyncio
import UserManager
import PROTOCOL as p


class Server:

    def __init__(self, ip, port):
        self.server = None
        self.ip = ip
        self.port = port
        self.userMgr = UserManager.UserManager()

    async def run_server(self) -> None:
        self.server = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with self.server:
            await self.server.serve_forever()

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
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
            if len(msg) == 4:
                msg_result = p.RASP_INFO_LOGIN_SUCCESS
            else:
                msg_result = p.RASP_INFO_LOGIN_FAIL

            writer.write(msg_result)
            await writer.drain()

            if msg_result == p.RASP_INFO_LOGIN_SUCCESS:
                await self.RaspInfoHandler(reader=reader, writer=writer, nodeId=msg[1],
                                           lati=float(msg[2]), long=float(msg[3]))

        elif msg[0] == "40":  # Raspberry PI Detector Connection
            if len(msg) == 2:
                msg_result = p.RASP_DETECTOR_LOGIN_SUCCESS
            else:
                msg_result = p.RASP_DETECTOR_LOGIN_FAIL

            writer.write(msg_result)
            await writer.drain()

            if msg_result == p.RASP_DETECTOR_LOGIN_SUCCESS:
                await self.RaspDetectorHandler(reader=reader, writer=writer, nodeId=msg[1])

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
                                if self.isBusAlarmTime(userMac=userMac) is True:
                                    self.AlarmUser(userMac=userMac)
                                    break

            # 클라이언트 위치 확인 안됨
            msg_result = p.USER_LOCATION_FIND_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

    async def userGPSHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, userMac: str):
        pass

    async def RaspInfoHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, nodeId: str,
                              lati: float, long: float):
        pass

    async def RaspDetectorHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, nodeId: str):
        pass

    async def BusDriverHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, vehlcleNo: str):
        pass

    async def connectionCheck(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        msg = p.CONNECTION_CHECK
        writer.write(msg.encode())
        await writer.drain()

        try:
            await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE), timeout=p.TIMEOUT_SEC)
        except asyncio.TimeoutError:
            return False

        return True

    def busCheck(self, userMac: str, routeNo: str) -> str:
        pass

    def busReservation(self, userMac: str, routeNo: str) -> str:
        pass

    def busCancel(self, userMac: str) -> str:
        pass

    def isBusReserved(self) -> bool:
        pass

    def isBusAlarmTime(self, userMac: str) -> bool:
        pass

    def AlarmUser(self, userMac: str):
        pass


if __name__ == "__main__":
    server = Server(ip='localhost', port=7777)
    asyncio.run(server.run_server())
