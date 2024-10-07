import json
import math
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from pathlib import Path
from typing import Any, List, Literal

import lightning
import numpy as np
import torch
from PIL import Image
from lightning import Trainer
from sklearn.metrics import confusion_matrix
from sklearn.utils import compute_class_weight
from torch import nn, optim
from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import CLIPVisionModelWithProjection, AutoProcessor, AutoModel, AutoTokenizer

# noinspection PyProtectedMember
from em.teach import _TeachNamingAndStateTrackingHandler, FOLLOWER_AGENT_ID, ACTION_ID_DIALOG, TEACH_INTERACTION_ACTIONS


class _ClipFeatureExtractor:

    def __init__(self,
                 clip_version: str = 'openai/clip-vit-base-patch32',
                 penultimate_layer_features=False,
                 device: str = None):
        super().__init__()
        self.vision_model = CLIPVisionModelWithProjection.from_pretrained(clip_version)
        self.processor = AutoProcessor.from_pretrained(clip_version)
        self.vision_model.to(device)
        self.device = device
        self._worker = ThreadPoolExecutor(max_workers=16)
        self.penultimate_layer_features = penultimate_layer_features

    def __call__(self, image_files):
        images = list(self._worker.map(lambda f: Image.open(str(f)).convert("RGB"), image_files))
        inputs = self.processor(images=images, return_tensors="pt", padding=True)
        inputs = inputs.to(self.device)
        image_outputs = self.vision_model(**inputs)
        if self.penultimate_layer_features:
            hidden_states = image_outputs.last_hidden_state
            return hidden_states
        else:
            img_feats = image_outputs.image_embeds
            img_feats = img_feats / img_feats.norm(p=2, dim=-1, keepdim=True)
            img_feats = img_feats.reshape(-1, img_feats.shape[-1])
            return img_feats


@torch.no_grad()
def preprocess_teach_data(
        teach_base: Path,
        split: str,
        output_file: Path,
        clip_version: str = 'openai/clip-vit-base-patch32',
        penultimate_layer_features=False,
        device: str = None,
):
    img_dir = teach_base / 'images' / split
    game_dir = teach_base / 'games' / split

    clip = _ClipFeatureExtractor(clip_version, penultimate_layer_features, device)

    result = {}
    episode_names = [p.name for p in img_dir.iterdir()]
    with tqdm(episode_names) as ep_iter:
        for episode in ep_iter:
            preprocessed_ep = _preprocess_episode(clip, episode, game_dir, img_dir)
            if preprocessed_ep:
                result[episode] = preprocessed_ep

    torch.save({
        'data': result,
        'action_vocab': sorted(set(chain(*(x['action_labels'] for x in result.values())))),
        'obj_vocab': sorted(set(chain(*(x['obj_labels'] for x in result.values())))),
    }, output_file)


def _preprocess_episode(clip_feature_extractor, episode, game_dir, img_dir):
    game_file = game_dir / f'{episode}.game.json'
    if not game_file.is_file():
        return
    game = json.loads(game_file.read_text())
    helper = _TeachNamingAndStateTrackingHandler(game)

    img_files = []
    action_labels = []
    action_obj_labels = []
    utterances = []
    timestamps = []
    for step in game['tasks'][0]['episodes'][0]['interactions']:
        action_id = step['action_id']
        agent = step['agent_id']
        ts = step['time_start']
        timestamps.append(str(ts))
        img_files.append(img_dir / episode / f'driver.frame.{ts}.jpeg')
        if helper.is_relevant_action(action_id) and agent == FOLLOWER_AGENT_ID and action_id != ACTION_ID_DIALOG:
            # noinspection PyProtectedMember
            action_labels.append(helper._action_id_to_name[action_id])
            if 'oid' in step and step['oid']:
                action_obj_labels.append(step['oid'].split('|')[0])
            else:
                action_obj_labels.append('')
        else:
            action_labels.append('')
            action_obj_labels.append('')
        if action_id == ACTION_ID_DIALOG:
            utterances.append(('Follower' if agent == FOLLOWER_AGENT_ID else 'Commander',
                               step.get("corrected_utterance", step["utterance"])))
        else:
            utterances.append(None)

    features = []
    bsz = 512
    for b in range(math.ceil(len(img_files) / bsz)):
        batch = img_files[b * bsz:(b + 1) * bsz]
        features.append(clip_feature_extractor(batch).cpu())
    features = torch.cat(features, dim=0)

    return {
        'id': episode,
        'timestamps': timestamps,
        'utterances': utterances,
        'features': features,
        'action_labels': action_labels,
        'obj_labels': action_obj_labels,
    }


