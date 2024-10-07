"""This script depends on YOLO World"""
import json
import math
import traceback
from functools import cache
from pathlib import Path
from typing import List

import cv2
import numpy as np
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from tqdm import tqdm
from transformers import AutoTokenizer, CLIPVisionModelWithProjection, CLIPTextModelWithProjection, AutoProcessor

from em.em_tree import HigherLevelSummary, GoalBasedSummary, SceneGraphInstant, ObjectNode

import torch
from mmengine.config import Config, DictAction
from mmengine.runner.amp import autocast
from mmengine.dataset import Compose
from mmengine.utils import ProgressBar
from mmdet.apis import init_detector
from mmdet.utils import get_test_pipeline_cfg

import supervision as sv

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


class YoloWorld:
    def __init__(self, config: str, checkpoint: str, device: str,
                 max_detections=100,
                 score_threshold=0.3,
                 use_amp=False,
                 ):
        # load config
        self.use_amp = use_amp
        self.score_threshold = score_threshold
        self.max_detections = max_detections
        cfg = Config.fromfile(config)
        cfg.work_dir = Path('./work_dirs') / Path(config).stem
        # init model
        cfg.load_from = checkpoint
        self.model = init_detector(cfg, checkpoint=checkpoint, device=device)
        pipeline = self.model.cfg.test_dataloader.dataset.pipeline
        pipeline[0].type = 'mmdet.LoadImageFromNDArray'
        self.test_pipeline = Compose(pipeline)
        self.texts = []

    def reconfigure_with_texts(self, texts: List[str]):
        self.texts = [[t] for t in texts]
        self.model.reparameterize(self.texts)

    def detect_objects(self,
                       image: np.ndarray,
                       output_file: Path = None):
        data_info = dict(img_id=0, img=image, texts=self.texts)
        data_info = self.test_pipeline(data_info)
        data_batch = dict(inputs=data_info['inputs'].unsqueeze(0),
                          data_samples=[data_info['data_samples']])

        with autocast(enabled=self.use_amp), torch.no_grad():
            output = self.model.test_step(data_batch)[0]
            pred_instances = output.pred_instances
            pred_instances = pred_instances[pred_instances.scores.float() > self.score_threshold]

        if len(pred_instances.scores) > self.max_detections:
            indices = pred_instances.scores.float().topk(self.max_detections)[1]
            pred_instances = pred_instances[indices]

        pred_instances = pred_instances.cpu().numpy()

        if 'masks' in pred_instances:
            masks = pred_instances['masks']
        else:
            masks = None

        detections = sv.Detections(xyxy=pred_instances['bboxes'],
                                   class_id=pred_instances['labels'],
                                   confidence=pred_instances['scores'],
                                   mask=masks)
        if output_file:
            labels = [
                f"{self.texts[class_id][0]} {confidence:0.2f}" for class_id, confidence in
                zip(detections.class_id, detections.confidence)
            ]
            image = BOUNDING_BOX_ANNOTATOR.annotate(image, detections)
            image = LABEL_ANNOTATOR.annotate(image, detections, labels=labels)
            if masks is not None:
                image = MASK_ANNOTATOR.annotate(image, detections)
            cv2.imwrite(str(output_file), image)

        return [self.texts[class_id][0] for class_id in detections.class_id]


