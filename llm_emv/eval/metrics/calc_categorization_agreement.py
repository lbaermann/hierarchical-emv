import json
import sys
from pathlib import Path
from typing import List, Tuple, Union

from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support, cohen_kappa_score

from .categories import FineEmvOutputCategory, BroadEmvOutputCategory


def _extract_labels_from_files(gt_file: Path, pred_file: Path) -> Tuple[
    Union[List[FineEmvOutputCategory], List[BroadEmvOutputCategory]],  # true labels
    Union[List[FineEmvOutputCategory], List[BroadEmvOutputCategory]]  # predicted labels
]:
    gt_categories_result = json.loads(gt_file.read_text())
    auto_eval_result = json.loads(pred_file.read_text())

    broad_mode = any(sample['cat'] not in FineEmvOutputCategory.all_names()
                     for sample in auto_eval_result['results'].values())
    label_type = BroadEmvOutputCategory if broad_mode else FineEmvOutputCategory

    labels_true, labels_pred = [], []
    for key, result in gt_categories_result['results'].items():
        assert 'cat' in result, f'{key} in {gt_file}'
        true_cat = FineEmvOutputCategory(result['cat'])
        labels_true.append(true_cat.broad if broad_mode else true_cat)
        labels_pred.append(label_type(auto_eval_result['results'][key]['cat']))

        if labels_true[-1] != labels_pred[-1]:
            print()
            print('Q   :', result['q'])
            print('GT  :', result['gt'])
            print('HYP :', result['hyp'])
            print('CAT :', result['cat'])
            print('PRED:', labels_pred[-1])

    return labels_true, labels_pred


def _print_results(name: str, y_true, y_pred, labels):
    max_label_len = max(len(lbl.name) for lbl in labels)

    print(f'\n** {name} **\n')
    print('Accuracy:', accuracy_score(y_true, y_pred))
    print('Confusion matrix:')
    print(confusion_matrix(y_true, y_pred, labels=list(range(len(labels)))))
    print('\nDetailed metrics:')
    precision, recall, f_score, support = precision_recall_fscore_support(y_true, y_pred)
    for cls, p, r, f, s in zip(labels, precision, recall, f_score, support):
        print(f'{cls.name.rjust(max_label_len)}: p={p:.2f}, r={r:.2f}, f={f:.2f}, n={s:0>3}')
    final_line = ('Macro ø'.rjust(max_label_len) + f': p={precision.mean():.2f}, r={recall.mean():.2f}, '
                                                   f'f={f_score.mean():.2f}, n={support.sum():0>3}')
    print('_' * len(final_line))
    print(final_line)


def main():
    y_true, y_pred = [], []
    y_true_broad, y_pred_broad = [], []
    cfg_name = sys.argv[1]
    fine_mode = True
    for arg in sys.argv[2:]:
        gt_file = Path(arg)
        pred_file = gt_file.with_suffix(f'.{cfg_name}.auto_eval.json')
        if not pred_file.is_file():
            print('!!! WARNING: Skipping non-existing prediction file', pred_file)
            continue

        gt_labels, pred_labels = _extract_labels_from_files(gt_file, pred_file)
        fine_mode = fine_mode and isinstance(gt_labels[0], FineEmvOutputCategory)

        if fine_mode:
            y_true += [c.index for c in gt_labels]
            y_pred += [c.index for c in pred_labels]
            y_true_broad += [c.broad.index for c in gt_labels]
            y_pred_broad += [c.broad.index for c in pred_labels]
        else:
            y_true_broad += [c.index for c in gt_labels]
            y_pred_broad += [c.index for c in pred_labels]

    if fine_mode:
        _print_results('Fine labels', y_true, y_pred, FineEmvOutputCategory)
    _print_results('Broad labels', y_true_broad, y_pred_broad, BroadEmvOutputCategory)


def inter_annotator_agreement(file_pairs: List[Tuple[Path, Path]]):
    label_pairs = []

    for f1, f2 in file_pairs:
        d1 = json.loads(f1.read_text())['results']
        d2 = json.loads(f2.read_text())['results']
        for key in d1.keys():
            if key in d2:
                label_pairs.append(
                    (FineEmvOutputCategory(d1[key]['cat']),
                     FineEmvOutputCategory(d2[key]['cat']))
                )

    y1 = [x[0].index for x in label_pairs]
    y2 = [x[1].index for x in label_pairs]
    y1_broad = [x[0].broad.index for x in label_pairs]
    y2_broad = [x[1].broad.index for x in label_pairs]
    print('Samples:', len(label_pairs))
    print("Fine labels cohen's kappa  :", cohen_kappa_score(y1, y2))
    print("Broad labels cohen's kappa :", cohen_kappa_score(y1_broad, y2_broad))
    print("Correct/Wrong cohen's kappa:", cohen_kappa_score(y1_broad, y2_broad, labels=[
        BroadEmvOutputCategory.correct.index, BroadEmvOutputCategory.wrong.index]))
    print("Partially correct cohen's kappa:", cohen_kappa_score(y1, y2, labels=[
        FineEmvOutputCategory.partially_correct_missing.index,
        FineEmvOutputCategory.partially_correct_tmi.index]))


if __name__ == '__main__':
    main()
