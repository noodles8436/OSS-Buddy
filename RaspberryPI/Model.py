import torch.hub
import cv2

class Model:

    def __init__(self):
        self.model = torch.hub.load(repo_or_dir="WongKinYiu/yolov7", model='custom',
                                    path_or_model='YoloV7/yolov7.pt', autoshape=True)

    def detect(self, cvImg):
        detections = self.model(cvImg)

        results = detections.pandas().xyxy[0].to_dict(orient="records")
        for result in results:
            con = result['confidence']
            cs = result['class']
            x1 = int(result['xmin'])
            y1 = int(result['ymin'])
            x2 = int(result['xmax'])
            y2 = int(result['ymax'])
            # Do whatever you want
            print(x1, y1, x2, y2, con, cs)
            #cv2.rectangle(frame, (x1, y1), (x2, y2), COLORS[0], 2)



if __name__ == "__main__":
    m = Model()
    m.detect(cv2.imread("DetectionTest/bus_img_test_0.jpg"))
