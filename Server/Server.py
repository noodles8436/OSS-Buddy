'''
OSS-BUDDY : Smart Bus Boarding System for the Blind
Copyright (C) 2022 OSS-BUDDY Authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import asyncio
import UserManager
import PROTOCOL as p


class Server:

    def __init__(self, ip, port):
        self.server = None
        self.ip = ip
        self.port = port
        self.userMgr = UserManager.UserManager()

    async def run_server(self) -> None:
        self.server = await asyncio.start_server(self.loginHandler, host=self.ip, port=self.port)
        async with self.server:
            await self.server.serve_forever()

    async def loginHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data: bytes = await reader.read(p.SERVER_PACKET_SIZE)
        msg = data.decode().split(p.TASK_SPLIT)

        print('ACCESS TRY : ', msg)

        if msg[0] == p.USER_REGISTER:  # User Register
            if len(msg) == 4:
                msg_result = self.userMgr.userRegister(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_REGISTER_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

        elif msg[0] == p.USER_LOGIN:  # User Login
            if len(msg) == 4:
                msg_result = self.userMgr.userLogin(name=msg[1], phone_num=msg[2], mac_add=msg[3])
            else:
                msg_result = p.USER_LOGIN_CLIENT_ERR

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.USER_LOGIN_SUCCESS:
                await self.userHandler(reader=reader, writer=writer, userName=msg[1],
                                       userPhone=msg[2], userMac=msg[3])

        elif msg[0] == p.USER_GPS_LOGIN:
            if len(msg) == 4:
                msg_result = self.userMgr.userLogin(name=msg[1], phone_num=msg[2], mac_add=msg[3])

                if msg_result == p.USER_LOGIN_SUCCESS:
                    msg_result = p.USER_GPS_LOGIN_SUCCESS
                else:
                    msg_result = p.USER_GPS_LOGIN_FAIL
            else:
                msg_result = p.USER_LOGIN_CLIENT_ERR

            writer.write(msg_result.encode())
            await writer.drain()

            print(msg_result)

            if msg_result == p.USER_GPS_LOGIN_SUCCESS:
                await self.userGPSHandler(reader=reader, writer=writer, userMac=msg[3])

        elif msg[0] == p.BUSDRIVER_REGISTER:  # Bus Driver Register
            if len(msg) == 4:
                msg_result = self.userMgr.busDriverRegister(vehicleNo=msg[1], name=msg[2], mac_add=msg[3])
            else:
                msg_result = p.BUSDRIVER_REGISTER_FAIL
            writer.write(msg_result.encode())
            await writer.drain()

        elif msg[0] == p.BUSDRIVER_LOGIN:  # Bus Driver Login
            if len(msg) == 5:
                msg_result = self.userMgr.busDriverLogin(vehicleNo=msg[1], name=msg[2], mac_add=msg[3])
            else:
                msg_result = p.BUSDRIVER_LOGIN_FAIL
            print(msg_result)
            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.BUSDRIVER_LOGIN_SUCCESS:
                await self.BusDriverHandler(reader=reader, writer=writer, vehlcleNo=msg[1], routeNo=msg[4])

        elif msg[0] == p.RASP_INFO_LOGIN:  # Raspberry PI InfoProvider Connection
            if len(msg) == 4:
                msg_result = p.RASP_INFO_LOGIN_SUCCESS
            else:
                msg_result = p.RASP_INFO_LOGIN_FAIL

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.RASP_INFO_LOGIN_SUCCESS:
                await self.RaspInfoHandler(reader=reader, writer=writer, nodeId=msg[1],
                                           lati=float(msg[2]), long=float(msg[3]))

        elif msg[0] == p.RASP_DETECTOR_LOGIN:  # Raspberry PI Detector Connection
            if len(msg) == 2:
                msg_result = p.RASP_DETECTOR_LOGIN_SUCCESS
            else:
                msg_result = p.RASP_DETECTOR_LOGIN_FAIL

            writer.write(msg_result.encode())
            await writer.drain()

            if msg_result == p.RASP_DETECTOR_LOGIN_SUCCESS:
                await self.RaspDetectorHandler(reader=reader, writer=writer, nodeId=msg[1])

        writer.close()

    async def userHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                          userName: str, userPhone: str, userMac: str):
        peername = writer.get_extra_info('peername')
        print(f"[SERVER] {peername} is connected!")

        try:
            while True:
                # 클라이언트 위치 확인
                while self.userMgr.getUserLocation(mac_add=userMac) is None:
                    await asyncio.sleep(p.LOCATION_SEARCH_TERM)
                    connectCheck = await self.connectionCheck(reader=reader, writer=writer)
                    if connectCheck is False:
                        msg_result = p.KICK_USER
                        writer.write(msg_result.encode())
                        await writer.drain()
                        print(f"[SERVER] {peername} is disconnected!")
                        return

                msg_result = p.USER_LOCATION_FIND_SUCCESS
                writer.write(msg_result.encode())
                await writer.drain()

                # 클라이언트 위치 이후 처리
                while self.userMgr.getUserLocation(mac_add=userMac) is not None:
                    # 예약, 취소 명령 받기
                    data = await reader.read(p.SERVER_PACKET_SIZE)
                    msg = data.decode().split(p.TASK_SPLIT)

                    if msg[0] == p.USER_BUS_CAN_RESERVATION:
                        if len(msg) == 2:
                            msg_result = self.busCheck(userMac=userMac, routeNo=msg[1])
                        else:
                            msg_result = p.USER_BUS_CAN_RESERVATION_NO

                        writer.write(msg_result.encode())
                        await writer.drain()

                    elif msg[0] == p.USER_BUS_RESERVATION_CONFIRM:
                        if len(msg) == 2:
                            msg_result = self.busReservation(userMac=userMac, routeNo=msg[1])
                        else:
                            msg_result = p.USER_BUS_RESERVATION_CONFIRM_FAIL
                            # TODO : REMOVE USER RESERVATION

                        writer.write(msg_result.encode())
                        await writer.drain()

                        print('USER BUS RESERVATION CONFIRM = ', msg_result)

                        if msg_result == p.USER_BUS_RESERVATION_CONFIRM_SUCCESS:
                            while True:
                                try:
                                    data: bytes = await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE),
                                                                         p.BUS_REALTIME_SEARCH_TERM)
                                    isCancel = data.decode().split(p.TASK_SPLIT)[0]
                                    if isCancel == p.USER_BUS_CANCEL:
                                        msg_result = self.busCancel(userMac=userMac)
                                        writer.write(msg_result.encode())
                                        await writer.drain()
                                        break

                                except asyncio.TimeoutError:
                                    if self.isBusAlarmTime(userMac=userMac) is True:
                                        # Alarm User
                                        writer.write(p.USER_BUS_ARRIVED_VIBE.encode())
                                        await writer.drain()
                                        self.userMgr.removeUserReserveBus(user_mac=userMac)
                                        break

                    elif msg[0] == p.USER_REQ_BUS_LIST:
                        node_id = self.userMgr.getUserLocation(mac_add=userMac)
                        result: dict or None = self.userMgr.getAllBusArrivalData(nodeId=node_id)

                        _msg_result = ""
                        print(result)
                        if result is None:
                            _msg_result = p.USER_REQ_BUS_LIST + p.TASK_SPLIT + "00"
                        else:
                            _msg_result = p.USER_REQ_BUS_LIST + p.TASK_SPLIT + str(len(result.keys()))
                            for routeNo in result.keys():
                                _msg_result += p.TASK_SPLIT + routeNo + ":" + str(result[routeNo][0])
                        print(_msg_result)
                        writer.write(_msg_result.encode())
                        await writer.drain()

                # 클라이언트 위치 확인 안됨
                msg_result = p.USER_LOCATION_FIND_FAIL
                writer.write(msg_result.encode())
                await writer.drain()
                self.userMgr.removeUserReserveBus(user_mac=userMac)

        except ConnectionAbortedError:
            self.userMgr.removeUserReserveBus(user_mac=userMac)

        except ConnectionResetError:
            self.userMgr.removeUserReserveBus(user_mac=userMac)

        except ConnectionRefusedError:
            self.userMgr.removeUserReserveBus(user_mac=userMac)

        except ConnectionError:
            self.userMgr.removeUserReserveBus(user_mac=userMac)

        except Exception:
            # 클라이언트 위치 확인 안됨
            self.userMgr.removeUserReserveBus(user_mac=userMac)
            msg_result = p.KICK_USER
            writer.write(msg_result.encode())
            await writer.drain()

    async def userGPSHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, userMac: str):
        try:
            while True:
                data = await reader.read(p.SERVER_PACKET_SIZE)
                msg = data.decode().split(p.TASK_SPLIT)
                lati = float(msg[1])
                long = float(msg[2])
                near_busStop = self.userMgr.searchNearBusStation(user_lati=lati, user_long=long)
                if near_busStop is None:
                    self.userMgr.removeUserLocation(user_mac=userMac)
                else:
                    self.userMgr.setUserLocation(user_mac=userMac, node_id=near_busStop)

        except Exception:
            self.userMgr.removeUserLocation(user_mac=userMac)
            await writer.drain()
            writer.close()
            await writer.wait_closed()

    async def RaspInfoHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, nodeId: str,
                              lati: float, long: float):

        try:
            await asyncio.sleep(p.CONNECTION_PREPARING)
            writer.write(p.RASP_GET_NODE_NM.encode())
            await writer.drain()

            data = await reader.read(p.SERVER_PACKET_SIZE)
            msg = data.decode().split(p.TASK_SPLIT)
            self.userMgr.setBusStopData(nodeId=nodeId, lati=lati, long=long, nodeNm=msg[1])
            await asyncio.sleep(p.CONNECTION_PREPARING)

            while True:
                writer.write(p.RASP_REQ_ALL_BUS_ARR.encode())
                await writer.drain()

                data = await reader.read(p.SERVER_PACKET_SIZE)
                msg = data.decode().split(p.TASK_SPLIT)

                cnt: int = int(msg[1])
                result = dict()

                for i in range(2, cnt + 2):
                    _busData = msg[i].split(":")
                    result[_busData[0]] = [int(_busData[1]), _busData[2]]

                self.userMgr.setBusArrivalData(nodeId=nodeId, arrivalDict=result)

                await asyncio.sleep(p.BUS_REALTIME_SEARCH_TERM)

        except ConnectionError or ConnectionResetError:
            self.userMgr.removeBusComing(node_id=nodeId)
            self.userMgr.removeBusArrivalData(nodeId=nodeId)
            return

        except Exception:
            await writer.drain()
            writer.close()
            await writer.wait_closed()

    async def RaspDetectorHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, nodeId: str):
        try:
            while True:
                data = await reader.read(p.SERVER_PACKET_SIZE)
                msg = data.decode().split(p.TASK_SPLIT)

                if msg[0] == p.RASP_DETECTOR_BUS_CATCH:
                    if len(msg) == 4:
                        routeNo = msg[2]
                        self.userMgr.setBusComing(node_id=nodeId, routeNo=routeNo)

                elif msg[0] == p.RASP_DETECTOR_BUS_NONE:
                    self.userMgr.removeBusComing(node_id=nodeId)

                sitCnt = int(msg[-1])
                self.userMgr.setNodeSitCount(node_id=nodeId, sitCnt=sitCnt)

        except (ConnectionError, ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
            self.userMgr.removeBusComing(node_id=nodeId)
            self.userMgr.removeNodeSitCount(node_id=nodeId)

        except Exception:
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            self.userMgr.removeBusComing(node_id=nodeId)
            self.userMgr.removeNodeSitCount(node_id=nodeId)

    async def BusDriverHandler(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, vehlcleNo: str,
                               routeNo: str, node_left_alarm=3):
        try:
            while True:
                self.userMgr.refreshBusDriverPoints(vehicleNo=vehlcleNo, routeNo=routeNo)
                reserve: list[int, str, str] or None = \
                    self.userMgr.getBusDriverStopPoint(vehicleNo=vehlcleNo, routeNo=routeNo)

                if reserve is not None:
                    _node_left: int = reserve[0]
                    _node_name: str = reserve[1]
                    _node_id: str = reserve[2]

                    if _node_left <= node_left_alarm:
                        msg_result = p.BUSDRIVER_NODE_ANNOUNCE + p.TASK_SPLIT + _node_name \
                                     + p.TASK_SPLIT + str(_node_left)

                        writer.write(msg_result.encode())
                        await writer.drain()

                        if _node_left <= 1:
                            self.userMgr.removeBusDriverStackNode(vehicleNo=vehlcleNo, nodeId=_node_id)
                else:
                    msg_result = p.BUSDRIVER_NODE_NONE + p.TASK_SPLIT

                    writer.write(msg_result.encode())
                    await writer.drain()

                await asyncio.sleep(p.BUS_REALTIME_SEARCH_TERM)

        except ConnectionError or ConnectionResetError:
            self.userMgr.busDriverLogOut(vehicleNo=vehlcleNo)
            return

        except Exception:
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            self.userMgr.busDriverLogOut(vehicleNo=vehlcleNo)
            return

    async def connectionCheck(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        msg = p.CONNECTION_CHECK
        writer.write(msg.encode())
        await writer.drain()

        try:
            await asyncio.wait_for(reader.read(p.SERVER_PACKET_SIZE), timeout=p.TIMEOUT_SEC)
        except asyncio.TimeoutError:
            return False

        return True

    def busCheck(self, userMac: str, routeNo: str) -> str:
        nodeId = self.userMgr.getUserLocation(mac_add=userMac)
        if nodeId is None:
            return p.USER_BUS_CAN_RESERVATION_NO

        busData = self.userMgr.getBusArrivalData(nodeId=nodeId, routeNo=routeNo)
        if busData is not None:
            return p.USER_BUS_CAN_RESERVATION_OK

        return p.USER_BUS_CAN_RESERVATION_NO

    def busReservation(self, userMac: str, routeNo: str) -> str:
        nodeId = self.userMgr.getUserLocation(mac_add=userMac)
        if nodeId is None:
            return p.USER_BUS_RESERVATION_CONFIRM_FAIL
        result: bool = self.userMgr.setUserReserveBus(user_mac=userMac, node_id=nodeId, routeNo=routeNo)
        if result:
            return p.USER_BUS_RESERVATION_CONFIRM_SUCCESS
        else:
            return p.USER_BUS_RESERVATION_CONFIRM_FAIL

    def busCancel(self, userMac: str) -> str:
        self.userMgr.removeUserReserveBus(user_mac=userMac)
        return p.USER_BUS_CANCEL_SUCCESS

    def isBusAlarmTime(self, userMac: str) -> bool:
        result: list = self.userMgr.getUserReserveBus(user_mac=userMac)
        if result is None:
            return False

        print(result[0], result[1])

        node_id = result[0]
        route_id = result[1]

        comingBus = self.userMgr.getBusComing(node_id=node_id)

        arrdata: list[int, str] or None = self.userMgr.getBusArrivalData(nodeId=node_id, routeNo=route_id)
        if arrdata is None:
            return False

        # print('3정거장 전', arrdata[0])
        # print('comingBus :', comingBus)

        if comingBus == route_id and arrdata[0] <= 3:
            return True
        else:
            return False


if __name__ == "__main__":
    print('        [ OSS Buddy Project ]       '.center(75))
    print('')
    host = input("[Raspberry] 서버 Open IP 를 입력하세요 (ex 192.168.0.1) : ")
    port = int(input("[Raspberry] 서버 Open PORT 를 입력하세요 (ex 8877) : ", ))

    server = Server(ip=host, port=port)
    asyncio.run(server.run_server())
