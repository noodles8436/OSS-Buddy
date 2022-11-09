import asyncio
import socket
import time

from Assignment import DetectResult, getDumpFromObject, loadDataFromDump
from PROTOCOL import *
import numpy as np


class DetectorConnector:

    def __init__(self, ip: str, port: int):
        self.writer = None
        self.reader = None
        self.globalServer_ip = ip
        self.globalServer_port = port
        self.client_socket = None
        self.connectServer()

    def connectServer(self):
        while True:
            print("[Raspberry][GLOBALSERVER] Try to Connect to Global Server")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.globalServer_ip, self.globalServer_port))
            self.client_socket = client_socket

            print("[Raspberry][GLOBALSERVER] Global Server Connected!")

            msg = CLIENT_RASPBERRY_LOGIN
            self.client_socket.sendall(msg.encode())

            print('[Raspberry][GLOBALSERVER] Try to Login Global Server')

            recv: bytes = client_socket.recv(GLOBAL_SERVER_PACKET_SIZE)
            _msg: str = str(recv.decode())

            print(' SERVER RECEIVED : ', _msg)
            print(CLIENT_LOGIN_SUCCESS)

            if _msg != CLIENT_LOGIN_SUCCESS:
                print("[Raspberry][GLOBALSERVER] Global Server Login Failed!")
                time.sleep(5)
                continue

            print("[Raspberry][GLOBALSERVER] Global Server Login Success!")
            break

    def disconnectServer(self):
        if self.client_socket is not None:
            self.client_socket.close()

    def detect(self, images: np.ndarray) -> DetectResult:
        import sys
        bytes_img: bytes = getDumpFromObject(images)
        print(sys.getsizeof(bytes_img))
        self.client_socket.send(bytes_img)

        print(' IMAGES SENT ! ')
        bytes_result: bytes = self.client_socket.recv(GLOBAL_SERVER_PACKET_SIZE)
        # bytes_result: bytes = await self.reader.read(GLOBAL_SERVER_PACKET_SIZE)
        detectResult: DetectResult = loadDataFromDump(bytes_result)

        print(' Result Received! ')

        return detectResult
