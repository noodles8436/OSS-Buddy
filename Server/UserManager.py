import Database
import PROTOCOL as p


class UserManager:

    def __init__(self):
        self.DB = Database.Database()
        self.busReserveDict = {}  # busReserveDict[user_mac] = [node_id, route_No]
        self.userBusStopDict = {}  # userBusStopDict[user_mac] = node_id

        self.busComingInfo = {}  # busComingInfo[node_id] = route_No
        self.busStopData = {} # busStopData[node_id] = [lati, long, nodeNm]
        self.busArrivalData = {} # busArrivalData[node_id] = dict[routeNo] => [Arrival, VehicleNo]

        self.busDriverTarget = {} # busDriverTarget[vehicleNo] = [nodeid]
        self.busDriverBusTack = {} # busDriverBusStack[vehicleNo] = dict[ord] => [nodeId]

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
        self.userBusStopDict.__delitem__(user_mac)

    def setUserReserveBus(self, user_mac: str, node_id: str, routeNo: str) -> None:
        if user_mac not in self.busReserveDict.keys():
            self.busReserveDict[user_mac] = [node_id, routeNo]

    def removeUserReserveBus(self, user_mac: str):
        if user_mac in self.busReserveDict.keys():
            self.busReserveDict.__delitem__(user_mac)

    def getUserReserveBus(self, user_mac: str) -> list[str, str] or None:
        if user_mac in self.busReserveDict.keys():
            return self.busReserveDict[user_mac]
        return None

    def getUserLocation(self, mac_add: str) -> str or None:
        if len(self.userBusStopDict) > 0:
            if mac_add in self.userBusStopDict.keys():
                return self.userBusStopDict[mac_add]
        return None

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

    def getBusArrivalData(self, nodeId: str, routeNo: str) -> list[str, str] or None:
        if nodeId in self.busArrivalData.keys():
            arrdata: dict = self.busArrivalData[nodeId]
            if routeNo in arrdata.keys():
                return arrdata[routeNo]
        return None


    # RaspBerry PI Detection Section

    def setBusComing(self, node_id: str, routeNo: str) -> None:
        self.busComingInfo[node_id] = routeNo

    def removeBusComing(self, node_id: str) -> None:
        self.busComingInfo.__delitem__(node_id)

    def getBusComing(self, node_id: str) -> str or None:
        if node_id in self.busComingInfo.keys():
            return self.busComingInfo[node_id]
        return None

    # Bus Driver Section

    def setBusDriver(self, nodeid: str, routeNo: str):
        busData = self.getBusArrivalData(nodeId=nodeid, routeNo=routeNo)
        vehicleNo = busData[1]


        self.busDriverTarget[vehicleNo] = nodeid

    def removeBusDriver(self, vehicleNo: str, nodeId):
        pass
