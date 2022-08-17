import requests
from bs4 import BeautifulSoup as bs

# 업로드시 주의 - API Key가 담겨져 있음.
APIEncodingKey = #######
APIDecodingKey = #######

# API URLS : 국토교통부 버스도착정보 API
URL_getSttnAcctoArvlPrearngeInfoList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList"
URL_getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList"
URL_getCtyCodeList = \
    "http://apis.data.go.kr/1613000/ArvlInfoInqireService/getCtyCodeList"


# APL URLS : 국토교통부 버스노선정보 API
URL_getRouteNoList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList"
URL_getRouteAcctoThrghSttnList = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteAcctoThrghSttnList"
URL_getRouteInfoIem = \
    "http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteInfoIem"

baseParams = "?ServiceKey=" + APIEncodingKey + "&_type=xml"

class BusTracker:

    def __init__(self):
        pass

    #버스 도착 정보 관련

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
            "&numOfRows=10" + "&pageNo=1"

        xml = requests.get(URL_getRouteNoList + queryParams).text
        root = bs(xml, features="xml")
        resultCode = root.find("resultCode").get_text()
        resultMsg = root.find("resultMsg").get_text()

        if resultCode != "00":
            print("[BusTracker][ERR] getBusInformation resultCode : " + resultCode)
            print("[BusTracker][ERR] ERR Msg : " + resultMsg)
            return None

        result = {}
        result['routeid'] = root.find('routeid').get_text()
        result['routeno'] = root.find('routeno').get_text()
        result['routetp'] = root.find('routetp').get_text()
        result['endnodenm'] = root.find('endnodenm').get_text()
        result['startnodenm'] = root.find('startnodenm').get_text()
        result['endvehicletime'] = root.find('endvehicletime').get_text()
        result['startvehicletime'] = root.find('startvehicletime').get_text()

        return result



if __name__ == "__main__":
    BT = BusTracker()
    print(BT.getAllServiceAreas())
    print(BT.getBusInformation('31250', '700-2'))
