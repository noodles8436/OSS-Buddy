import asyncio
import numpy as np
import PROTOCOL as p
from Model import Model
from Assignment import DetectResult, loadDataFromDump, getDumpFromObject


class DeployServer:

    def __init__(self, host: str, port: int):
        self.model = Model()
        self.host = host
        self.port = port

    async def start(self):
        self.serverTask = await asyncio.tasks.create_task(self.run())

    async def run(self):
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        while True:
            try:
                print('[Deploy Server] Try to Connect to Global Server')
                reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
                print('[Deploy Server] Global Server Connected!')

                print('[Deploy Server] Try to Login to Global Server')
                msg = p.DEPLOY_SERVER_LOGIN
                writer.write(msg.encode())
                await writer.drain()

                recv: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                msg: str = recv.decode()

                if msg != p.DEPLOY_SERVER_LOGIN_SUCCESS:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()
                    print('[Deploy Server] Failed to Login to Global Server\n\n')
                    await asyncio.sleep(1)
                    continue
                print('[Deploy Server] Successfully Logined to Global Server\n\n')

                while True:
                    print('[Deploy Server] Waiting Assignment from global server')
                    recv: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                    images: np.ndarray = loadDataFromDump(recv)
                    print('[Deploy Server] Assigned! Received images...')

                    print('[Deploy Server] predict images using model...')
                    _pred_Bus, _pred_Person, top_classes, top_labels = self.predict(images)

                    print('[Deploy Server] predicted! create detect result object...')
                    result: DetectResult = DetectResult()
                    result.setResult_OCR(_pred_Bus)
                    result.setResult_ObjDetection(_pred_Person)
                    result.setResult_Understanding(top_classes)
                    result.setComplete()

                    print('[Deploy Server] object created! send detect result object to server')
                    msg: bytes = getDumpFromObject(result)
                    writer.write(msg)
                    await writer.drain()

                    print('[Deploy Server] Assigned work was done!\n')

            except (ConnectionError, ConnectionRefusedError,
                    ConnectionResetError, ConnectionAbortedError) as e:
                print('[Deploy Server] Error : ', str(e), '\n\n')
                await asyncio.sleep(1)

            except Exception as e:
                print('[Deploy Server] Error : ', str(e))
                print('[Deploy Server] Close Connection..Retry to Connect\n\n')
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()
                await asyncio.sleep(1)

    def predict(self, images: np.ndarray):
        _pred_Bus, top_scores, top_classes, top_labels = self.model.understanding(images)
        return _pred_Bus, top_scores, top_classes, top_labels


if __name__ == "__main__":
    print('        [ OSS Buddy Project ]       '.center(75))
    print('')
    host = input("[Deploy Server] 호스트 IP 를 입력하세요 (ex 192.168.0.1) : ")
    port = int(input("[Deploy Server] 호스트 PORT 를 입력하세요 (ex 8877) : ", ))
    deployServer = DeployServer(host=host, port=port)
    asyncio.run(deployServer.run())
