"""
Adapted from https://github.com/AILab-CVC/YOLO-World/blob/master/deploy/onnx_demo.py.
Needs an environment as described there.
"""

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort
import supervision as sv
from mmengine.utils import ProgressBar

try:
    import torch
    from torchvision.ops import nms
except Exception as e:
    print(e)

BOUNDING_BOX_ANNOTATOR = sv.BoundingBoxAnnotator(thickness=1)
MASK_ANNOTATOR = sv.MaskAnnotator()


class LabelAnnotator(sv.LabelAnnotator):

    @staticmethod
    def resolve_text_background_xyxy(
            center_coordinates,
            text_wh,
            position,
    ):
        center_x, center_y = center_coordinates
        text_w, text_h = text_wh
        return center_x, center_y, center_x + text_w, center_y + text_h


LABEL_ANNOTATOR = LabelAnnotator(text_padding=4,
                                 text_scale=0.5,
                                 text_thickness=1)


def parse_args():
    parser = argparse.ArgumentParser('YOLO-World ONNX Demo')
    parser.add_argument('onnx', help='onnx file')
    parser.add_argument(
        'text',
        help=
        'detecting texts (str or json), should be consistent with the ONNX model'
    )
    parser.add_argument(
        'base_dir',
        type=Path,
        help='base dir that contains directories with images'
    )
    parser.add_argument(
        'game_ids',
        nargs='+',
        help='TEACh game ids, that must be directory names inside base_dir, containing many driver.frame.*.jpeg files.'
             'Use "*" for all game_ids inside that base_dir.'
    )
    parser.add_argument('--visualize', action='store_true', default=False)
    # assuming onnx-nms
    args = parser.parse_args()
    return args


def preprocess(image, size=(640, 640)):
    h, w = image.shape[:2]
    max_size = max(h, w)
    scale_factor = size[0] / max_size
    pad_h = (max_size - h) // 2
    pad_w = (max_size - w) // 2
    pad_image = np.zeros((max_size, max_size, 3), dtype=image.dtype)
    pad_image[pad_h:h + pad_h, pad_w:w + pad_w] = image
    image = cv2.resize(pad_image, size,
                       interpolation=cv2.INTER_LINEAR).astype('float32')
    image /= 255.0
    image = image[None]
    return image, scale_factor, (pad_h, pad_w)


def visualize(image, bboxes, labels, scores, texts):
    detections = sv.Detections(xyxy=bboxes, class_id=labels, confidence=scores)
    labels = [
        f"{texts[class_id][0]} {confidence:0.2f}" for class_id, confidence in
        zip(detections.class_id, detections.confidence)
    ]

    image = BOUNDING_BOX_ANNOTATOR.annotate(image, detections)
    image = LABEL_ANNOTATOR.annotate(image, detections, labels=labels)
    return image


def inference(ort_session,
              image_path,
              texts,
              output_file,
              size=(640, 640),
              visualize=False):
    # normal export
    # with NMS and postprocessing
    ori_image = cv2.imread(image_path)
    h, w = ori_image.shape[:2]
    image, scale_factor, pad_param = preprocess(ori_image[:, :, [2, 1, 0]], size)
    input_ort = ort.OrtValue.ortvalue_from_numpy(image.transpose((0, 3, 1, 2)))
    results = ort_session.run(["num_dets", "labels", "scores", "boxes"],
                              {"images": input_ort})
    num_dets, labels, scores, bboxes = results
    num_dets = num_dets[0][0]
    labels = labels[0, :num_dets]
    scores = scores[0, :num_dets]
    bboxes = bboxes[0, :num_dets]

    bboxes -= np.array(
        [pad_param[1], pad_param[0], pad_param[1], pad_param[0]])
    bboxes /= scale_factor
    bboxes[:, 0::2] = np.clip(bboxes[:, 0::2], 0, w)
    bboxes[:, 1::2] = np.clip(bboxes[:, 1::2], 0, h)
    bboxes = bboxes.round().astype('int')

    detections = sv.Detections(xyxy=bboxes, class_id=labels, confidence=scores)
    output_file.write_text(json.dumps({
        'detections': [
            {
                'class': texts[class_id][0],
                'confidence': float(confidence),
                'xyxy': bbox.tolist()
            }
            for class_id, confidence, bbox in zip(detections.class_id, detections.confidence, detections.xyxy)
        ]
    }))
    if visualize:
        labels = [
            f"{texts[class_id][0]} {confidence:0.2f}" for class_id, confidence in
            zip(detections.class_id, detections.confidence)
        ]
        output_image = BOUNDING_BOX_ANNOTATOR.annotate(ori_image, detections)
        output_image = LABEL_ANNOTATOR.annotate(output_image, detections, labels=labels)
        cv2.imwrite(output_file.with_suffix('.jpeg'), output_image)


def main():
    args = parse_args()
    onnx_file = args.onnx
    # init ONNX session
    ort_session = ort.InferenceSession(
        onnx_file, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    print("Init ONNX Runtime session")
    output_dir = Path("output_teach_objects")
    if not output_dir.is_dir():
        output_dir.mkdir(exist_ok=True)

    game_ids = args.game_ids
    if len(game_ids) == 1 and game_ids[0] == "*":
        game_ids = [f.name for f in args.base_dir.iterdir()]
    images = []
    for game_id in game_ids:
        img_files = list((args.base_dir / game_id).glob('driver.frame.*.jpeg'))
        images += img_files

    with open(args.text) as f:
        lines = f.readlines()
    texts = [[t.rstrip('\r\n')] for t in lines]

    print("Start to inference.")
    progress_bar = ProgressBar(len(images))
    for img in images:
        output_file = output_dir / img.parent.name / img.with_suffix('.json').name
        output_file.parent.mkdir(exist_ok=True)
        inference(ort_session, str(img), texts, output_file=output_file, visualize=args.visualize)
        progress_bar.update()
    print("Finish inference")


if __name__ == "__main__":
    main()
