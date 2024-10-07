import argparse
import pickle
import traceback
from collections import OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Dict

import numpy as np
import torch
import torch.utils.data
import torchvision.transforms as transforms
import torchvision.transforms._transforms_video as transforms_video
from PIL import Image
from tqdm import tqdm
from transformers import AutoTokenizer

from ..em_tree import EventBasedSummary, SceneGraphInstant, RawDataInstant, HigherLevelSummary
from ..rule_based_summary import select_goal_indices, build_goal_summaries_with_indices

try:
    from moviepy.editor import VideoFileClip
    from src.data.video_transforms import Permute
    from src.models.video_recap import VideoRecap
    from src.data.datasets import VideoCaptionDataset, CaptionDataCollator
    from src.models.timesformer import SpaceTimeTransformer
    from src.models.openai_model import QuickGELU
    from src.configs.defaults import defaultConfigs
except ImportError:
    print('VideoReCapHistoryLoader requires installing https://github.com/md-mohaiminul/VideoRecap')
    traceback.print_exc()


class ReverseNormalize(torch.nn.Module):

    def __init__(self, forward_normalize) -> None:
        super().__init__()
        self.mean = forward_normalize.mean
        self.std = forward_normalize.std

    def forward(self, img):
        mean = torch.as_tensor(self.mean, dtype=img.dtype, device=img.device).view(-1, 1, 1)
        std = torch.as_tensor(self.std, dtype=img.dtype, device=img.device).view(-1, 1, 1)
        return img * std + mean


# Adapted from https://github.com/md-mohaiminul/VideoRecap/blob/master/demo.ipynb

