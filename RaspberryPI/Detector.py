import cv2
import Model


class Detector:

    def __init__(self):
        self.model = Model.Model()
        self.Camera = cv2.VideoCapture(0)

    def detect(self) -> list[list[str, float, int]] or None:
        ret, frame = self.Camera.read()

        if not ret:
            print('[DETCTOR] Failed to grab frame in Camera')
            raise Exception  # 추후에 바꿔야함

        return self.model.detect(frame)

    def __del__(self):
        self.Camera.release()


if __name__ == "__main__":
    detector = Detector()
    print(detector.detect())
