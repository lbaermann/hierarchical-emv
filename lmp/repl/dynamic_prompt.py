import ast
import json
import re
import sys
from functools import cached_property
from pathlib import Path
from typing import Tuple, List

import torch
from sentence_transformers import util, SentenceTransformer

END_OF_TASK = 'wait_for_trigger()'
WAIT_FOR_USER_INPUT = re.compile(r"ask\(('[^']+'|\"[^\"]+\")\)|" + re.escape(END_OF_TASK))


class DynamicPromptBuilder:
    # This class is hardcoded on the wait_for_trigger() and ask(...) syntax in prompts
    # query can be either plain string (in response to "ask(...)")
    # or {'type': 'dialog', 'text': ...}
    # or {'type': 'action_recognition', 'activity': ..., 'person': ...}

    def __init__(self, base_prompt: str,
                 prompt_db: List[str],  # List of all exemplary interactions
                 loop_prevention_prompt: str,
                 suffix_prompt='',
                 prompt_separator='\n',
                 custom_prompt_db_file: str = None,
                 query_history_importance_decay=0.6,
                 top_k=2,
                 query_keep_last_n=3,
                 sentence_similarity_model='all-MiniLM-L6-v2',
                 device='cpu') -> None:
        super().__init__()
        self.base_prompt = base_prompt
        self.loop_prevention_prompt = loop_prevention_prompt
        self.prompt_suffix = suffix_prompt
        self.top_k = top_k
        self.query_keep_last_n = query_keep_last_n
        self.query_history_importance_decay = query_history_importance_decay
        self.prompt_separator = prompt_separator
        self.predefined_prompt_db = prompt_db
        self.custom_prompt_db_file = Path(custom_prompt_db_file) if custom_prompt_db_file else None
        print('No custom prompt db' if self.custom_prompt_db_file is None else self.custom_prompt_db_file.resolve())
        self.custom_prompt_db = (json.loads(self.custom_prompt_db_file.read_text())
                                 if custom_prompt_db_file and self.custom_prompt_db_file.exists() else [])
        self.sim_model = SentenceTransformer(sentence_similarity_model)
        if device:
            self.sim_model.to(device)

    @cached_property
    def prompt_db(self) -> List[Tuple[str, List[dict]]]:
        all_prompts: List[str] = self.predefined_prompt_db + self.custom_prompt_db
        response_lists: List[List[dict]] = []
        for p in all_prompts:
            response_lists.append(self._extract_responses_from_prompt(p))
        return list(zip(all_prompts, response_lists))

    @staticmethod
    def _extract_responses_from_prompt(p: str):
        result = []
        for match in WAIT_FOR_USER_INPUT.finditer(p):
            newline_idx = match.end()
            end_of_result_line = p.find('\n', newline_idx + 1)
            if end_of_result_line == -1:
                end_of_result_line = len(p)  # In case there is no trailing newline
            response = p[newline_idx + 1:end_of_result_line]
            if response.startswith('>>>') or response.startswith('...'):
                continue  # The "ask/wait_for_trigger" was part of a compound/control flow statement, ignore
            if not response.startswith('{'):
                if response.startswith("'") or response.startswith('"'):
                    response = response[1:-1]  # Avoid duplicate hyphens
                response = "{'type': 'dialog', 'text': '" + response + "'}"
            try:
                result.append(ast.literal_eval(response))
            except SyntaxError as e:
                # Try fixing simple hyphen error:
                match = re.fullmatch(r"\{\s*'type'\s*:\s*'dialog'\s*,\s*'text'\s*:\s*'(.*)'\s*}", response)
                if match:
                    fixed_response = "{'type': 'dialog', 'text': \"" + match.group(1).replace('"', r'\"') + "\"}"
                    try:
                        result.append(ast.literal_eval(fixed_response))
                        continue
                    except SyntaxError:
                        pass
                print('in _extract_responses_from_prompt: Response line not parsable:', str(e), '\n',
                      response, '\nin prompt:\n', p, file=sys.stderr)
                raise
        return result

    def _calc_prompt_embeddings_and_idx_map(self, queries: List[List[dict]]) -> Tuple[torch.Tensor, List[int]]:
        if len(queries) == 0:
            return torch.empty(0, self.sim_model.get_sentence_embedding_dimension(),
                               device=self.sim_model.device), []
        idx_map = []
        flattened = []
        for i, responses in enumerate(queries):
            for r in responses:
                idx_map.append(i)
                if r['type'] == 'dialog':
                    flattened.append(r['text'])
                elif r['type'] == 'action_recognition':
                    flattened.append(r['activity'])
                elif r['type'] == 'perform_search':
                    flattened.append(r['object'])
                elif r['type'] == 'task_end':
                    flattened.append(r['message'])
                elif r['type'] == 'action_end':
                    flattened.append(r['result'])
                elif r['type'] == 'task':
                    flattened.append(r['instruction'])
                elif r['type'] == 'query_to_human':
                    flattened.append(r['query'])
                else:
                    raise NotImplementedError(r)
        return self.sim_model.encode(flattened, convert_to_tensor=True), idx_map

    @cached_property
    def _prompt_embeddings_cache(self):
        return self._calc_prompt_embeddings_and_idx_map([q for p, q in self.prompt_db])

    def __call__(self, exec_history: str, loop_detected=False):
        """
        :param exec_history: the full exec history. user queries are extracted from that
        :return:
        """
        suffix = self.prompt_separator + self.prompt_suffix if self.prompt_suffix else ''

        if loop_detected:
            return self.base_prompt + self.prompt_separator + self.loop_prevention_prompt + suffix

        if len(self.prompt_db) == 0:
            return self.base_prompt + suffix

        query_history = self._extract_responses_from_prompt(exec_history)
        query_history = list(reversed(query_history))[:self.query_keep_last_n]
        # now, query history is from most recent (index 0) to oldest (index query_keep_last_n - 1)
        query_types = {q['type'] for q in query_history}
        query_hist_feats, _ = self._calc_prompt_embeddings_and_idx_map([query_history])
        decay = self.query_history_importance_decay * torch.ones(len(query_history), device=self.sim_model.device)
        decay **= torch.arange(len(query_history), device=decay.device)
        combined_query_feats = (query_hist_feats * decay[:, None]).sum(dim=0)

        prompt_embeddings, idx_map = self._prompt_embeddings_cache
        filter_by_type_indices = [i for i, d in enumerate(d for p, ds in self.prompt_db for d in ds)
                                  if d['type'] in query_types]
        prompt_embeddings = prompt_embeddings[filter_by_type_indices]
        idx_map = [idx for i, idx in enumerate(idx_map) if i in filter_by_type_indices]

        similarities = util.cos_sim(combined_query_feats, prompt_embeddings).squeeze()
        top_indices = similarities.argsort(descending=True)
        top_prompts = []  # To avoid duplicates
        for i in top_indices:
            if len(top_prompts) == self.top_k:
                break
            p = self.prompt_db[idx_map[i]][0]
            if p not in top_prompts:
                top_prompts.append(p)

        final_prompt = (
                self.base_prompt + self.prompt_separator +
                self.prompt_separator.join(reversed(top_prompts)) +
                suffix
        )
        return final_prompt

    def remember_interaction(self, interaction: str, **kwargs):
        try:
            self._extract_responses_from_prompt(interaction)
        except SyntaxError:
            print('Will not save interaction that is not syntactically valid!')
            print(interaction)
            return

        self.custom_prompt_db.append(interaction)
        if self.custom_prompt_db_file:
            print('Writing custom_prompt_db_file', self.custom_prompt_db_file)
            self.custom_prompt_db_file.write_text(json.dumps(self.custom_prompt_db))

        # invalidate caches
        # noinspection PyPropertyAccess
        del self.prompt_db
        # noinspection PyPropertyAccess
        del self._prompt_embeddings_cache
