import importlib
from pathlib import Path
from typing import Dict

import yaml
from langchain.chat_models.base import BaseChatModel
from langchain.schema.language_model import BaseLanguageModel

import lmp.repl.error_handlers
from .code_execution import CodeExecutionEnvironment
from .function_gen_lmp import FunctionGenerationLMP
from .lmp import LMP, LMPBase
from .namespace import DynamicNamespaceDict
from .repl.code_execution import ReplExecutionEnvironment
from .repl.dynamic_prompt import DynamicPromptBuilder
from .repl.learn_from_interaction import ChatLearnFromInteractionModule
from .repl.repl_lmp import ReplLMP


def _merge_dicts(prio: dict, new: dict):
    for k, v in new.items():
        if k not in prio:
            prio[k] = v
        elif isinstance(prio[k], dict) and isinstance(new[k], dict):
            _merge_dicts(prio[k], new[k])


def load_config(cfg_file: Path, prompt_cfg_file_keys=((None, ('base', 'loop_prevention', 'suffix')),)) -> Dict:
    loaded_cfgs = {}
    prompt_cfg_file_keys = {k: v for k, v in prompt_cfg_file_keys}

    def _load_yaml_to_dict(f: Path) -> dict:
        cfg: dict = yaml.safe_load(f.read_text())
        include_cfgs = cfg.pop('+include', [])
        if isinstance(include_cfgs, str):
            include_cfgs = [include_cfgs]
        for incl_cfg in include_cfgs:
            sub_cfg = _load_yaml_to_dict((f.parent / f'{incl_cfg}.yaml').resolve())
            _merge_dicts(cfg, sub_cfg)  # Includes have lower priority
        return cfg

    def _load(f: Path):
        cfg = _load_yaml_to_dict(f)
        prompt_cfg_keys_for_type = prompt_cfg_file_keys.get(cfg.get('type', None), prompt_cfg_file_keys[None])
        _load_prompts(cfg, f, prompt_cfg_keys_for_type)
        loaded_cfgs[str(f.resolve())] = cfg
        imported_cfgs = {}
        for sub_name, sub_f in cfg.pop('import_lmps', {}).items():
            sub_f = (f.parent / f'{sub_f}.yaml').resolve()
            cache_key = str(sub_f.resolve())
            if cache_key in loaded_cfgs:
                sub_cfg = loaded_cfgs[cache_key]
            else:
                sub_cfg = _load(sub_f)
            imported_cfgs[sub_name] = sub_cfg
        cfg['import_lmps'] = imported_cfgs
        return cfg

    return _load(cfg_file)


def _load_prompts(cfg, base_f, prompt_cfg_file_keys):
    def _resolve_rel_path(name, extension=''):
        return (base_f.parent / f'{name}{extension}').resolve()

    def _load_prompt_file(name):
        prompt_file = _resolve_rel_path(name, '.prompt.py')
        if not prompt_file.is_file():
            prompt_file = _resolve_rel_path(name, '.prompt.txt')
        return prompt_file.read_text().strip()

    if 'prompt_cfg' in cfg:
        prompt_cfg = cfg['prompt_cfg']
        if prompt_cfg is None:
            return  # Indicates that this is a config that needs no prompts
        prompts = []
        new_prompt_cfg = {}
        for key in prompt_cfg_file_keys:
            if key in prompt_cfg:
                new_prompt_cfg[f'{key}_prompt'] = _load_prompt_file(prompt_cfg.pop(key))

        if 'db' in prompt_cfg:
            new_prompt_cfg['prompt_db'] = prompts
        if 'custom_prompt_db_file' in prompt_cfg:
            new_prompt_cfg['custom_prompt_db_file'] = _resolve_rel_path(prompt_cfg.pop('custom_prompt_db_file'))
        for include_path in prompt_cfg.pop('db', []):
            if '*' in include_path:
                for prompt_f in base_f.parent.glob(f'{include_path}.prompt.py'):
                    prompts.append(prompt_f.resolve().read_text().strip())
            else:
                prompts.append(_load_prompt_file(include_path))
        new_prompt_cfg.update(prompt_cfg)
        cfg['prompt_cfg'] = new_prompt_cfg
    else:
        cfg['prompt_text'] = _load_prompt_file(base_f.stem)

    if 'learn_from_interaction_cfg' in cfg:
        cfg['learn_from_interaction_cfg']['few_shot_file'] = _resolve_rel_path(
            cfg['learn_from_interaction_cfg']['few_shot_file'])


