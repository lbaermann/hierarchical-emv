from datetime import datetime
from pathlib import Path

from em.em_tree import HigherLevelSummary
from lmp.api_visibility_wrapper import ApiVisibilityWrapper
from lmp.namespace import DynamicNamespaceDict
from lmp.repl.code_execution import ReplExecutionEnvironment
from lmp.setup import setup_lmp, load_config
from .emv_dialog_api import EmvDialogAPI
from ...setup import setup_llm_emv


def setup_interactive_emv_lmp(history: HigherLevelSummary,
                              now_time: datetime,
                              interactive_cfg='teach/paper',
                              wait_for_trigger_callback=lambda: {'type': 'dialog', 'text': input('User:')},
                              tts=lambda s: print('System:', s),
                              language_rule_manager=None,
                              ):
    full_cfg_path = Path(__file__).parent.parent.parent / 'config' / 'interactive' / f'{interactive_cfg}.yaml'
    cfg = load_config(full_cfg_path)

    def _exit_lmp_on_wait_for_trigger():
        raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, None))

    def _exit_lmp_and_report_output(s: str):
        raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, s))

    emv_cfg_name = cfg.pop('emv_cfg_name')
    only_emv_mode = cfg.pop('only_emv_no_dialog', False)
    emv_model = setup_llm_emv(emv_cfg_name, history, now_time,
                              wait_for_trigger_callback=_exit_lmp_on_wait_for_trigger,
                              tts=_exit_lmp_and_report_output,
                              return_answer_with_reasoning=cfg.pop('return_answer_with_reasoning',
                                                                   not only_emv_mode))
    if only_emv_mode:
        return emv_model
    else:
        api = EmvDialogAPI(wait_for_trigger=wait_for_trigger_callback, tts=tts,
                           emv_model=emv_model, language_rule_manager=language_rule_manager)
        api = ApiVisibilityWrapper(api, **cfg.pop('api'))
        namespace = DynamicNamespaceDict(api)
        return setup_lmp(cfg, namespace)
