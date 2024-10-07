from datetime import datetime
from functools import partial
from typing import Dict, Callable, Literal, List

import torch
from PIL.Image import Image
from langchain_core.messages import HumanMessage
from sentence_transformers import util

from em.em_tree import HigherLevelSummary, type_to_children_property_map, HighestPredefinedSummaryLevel, AnyTreeNode
from lmp.api_visibility_wrapper import group
from lmp.namespace import comment
from lmp.repl.semantic_hint_errror import SemanticHintError
from .interactive_tree import ExpandableTreeNode, ExpandableList, create_expandable_tree_node_filter_fn
from .vlm import VLM


class EMVerbalizationAPI:

    def __init__(
            self,
            wait_for_trigger: Callable[[], Dict[str, str]],
            tts: Callable[[str], None],
            history: HigherLevelSummary,
            now_time: datetime = None,
            hierarchy_level: Literal['none', 'predefined', 'predefined+', 'deep'] = 'deep',
            vlm: VLM = None,
            search_embedding_fn: Callable[[List[str]], torch.Tensor] = None,
            search_filter_kwargs=None
    ) -> None:
        super().__init__()
        self._vlm = vlm
        self._wait_for_trigger = wait_for_trigger
        self._tts = tts
        self._now_time = now_time
        if hierarchy_level == 'deep':
            self._history: ExpandableTreeNode = make_tree_interactive(history, search_embedding_fn,
                                                                      search_filter_kwargs)
        elif hierarchy_level.startswith('predefined'):
            # noinspection PyTypeChecker
            nodes = [make_tree_interactive(x, search_embedding_fn, search_filter_kwargs)
                     for x in (find_all_predefined_summary_nodes
                               if hierarchy_level == 'predefined'
                               else find_all_parents_of_predefined_summary_nodes)(history)]
            # noinspection PyProtectedMember
            self._history = ExpandableList(
                nodes,
                filter_fn_generator=create_expandable_tree_node_filter_fn,
                search_filter_fn=nodes[0]._search_filter_fn if len(nodes) > 0 else None,
            )
        else:
            self._history = make_tree_interactive(history, search_embedding_fn, search_filter_kwargs).all_leaves

        try:
            print('Initializing search embeddings eagerly...')
            self._history.search('')
        except SemanticHintError:
            pass
        finally:
            self._history.collapse_deep()

    #########################
    # dialog

    @comment('always call this to wait for next command or end the interaction')
    @group('dialog')
    def wait_for_trigger(self) -> Dict[str, str]:
        return self._wait_for_trigger()

    @group('dialog')
    def ask(self, question: str):
        self.say(question)
        while True:
            trigger = self.wait_for_trigger()
            if trigger['type'] == 'dialog':
                return trigger['text']

    @group('dialog')
    def say(self, text: str):
        return self._tts(text)

    @group('dialog')
    def answer(self, reasoning: str = None, answer: str = ...):
        if answer is Ellipsis:
            if reasoning is None:
                raise SemanticHintError('answer(answer="...") is missing its required argument "answer".')
            else:
                # Call was positional-only: answer("..."), using only argument as answer
                answer = reasoning
                reasoning = None
        print('Answering', answer, ' with reason:', reasoning)
        return self._tts(answer)

    #########################
    # Utils

    @group('util')
    def now(self) -> datetime:
        return self._now_time or datetime.now()

    #########################
    # EM Access

    @property
    @comment('Returns the history tree in its current state')
    @group('em')
    def history(self):
        return self._history

    #########################
    # External tools
    @group('tools')
    def vqa(self, question: str, *images: Image):
        for image in images:
            if image is None:
                raise SemanticHintError('Image passed to vqa(...) is None. Use an image from a different node.')
        msg_content = self._vlm.prepare_multimodal_message_content(question, *images)
        msg = HumanMessage(content=msg_content)
        response = self._vlm.model.invoke([msg])
        return response.content


def make_tree_interactive(history: HigherLevelSummary,
                          embedding_fn: Callable[[List[str]], torch.Tensor] = None,
                          search_filter_kwargs=None):
    return ExpandableTreeNode(
        history,
        children_extractor=lambda c:
        getattr(c, type_to_children_property_map[type(c)])
        if type(c) in type_to_children_property_map else None,
        search_similarity_fn=partial(history_search_similarity, embedding_fn),
        search_filter_kwargs=search_filter_kwargs
    )


def find_all_predefined_summary_nodes(history: HigherLevelSummary):
    result = []
    for node in history.children:
        if isinstance(node, HighestPredefinedSummaryLevel):
            result.append(node)
        else:
            result.extend(find_all_predefined_summary_nodes(node))
    return result


def find_all_parents_of_predefined_summary_nodes(history: HigherLevelSummary):
    result = []
    for node in history.children:
        if isinstance(node, HighestPredefinedSummaryLevel):
            return [history]
        else:
            result.extend(find_all_parents_of_predefined_summary_nodes(node))
    return result


def history_search_similarity(embedding_fn: Callable[[List[str]], torch.Tensor],  # returns 1xH tensor
                              query: str, node: AnyTreeNode):
    if embedding_fn is None:
        return 0.0

    if hasattr(node, '_embedding_cache'):
        embedding = getattr(node, '_embedding_cache')
    else:
        embedding = embedding_fn([s for s in node.index_content if s])
        setattr(node, '_embedding_cache', embedding)

    query_emb = embedding_fn([query])
    similarity = util.cos_sim(embedding, query_emb).max().item()
    return similarity