class VideoReCapHistoryLoader:
    segment_old_args: Any
    segment_tokenizer: Any
    segment_collator: Any
    segment_model: Any

    video_old_args: Any
    video_tokenizer: Any
    video_collator: Any
    video_model: Any

    def __init__(self,
                 ckpt_dir: Path,
                 working_data_dir: Path,
                 clip_seconds=4,  # Extract clip caption at each 4 seconds
                 segment_seconds=180  # Extract one segment description at each 180 sconds
                 ):
        super().__init__()
        self.working_data_dir = working_data_dir.absolute()
        self.clip_seconds = clip_seconds
        self.segment_seconds = segment_seconds

        clip_ckpt_path = ckpt_dir / 'videorecap_clip.pt'
        clip_ckpt = torch.load(str(clip_ckpt_path), map_location='cpu')
        old_args = clip_ckpt['args']
        old_args.video_feature_type = 'pixel'
        old_args.num_video_feat = 4  # number of frames per clip caption
        old_args.video_loader_type = 'moviepy'
        old_args.chunk_len = -1  # load from raw video
        old_args.video_feature_path = str(self.working_data_dir)  # path to the video folder
        self.clip_old_args = old_args
        crop_size = 224
        self.video_transform = transforms.Compose([
            Permute([3, 0, 1, 2]),  # T H W C -> C T H W
            transforms.Resize(crop_size),
            transforms.CenterCrop(crop_size),
            transforms_video.NormalizeVideo(mean=[108.3272985, 116.7460125, 104.09373615000001],
                                            std=[68.5005327, 66.6321579, 70.32316305]),
        ])
        self.reverse_normalize_transform = ReverseNormalize(self.video_transform.transforms[-1])

        self.clip_tokenizer = AutoTokenizer.from_pretrained(old_args.decoder_name)
        self.clip_model = self._prepare_model_from_ckpt(clip_ckpt, clip_ckpt_path, name='clip')

        segment_ckpt_path = ckpt_dir / 'videorecap_segment.pt'
        self._load_higher_level_ckpt(str(segment_ckpt_path), name='segment')
        self.segment_old_args.clip_seconds = clip_seconds
        # NOTE: For this too work, need to modify VideoReCap/src/data/datasets.py:236 and following (inside if
        # self.args.dataset == 'segment_description'):
        #       clip_secs = getattr(self.args, 'clip_seconds', 4)
        #       start = int(s['start_sec']/clip_secs) if 'start_sec' in s else 0
        #       end = int(s['end_sec']//clip_secs) if 'end_sec' in s else video_features.shape[0]
        # github.com/md-mohaiminul/VideoRecap/blob/7dce249118e590d4fa28d5c7cff88f925747b0bf/src/data/datasets.py#L263

        video_ckpt_path = ckpt_dir / 'videorecap_video.pt'
        self._load_higher_level_ckpt(str(video_ckpt_path), name='video')

    def _load_higher_level_ckpt(self, ckpt_path: str, name=''):
        ckpt = torch.load(ckpt_path, map_location='cpu')
        old_args = ckpt['args']
        old_args.video_feature_type = 'cls'
        old_args.video_feature_path = str(self.working_data_dir)

        tokenizer = AutoTokenizer.from_pretrained(old_args.decoder_name)
        collator = CaptionDataCollator(tokenizer, max_gen_tokens=old_args.max_gen_tokens,
                                       add_bos=True, add_eos=True, pad_token_id=0)
        model = VideoReCapHistoryLoader._prepare_model_from_ckpt(ckpt, ckpt_path, name)

        setattr(self, f'{name}_old_args', old_args)
        setattr(self, f'{name}_tokenizer', tokenizer)
        setattr(self, f'{name}_collator', collator)
        setattr(self, f'{name}_model', model)

    @staticmethod
    def _prepare_model_from_ckpt(ckpt, ckpt_path, name=''):
        old_args = ckpt['args']

        state_dict = OrderedDict()
        for k, v in ckpt['state_dict'].items():
            state_dict[k.replace('module.', '')] = v

        print(f"=> Creating {name} model")
        model = VideoRecap(old_args, eval_only=True)
        model = model.cuda()
        model.load_state_dict(state_dict, strict=True)
        print(f"=> loaded resume checkpoint '{ckpt_path}' (epoch {ckpt['epoch']})")

        return model

    def __call__(self, video: Path, start_time: datetime = None):
        if start_time is None:
            start_time = datetime.now()

        v_id = str(abs(hash(str(video))))
        working_file = self.working_data_dir / f'{v_id}{video.suffix}'
        if not working_file.is_file():
            working_file.symlink_to(video)

        video = VideoFileClip(str(working_file))
        try:
            print('Video length', video.duration, 'seconds')

            data_loader, dataset = self._load_clip_data(v_id, video)
            captions, raw_imgs = self._generate_clip_captions(data_loader, dataset)

            features = self._extract_features(data_loader, dataset)
            np.save(str(self.working_data_dir / f'{v_id}.npy'), features)

            data_loader, dataset = self._load_segment_data(captions, v_id, video)
            segment_descriptions = self._generate_segment_descriptions(data_loader, dataset)

            data_loader, dataset = self._load_full_video_data(segment_descriptions, v_id, video)
            video_summary = self._generate_full_video_summary(data_loader, dataset)

            return _construct_hierarchy_from_recap_captions(captions, raw_imgs, segment_descriptions,
                                                            video_summary, start_time)
        finally:
            video.close()

    def _load_clip_data(self, v_id, video):
        caption_duration = self.clip_seconds

        metadata = []
        for i in np.arange(0, video.duration, caption_duration):
            metadata.append([v_id, i, min(i + caption_duration, video.duration)])
        print('number of captions', len(metadata))
        self.clip_old_args.metadata = metadata

        dataset = VideoCaptionDataset(self.clip_old_args, transform=self.video_transform)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=False,
                                                  num_workers=8, pin_memory=True, drop_last=False)
        return data_loader, dataset

    def _load_segment_data(self, captions, v_id, video):
        segment_step = self.segment_seconds
        metadata = []
        for i in np.arange(0, video.duration, segment_step):
            dd = {
                'vid': v_id,
                'start_sec': i,
                'end_sec': min(i + segment_step, video.duration),
                'captions_pred': []
            }
            for s, c in captions.items():
                if c[1] >= dd['start_sec'] and c[2] <= dd['end_sec']:
                    dd['captions_pred'].append(c)
            metadata.append(dd)
        print('Number of segments', len(metadata))
        self.segment_old_args.metadata = metadata
        dataset = VideoCaptionDataset(self.segment_old_args, transform=None)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=False, num_workers=4, pin_memory=True,
                                                  collate_fn=self.segment_collator, drop_last=False)
        return data_loader, dataset

    def _load_full_video_data(self, segment_descriptions, v_id, video):
        metadata = []
        dd = {
            'vid': v_id,
            'start_sec': 0,
            'end_sec': video.duration,
            'segment_descriptions_pred': []
        }
        for s, c in segment_descriptions.items():
            dd['segment_descriptions_pred'].append(c)
        metadata.append(dd)
        print('Number of segments', len(metadata))

        self.video_old_args.metadata = metadata
        dataset = VideoCaptionDataset(self.video_old_args, transform=None)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, collate_fn=self.video_collator,
                                                  num_workers=1, pin_memory=True, drop_last=False)
        return data_loader, dataset

    def _generate_clip_captions(self, data_loader, dataset):
        captions = {}
        caption_imgs = {}
        with torch.no_grad():
            for data_iter, samples in enumerate(data_loader):
                indices = samples['index']
                generated_text_ids, raw_imgs = self._forward_features_and_generate(self.clip_old_args, self.clip_model,
                                                                                   samples, self.clip_tokenizer)

                for j in range(generated_text_ids.shape[0]):
                    sample = dataset.samples[indices[j].item()]
                    start_sec, end_sec = sample[1], sample[2]
                    for k in range(self.clip_old_args.caption_num_return_sequences):
                        jj = j * self.clip_old_args.caption_num_return_sequences + k
                        generated_text_str = _decode_one(generated_text_ids[jj], self.clip_tokenizer).strip()
                        captions[start_sec] = sample + [generated_text_str]
                        caption_imgs[start_sec] = raw_imgs[j]
                        print(start_sec, end_sec, generated_text_str)
        return captions, caption_imgs

    def _generate_segment_descriptions(self, data_loader, dataset):
        segment_descriptions = {}
        with torch.no_grad():
            for data_iter, samples in enumerate(data_loader):
                indices = samples['indices']
                generated_text_ids, _ = self._forward_features_and_generate(self.segment_old_args, self.segment_model,
                                                                            samples, self.segment_tokenizer)

                for j in range(generated_text_ids.shape[0]):
                    sample = dataset.samples[indices[j].item()]
                    start_sec = sample['start_sec']
                    for k in range(self.segment_old_args.caption_num_return_sequences):
                        jj = j * self.segment_old_args.caption_num_return_sequences + k
                        generated_text_str = _decode_one(generated_text_ids[jj], self.segment_tokenizer).strip()
                        segment_descriptions[start_sec] = generated_text_str
                        print(sample['start_sec'], sample['end_sec'], generated_text_str)
        return segment_descriptions

    def _generate_full_video_summary(self, data_loader, dataset):
        video_summary = {}
        with torch.no_grad():
            for data_iter, samples in enumerate(data_loader):
                indices = samples['indices']
                generated_text_ids, _ = self._forward_features_and_generate(self.video_old_args, self.video_model,
                                                                            samples, self.video_tokenizer)

                for j in range(generated_text_ids.shape[0]):
                    sample = dataset.samples[indices[j].item()]
                    start_sec = sample['start_sec']
                    for k in range(self.video_old_args.caption_num_return_sequences):
                        jj = j * self.video_old_args.caption_num_return_sequences + k
                        generated_text_str = _decode_one(generated_text_ids[jj], self.video_tokenizer).strip()
                        video_summary[start_sec] = generated_text_str
                        print(generated_text_str)
        return video_summary

    def _forward_features_and_generate(self, args, model, samples, tokenizer):
        pil_imgs = None
        if hasattr(model, "vision_model"):
            image = samples["video_features"].permute(0, 2, 1, 3, 4).contiguous().cuda()  # BCTHW -> BTCHW
            if args.video_feature_type == 'pixel':
                real_imgs = self.reverse_normalize_transform(image[:, -1])
                pil_imgs = [Image.fromarray((i.permute(1, 2, 0)).to(torch.uint8).cpu().numpy()) for i in real_imgs]
            samples["video_features"] = model.vision_model.forward_features(
                image, use_checkpoint=args.use_checkpoint, cls_at_last=False)  # NLD
        queries = model.map_features(samples)
        assert args.caption_sample == 'multinomial_sample'
        generated_text_ids, ppls = model.generate(
            queries,
            tokenizer,
            do_sample=False,
            max_text_length=args.max_gen_tokens,
            num_return_sequences=args.caption_num_return_sequences,
        )
        return generated_text_ids, pil_imgs

    def _extract_features(self, data_loader, dataset):
        all_features = {}
        with torch.no_grad():
            for data_iter, samples in enumerate(tqdm(data_loader)):
                image = samples["video_features"].permute(0, 2, 1, 3, 4).contiguous().cuda()  # BCTHW -> BTCHW
                features = self.clip_model.vision_model.forward_features(image, cls_at_last=True)  # NLD
                for j in range(features.shape[0]):
                    start_sec = dataset.samples[samples['index'][j].item()][1]
                    all_features[start_sec] = features[j].detach().cpu().numpy()
        features = np.stack([all_features[s] for s in sorted(all_features.keys())])
        print(features.shape)
        return features


