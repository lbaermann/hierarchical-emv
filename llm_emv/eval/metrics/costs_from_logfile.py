import ast
import json
import sys
from pathlib import Path


def sum_costs_from_logfile(p: Path, json_file: Path = None):
    if json_file is None:
        if p.with_suffix('.json').is_file():
            json_file = p.with_suffix('.json')
    existing_samples = []
    if json_file:
        json_eval = json.loads(json_file.read_text())
        ooc_sample_ids = []
        for sample_id, sample in json_eval['results'].items():
            existing_samples.append(sample_id)
            if '###ERROR###' in sample['hyp'] and 'too long' in sample['hyp']:
                ooc_sample_ids.append(sample_id)
    else:
        ooc_sample_ids = []
    lines = p.read_text().splitlines()
    manual_token_prefix = 'Manual token count estimate: '
    cost_prefix = 'Total Cost (USD): $'
    prompt_tokens_prefix = '        Prompt Tokens: '
    completion_tokens_prefix = '        Completion Tokens: '
    current_sample_prefix = 'Evaluating sample '
    current_multi_samples_prefix = "Evaluating samples ['"
    total_cost = 0
    total_prompt_tokens, total_completion_tokens = 0, 0
    manual_tokens, manual_tokens_without_ooc, manual_tokens_existing_samples = 0, 0, 0
    manual_tokens_current_sample = 0
    current_sample = None
    for line in lines:
        if line.startswith(current_multi_samples_prefix):
            if current_sample and all(x in existing_samples for x in current_sample):
                manual_tokens_existing_samples += manual_tokens_current_sample
            current_sample = ast.literal_eval(line[len('Evaluating samples '):])
            manual_tokens_current_sample = 0
        if line.startswith(current_sample_prefix):
            if current_sample not in ooc_sample_ids:
                manual_tokens_without_ooc += manual_tokens_current_sample
            current_sample = line[len(current_sample_prefix):]
            manual_tokens_current_sample = 0
        if line.startswith(manual_token_prefix):
            number = line[len(manual_token_prefix):]
            if number.startswith('total_tokens: '):
                number = number[len('total_tokens: '):]
            manual_tokens += float(number)
            manual_tokens_current_sample += float(number)
        if line.startswith(cost_prefix):
            number = line[len(cost_prefix):]
            total_cost += float(number)
        if line.startswith(prompt_tokens_prefix):
            number = line[len(prompt_tokens_prefix):]
            total_prompt_tokens += int(number)
        if line.startswith(completion_tokens_prefix):
            number = line[len(completion_tokens_prefix):]
            total_completion_tokens += int(number)

    if current_sample and all(x in existing_samples for x in current_sample):
        manual_tokens_existing_samples += manual_tokens_current_sample
    if current_sample not in ooc_sample_ids:
        manual_tokens_without_ooc += manual_tokens_current_sample

    print('prompt tokens:    ', total_prompt_tokens)
    print('completion tokens:', total_completion_tokens)
    print('                 $', total_cost)
    print('manual tokens                 :', manual_tokens)
    print('manual tokens w/o OOC         :', manual_tokens_without_ooc)
    print('manual tokens existing samples:', manual_tokens_existing_samples)


if __name__ == '__main__':
    sum_costs_from_logfile(Path(sys.argv[1]),
                           Path(sys.argv[2]) if len(sys.argv) > 2 else None)
