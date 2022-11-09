import Database
import PROTOCOL as p
import traceback


class UserManager:

    def __init__(self):
        self.DB = Database.Database()
        self.busReserveDict = {}  # busReserveDict[user_mac] = [node_id, route_No]
        self.userBusStopDict = {}  # userBusStopDict[user_mac] = node_id

        self.busComingInfo = {}  # busComingInfo[node_id] = route_No
        self.busStopData = {}  # busStopData[node_id] = [lati, long, nodeNm]
        self.busArrivalData = {}  # busArrivalData[node_id] = dict[routeNo] => [Arrival, VehicleNo]
        self.nodeSitCount = {}  # nodeSitCount[node_id] = int

        self.busDriverBusStack = {}  # busDriverBusStack[vehicleNo] = list[nodeId, nodeId...]

    # User Manage Section

    def userRegister(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.addUser(name=name, phone_num=phone_num, mac_add=mac_add)

        if result is True:
            msg = p.USER_REGISTER_SUCCESS
        else:
            msg = p.USER_REGISTER_FAIL

        return msg

    def userLogin(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.isUserExist(name=name, phone_num=phone_num, mac_add=mac_add)
        msg = ""

        if result == 1:
            msg = p.USER_LOGIN_SUCCESS

        elif result == 0:
            msg = p.USER_LOGIN_FAIL

        elif result == -1:
            msg = p.USER_LOGIN_SERVER_ERR

        return msg

    def setUserLocation(self, user_mac: str, node_id: str) -> None:
        self.userBusStopDict[user_mac] = node_id

    def removeUserLocation(self, user_mac: str) -> None:
        if user_mac in self.userBusStopDict.keys():
            self.userBusStopDict.__delitem__(user_mac)

    def setUserReserveBus(self, user_mac: str, node_id: str, routeNo: str) -> bool:
        print('Set Reserve Node Id : ', user_mac, node_id, routeNo)
        if user_mac not in self.busReserveDict.keys():
            self.busReserveDict[user_mac] = [node_id, routeNo]
            return self.setBusDriver(nodeid=node_id, routeNo=routeNo)
        return False

    def removeUserReserveBus(self, user_mac: str):
        if user_mac in self.busReserveDict.keys():
            reserve = self.getUserReserveBus(user_mac=user_mac)
            print('[Remove] Reserve Bus : ', reserve)
            vehicleNo = self.getBusArrivalData(nodeId=reserve[0], routeNo=reserve[1])[1]
            print('[Remove] Vehicle No : ', vehicleNo)
            self.removeBusDriverStackNode(vehicleNo=vehicleNo, nodeId=reserve[0])
            try:
                print('[Remove] total', self.busReserveDict)
                print('[Remove] Remove User Reserve Data : ', self.busReserveDict[user_mac])
                del self.busReserveDict[user_mac]
                print('[Remove] total', self.busReserveDict)
            except Exception as e:
                print('[Remove] ERROR : ', e.args[0])
                traceback.print_exc()

    def getUserReserveBus(self, user_mac: str) -> list[str, str] or None:
        print(self.busReserveDict)
        if user_mac in self.busReserveDict.keys():
            return self.busReserveDict[user_mac]
        return None

    def getUserLocation(self, mac_add: str) -> str or None:
        if len(self.userBusStopDict) > 0:
            if mac_add in self.userBusStopDict.keys():
                return self.userBusStopDict[mac_add]
        return None

    def getBusReserveUserNum(self, nodeId: str, routeNo: str) -> int:

        total = 0

        for user_mac in self.busReserveDict.keys():
            if self.busReserveDict[user_mac][0] == nodeId:
                if self.busReserveDict[user_mac][1] == routeNo:
                    total += 1

        return total

    def searchNearBusStation(self, user_lati: float, user_long: float, radius=0.1) -> str or None:
        for nodeid in self.busStopData.keys():
            stopData: list = self.busStopData[nodeid]
            lati = stopData[0]
            long = stopData[1]
            dis_lati = abs(user_lati - lati)
            dis_long = abs(user_long - long)
            dis = (dis_lati + dis_long) ** (1 / 2)

            if dis <= radius:
                return nodeid

        return None

    # 37.277109 127.903578
    # 37.277111 127.903692

    # RaspBerry PI InfoProvider Section

    def isBusStopDataExist(self, nodeId: str):
        if nodeId in self.busStopData.keys():
            return True
        return False

    def setBusStopData(self, nodeId: str, lati: float, long: float, nodeNm: str):
        self.busStopData[nodeId] = [lati, long, nodeNm]

    def removeBusStopData(self, nodeId: str):
        if self.isBusStopDataExist(nodeId=nodeId):
            self.busStopData.__delitem__(nodeId)

    def getBusStopData(self, nodeId: str) -> list:
        if self.isBusStopDataExist(nodeId=nodeId):
            return self.busStopData[nodeId]
        return list()

    def setBusArrivalData(self, nodeId: str, arrivalDict: dict):
        self.busArrivalData[nodeId] = arrivalDict

    def removeBusArrivalData(self, nodeId: str):
        if nodeId in self.busArrivalData.keys():
            self.busArrivalData.__delitem__(nodeId)

    def getBusArrivalData(self, nodeId: str, routeNo: str) -> list[int, str] or None:
        if nodeId in self.busArrivalData.keys():
            arrdata: dict = self.busArrivalData[nodeId]
            if routeNo in arrdata.keys():
                return arrdata[routeNo]
        return None

    def getAllBusArrivalData(self, nodeId: str) -> dict or None:
        if nodeId in self.busArrivalData.keys():
            return self.busArrivalData[nodeId]
        return None

    # RaspBerry PI Detection Section

    def setBusComing(self, node_id: str, routeNo: str) -> None:
        self.busComingInfo[node_id] = routeNo

    def removeBusComing(self, node_id: str) -> None:
        if node_id in self.busComingInfo.keys():
            self.busComingInfo.__delitem__(node_id)

    def getBusComing(self, node_id: str) -> str or None:
        if node_id in self.busComingInfo.keys():
            return self.busComingInfo[node_id]
        return None

    def setNodeSitCount(self, node_id: str, sitCnt: int) -> None:
        self.nodeSitCount[node_id] = sitCnt

    def getNodeSitCount(self, node_id: str, sitCnt: int) -> int:
        if node_id in self.nodeSitCount.keys():
            return self.nodeSitCount[node_id]
        return 0

    def removeNodeSitCount(self, node_id: str) -> None:
        if node_id in self.nodeSitCount.keys():
            self.nodeSitCount.__delitem__(node_id)

    # Bus Driver Section
    def busDriverRegister(self, vehicleNo: str, name: str, mac_add: str) -> str:
        result: bool = self.DB.addBusDriver(vehicleno=vehicleNo, name=name, mac_add=mac_add)
        if result is True:
            return p.BUSDRIVER_REGISTER_SUCCESS
        else:
            return p.BUSDRIVER_REGISTER_FAIL

    def busDriverLogin(self, vehicleNo: str, name: str, mac_add: str) -> str:
        result: int = self.DB.isBusDriverExist(vehicleno=vehicleNo, name=name, mac_add=mac_add)

        if result == 1:
            self.busDriverBusStack[vehicleNo] = list()
            return p.BUSDRIVER_LOGIN_SUCCESS
        elif result == 0:
            return p.BUSDRIVER_LOGIN_FAIL
        elif result == -1:
            return p.BUSDRIVER_LOGIN_ERR

    def setBusDriver(self, nodeid: str, routeNo: str) -> bool:
        busData = self.getBusArrivalData(nodeId=nodeid, routeNo=routeNo)
        vehicleNo = busData[1]

        if vehicleNo not in self.busDriverBusStack.keys():
            return False
        index = 0
        nodeList: list = self.busDriverBusStack[vehicleNo]

        for i in range(len(nodeList)):
            _reserved_node_id = nodeList[i]
            if _reserved_node_id == nodeid:
                return True

            _other_node_bus_data = self.getBusArrivalData(nodeId=_reserved_node_id, routeNo=routeNo)
            if busData[0] < _other_node_bus_data[0]:
                break
            index = i + 1

        nodeList.insert(index, nodeid)

        self.busDriverBusStack[vehicleNo] = nodeList
        return True

    def removeBusDriverStackNode(self, vehicleNo: str, nodeId: str):
        nodeList: list[str] = self.busDriverBusStack[vehicleNo]
        print('Searched Nodes of Vehicle', nodeList)
        if nodeId in nodeList:
            print('[Remove] Node List in Stack!')
            try:
                nodeList.remove(nodeId)
            except Exception as e:
                print('[Remove]', e.args[0])
            print('[Remove] Removed List Status :', nodeList)
            self.busDriverBusStack[vehicleNo] = nodeList

    def getBusDriverStopPoint(self, vehicleNo: str, routeNo: str) -> list[int, str, str] or None:
        self.refreshBusDriverPoints(vehicleNo=vehicleNo, routeNo=routeNo)
        nodeList: list[str] = self.busDriverBusStack[vehicleNo]
        print(" BUS DRIVER STOP LIST : ", nodeList)
        if len(nodeList) == 0:
            return None

        nodeid = nodeList[0]
        _bus_data = self.getBusArrivalData(nodeId=nodeid, routeNo=routeNo)

        arrival: int = _bus_data[0]
        nodeNm = self.getBusStopData(nodeId=nodeid)[2]
        return [arrival, nodeNm, nodeid]

    def refreshBusDriverPoints(self, vehicleNo: str, routeNo: str) -> None:
        if vehicleNo not in self.busDriverBusStack.keys():
            return

        for nodeId in self.busDriverBusStack[vehicleNo]:
            if self.getBusReserveUserNum(nodeId=nodeId, routeNo=routeNo) <= 0:
                self.busDriverBusStack[vehicleNo].remove(nodeId)

    def busDriverLogOut(self, vehicleNo: str):
        if vehicleNo in self.busDriverBusStack:
            del self.busDriverBusStack[vehicleNo]
