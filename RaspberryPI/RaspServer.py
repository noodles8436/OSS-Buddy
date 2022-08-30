import asyncio
import Server.PROTOCOL as p
import BusManager
import Detector


class RaspMain:

    def __init__(self, host: str, port: int):
        self.busManager = BusManager.BusManager()
        self.Detector = Detector.Detector()
        self.host = host
        self.port = port
        self.serverTask = asyncio.gather(self.busDetector(), self.infoProvider())

    def start(self):
        asyncio.run(self.serverTask)

    async def busDetector(self) -> None:
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        while True:
            try:
                print("[Rasp Detector] Try to Connect Server")
                reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
                print("[Rasp Detector] Server Connected")

                msg = p.RASP_DETECTOR_LOGIN + p.TASK_SPLIT + self.busManager.getNodeId()
                writer.write(msg.encode())
                await writer.drain()
                print("[Rasp Detector] Try to Login Server")

                recv = await reader.read(p.SERVER_PACKET_SIZE)

                if recv != p.RASP_DETECTOR_LOGIN_SUCCESS:
                    print("[Rasp Detector][ERR] Server Login Failed!")
                    continue

                print("[Rasp Detector] Server Login Success")

                while True:
                    # Detecting Bus and send to Server
                    pass

            except Exception as e:
                print(e.args[0])
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()

    async def infoProvider(self) -> None:
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        while True:
            try:
                print("[Rasp INFO] Try to Connect Server")
                reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
                print("[Rasp INFO] Server Connected")

                msg = p.RASP_INFO_LOGIN + p.TASK_SPLIT + self.busManager.getNodeId()
                writer.write(msg.encode())
                await writer.drain()
                print("[Rasp INFO] Try to Login Server")

                recv = await reader.read(p.SERVER_PACKET_SIZE)

                if recv != p.RASP_INFO_LOGIN_SUCCESS:
                    print("[Rasp INFO][ERR] Server Login Failed!")
                    continue

                print("[Rasp INFO] Server Login Success")

                while True:
                    # Repeat : listening server and answer to server
                    pass

            except Exception as e:
                print(e.args[0])
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()


if __name__ == "__main__":
    main = RaspMain(host=p.SERVER_IP, port=p.SERVER_PORT)
    main.start()
