import asyncio
import PROTOCOL as p

async def run_client(host: str, port: int):
    # 서버와의 연결을 생성합니다.
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(host, port)
    # show connection info
    print("[C] connected")
    # 루프를 돌면서 입력받은 내용을 서버로 보내고,
    # 응답을 받으면 출력합니다.

    line = input("[C] enter message: ")
    # 입력받은 내용을 서버로 전송

    payload = line.encode()
    writer.write(payload)
    await writer.drain()

    print(f"[C] sent: {len(payload)} bytes.\n")

    test_num = 0

    while True:

        # 서버로부터 받은 응답을 표시
        data = await reader.read(1024)  # type: bytes
        print(f"[C] received: {len(data)} bytes")
        print(f"[C] message: {data.decode()}")

        if data.decode() == p.CONNECTION_CHECK and test_num < 5:
            payload = p.CONNECTION_CHECK
            writer.write(payload.encode())
            await writer.drain()
            test_num += 1

        if data.decode() == p.KICK_USER:
            break

    # 연결을 종료합니다.
    print("[C] closing connection...")
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(run_client("localhost", 7777))
