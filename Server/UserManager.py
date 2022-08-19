import Database
import PROTOCOL as p


class UserManager:

    def __init__(self):
        self.DB = Database.Database()
        self.busReserveDict = {}
        self.userBusStopDict = {}

    def register(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.addUser(name=name, phone_num=phone_num, mac_add=mac_add)

        if result is True:
            msg = p.USER_REGISTER_SUCCESS
        else:
            msg = p.USER_REGISTER_FAIL

        return msg

    def login(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.isUserExist(name=name, phone_num=phone_num, mac_add=mac_add)

        if result == 1:
            msg = p.USER_LOGIN_SUCCESS

        elif result == 0:
            msg = p.USER_LOGIN_FAIL

        elif result == -1:
            msg = p.USER_LOGIN_SERVER_ERR

        return msg

    def setUserPlace(self):
        pass

    def setUserBus(self):
        pass

    def getUserMac(self):
        pass

    def getUserPlace(self):
        pass
