import Database
import PROTOCOL as p


class UserManager:

    def __init__(self):
        self.DB = Database.Database()
        self.busReserveDict = {}  #busReserveDict[user_mac] = [node_id, route_No]
        self.userBusStopDict = {}  #userBusStopDict[user_mac] = node_id

    def userRegister(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.addUser(name=name, phone_num=phone_num, mac_add=mac_add)

        if result is True:
            msg = p.USER_REGISTER_SUCCESS
        else:
            msg = p.USER_REGISTER_FAIL

        return msg

    def userLogin(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.isUserExist(name=name, phone_num=phone_num, mac_add=mac_add)

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

    def setUserBus(self, user_mac: str, node_id: str, route_id: str) -> None:
        if user_mac not in self.busReserveDict.keys():
            self.busReserveDict[user_mac] = [node_id, route_id]

    def getUserLocation(self, mac_add: str) -> str or None:
        if len(self.userBusStopDict) > 0:
            if mac_add in self.userBusStopDict.keys():
                return self.userBusStopDict[mac_add]
        return None
