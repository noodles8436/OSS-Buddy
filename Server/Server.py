import asyncio


class Server:

    # 작업번호:내용
    
    # (사용자 등록) 00;이름;전화번호;맥주소
    # (Res. 사용자 등록) 성공 = 00;00 or 실패 = 00;01
    
    # (사용자 로그인) 01;이름;전화번호;맥주소
    # (Res. 사용자 로그인) 성공 = 01;00 or 실패 = 01;01 <실패시 바로 접속끊기>
    
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
    
    # (RaspBerry 주변 새로은 MAC 유저 확인 ) 33;mac
    # (Res. RaspBerry 주변 새로은 MAC 유저 확인 ) 있는 유저 = 33;00 or 없는 유저 = 33;01

    # (RaspBerry 주변 등록된 유저 사라짐 ) 34;mac

    def __init__(self):
        self.ip = "localhost"
        self.port = 7777
        self.packetSize = 1024
        self.busReserveDict = {}
        self.userBusStopDict = {}

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data: bytes = await reader.read(self.packetSize)
        msg = data.decode().split(';')
        
        if msg[0] == "00":
            pass

        elif msg[0] == "01":  # User Login
            pass

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

    def buscheck(self):
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
