import FileManager
import BusTracker


class BusManager:

    def __init__(self):
        self.BusData = FileManager.configManager("./buddy_bus.json")
        self.BusTracker = BusTracker.BusTracker()
        if self.BusData.isKey("cityCode") is False or self.BusData.isKey("nodeId") is False:
            print('[RaspBerry PI][ERR] 초기값을 설정해야 합니다!')
            print('[RaspBerry PI] cityCode : ', end='')
            cityCode = input()
            print('[RaspBerry PI] nodeID : ', end='')
            nodeID = input()
            print('[RaspBerry PI] nodeNo : ', end='')
            nodeNo = input()
            print('[RaspBerry PI] nodeNm : ', end='')
            nodeNm = input()
            self.resetBusStop(new_CityCode=cityCode, new_NodeId=nodeID,
                              new_NodeNo=nodeNo, new_NodeNm=nodeNm)

    def resetBusStop(self, new_CityCode: str, new_NodeId: str, new_NodeNo: str, new_NodeNm: str) -> None:
        self.BusData.setValue('cityCode', new_CityCode)
        self.BusData.setValue('nodeId', new_NodeId)
        self.BusData.setValue('nodeNo', new_NodeNo)
        self.BusData.setValue('nodeNm', new_NodeNm)
        print(f'[RaspBerry PI] cityCode : {new_CityCode} , nodeId : {new_NodeId}, nodeNo : {new_NodeNo},'
              f' nodeNm : {new_NodeNm}로 설정되었습니다.')

    def addBusRoute(self, cityCode: str, routeId: str, routeNo: str, vehicleNo: str) -> bool:

        busdata = self.getBusDict()
        if busdata is None:
            busdata = dict()

        newBus = dict()
        newBus['cityCode'] = cityCode
        newBus['routeId'] = routeId

        busdata[routeNo] = newBus
        self.setBusDict(busdata)

        return True

    def setBusDict(self, busDict: dict) -> bool:
        self.BusData.setValue('busList', busDict)

    def getBusRouteNoList(self) -> list:
        busdict = self.getBusDict()
        if busdict is None:
            return list()
        return busdict.keys()

    def getBusData(self) -> dict:
        busdict = self.getBusDict()
        if busdict is None:
            return dict()
        return busdict

    def getBusFromNo(self, routeNo: str) -> dict() or None:
        if routeNo in self.getBusRouteIdFromNo():
            return self.getBusData()[routeNo]
        return None

    def getBusRouteIdFromNo(self, routeNo: str) -> str or None:
        busdata = self.getBusFromNo(routeNo)
        if busdata is not None:
            return busdata['routeId']
        return None

    def getBusCityCodeFromNo(self, routeNo: str) -> str or None:
        busdata = self.getBusFromNo(routeNo)
        if busdata is not None:
            return busdata['cityCode']
        return None

    def getSpecificBusFastArrival(self, routeNo: str, limitFastNode=2) -> list or None:

        if self.isBusThrgh(routeNo=routeNo) is False:
            return None

        nodeId = self.getNodeId()
        nodeOrd = -1
        cityCode = self.getBusCityCodeFromNo(routeNo=routeNo)
        routeId = self.getBusRouteIdFromNo(routeNo=routeNo)

        if routeId is None or cityCode:
            return None

        busThrghSttnList = self.BusTracker.getBusThrghSttnList(cityCode=cityCode, routeId=routeId)

        for _nodeOrd in busThrghSttnList['nodeDict'].keys():
            if busThrghSttnList['nodeDict'][_nodeOrd]['nodeid'] == nodeId:
                nodeOrd = _nodeOrd
                break

        if nodeOrd == -1:
            return None

        getAllBusinRoute = self.BusTracker.getAllBusinRoute(cityCode=cityCode, routeId=routeId)['busDict']

        nodeArrivalCount = -1
        busitemKey = None

        for key in getAllBusinRoute.keys():

            diff = nodeOrd - getAllBusinRoute[key]['nodeord']

            if nodeArrivalCount == -1 and diff > limitFastNode:
                nodeArrivalCount = diff
                busitemKey = key
            elif nodeArrivalCount > diff > limitFastNode:
                nodeArrivalCount = diff
                busitemKey = key

        if nodeArrivalCount == -1:
            return None

        result = [nodeArrivalCount, getAllBusinRoute[busitemKey]['vehicleNo']]

        return result

    def getCityCode(self) -> str:
        return self.BusData.getValue('cityCode')

    def getNodeId(self) -> str:
        return self.BusData.getValue('nodeId')

    def getNodeNm(self) -> str:
        return self.BusData.getValue('nodeNo')

    def getNodeNo(self) -> str:
        return self.BusData.getValue('nodeNm')

    def getBusDict(self) -> dict or None:
        return self.BusData.getValue('busDict')

    def isBusThrgh(self, routeNo: str) -> bool:
        if routeNo in self.getBusRouteNoList():
            return True
        return False

    def removeBusRoute(self, routeNo: str) -> bool:
        if self.isBusThrgh(routeNo=routeNo):
            self.BusData.removeKey(routeNo)
            return True
        return False
