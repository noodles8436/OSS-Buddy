import numpy as np
import pickle
from PROTOCOL import SUB_TASK_SPLIT


def getDumpFromObject(target: object):
    return pickle.dumps(target)


def loadDataFromDump(dumpData: bytes):
    return pickle.loads(dumpData)


class DetectResult:

    def __init__(self):
        self.resultDict = dict()
        self.isComplete = False

    def setResult_ObjDetection(self, result: list):
        self.resultDict['ObjDetection'] = result

    def getResult_ObjDetection(self) -> list or None:
        if "ObjDetection" in self.resultDict.keys():
            return self.resultDict['ObjDetection']
        return None

    def setResult_OCR(self, result: list):
        self.resultDict['OCR_BUS'] = result

    def getResult_OCR(self) -> list or None:
        if "OCR_BUS" in self.resultDict.keys():
            return self.resultDict['OCR_BUS']
        return None

    def setResult_Understanding(self, result: list):
        self.resultDict['Understanding'] = result

    def getResult_Understanding(self) -> list or None:
        if "Understanding" in self.resultDict.keys():
            return self.resultDict['Understanding']
        return None

    def setResult_Chairs(self, result: list):
        self.resultDict['Chairs'] = result

    def getResult_Chairs(self) -> list or None:
        if "Chairs" in self.resultDict.keys():
            return self.resultDict["Chairs"]
        return None

    def getResult_Understanding_cntDict(self) -> dict:
        uniq, cnt = np.unique(self.getResult_Understanding(), return_counts=True)
        return dict(zip(uniq, cnt))

    def getResult_Understanding_sitCnt(self) -> int:
        cntDict = self.getResult_Understanding_cntDict()
        if "11" in cntDict.keys():
            return cntDict["11"]
        return 0

    def getResult_Chairs_Cnt(self) -> int:
        if "Chairs" in self.resultDict.keys():
            return len(self.resultDict["Chairs"])
        return 0

    def setComplete(self):
        self.isComplete = True

    def getComplete(self):
        return self.isComplete

    def toString(self) -> str:
        result = ""
        for key in self.resultDict.keys():
            result += key + SUB_TASK_SPLIT + self.resultDict[key] + SUB_TASK_SPLIT

        result = result[:-1]
        return result

    def getCanSitCnt(self) -> int:
        return max(0, self.getResult_Chairs_Cnt() - self.getResult_Understanding_sitCnt())


class Assignment:

    def __init__(self, client_ip: str, images: np.ndarray):
        self.client_ip = client_ip
        self.images = images
        self.DetectResult = None

    def setDetectResult_FromDump(self, bytes_result: bytes) -> None:
        self.DetectResult = pickle.loads(bytes_result)
        self.isAssignCompleted_Flag = True

    def getDetectResult(self) -> DetectResult or None:
        return self.DetectResult

    def getDump_Images(self) -> bytes:
        return pickle.dumps(self.images)

    def getClient_IP(self) -> str:
        return self.client_ip
