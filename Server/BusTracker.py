import requests
from bs4 import BeautifulSoup as bs

# 업로드시 주의 - API Key가 담겨져 있음.
APIEncodingKey = ######
APIDecodingKey = ######

# API URLS : 국토교통부 버스도착정보 API
URL_getSttnAcctoArvlPrearngeInfoList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList"
URL_getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
URL_getCtyCodeList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getCtyCodeList"

# API URLS : 국토교통부 버스노선정보 API
URL_getRouteNoList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList"
URL_getRouteAcctoThrghSttnList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteAcctoThrghSttnList"
URL_getRouteInfoIem = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteInfoIem"

# API URLS : 국토교통부 버스위치정보 API
URL_getRouteAcctoBusLcList = \
    "http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList"
URL_getRouteAcctoSpcifySttnAccesBusLcInfo = \
    "http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoSpcifySttnAccesBusLcInfo"

baseParams = "?ServiceKey=" + APIEncodingKey + "&_type=xml"


class BusTracker:

    def __init__(self):
        pass

    # 버스 도착 정보 관련

    def getBusLocation(self):
        pass

    def getBusStopArrival(self):
        pass

    def getAllServiceAreas(self) -> dict or None:
        queryParams = baseParams

        xml = requests.get(URL_getCtyCodeList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getAllServiceAreas resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        items = root.select('item')

        result = {}

        for item in items:
            result[item.find('citycode').get_text()] = item.find('cityname').get_text()

        return result

    # 버스 노선 관련

    def getBusInformation(self, cityCode: str, routeNo: str) -> dict or None:
        queryParams = baseParams + "&cityCode=" + cityCode + "&routeNo=" + routeNo + \
                      "&numOfRows=1" + "&pageNo=1"

        xml = requests.get(URL_getRouteNoList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getBusInformation resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        print(root)

        result = {}
        result['routeid'] = root.find('routeid').get_text()
        result['routeno'] = root.find('routeno').get_text()
        result['routetp'] = root.find('routetp').get_text()
        result['endnodenm'] = root.find('endnodenm').get_text()
        result['startnodenm'] = root.find('startnodenm').get_text()
        result['endvehicletime'] = root.find('endvehicletime').get_text()
        result['startvehicletime'] = root.find('startvehicletime').get_text()

        return result

    def getBusThrghSttnList(self, cityCode: str, routeId: str) -> dict or None:
        queryParams = baseParams + "&cityCode=" + cityCode + "&routeId=" + routeId + \
                      "&numOfRows=-1" + "&pageNo=1"

        xml = requests.get(URL_getRouteAcctoThrghSttnList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getBusThrghSttnList resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        result['routeid'] = root.find('routeid').get_text()
        result['totalCount'] = int(root.find('totalCount').get_text())

        items = root.select("item")
        for item in items:
            nodeItem = dict()
            #if item.find('nodeno') == None: print(item.find('nodenm'))
            nodeItem['gpslati'] = float(item.find('gpslati').get_text())
            nodeItem['gpslong'] = float(item.find('gpslong').get_text())
            nodeItem['nodeid'] = item.find('nodeid').get_text()
            #nodeItem['nodeno'] = int(item.find('nodeno').get_text())
            nodeItem['nodeord'] = int(item.find('nodeord').get_text())
            nodeItem['nodenm'] = item.find('nodenm').get_text()
            result['node_' + str(nodeItem['nodeord'])] = nodeItem

        return result

    # 버스 위치 관련

    def getAllBusinRoute(self, cityCode: str, routeId: str):
        queryParams = baseParams + "&cityCode=" + cityCode + "&routeId=" + routeId + \
                      "&numOfRows=-1" + "&pageNo=1"

        xml = requests.get(URL_getRouteAcctoBusLcList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getAllBusinRoute resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        result['routenm'] = root.find('routenm').get_text()
        result['totalCount'] = int(root.find('totalCount').get_text())

        items = root.select("item")
        locations = []
        for item in items:
            busItem = dict()
            busItem['gpslati'] = float(item.find('gpslati').get_text())
            busItem['gpslong'] = float(item.find('gpslong').get_text())
            busItem['nodeid'] = item.find('nodeid').get_text()
            busItem['nodeord'] = int(item.find('nodeord').get_text())
            locations.append(busItem['nodeord'])
            busItem['nodenm'] = item.find('nodenm').get_text()
            busItem['routetp'] = item.find('routetp').get_text()
            busItem['vehicleno'] = item.find('vehicleno').get_text()
            result['bus_' + str(busItem['nodeord'])] = busItem

        result['locations'] = locations

        return result


if __name__ == "__main__":
    BT = BusTracker()
    #print(BT.getAllServiceAreas())
    #print(BT.getBusInformation('31250', '720-2')) # GGB234000021 #GGB234000026
    #print(BT.getBusThrghSttnList('31250', 'GGB234000021')) #오리역 GGB206000215 GGB206000040
    #print(BT.getBusThrghSttnList('31250', 'GGB234000026')) #오리역 GGB206000040 GGB206000215
    print(BT.getAllBusinRoute('31250', 'GGB234000021'))
