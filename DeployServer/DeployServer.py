import time
import numpy as np

import torch
import cv2
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor

from pytorchvideo.transforms.functional import (
    uniform_temporal_subsample,
    short_side_scale_with_boxes,
    clip_boxes_to_image,
)
from torchvision.transforms._functional_video import normalize
from pytorchvideo.data.ava import AvaLabeledVideoFramePaths
from pytorchvideo.models.hub import slow_r50_detection

import warnings

warnings.filterwarnings(action='ignore')

# Load slow_r50_detection model
device = 'cuda'  # or 'cpu'
video_model = slow_r50_detection(True)  # Another option is slowfast_r50_detection
video_model = video_model.eval().to(device)

# Load Detectron2 Model
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.55  # set threshold for this model
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)

# Create an id to label name mapping
label_map, allowed_class_ids = AvaLabeledVideoFramePaths.read_label_map('ava_action_list.pbtxt')


# This method takes in an image and generates the bounding boxes for people in the image.
def get_person_bboxes(inp_img, predictor):
    predictions = predictor(inp_img.cpu().detach().numpy())['instances'].to('cpu')
    boxes = predictions.pred_boxes if predictions.has("pred_boxes") else None
    scores = predictions.scores if predictions.has("scores") else None
    classes = np.array(predictions.pred_classes.tolist() if predictions.has("pred_classes") else None)
    predicted_boxes = boxes[np.logical_and(classes == 0, scores > 0.75)].tensor.cpu()  # only person
    return predicted_boxes


def ava_inference_transform(
        clip,
        boxes,
        num_frames=4,  # if using slowfast_r50_detection, change this to 32
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


def getLabel(class_id: int):
    return label_map[class_id]


def predict(inp_imgs: torch.Tensor, thres=0.5) -> (list, list, list):
    # Generate people bbox predictions using Detectron2's off the self pre-trained predictor
    # We use the middle image in each clip to generate the bounding boxes.

    inp_img = inp_imgs[len(inp_imgs) // 2]
    inp_img = inp_img.permute(0, 1, 2)

    # Predicted boxes are of the form List[(x_1, y_1, x_2, y_2)]
    predicted_boxes = get_person_bboxes(inp_img, predictor)
    if len(predicted_boxes) == 0:
        return [], [], []

    inp_imgs = inp_imgs.permute(3, 0, 1, 2)
    # Preprocess clip and bounding boxes for video action recognition.
    inputs, inp_boxes, _ = ava_inference_transform(inp_imgs, predicted_boxes.numpy())
    # Prepend data sample id for each bounding box.
    # For more details refere to the RoIAlign in Detectron2
    inp_boxes = torch.cat([torch.zeros(inp_boxes.shape[0], 1), inp_boxes], dim=1)

    # Generate actions predictions for the bounding boxes in the clip.
    # The model here takes in the pre-processed video clip and the detected bounding boxes.
    preds = video_model(inputs.unsqueeze(0).to(device), inp_boxes.to(device))

    preds = preds.to('cpu')
    # The model is trained on AVA and AVA labels are 1 indexed so, prepend 0 to convert to 0 index.
    preds = torch.cat([torch.zeros(preds.shape[0], 1), preds], dim=1)

    top_scores, top_classes, top_labels = [], [], []

    for pred in preds:
        mask = pred >= thres
        top_scores.append(pred[mask].tolist())
        top_class = torch.squeeze(torch.nonzero(mask), dim=-1).tolist()
        top_classes.append(top_class)
        top_label = list(map(getLabel, top_class))
        top_labels.append(top_label)

    return top_scores, top_classes, top_labels


if __name__ == "__main__":
    video_data = list()
    prev_time = 0
    cap = cv2.VideoCapture(0)
    FPS = 4

    while True:

        ret, frame = cap.read()
        current_time = time.time() - prev_time

        if cv2.waitKey(1) & 0xFF == 27:
            break

        if (ret is True) and (current_time > 1. / FPS):
            prev_time = time.time()
            video_data.append(frame)

            if len(video_data) >= 4:
                inp_imgs = np.array(video_data)
                inp_imgs = torch.Tensor(inp_imgs)
                video_data = list()
                top_scores, top_classes, top_labels = predict(inp_imgs)
                print(top_scores)
                print(top_classes)
                print(top_labels)

    cap.release()
    cv2.destroyAllWindows()
