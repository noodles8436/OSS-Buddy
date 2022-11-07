import os
import warnings
import easyocr
import torch.hub
import numpy as np
import torch
import cv2

from pytorchvideo.transforms.functional import (
    uniform_temporal_subsample,
    short_side_scale_with_boxes,
    clip_boxes_to_image,
)
from torchvision.transforms._functional_video import normalize
from pytorchvideo.data.ava import AvaLabeledVideoFramePaths
from pytorchvideo.models.hub import slow_r50_detection

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore", category=UserWarning)
YOLO_PERSON_CLASS = 0
YOLO_BUS_LABEL = 5
device = 'cuda'  # or 'cpu'
FPS = 4


def ava_inference_transform(
        clip,
        boxes,
        num_frames=FPS,  # if using slowfast_r50_detection, change this to 32
        crop_size=256,
        data_mean=[0.45, 0.45, 0.45],
        data_std=[0.225, 0.225, 0.225],
        slow_fast_alpha=None,  # if using slowfast_r50_detection, change this to 4
):
    boxes = np.array(boxes)
    ori_boxes = boxes.copy()

    # Image [0, 255] -> [0, 1].
    clip = uniform_temporal_subsample(clip, num_frames)
    clip = clip.float()
    clip = clip / 255.0

    height, width = clip.shape[2], clip.shape[3]
    # The format of boxes is [x1, y1, x2, y2]. The input boxes are in the
    # range of [0, width] for x and [0,height] for y
    boxes = clip_boxes_to_image(boxes, height, width)

    # Resize short side to crop_size. Non-local and STRG uses 256.
    clip, boxes = short_side_scale_with_boxes(
        clip,
        size=crop_size,
        boxes=boxes,
    )

    # Normalize images by mean and std.
    clip = normalize(
        clip,
        np.array(data_mean, dtype=np.float32),
        np.array(data_std, dtype=np.float32),
    )

    boxes = clip_boxes_to_image(
        boxes, clip.shape[2], clip.shape[3]
    )

    # In case of slowfast, generate both pathways
    if slow_fast_alpha is not None:
        fast_pathway = clip
        # Perform temporal sampling from the fast pathway.
        slow_pathway = torch.index_select(
            clip,
            1,
            torch.linspace(
                0, clip.shape[1] - 1, clip.shape[1] // slow_fast_alpha
            ).long(),
        )
        clip = [slow_pathway, fast_pathway]

    return clip, torch.from_numpy(boxes), ori_boxes


class Model:

    def __init__(self):
        self.detector = torch.hub.load(repo_or_dir="WongKinYiu/yolov7", model='custom',
                                       path_or_model='YoloV7/yolov7.pt', autoshape=True)
        self.reader = easyocr.Reader(['en'], gpu=True)

        self.understander = slow_r50_detection(True)  # Another option is slowfast_r50_detection
        self.understander.eval().to(device)

        self.label_map, _ = AvaLabeledVideoFramePaths.read_label_map('ava_action_list.pbtxt')

    def detectObjects(self, inp_img: np.ndarray, confidence=0.5):
        inp_img = torch.Tensor(inp_img)
        inp_img = inp_img.permute(1, 0, 2)

        detections = self.detector(inp_img.cpu().detach().numpy())
        results = detections.pandas().xyxy[0].to_dict(orient="records")
        print(results)

        _pred_Person = list()
        _pred_Bus = list()

        for result in results:
            if result['confidence'] < confidence:
                continue

            xyxy = (result['xmin'], result['ymin'], result['xmax'], result['ymax'])

            if result['class'] == YOLO_PERSON_CLASS:
                _pred_Person.append(xyxy)

            if result['class'] == YOLO_BUS_LABEL:
                _pred_Bus.append(self.detectBusNumber(cvImg=inp_img, xyxy=xyxy))

        _pred_Person = np.array(_pred_Person)
        _pred_Person = torch.FloatTensor(_pred_Person)

        return _pred_Bus, _pred_Person

    def detectBusNumber(self, cvImg, xyxy):
        x1 = int(xyxy[0])
        x2 = int(xyxy[1])
        y1 = int(xyxy[2])
        y2 = int(xyxy[3])

        cropImg = cvImg[y1:int(y2 / 2), x1:x2, :]
        cropImg = cv2.cvtColor(cropImg, cv2.COLOR_BGR2GRAY)

        ocr_result = self.reader.readtext(cropImg)
        _data: list = list()

        if len(ocr_result) == 0:
            return _data

        for (bbox, text, prob) in ocr_result:
            _data.append([text, prob, (x1 + x2) // 2])

        return _data

    def understanding(self, inp_imgs: np.ndarray, thres=0.5) -> (list, list, list):

        def getLabel(class_id: int):
            return self.label_map[class_id]

        inp_img = inp_imgs[len(inp_imgs) // 2]
        _pred_Bus, _pred_Person = self.detectObjects(inp_img)

        if len(_pred_Person) == 0:
            return [], [], [], []

        inp_imgs = torch.Tensor(inp_imgs)

        inp_imgs = inp_imgs.permute(3, 0, 1, 2)
        inputs, inp_boxes, _ = ava_inference_transform(inp_imgs, _pred_Person.numpy())
        inp_boxes = torch.cat([torch.zeros(inp_boxes.shape[0], 1), inp_boxes], dim=1)

        preds = self.understander(inputs.unsqueeze(0).to(device), inp_boxes.to(device))
        preds = preds.to('cpu')
        preds = torch.cat([torch.zeros(preds.shape[0], 1), preds], dim=1)

        top_classes = []

        for pred in preds:
            mask = pred >= thres
            top_class = torch.squeeze(torch.nonzero(mask), dim=-1).tolist()
            top_classes.append(top_class)

        return _pred_Bus, _pred_Person, top_classes


if __name__ == "__main__":
    m = Model()
    output = m.detectObjects(cv2.imread("./DetectionTest/human_bus_img_test_1.jpeg"))
    print(output)
