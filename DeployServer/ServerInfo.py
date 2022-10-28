from Assignment import Assignment


class ServerInfo:

    def __init__(self, ip: str):
        self.ip = ip
        self.status = False
        self.Assignment = None

    def setStatus_Working(self) -> None:
        self.status = True

    def setStatus_Sleep(self):
        self.status = False

    def getStatus(self) -> bool:
        return self.status

    def setAssign(self, assignment: Assignment) -> None:
        self.Assignment = assignment

    def delAssign(self) -> None:
        self.Assignment = None

    def getAssign(self) -> Assignment:
        return self.Assignment
