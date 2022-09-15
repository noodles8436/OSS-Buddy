import requests
from bs4 import BeautifulSoup as bs

# 업로드시 주의 - API Key가 담겨져 있음.
APIEncodingKey = ######
APIDecodingKey = ######

# API URLS : 국토교통부 버스노선정보 API
URL_getRouteNoList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList"
URL_getRouteAcctoThrghSttnList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteAcctoThrghSttnList"

# API URLS : 국토교통부 버스위치정보 API
URL_getRouteAcctoBusLcList = \
    "http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList"
URL_getCtyCodeList = \
    "http://apis.data.go.kr/1613000/BusLcInfoInqireService/getCtyCodeList"

# API URLS : 국토교통부 버스정류장정보 API
URL_getSttnNoList = \
    "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getSttnNoList"

URL_getSttnThrghRouteList = \
    "http://apis.data.go.kr/1613000/BusSttnInfoInqireService/getSttnThrghRouteList"

baseParams = "?ServiceKey=" + APIEncodingKey + "&_type=xml"


class BusTracker:

    def __init__(self):
        pass

    # 버스 도착 정보 관련

    def getAllServiceAreas(self) -> dict or None:
        queryParams = baseParams

        xml = requests.get(URL_getCtyCodeList + queryParams).text
        print(xml)
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
        result['nodeDict'] = dict()

        items = root.select("item")
        for item in items:
            nodeItem = dict()
            # if item.find('nodeno') == None: print(item.find('nodenm'))
            nodeItem['gpslati'] = float(item.find('gpslati').get_text())
            nodeItem['gpslong'] = float(item.find('gpslong').get_text())
            nodeItem['nodeid'] = item.find('nodeid').get_text()
            nodeItem['nodeno'] = int(item.find('nodeno').get_text())
            nodeItem['nodeord'] = int(item.find('nodeord').get_text())
            nodeItem['nodenm'] = item.find('nodenm').get_text()
            result['nodeDict'][str(nodeItem['nodeord'])] = nodeItem

        return result

    # 버스 위치 관련

    def getAllBusinRoute(self, cityCode: str, routeId: str) -> dict or None:
        queryParams = baseParams + "&cityCode=" + cityCode + "&routeId=" + routeId + \
                      "&numOfRows=20" + "&pageNo=1"

        xml = requests.get(URL_getRouteAcctoBusLcList + queryParams).text
        root = bs(xml, features="xml")
        #print(root)

        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getAllBusinRoute resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        result['routenm'] = root.find('routenm').get_text()
        result['totalCount'] = int(root.find('totalCount').get_text())
        result['busDict'] = dict()

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
            busItem['vehicleNo'] = item.find('vehicleno').get_text()
            result['busDict'][str(busItem['nodeord'])] = busItem

        result['locations'] = locations

        return result

    # 버스 정류장 정보 관련

    def getSttnNoList(self, cityCode: str, nodeNm: str, nodeNo: str) -> dict or None:
        queryParams = baseParams + "&cityCode=" + cityCode + "&nodeNm=" + nodeNm + \
                      "&nodeNo=" + nodeNo + "&numOfRows=1" + "&pageNo=1"

        xml = requests.get(URL_getSttnNoList + queryParams).text
        root = bs(xml, features="xml")

        print(xml)

        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getAllBusinRoute resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        items = root.select("item")
        for item in items:
            nodeItem = dict()
            nodeItem['gpslati'] = float(item.find('gpslati').get_text())
            nodeItem['gpslong'] = float(item.find('gpslong').get_text())
            nodeItem['nodeid'] = item.find('nodeid').get_text()
            nodeItem['nodenm'] = item.find('nodenm').get_text()
            nodeItem['nodeno'] = item.find('nodeno').get_text()
            result[nodeItem['nodeid']] = nodeItem

        return result

    def getSttnThrghRouteList(self, cityCode: str, nodeId: str) -> dict or None:
        queryParams = baseParams + "&cityCode=" + cityCode + "&nodeid=" + nodeId + \
                      "&numOfRows=50" + "&pageNo=1"

        xml = requests.get(URL_getSttnThrghRouteList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getAllBusinRoute resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        items = root.select("item")
        for item in items:
            busItem = dict()
            busItem['routeid'] = item.find('routeid').get_text()
            busItem['routeno'] = item.find('routeno').get_text()
            busItem['routetp'] = item.find('routetp').get_text()
            busItem['endnodenm'] = item.find('endnodenm').get_text()
            busItem['startnodenm'] = item.find('startnodenm').get_text()
            result[busItem['routeno']] = busItem

        return result


if __name__ == "__main__":
    BT = BusTracker()
    #print(BT.getAllServiceAreas()) #지역 코드 얻기
    #print(BT.getBusInformation('32020', '30')) # 30번 : WJB251000068
    #print(BT.getBusThrghSttnList('32020', 'WJB251000068'))
    #print(BT.getSttnNoList(cityCode='32020', nodeNm='연세대 복지타운', nodeNo='36043'))
    # 연세대 복지타운 : WJB251036043 , 51번 순서 정류장, lati:37.277093, long:127.903682
    # nodeno : 36043

    #print(BT.getSttnThrghRouteList(cityCode='32020', nodeId='WJB251036035'))
    # 세동마을 : WJB251036035, nodeno: 36035, lati:37.280122 long:127.91001 46번 정류장

    # print(BT.getAllBusinRoute('31250', 'GGB234000021'))

    # cityCode는 어케 얻지?
    # cityCode, 정류장 (nodeId), routeid, routeNo 는 RaspBerry PI 에서 얻음.
    # BT.getBusInformation(cityCode, routeNo) 로 routeid를 획득함
    # BT.getBusThrghSttnList(cityCode, routeid) 를 통해서 nodeord를 획득함
    # BT.getAllBussinRoute(cityCode, routeid) 를 통해서 최단거리에있는 버스를 얻을 수 있음
