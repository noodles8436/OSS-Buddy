from Assignment import Assignment


class ServerInfo:

    def __init__(self, server_ip: str):
        self.ip = server_ip
        self.Assignment = None

    def setAssign(self, assignment: Assignment) -> None:
        self.Assignment = assignment

    def delAssign(self) -> None:
        self.Assignment = None

    def getServer_IP(self) -> str:
        return self.ip

    def getAssign(self) -> Assignment or None:
        return self.Assignment

    def isAssigned(self) -> bool:
        if self.getAssign() is not None:
            return True
        return False
