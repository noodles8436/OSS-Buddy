import asyncio
import Server.PROTOCOL as p
import BusManager
import Detector


class RaspMain:

    def __init__(self, host: str, port: int):
        self.busManager = BusManager.BusManager()
        if self.busManager.setUp() is False:
            return

        print(self.busManager.getNodeLatiLong())
        self.Detector = Detector.Detector()
        self.host = host
        self.port = port

    async def start(self):
        self.serverTask = await asyncio.gather(self.busDetector(), self.infoProvider())

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

                recv: bytes = await reader.read(p.SERVER_PACKET_SIZE)
                _msg: str = recv.decode()

                if _msg != p.RASP_DETECTOR_LOGIN_SUCCESS:
                    print("[Rasp Detector][ERR] Server Login Failed!")
                    await asyncio.sleep(1)
                    continue

                print("[Rasp Detector] Server Login Success")

                while True:
                    _send = ""
                    _pred = self.Detector.detect()

                    print("_pred : ", _pred)

                    if _pred is not None:
                        routeNo = self.bus_number_filter(_pred=_pred)
                    else:
                        routeNo = None

                    if routeNo is None:
                        _send = p.RASP_DETECTOR_BUS_NONE
                    else:
                        _send = p.RASP_DETECTOR_BUS_CATCH + p.TASK_SPLIT \
                              + self.busManager.getBusRouteIdFromNo(routeNo=routeNo) + p.TASK_SPLIT + routeNo

                    print('send Detector : ', _send)

                    writer.write(_send.encode())
                    await writer.drain()
                    await asyncio.sleep(p.BUS_REALTIME_SEARCH_TERM)

            except Exception as e:
                print(e.args[0])
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()

    def bus_number_filter(self, _pred: list[list[str, float, int]]) -> str or None:
        busList = self.busManager.getBusRouteNoList()
        mostLeft = -1
        routeNo = None
        for (_text, _prob, _xpos) in _pred:
            if _text in busList:
                if mostLeft == -1 or mostLeft > _xpos:
                    mostLeft = _xpos
                    routeNo = _text

        return routeNo

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

                print('in login RASP INFO : ', msg)

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
                    print('Server Requested : ', msg)

                    if msg[0] == p.RASP_REQ_ALL_BUS_ARR:
                        _busDict, isExist = self.busManager.getAllBusFastArrival()

                        if isExist is False:
                            _sendMsg: str = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + "0"
                        else:
                            _sendMsg: str = p.RASP_REQ_ALL_BUS_ARR + p.TASK_SPLIT + str(len(_busDict.keys()))
                            for _routeNo in _busDict.keys():
                                _sendMsg += p.TASK_SPLIT + _routeNo + ":" + _busDict[_routeNo][0] \
                                            + ":" + _busDict[_routeNo][1]

                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_CHECK_BUS:
                        _sendMsg: str = ""
                        if len(msg) == 2:
                            _routeNo = msg[1]
                            if self.busManager.isBusThrgh(_routeNo):
                                _sendMsg = p.RASP_CHECK_BUS_POSSIBLE
                            else:
                                _sendMsg = p.RASP_CHECK_BUS_IMPOSSIBLE
                        else:
                            _sendMsg = p.RASP_CHECK_BUS_IMPOSSIBLE

                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_CHECK_ARRIVAL:

                        _sendMsg: str = ""

                        if len(msg) == 2:
                            _routeNo = msg[1]
                            _busArrival = self.busManager.getSpecificBusFastArrival(routeNo=_routeNo)
                            _sendMsg = p.RASP_CHECK_ARRIVAL + p.TASK_SPLIT + _busArrival[0] \
                                       + p.TASK_SPLIT + _busArrival[1]
                        else:
                            _sendMsg = p.RASP_CHECK_ARRIVAL + p.TASK_SPLIT + "-1" + p.TASK_SPLIT + "-1"

                        writer.write(_sendMsg.encode())
                        await writer.drain()

                    elif msg[0] == p.RASP_GET_NODE_NM:
                        _sendMsg: str = p.RASP_GET_NODE_NM + p.TASK_SPLIT + self.busManager.getNodeNm()
                        writer.write(_sendMsg.encode())
                        await writer.drain()

            except Exception as e:
                print(e.args[0])
                if writer is not None:
                    await writer.drain()
                    writer.close()
                    await writer.wait_closed()


if __name__ == "__main__":
    main = RaspMain(host=p.SERVER_IP, port=p.SERVER_PORT)
    asyncio.run(main.start())