def preprocess_yolo_obj_dets(yolo_world_obj_det_dir: Path,
                             transformer_model_name: str,
                             output_file: Path,
                             max_detections_per_img=3,
                             min_confidence=0.15):
    if output_file.is_file():
        results = torch.load(output_file)
    else:
        results = {}

    tokenizer = AutoTokenizer.from_pretrained(transformer_model_name)
    with tqdm(list(yolo_world_obj_det_dir.iterdir())) as iterator:
        for obj_det_dir in iterator:
            if not obj_det_dir.is_dir():
                continue
            sample_id = obj_det_dir.name
            aux_inputs = []
            json_files = sorted(obj_det_dir.glob('driver.frame.*.*.json'), key=lambda f: float(f.name[13:-5]))
            if sample_id in results and len(json_files) == len(results[sample_id]):
                continue
            for obj_det_file in json_files:
                obj_det = json.loads(obj_det_file.read_text())
                sorted_dets = sorted(obj_det['detections'], key=lambda det: det['confidence'], reverse=True)
                top_k = sorted_dets[:max_detections_per_img]
                above_threshold = [det for det in top_k if det['confidence'] > min_confidence]
                detections = ' '.join(det['class'] for det in above_threshold)
                aux_inputs.append(tokenizer(detections, add_special_tokens=False).input_ids if detections else [])
            results[sample_id] = aux_inputs

    torch.save(results, output_file)


