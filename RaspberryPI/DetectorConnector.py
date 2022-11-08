import asyncio
from Assignment import DetectResult, getDumpFromObject, loadDataFromDump
from PROTOCOL import GLOBAL_SERVER_PACKET_SIZE
import numpy as np


class DetectorConnector:

    def __init__(self, ip: str, port: int):
        self.writer = None
        self.reader = None
        self.globalServer_ip = ip
        self.globalServer_port = port

        asyncio.run(self.connectServer())

        print('[Detector-Connector] reader -> ', self.reader)
        print('[Detector-Connector] writer -> ', self.writer)

    def detect(self, images: np.ndarray) -> DetectResult:
        return asyncio.run(self.run(images=images))

    async def connectServer(self):
        reader, writer = await asyncio.open_connection(host=self.globalServer_ip, port=self.globalServer_port)
        self.reader = reader
        self.writer = writer

    async def disconnectServer(self):
        if self.writer is not None:
            try:
                await self.writer.drain()
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass

        self.writer = None
        self.reader = None

    async def run(self, images: np.ndarray) -> DetectResult:
        self.writer: asyncio.StreamWriter
        self.reader: asyncio.StreamReader
        bytes_img: bytes = getDumpFromObject(images)

        self.writer.write(bytes_img)
        await self.writer.drain()

        bytes_result: bytes = await self.reader.read(GLOBAL_SERVER_PACKET_SIZE)
        detectResult: DetectResult = loadDataFromDump(bytes_result)

        return detectResult
