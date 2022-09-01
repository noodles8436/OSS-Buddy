import os
import warnings
import easyocr
import torch.hub
import cv2

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore", category=UserWarning)
YOLO_BUS_LABEL = 5


class Model:

    def __init__(self):
        self.model = torch.hub.load(repo_or_dir="WongKinYiu/yolov7", model='custom',
                                    path_or_model='YoloV7/yolov7.pt', autoshape=True)
        self.reader = easyocr.Reader(['en'], gpu=False)

    def detect(self, cvImg, confidence=0.8) -> list[list[str, float]]:
        detections = self.model(cvImg)
        results = detections.pandas().xyxy[0].to_dict(orient="records")
        _pred: list = list()

        for result in results:
            if result['class'] != YOLO_BUS_LABEL or result['confidence'] < confidence:
                continue

            x1 = int(result['xmin'])
            y1 = int(result['ymin'])
            x2 = int(result['xmax'])
            y2 = int(result['ymax'])

            cropImg = cvImg[y1:int(y2 / 2), x1:x2, :]
            cropImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('Final', cropImg)
            # cv2.waitKey(0)
            result = self.reader.readtext(cropImg)
            _data: list = list()
            for (bbox, text, prob) in result:
                _data.append([text, prob])

            _pred.append(_data)

        return _pred


if __name__ == "__main__":
    m = Model()
    m.detect(cv2.imread("./DetectionTest/bus_img_test_2.jpg"))