# Caption decoding function
def _decode_one(generated_ids, tokenizer):
    if tokenizer.eos_token_id == tokenizer.bos_token_id:
        if tokenizer.eos_token_id in generated_ids[1:].tolist():
            eos_id = generated_ids[1:].tolist().index(tokenizer.eos_token_id) + 1
        else:
            eos_id = len(generated_ids.tolist()) - 1
    elif tokenizer.eos_token_id in generated_ids.tolist():
        eos_id = generated_ids.tolist().index(tokenizer.eos_token_id)
    else:
        eos_id = len(generated_ids.tolist()) - 1
    generated_text_str = tokenizer.decode(generated_ids[1:eos_id].tolist())
    return generated_text_str


def _construct_hierarchy_from_recap_captions(captions: Dict[float, List[Any]],
                                             raw_imgs: Dict[float, Image.Image],
                                             segment_descriptions: Dict[float, str],
                                             video_summary: Dict[float, str],
                                             start_time: datetime):
    summaries = sorted(segment_descriptions.items())

    events = []
    for ts, caption in sorted(captions.items()):
        while len(summaries) > 1 and ts > summaries[1][0]:
            summaries.pop(0)
        events.append(EventBasedSummary(scenes=[SceneGraphInstant(objects=[], relations=[], raw=RawDataInstant(
            timestamp=start_time + timedelta(seconds=ts),
            image=raw_imgs[ts],
            current_action=caption[-1],
            current_goal=summaries[0][1] if summaries else None,
        ))]))

    goal_indices = select_goal_indices(events)
    goals = build_goal_summaries_with_indices(events, goal_indices)

    assert len(video_summary) == 1, str(video_summary)
    return HigherLevelSummary(
        nl_summary=next(iter(video_summary.values())),
        children=goals
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--working-dir', type=Path, required=True,
                        help='Working directory where features will be saved')
    parser.add_argument('-c', '--ckpt-dir', type=Path, required=True,
                        help='Directory where to find VideoReCap checkpoint files')
    parser.add_argument('-v', '--video', nargs='+', type=Path, required=True,
                        help='Video files to process.')
    parser.add_argument('-o', '--output-dir', type=Path, default=None,
                        help='Directory where to place result files. Defaults to working-dir')
    parser.add_argument('--clip-seconds', type=int, default=4, metavar='X',
                        help='Extract clip caption at each X seconds')
    parser.add_argument('--segment-seconds', type=int, default=180, metavar='X',
                        help='Extract segment description at each X seconds')
    args = parser.parse_args()

    assert args.working_dir.is_dir()
    assert args.ckpt_dir.is_dir()
    if not args.output_dir.is_dir():
        args.output_dir.mkdir()

    loader = VideoReCapHistoryLoader(args.ckpt_dir, args.working_dir, args.clip_seconds, args.segment_seconds)
    for video_file in args.video:
        result = loader(video_file)
        output_file = args.output_dir / f'{video_file.stem}.history.pkl'
        output_file.write_bytes(pickle.dumps(result))
        print('Wrote history loaded from', video_file, 'to', output_file)


if __name__ == '__main__':
    main()
