import FileManager


class BusManager:

    def __init__(self):
        self.BusData = FileManager.configManager()
        if self.BusData.isKey("cityCode") is False or self.BusData.isKey("nodeID") is False:
            print('[RaspBerry PI][ERR] 초기값을 설정해야 합니다!')
            print('[RaspBerry PI] cityCode : ', end='')
            cityCode = input()
            print('[RaspBerry PI] nodeID : ', end='')
            nodeID = input()
            self.resetBusStop(new_CityCode=cityCode, new_NodeId=nodeID)

        pass

    def resetBusStop(self, new_CityCode: str, new_NodeId: str):
        self.BusData.setValue('cityCode', new_CityCode)
        self.BusData.setValue('nodeID', new_NodeId)
        print(f'[RaspBerry PI] cityCode : {new_CityCode} , nodeID : {new_NodeId} 로 설정되었습니다.')

    def addBusRoute(self, cityCode: str, routeId: str, routeNo: str, vehicleNo: str) -> bool:
        pass

    def getBusList(self):
        pass

    def getSpecificBusArrival(self, routeNo: str) -> list:
        pass

    def isBusThrgh(self, routeNo: str) -> dict:
        pass

    def getBusThrgh(self, routeNo: str) -> dict:
        pass

    def removeBusRoute(self, cityCode: str, routeId: str) -> bool:
        pass
