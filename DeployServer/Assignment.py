import numpy as np
import pickle


class DetectResult:

    def __init__(self):
        self.resultDict = dict()

    def setResult_ObjDetection(self):
        pass

    def getResult_ObjDetection(self):
        pass

    def setResult_OCR(self):
        pass

    def getResult_OCR(self):
        pass

    def setResult_Understanding(self):
        pass

    def getResult_Understanding(self):
        pass


class Assignment:

    def __init__(self, client_ip: str, image: np.ndarray):
        self.client_ip = client_ip
        self.image = image
        self.DetectResult = None
        self.isAssignCompleted_Flag = False

    def setDetectResult_FromDump(self, bytes_result: bytes) -> None:
        self.DetectResult = pickle.loads(bytes_result)
        self.isAssignCompleted_Flag = True

    def getDetectResult(self) -> DetectResult or None:
        return self.DetectResult

    def getDump_DetectResult(self) -> bytes:
        return pickle.dumps(self.DetectResult)

    def getDump_Image(self) -> bytes:
        return pickle.dumps(self.image)

    def getClient_IP(self) -> str:
        return self.client_ip

    def isAssignCompleted(self):
        return self.isAssignCompleted_Flag
