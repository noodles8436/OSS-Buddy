from typing import Tuple, Dict, Any, List

import FileManager
import BusTracker


class BusManager:

    def __init__(self):
        self.BusTracker = None
        self.BusData = None

    def setUp(self) -> bool:
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
            return self.resetBusStop(new_CityCode=cityCode, new_NodeId=nodeID,
                                     new_NodeNo=nodeNo, new_NodeNm=nodeNm)

        return True

    def resetBusStop(self, new_CityCode: str, new_NodeId: str, new_NodeNo: str, new_NodeNm: str) -> bool:

        result = self.BusTracker.getSttnNoList(cityCode=new_CityCode, nodeNm=new_NodeNm, nodeNo=new_NodeNo)

        if result is None or len(result) == 0:
            print("[RaspBerry PI][ERR] 위치 정보가 잘못되었습니다!")
            return False

        self.BusData.setValue('cityCode', new_CityCode)
        self.BusData.setValue('nodeId', new_NodeId)
        self.BusData.setValue('nodeNo', new_NodeNo)
        self.BusData.setValue('nodeNm', new_NodeNm)
        print(result)
        self.BusData.setValue('lati', result[new_NodeId]['gpslati'])
        self.BusData.setValue('long', result[new_NodeId]['gpslong'])
        self.BusData.setValue('busDict', dict())
        print(f'[RaspBerry PI] cityCode : {new_CityCode} , nodeId : {new_NodeId}, nodeNo : {new_NodeNo},'
              f' nodeNm : {new_NodeNm}로 설정되었습니다.')

        return True

    def addBusRoute(self, cityCode: str, routeId: str, routeNo: str) -> bool:

        busdata = self.getBusDict()
        if busdata is None:
            busdata = dict()

        newBus = dict()
        newBus['cityCode'] = cityCode
        newBus['routeId'] = routeId

        busdata[routeNo] = newBus
        self.setBusDict(busdata)

        return True

    def setBusDict(self, busDict: dict) -> None:
        self.BusData.setValue('busDict', busDict)

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

    def getBusFromNo(self, routeNo: str) -> dict or None:
        if routeNo in self.getBusRouteNoList():
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

    def getBusMaxNodeFromNo(self, routeNo: str) -> int:

        _cityCode = self.getBusCityCodeFromNo(routeNo=routeNo)
        _routeId = self.getBusRouteIdFromNo(routeNo=routeNo)

        if _cityCode is None or _routeId is None:
            return -1

        _sttnList = self.BusTracker.getBusThrghSttnList(self.getBusCityCodeFromNo(routeNo=routeNo),
                                                        self.getBusRouteIdFromNo(routeNo=routeNo))

        if _sttnList is None:
            return -2

        return len(_sttnList['nodeDict'].keys()) - 1

    def getSpecificBusFastArrival(self, routeNo: str, limitFastNode=1) -> list or None:

        if self.isBusThrgh(routeNo=routeNo) is False:
            return None
        nodeId = self.getNodeId()
        nodeOrd = -1
        cityCode = self.getBusCityCodeFromNo(routeNo=routeNo)
        routeId = self.getBusRouteIdFromNo(routeNo=routeNo)
        if routeId is None or cityCode is None:
            return None

        busThrghSttnList = self.BusTracker.getBusThrghSttnList(cityCode=cityCode, routeId=routeId)

        if busThrghSttnList is None:
            return None

        for _nodeOrd in busThrghSttnList['nodeDict'].keys():
            if busThrghSttnList['nodeDict'][_nodeOrd]['nodeid'] == nodeId:
                nodeOrd = int(_nodeOrd)
                break

        if nodeOrd == -1:
            return None

        getAllBusinRoute = self.BusTracker.getAllBusinRoute(cityCode=cityCode, routeId=routeId)['busDict']

        if getAllBusinRoute is None:
            return None

        nodeArrivalCount = -1
        busitemKey = None

        if nodeOrd == 0:
            if min(getAllBusinRoute.keys()) == 0:
                busitemKey = 0
                nodeArrivalCount = 0
            else:
                busitemKey = max(getAllBusinRoute.keys())
                nodeArrivalCount = self.getBusMaxNodeFromNo(routeNo=routeNo) - busitemKey

        else:
            for key in getAllBusinRoute.keys():
                diff = nodeOrd - int(getAllBusinRoute[key]['nodeord'])

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

    def getAllBusFastArrival(self, limitFastNode=1) -> tuple[dict[Any, list[int | Any] | None], bool]:
        routeNoList = self.getBusRouteNoList()
        result = dict()
        isExist = False
        for routeNo in routeNoList:
            _busArrival = self.getSpecificBusFastArrival(routeNo=routeNo, limitFastNode=limitFastNode)
            print('A')
            if _busArrival is not None:
                result[routeNo] = _busArrival
                isExist = True
            print('B')

        return result, isExist

    def getCityCode(self) -> str:
        return self.BusData.getValue('cityCode')

    def getNodeId(self) -> str:
        return self.BusData.getValue('nodeId')

    def getNodeNm(self) -> str:
        return self.BusData.getValue('nodeNm')

    def getNodeNo(self) -> str:
        return self.BusData.getValue('nodeNo')

    def getNodeLatiLong(self) -> [float, float]:
        return [self.BusData.getValue('lati'), self.BusData.getValue('long')]

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


if __name__ == "__main__":
    busMgr = BusManager()
    busMgr.setUp()
    #busMgr.resetBusStop(new_CityCode='32020', new_NodeId='WJB251036043', new_NodeNo='36043', new_NodeNm='연세대 복지타운')
    #busMgr.addBusRoute('32020', routeId='WJB251000074', routeNo='31')  (오류) # 추후 중복 예외 처리
    #busMgr.addBusRoute('32020', routeId='WJB251000331', routeNo='34-1')  # 추후 중복 예외 처리
    #busMgr.addBusRoute('32020', routeId='WJB251000082', routeNo='34')  # 추후 중복 예외 처리

