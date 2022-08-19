import asyncio
import UserManager
import PROTOCOL as p


class Server:

    # 작업번호:내용

    # (사용자 등록) 00;이름;전화번호;맥주소
    # (Res. 사용자 등록) 성공 = 00;00 or 실패 = 00;01 -> 클라는 연결을 한번 끊고 다시 시도해야함

    # (사용자 로그인) 01;이름;전화번호;맥주소
    # (Res. 사용자 로그인) 성공 = 01;00 or 실패 = 01;01 <실패시 바로 접속끊기> or 실패_서버문제 = 01;02 or 실패_클라문제 = 01;03

    # (Res. 사용자 위치 확인) 성공 = 02;00 or 실패 = 02;01

    # (사용자 버스 예약) 03;버스번호
    # (Res. 사용자 버스 예약) 예약 가능한 버스 = 03;00, 예약 불가능한 버스 = 03;01

    # (사용자 버스 예약 확정) 04;버스번호
    # (Res. 사용자 버스 예약 확정) 성공 = 04;00, 실패 = 04;01

    # (사용자 버스 예약 취소) 05;00
    # (Res. 사용자 버스 예약 취소) 성공 = 05;00, 실패 = 05;01

    # (사용자 버스 도착 진동) 06;00

    # (버스기사 등록) 20;차량번호;이름;맥주소
    # (Res. 버스기사 등록) 성공 = 20;00 or 실패 = 20;01

    # (버스기사 로그인) 21;차량번호;이름;맥주소
    # (Res. 버스기사 로그인) 성공 = 21;00 or 실패 = 21;01

    # (버스기사 알림) 22;정거장이름;남은 정거장 수

    # (RaspBerry 연결) 30;nodeid;mac
    # (Res. RaspBerry 연결) 성공 = 30;00 or 실패 = 30;01

    # (RaspBerry 초접근 버스 안내) 32;routeid;routeNo

    # (RaspBerry 주변 새로은 MAC 유저 확인 ) 33;mac;nodeid
    # (Res. RaspBerry 주변 새로은 MAC 유저 확인 ) 있는 유저 = 33;00 or 없는 유저 = 33;01

    # (RaspBerry 주변 등록된 유저 사라짐) 34;usermac;nodeid

    def __init__(self):
        self.ip = "localhost"
        self.port = 7777
        self.packetSize = 1024
        self.userMgr = UserManager.UserManager()

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data: bytes = await reader.read(self.packetSize)
        msg = data.decode().split(';')

        if msg[0] == p.USER_REGISTER:
            if len(msg) == 4:
                msg_result = self.userMgr.register(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_REGISTER_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

        elif msg[0] == p.USER_LOGIN:  # User Login
            if len(msg) == 4:
                msg_result = self.userMgr.login(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_LOGIN_CLIENT_ERR

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.USER_LOGIN_SUCCESS:
                await self.userHandler(reader=reader, writer=writer)

        elif msg[0] == "20":  # Bus Driver Login
            pass

        elif msg[0] == "21":  # Bus Driver Login
            pass

        elif msg[0] == "30":  # Raspberry PI Connection
            pass

    async def userHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        print(f"[SERVER] {peername} is connected!")
        while True:
            # 클라이언트가 보낸 내용을 받기
            data: bytes = await reader.read(self.packetSize)
            # 받은 내용을 출력하고,
            # 가공한 내용을 다시 내보내기
            if len(data) == 0:
                print(f"[SERVER] {peername} is disconnected...")
                break

            print(f"[S] received: {len(data)} bytes from {peername}")
            mes = data.decode()
            print(f"[S] message: {mes}")
            res = mes.upper()
            writer.write(res.encode())
            await writer.drain()

    async def run_server(self) -> None:
        server = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with server:
            await server.serve_forever()

    def busCheck(self):
        pass

    def busReservation(self):
        pass

    def busCancel(self):
        pass

    def isBusReserved(self):
        pass

    def isBusAlarmTime(self):
        pass


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run_server())
