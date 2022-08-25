

class BusManager:

    def __init__(self):
        self.BusData = dict()
        pass

    def resetBusStop(self, new_CityCode: str, new_NodeId: str):
        pass

    def addBusRoute(self, cityCode: str, routeId: str, routeNo: str, vehicleNo: str) -> bool:
        pass

    def getBusRouteList(self):
        pass

    def isBusThrgh(self, routeNo: str) -> dict:
        pass

    def getBusThrgh(self, routeNo: str) -> dict:
        pass

    def removeBusRoute(self, cityCode: str, routeId: str) -> bool:
        pass