def setup_lmp(cfg: Dict, namespace: DynamicNamespaceDict) -> LMPBase:
    cfg = dict(cfg)  # Copy to keep "pop"s locally, since loaded dict might be shared on multi-way imports
    lmp_type = cfg.pop('type', 'lmp')
    llm = instantiate_llm(cfg.pop('llm', {}))

    imports = cfg.pop('import_lmps', {})
    imported_lmps = {
        name: setup_lmp(sub_cfg, namespace)
        for name, sub_cfg in imports.items()
    }

    namespace.permanent_definitions.update({
        k: imported_lmps[k]
        for k in imported_lmps.keys() - {'fgen'}
    })
    if lmp_type == 'repl':
        exec_env = ReplExecutionEnvironment(namespace)

        if 'result_function' in cfg:
            exec_env.set_result_function_name(cfg.pop('result_function'))

        prompt_builder = DynamicPromptBuilder(**cfg.pop('prompt_cfg'))
        if 'learn_from_interaction_cfg' in cfg:
            learn_from_interaction = _instantiate_learn_from_interaction(cfg.pop('learn_from_interaction_cfg'))
        else:
            learn_from_interaction = None
        error_handlers = instantiate_error_handlers(cfg)
        if 'fgen' in imported_lmps:
            cfg['fgen_lmp'] = imported_lmps['fgen']

        return ReplLMP(
            llm,
            exec_env,
            prompt_builder,
            error_handlers,
            learn_from_interaction,
            **cfg
        )
    else:
        exec_env = CodeExecutionEnvironment(namespace)
        if lmp_type == 'fgen':
            return FunctionGenerationLMP(cfg, llm, exec_env)
        else:
            return LMP(cfg, imported_lmps['fgen'], llm, exec_env)


def instantiate_error_handlers(cfg):
    error_handlers = [
        _instantiate_from_cfg(handler_cfg, lmp.repl.error_handlers)
        for handler_cfg in cfg.pop('error_handlers', lmp.repl.error_handlers.default_error_handler_config())
    ]
    return error_handlers


def _instantiate_learn_from_interaction(learn_cfg: Dict):
    llm = instantiate_llm(learn_cfg.get('llm', {}))
    assert isinstance(llm, BaseChatModel), 'ChatLearnFromInteractionModule only supports Chat LLM'
    return ChatLearnFromInteractionModule(
        llm,
        Path(learn_cfg['few_shot_file']))


def instantiate_llm(llm_cfg: Dict) -> BaseLanguageModel:
    llm_cfg.setdefault('type', 'ChatOpenAI')
    if 'OpenAI' in llm_cfg['type']:
        import openai
        if 'openai_api_key' not in llm_cfg:
            llm_cfg['openai_api_key'] = openai.api_key
        llm_cfg.setdefault('request_timeout', 15)
    if 'llm' in llm_cfg:  # This seems to be a wrapper
        llm_cfg['llm'] = instantiate_llm(llm_cfg['llm'])

    pkgs = [
        'langchain_openai',
        'langchain_google_genai',
        'langchain_community.chat_models',
        'langchain_community.llms',
        'langchain_huggingface.chat_models',
        'langchain_huggingface.llms',
        'langchain_experimental.chat_models',
        'langchain_experimental.llms',
    ]
    available_pkgs = []
    for module_name in pkgs:
        try:
            module = importlib.import_module(module_name)
            available_pkgs.append(module)
        except ImportError:
            pass
    return _instantiate_from_cfg(llm_cfg, *available_pkgs)


def _instantiate_from_cfg(cfg: Dict, *base_pkgs):
    t = cfg.pop('type')
    cls = None
    for pkg in base_pkgs:
        if hasattr(pkg, t):
            cls = getattr(pkg, t)
            break
    if cls is None:
        raise ValueError(f'Type {t} not found in {base_pkgs}')
    return cls(**cfg)
