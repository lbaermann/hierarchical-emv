import json
import sys
from copy import deepcopy
from itertools import groupby
from pathlib import Path


def main():
    in_file = Path(sys.argv[1])
    dataset = json.loads(in_file.read_text())
    output_dataset = deepcopy(dataset)

    for history_id, episodes in dataset['data'].items():
        print('History ID', history_id)
        all_qa_samples = [
            sample
            for episode in episodes
            for qa_t, qa_samples in episode['qa'].items()
            for sample in qa_samples
        ]
        all_qa_serialized = json.dumps(all_qa_samples)
        all_qa_samples.sort(key=lambda sample: sample['pairid'])
        print('valuable:', 'valuable item' in all_qa_serialized)
        print('person:', 'person' in all_qa_serialized)
        print('medicine:', 'medicine' in all_qa_serialized)
        print('beverage:', 'beverage' in all_qa_serialized)
        print('stop:', 'stop' in all_qa_serialized)
        print('Num pairs:', len(all_qa_samples) // 2)
        should_skip = input('Skip history? (s = skip, p = print and skip, q = print and quit, other = continue): ')
        if should_skip in ('p', 'q'):
            for pair_id, qa_pair in groupby(all_qa_samples, key=lambda sample: sample['pairid']):
                qa_pair = list(qa_pair)
                print(' Q:', qa_pair[0]['question'])
                print('  >', qa_pair[0]['answer'])
                print('  <', qa_pair[0]['correction'])
        if should_skip == 'q':
            return
        if should_skip in ('s', 'p'):
            output_dataset['data'].pop(history_id)
            continue

        selected_pair_ids = []
        for i, (pair_id, qa_pair) in enumerate(groupby(all_qa_samples, key=lambda sample: sample['pairid'])):
            qa_pair = list(qa_pair)
            print('\nPair', pair_id, '(selected so far:', len(selected_pair_ids),
                  ', remaining pairs:', len(all_qa_samples) // 2 - i, ')')
            print(' Q:', qa_pair[0]['question'])
            print('   ', qa_pair[1]['question'])
            print(' A:', qa_pair[0]['answer'])
            print('   ', qa_pair[1]['answer'])
            print(' C:', qa_pair[0]['correction'])
            print('   ', qa_pair[1]['correction'])
            decision = input('Keep? (y = keep, other = drop): ')
            if decision == 'y':
                selected_pair_ids.append(pair_id)

        for episode in output_dataset['data'][history_id]:
            for qa_t, qa_samples in list(episode['qa'].items()):
                for sample in list(qa_samples):
                    if sample['pairid'] not in selected_pair_ids:
                        qa_samples.remove(sample)
                if len(qa_samples) == 0:
                    episode['qa'].pop(qa_t)

    in_file.with_suffix('.filtered.json').write_text(json.dumps(output_dataset, indent=2))


if __name__ == '__main__':
    main()