class TeachActivityRecoTransformer(lightning.LightningModule):
    def __init__(self, transformer_base_model, action_vocab, obj_vocab, img_hidden_dim,
                 use_penultimate_features: int = None,
                 penultimate_feature_compression_factor: int = 1,
                 mode: Literal['actions', 'objects', 'both'] = 'both',
                 enable_obj_aux_input=True,
                 obj_ignore_empty_indices=False,
                 obj_class_loss_weights=None,
                 obj_classifier_bias=False):
        super().__init__()
        self.use_penultimate_features = use_penultimate_features
        self.penultimate_feature_compression_factor = penultimate_feature_compression_factor
        self.lr = 1e-3
        self.enable_obj_aux_input = enable_obj_aux_input
        self.action_vocab = action_vocab
        self.obj_vocab = obj_vocab
        self.transformer = AutoModel.from_pretrained(transformer_base_model)
        if hasattr(self.transformer, 'encoder'):
            self.transformer = self.transformer.encoder  # Token classification => only use encoder model
        self.transformer.requires_grad_(False)
        h = self.transformer.config.hidden_size
        if use_penultimate_features:
            assert use_penultimate_features % penultimate_feature_compression_factor == 0
            self.img_adapter = nn.Linear(
                (use_penultimate_features // penultimate_feature_compression_factor) * img_hidden_dim
                if use_penultimate_features else img_hidden_dim, h)
        else:
            self.img_adapter = nn.Linear(img_hidden_dim, h)
        if mode in ['actions', 'both']:
            self.action_classifier = nn.Linear(h, len(action_vocab))
        else:
            self.action_classifier = None
        if mode in ['objects', 'both']:
            self.obj_classifier = nn.Linear(h, len(obj_vocab), bias=obj_classifier_bias)
        else:
            self.obj_classifier = None
        self.action_loss_fct = CrossEntropyLoss()
        self.obj_loss_fct = CrossEntropyLoss(
            weight=None if obj_class_loss_weights is None else torch.as_tensor(obj_class_loss_weights,
                                                                               dtype=torch.float),
            ignore_index=0 if obj_ignore_empty_indices else -100)
        self.save_hyperparameters()

    def forward(self, sample: dict) -> Any:
        img_features = sample['features']

        img_shape = img_features.shape
        if self.use_penultimate_features:
            assert len(img_shape) == 4
            v = img_shape[2]  # vision tokens
            img_features = img_features.reshape(
                *img_shape[:2],  # B x T
                v // self.penultimate_feature_compression_factor,
                self.penultimate_feature_compression_factor,
                img_shape[-1]  # H
            )
            img_features = img_features.mean(dim=3)
            img_features = img_features.reshape(*img_shape[:2], -1)
        else:
            assert len(img_shape) == 3
        transformed_imgs = self.img_adapter(img_features)
        if 'obj_aux_input' in sample and self.enable_obj_aux_input:
            embeddings = self.transformer.get_input_embeddings()
            embedded_aux_input_flat = embeddings(
                torch.tensor(list(chain(*sample['obj_aux_input'])), device=self.device)
            )[None, :]  # bsz (=1) X num aux inputs X embed dim
            aux_input_lengths = torch.tensor([len(x) for x in sample['obj_aux_input']])
            aux_input_to_flat_indices = torch.cumsum(aux_input_lengths, dim=0) - aux_input_lengths
            seq = []
            mask = []
            for i in range(transformed_imgs.shape[1]):
                idx = aux_input_to_flat_indices[i]
                length = aux_input_lengths[i]
                seq.append(embedded_aux_input_flat[:, idx:idx + length])
                mask += [False] * length
                seq.append(transformed_imgs[:, i:i + 1])
                mask.append(True)
            input_seq = torch.cat(seq, dim=1)
            classifier_mask = torch.tensor([mask], device=self.device, dtype=torch.bool)
        else:
            input_seq = transformed_imgs
            classifier_mask = torch.ones(*transformed_imgs.shape[:2], device=self.device, dtype=torch.bool)
        output = self.transformer(inputs_embeds=input_seq)
        states = output.last_hidden_state
        classifier_relevant_states = states[classifier_mask]
        if self.action_classifier is None:
            action_logits = torch.zeros(classifier_relevant_states.shape[0],
                                        len(self.action_vocab),
                                        dtype=self.dtype, device=self.device)
        else:
            action_logits = self.action_classifier(classifier_relevant_states)
        if self.obj_classifier is None:
            obj_logits = torch.zeros(classifier_relevant_states.shape[0],
                                     len(self.obj_vocab),
                                     dtype=self.dtype, device=self.device)
        else:
            obj_logits = self.obj_classifier(classifier_relevant_states)

        return action_logits, obj_logits

    def _calc_loss(self, batch, action_logits, obj_logits):
        action_labels = batch['action_labels']
        obj_labels = batch['obj_labels']

        action_loss = self.action_loss_fct(action_logits.view(-1, len(self.action_vocab)), action_labels.view(-1))
        obj_loss = self.obj_loss_fct(obj_logits.view(-1, len(self.obj_vocab)), obj_labels.view(-1))

        return action_loss, obj_loss

    def training_step(self, batch, batch_idx):
        action_logits, obj_logits = self(batch)
        action_loss, obj_loss = self._calc_loss(batch, action_logits, obj_logits)
        total_loss = action_loss + obj_loss

        self.log_dict({'train_action_loss': action_loss,
                       'train_obj_loss': obj_loss,
                       'train_loss': total_loss})

        return total_loss

    def validation_step(self, batch, batch_idx):
        action_labels = batch['action_labels'].to(self.device)
        obj_labels = batch['obj_labels'].to(self.device)

        action_logits, obj_logits = self(batch)
        action_loss, obj_loss = self._calc_loss(batch, action_logits, obj_logits)

        action_scores, obj_scores = torch.softmax(action_logits, dim=-1), torch.softmax(obj_logits, dim=-1)
        action_pred, obj_pred = torch.argmax(action_scores, dim=-1), torch.argmax(obj_scores, dim=-1)
        # noinspection PyTypeChecker
        action_acc = torch.sum(action_pred == action_labels).item() / action_labels.numel()
        # noinspection PyTypeChecker
        obj_acc = torch.sum(obj_pred == obj_labels).item() / obj_labels.numel()
        non_empty_indices = obj_labels != 0
        # noinspection PyTypeChecker
        obj_acc_ignore_empty = torch.sum(obj_pred[non_empty_indices[0]] ==
                                         obj_labels[non_empty_indices]).item() / non_empty_indices.sum()

        self.log_dict({'val_action_loss': action_loss,
                       'val_obj_loss': obj_loss,
                       'val_loss': action_loss + obj_loss,
                       'val_action_acc': action_acc,
                       'val_obj_acc': obj_acc,
                       'val_obj_acc_ignore_empty': obj_acc_ignore_empty,
                       'val_acc': (action_acc + obj_acc) / 2.0})

    def predict_step(self, batch, batch_idx):
        action_logits, obj_logits = self(batch)
        action_scores, obj_scores = torch.softmax(action_logits, dim=-1), torch.softmax(obj_logits, dim=-1)
        action_pred, obj_pred = torch.argmax(action_scores, dim=-1), torch.argmax(obj_scores, dim=-1)
        return {
            'id': batch['id'],
            'timestamps': batch['timestamps'],
            'action_scores': action_scores,
            'obj_scores': obj_scores,
            'action_pred': action_pred,
            'obj_pred': obj_pred,
        }

    def configure_optimizers(self):
        optimizer = optim.Adam(self.parameters(), lr=self.lr)
        return optimizer


def load_dataset(preprocessed_file: Path, obj_det_preprocessed_file: Path = None):
    data = torch.load(preprocessed_file)
    action_vocab, obj_vocab = data['action_vocab'], data['obj_vocab']
    obj_detections = {} if obj_det_preprocessed_file is None else torch.load(obj_det_preprocessed_file)

    samples = []
    for sample_id, sample in data['data'].items():
        ds_sample = {
            'id': sample_id,
            'features': sample['features'],
            'action_labels': torch.tensor([action_vocab.index(a) for a in sample['action_labels']]),
            'obj_labels': torch.tensor([obj_vocab.index(a) for a in sample['obj_labels']]),
        }
        samples.append(ds_sample)
        if sample_id not in obj_detections:
            continue
        obj_det_for_sample = obj_detections[sample_id]
        assert len(obj_det_for_sample) == len(sample['timestamps']), sample_id
        ds_sample['obj_aux_input'] = obj_det_for_sample

    # noinspection PyTypeChecker
    return DataLoader(samples, shuffle='train' in preprocessed_file.name), action_vocab, obj_vocab


def train(train_file: Path, val_file: Path, transformer_model: str, obj_det_preprocessed_file=None,
          warmup_epochs: int = None, warmup_phase_lr=1e-3,
          use_obj_class_weighing=False, model_args: dict = None,
          lr=1e-3, **trainer_args):
    train_data, action_vocab, obj_vocab = load_dataset(train_file, obj_det_preprocessed_file)
    val_data, _, _ = load_dataset(val_file, obj_det_preprocessed_file)
    img_feature_shape = next(iter(train_data))['features'].shape
    img_hidden_dim = img_feature_shape[-1]
    model_args['use_penultimate_features'] = img_feature_shape[-2] if len(img_feature_shape) == 4 else None
    if use_obj_class_weighing:
        all_obj_labels = np.concatenate([np.asarray(sample['obj_labels'][0])
                                         for sample in iter(train_data)])
        model_args['obj_class_loss_weights'] = compute_class_weight(
            'balanced', classes=np.arange(len(obj_vocab)), y=all_obj_labels)
    model = TeachActivityRecoTransformer(transformer_model, action_vocab,
                                         obj_vocab, img_hidden_dim, **(model_args or {}))
    trainer = Trainer(**trainer_args)
    if warmup_epochs:
        model.lr = warmup_phase_lr
        prev = trainer.max_epochs
        trainer.fit_loop.max_epochs = warmup_epochs
        trainer.fit(model=model, train_dataloaders=train_data, val_dataloaders=val_data)
        trainer.fit_loop.max_epochs = prev
    if warmup_epochs is not None:
        model.transformer.requires_grad_(True)
        model.transformer.train()
    model.lr = lr
    trainer.fit(model=model, train_dataloaders=train_data, val_dataloaders=val_data)


@torch.no_grad()
def test(preprocessed_test_file: Path, episodes: List[str],
         ckpt_path: Path, output_path: Path,
         obj_det_preprocessed_file: Path = None,
         **trainer_args):
    preprocessed_data = torch.load(preprocessed_test_file)
    obj_detections = {} if obj_det_preprocessed_file is None else torch.load(obj_det_preprocessed_file)
    if episodes == '*':
        episodes = preprocessed_data['data'].keys()

    data = []
    for ep_id in episodes:
        episode = preprocessed_data['data'][ep_id]
        del episode['utterances']  # Causes problems with DataLoader since it contains None entries
        episode.setdefault('id', ep_id)
        if ep_id in obj_detections:
            episode['obj_aux_input'] = obj_detections[ep_id]
        data.append(episode)

    trainer = Trainer(**trainer_args)
    model = TeachActivityRecoTransformer.load_from_checkpoint(ckpt_path)

    # noinspection PyTypeChecker
    predictions = trainer.predict(model, DataLoader(data), return_predictions=True)

    action_vocab, obj_vocab = model.action_vocab, model.obj_vocab
    action_vocab.append('OOV')
    obj_vocab.append('OOV')
    action_oov, obj_oov = len(action_vocab) - 1, len(obj_vocab) - 1
    actions_true = [action_vocab.index(label) if label in action_vocab else action_oov
                    for sample in data for label in sample['action_labels']]
    objs_true = [obj_vocab.index(label) if label in obj_vocab else obj_oov
                 for sample in data for label in sample['obj_labels']]
    actions_pred = list(chain(*(pred['action_pred'].tolist() for pred in predictions)))
    objs_pred = list(chain(*(pred['obj_pred'].tolist() for pred in predictions)))

    torch.save({
        'predictions': predictions,
        'actions_true': actions_true,
        'objs_true': objs_true,
        'actions_pred': actions_pred,
        'objs_pred': objs_pred,
        'action_confusion_matrix': confusion_matrix(actions_true, actions_pred, labels=list(range(len(action_vocab)))),
        'obj_confusion_matrix': confusion_matrix(objs_true, objs_pred, labels=list(range(len(obj_vocab)))),
        'action_vocab': action_vocab,
        'obj_vocab': obj_vocab,
    }, output_path)


def export_test_output_to_teach_action_files(output_base_dir: Path, eval_file: Path, obj_eval_file: Path = None):
    data = torch.load(eval_file)
    if obj_eval_file is None:
        obj_data = data
    else:
        obj_data = torch.load(obj_eval_file)
    action_vocab, obj_vocab = data['action_vocab'], data['obj_vocab']
    obj_data_map = {
        p['id'][0]: p['obj_pred']
        for p in obj_data['predictions']
    }
    for pred in data['predictions']:
        ep_id = pred['id'][0]
        ep_dir = output_base_dir / ep_id
        ep_dir.mkdir(exist_ok=True)
        obj_pred = obj_data_map[ep_id]
        for (ts,), action_id, obj_id in zip(pred['timestamps'], pred['action_pred'], obj_pred):
            action = action_vocab[action_id]
            params = []
            if action in TEACH_INTERACTION_ACTIONS:
                params.append(obj_vocab[obj_id])
            (ep_dir / f'{ts}.json').write_text(json.dumps({
                'action': action,
                'params': params,
            }))