class ClipBasedObjectCategoryProposal:
    def __init__(self,
                 clip_version: str = 'openai/clip-vit-base-patch32',
                 device: str = None,
                 top_k_default_objects=100):
        device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.top_k_default_objects = top_k_default_objects
        self.device = device
        tokenizer = AutoTokenizer.from_pretrained(clip_version)
        self.vision_model = CLIPVisionModelWithProjection.from_pretrained(clip_version)
        text_model = CLIPTextModelWithProjection.from_pretrained(clip_version)
        self.processor = AutoProcessor.from_pretrained(clip_version)
        self.vision_model.to(device)
        text_model.to(device)

        self.default_categories = _get_object_db()
        with torch.no_grad():
            bsz = 128
            all_feats = []
            for i in range(math.ceil(len(self.default_categories) / bsz)):
                default_texts = tokenizer(text=self.default_categories[i * bsz:(i + 1) * bsz],
                                          return_tensors='pt', padding=True).to(device)
                default_txt_feats = text_model(**default_texts).text_embeds
                default_txt_feats = default_txt_feats / default_txt_feats.norm(p=2, dim=-1, keepdim=True)
                all_feats.append(default_txt_feats.reshape(-1, default_txt_feats.shape[-1]))
            self.default_txt_feats = torch.cat(all_feats, dim=0)

    def _forward_clip_vision_model(self, images):
        inputs = self.processor(images=images, return_tensors="pt", padding=True)
        inputs = inputs.to(self.device)
        image_outputs = self.vision_model(**inputs)
        img_feats = image_outputs.image_embeds
        img_feats = img_feats / img_feats.norm(p=2, dim=-1, keepdim=True)
        img_feats = img_feats.reshape(-1, img_feats.shape[-1])
        return img_feats

    def score_images(self, np_images: np.ndarray):
        img_feats = self._forward_clip_vision_model(np_images)
        # Batch mean to simplify YoloWorld object categories (fixed per goal)
        mean_img_feats = torch.mean(img_feats, dim=0)[None, ...]  # keep bsz=1

        scores = (self.default_txt_feats @ mean_img_feats.T).T
        scores_sorted, high_to_low_ids = torch.sort(scores, descending=True)
        return [self.default_categories[i] for i in high_to_low_ids[0]][:self.top_k_default_objects]


@cache
def _get_object_db():
    # Load object categories from LVIS. Inspired by Google's "Socratic Models", but using LVIS instead of Tencent ML
    #  Images, since the latter has way too many object classes leading to weird false detections
    cache_file = Path(__file__).parent / 'lvis_val_100_classes.json'
    return json.loads(cache_file.read_text())


def _iter_goals(history: HigherLevelSummary):
    for c in history.children:
        if isinstance(c, GoalBasedSummary):
            yield c
        else:
            yield from _iter_goals(c)


@torch.no_grad()
def insert_objs_into_history(
        history: HigherLevelSummary,
        obj_proposal_llm: BaseChatModel,
        obj_detector: YoloWorld,
        clip_base_class_filter: ClipBasedObjectCategoryProposal,
        img_output_dir: Path = None
):
    proposal_chain = (
                             SystemMessagePromptTemplate.from_template(
                                 'Your task is to generate a JSON list of strings of objects that are likely to '
                                 'appear in the context of the given activity. No other output.'
                             )
                             + HumanMessagePromptTemplate.from_template('Current activity: {activity}')
                     ) | obj_proposal_llm | JsonOutputParser()

    with tqdm(list(_iter_goals(history))) as iterable:
        for goal_node in iterable:
            goal = goal_node.explicit_goal or goal_node.latest_raw.current_goal
            all_scenes = [s for e in goal_node.events for s in e.scenes]
            np_images = np.stack([np.array(s.raw.image) for s in all_scenes])
            filtered_base_classes = clip_base_class_filter.score_images(np_images)

            try:
                additional_objects = proposal_chain.invoke(dict(activity=goal))
                additional_objects = [x for x in additional_objects if isinstance(x, str)]
            except:
                traceback.print_exc()
                additional_objects = []

            obj_detector.reconfigure_with_texts(filtered_base_classes + additional_objects)

            scene: SceneGraphInstant
            for img, scene in zip(np_images, all_scenes):
                detections = obj_detector.detect_objects(
                    img, img_output_dir / f'scene-{scene.raw.timestamp.timestamp()}.png' if img_output_dir else None)
                objs_with_id = [
                    (d, detections[:i].count(d))
                    for i, d in enumerate(detections)
                ]
                scene.objects = [ObjectNode(o, f'{o}_{oid}') for o, oid in objs_with_id]

    return history
