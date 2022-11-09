import asyncio
import socket
import threading
import time

import numpy as np

import DetectorConnector
import PROTOCOL as p
import BusManager
from Assignment import DetectResult
import cv2


class busDetectorThread(threading.Thread):

    def __init__(self, host, port, busManager, detector_host: str, detector_port: int):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.detector_host = detector_host
        self.detector_port = detector_port
        self.Detector = DetectorConnector.DetectorConnector(ip=self.detector_host, port=self.detector_port)
        self.busManager = busManager
        self.cap = cv2.VideoCapture(0)
        self.FPS = 4
        self.prev_time = 0

    def bus_number_filter(self, _pred: list[list[str, float, int]]) -> str or None:
        busList = self.busManager.getBusRouteNoList()
        mostLeft = -1
        routeNo = None
        for _predBus in _pred:
            print(_predBus)
            for textData in _predBus:
                print(textData)
                _text = textData[0]
                _prob = textData[1]
                _xpos = textData[2]
                if _text in busList:
                    if mostLeft == -1 or mostLeft > _xpos:
                        mostLeft = _xpos
                        routeNo = _text

        return routeNo

    def run(self):
        client_socket = None

        while True:
            try:
                print("[Rasp Detector] Try to Connect Server")
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))
                print("[Rasp Detector] Server Connected")

                msg = p.RASP_DETECTOR_LOGIN + p.TASK_SPLIT + self.busManager.getNodeId()
                client_socket.sendall(msg.encode())
                print("[Rasp Detector] Try to Login Server")

                recv: bytes = client_socket.recv(p.SERVER_PACKET_SIZE)
                _msg: str = recv.decode()

                if _msg != p.RASP_DETECTOR_LOGIN_SUCCESS:
                    print("[Rasp Detector][ERR] Server Login Failed!")
                    time.sleep(1)
                    continue

                print("[Rasp Detector] Server Login Success")

                while True:
                    try:
                        _send = ""
                        detectResult: DetectResult = self.Detector.detect(self.getCameraImgs())
                        _pred_bus = detectResult.getResult_OCR()

                        print(detectResult)

                        if _pred_bus is not None and len(_pred_bus) != 0:
                            routeNo = self.bus_number_filter(_pred=_pred_bus)
                        else:
                            routeNo = None

                        if routeNo is None:
                            _send = p.RASP_DETECTOR_BUS_NONE
                        else:
                            _send = p.RASP_DETECTOR_BUS_CATCH + p.TASK_SPLIT \
                                    + self.busManager.getBusRouteIdFromNo(routeNo=routeNo) + p.TASK_SPLIT + routeNo

                        sitCnt: int = detectResult.getResult_Understanding_sitCnt()
                        _send += p.TASK_SPLIT + str(sitCnt)

                        client_socket.sendall(_send.encode())
                        time.sleep(1)
                    except (ConnectionError, ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                        self.Detector.disconnectServer()
                        time.sleep(1)
                        self.Detector.connectServer()

            except Exception as e:
                print(e.args[0])
                if client_socket is not None:
                    client_socket.close()
                time.sleep(1)

    def getCameraImgs(self) -> np.ndarray:
        video_data = list()
        while True:
            ret, frame = self.cap.read()
            current_time = time.time() - self.prev_time

            if cv2.waitKey(1) & 0xFF == 27:
                break

            if (ret is True) and (current_time > 1. / self.FPS):
                prev_time = time.time()
                video_data.append(frame)

                if len(video_data) >= 4:
                    return np.array(video_data)


class RaspMain:

    def __init__(self, host: str, port: int, detector_host: str, detector_port: int):
        self.serverTask = None
        self.busManager = BusManager.BusManager()
        if self.busManager.setUp() is False:
            return

        self.host = host
        self.port = port
        self.busDetectorThread = busDetectorThread(self.host, self.port, self.busManager, detector_host, detector_port)

    async def start(self):
        self.busDetectorThread.start()
        self.serverTask = await asyncio.tasks.create_task(self.infoProvider())

    async def infoProvider(self) -> None:
        reader: asyncio.StreamReader
        writer: asyncio.StreamWriter

        while True:
            try:
                print("[Rasp INFO] Try to Connect Server")
                reader, writer = await asyncio.open_connection(host=self.host, port=self.port)
                print("[Rasp INFO] Server Connected")

                lati_long = self.busManager.getNodeLatiLong()

                msg = p.RASP_INFO_LOGIN + p.TASK_SPLIT + self.busManager.getNodeId() + \
                      p.TASK_SPLIT + str(lati_long[0]) + p.TASK_SPLIT + str(lati_long[1])

                writer.write(msg.encode())
                await writer.drain()
                print("[Rasp INFO] Try to Login Server")

                recv: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                msg: str = recv.decode()

                if msg != p.RASP_INFO_LOGIN_SUCCESS:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()
                    print("[Rasp INFO][ERR] Server Login Failed!")
                    await asyncio.sleep(1)
                    continue

                print("[Rasp INFO] Server Login Success")

                while True:
                    recv: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                    msg: list[str] = recv.decode().split(p.TASK_SPLIT)

                    if msg[0] == p.RASP_REQ_ALL_BUS_ARR:
                        print('[Rasp INFO] Server Requested : RASP_REQ_ALL_BUS_ARR')

                        try:
                            _busDict, isExist = self.busManager.getAllBusFastArrival()

                            if isExist is False:
                                _sendMsg: str = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + "0"
                            else:
                                _sendMsg: str = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + str(len(_busDict.keys()))
                                for _routeNo in _busDict.keys():
                                    _sendMsg += p.TASK_SPLIT + _routeNo + ":" + str(_busDict[_routeNo][0]) \
                                                + ":" + str(_busDict[_routeNo][1])
                            print('[Rasp INFO] Send Request To Server', _sendMsg)

                        except Exception:
                            _sendMsg: str = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + "0"

                        # ONLY TEST
                        _sendMsg = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + "01" + p.TASK_SPLIT + "30:3:강원71자1529"
                        print('[Rasp INFO] Send Request To Server', _sendMsg)

                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_CHECK_BUS:
                        print('[Rasp INFO] Server Requested : RASP_CHECK_BUS')
                        _sendMsg: str = ""
                        if len(msg) == 2:
                            _routeNo = msg[1]
                            if self.busManager.isBusThrgh(_routeNo):
                                _sendMsg = p.RASP_CHECK_BUS_POSSIBLE
                            else:
                                _sendMsg = p.RASP_CHECK_BUS_IMPOSSIBLE
                        else:
                            _sendMsg = p.RASP_CHECK_BUS_IMPOSSIBLE
                        print('[Rasp INFO] Send Request To Server', _sendMsg)
                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_CHECK_ARRIVAL:
                        print('[Rasp INFO] Server Requested : RASP_CHECK_ARRIVAL')
                        _sendMsg: str = ""

                        if len(msg) == 2:
                            _routeNo = msg[1]
                            _busArrival = self.busManager.getSpecificBusFastArrival(routeNo=_routeNo)
                            _sendMsg = p.RASP_CHECK_ARRIVAL + p.TASK_SPLIT + _busArrival[0] \
                                       + p.TASK_SPLIT + _busArrival[1]
                        else:
                            _sendMsg = p.RASP_CHECK_ARRIVAL + p.TASK_SPLIT + "-1" + p.TASK_SPLIT + "-1"

                        print('[Rasp INFO] Send Request To Server', _sendMsg)
                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_GET_NODE_NM:
                        print('[Rasp INFO] Server Requested : RASP_GET_NODE_NM')
                        _sendMsg: str = p.RASP_GET_NODE_NM + p.TASK_SPLIT + self.busManager.getNodeNm()
                        print('[Rasp INFO] Send Request To Server', _sendMsg)
                        writer.write(_sendMsg.encode())
                        await writer.drain()

            except Exception as e:
                print(e.args[0])
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()


if __name__ == "__main__":
    print('        [ OSS Buddy Project ]       '.center(75))
    print('')
    host = input("[Raspberry] 서버 IP 를 입력하세요 (ex 192.168.0.1) : ")
    port = int(input("[Raspberry] 서버 PORT 를 입력하세요 (ex 8877) : ", ))
    detector_host = input("[Raspberry] DETECTOR 서버 IP 를 입력하세요 (ex 192.168.0.1) : ")
    detector_port = int(input("[Raspberry] DETECTOR 서버 PORT 를 입력하세요 (ex 8877) : ", ))

    main = RaspMain(host=host, port=port, detector_host=detector_host, detector_port=detector_port)
    asyncio.run(main.start())
