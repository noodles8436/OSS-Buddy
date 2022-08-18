import asyncio


class Server:

    def __init__(self):
        self.ip = "localhost"
        self.port = 7777
        self.packetSize = 1024

    async def handler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peername = writer.get_extra_info('peername')
        print(f"[SERVER] {peername} is connected!")
        while True:
            # 클라이언트가 보낸 내용을 받기
            data: bytes = await reader.read(1024)
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
        server = await asyncio.start_server(self.handler, host=self.ip, port=self.port)
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run_server())
