import Database


class UserManager:

    def __init__(self):
        self.DB = Database.Database()

    def register(self, name: str, phone_num: str, mac_add: str) -> str:
        result = self.DB.addUser(name=name, phone_num=phone_num, mac_add=mac_add)

        if result is True:
            msg = "00;00"
        else:
            msg = "00;01"

        return msg

    def login(self):
        pass

    def getUserMac(self):
        pass

    def getUserPlace(self):
        pass

    def setUserPlace(self):
        pass

    def setUserBus(self):
        pass
