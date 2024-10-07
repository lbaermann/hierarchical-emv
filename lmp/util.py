from pathlib import Path
from typing import List

import numpy as np
from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_core.messages import BaseMessage, BaseMessageChunk

NoneType = type(None)


def llm_predict(llm, text, **kwargs):
    response = llm.invoke(text, **kwargs)
    if isinstance(response, BaseMessage):
        return response.content
    elif isinstance(response, str):
        return response
    else:
        raise TypeError(response)


def llm_predict_stream(llm, text, **kwargs):
    generator = llm.stream(text, **kwargs)
    for chunk in generator:
        if isinstance(chunk, BaseMessageChunk):
            yield chunk.content
        elif isinstance(chunk, str):
            yield chunk
        else:
            raise TypeError(chunk)


def print_prompt(prompt):
    if isinstance(prompt, str):
        print_code(prompt)
    elif isinstance(prompt, List) and len(prompt) > 0 and isinstance(prompt[0], BaseMessage):
        for msg in prompt:
            print(f'\n**{type(msg).__name__}**:', f'"""{msg.content}"""', sep='\n')
    else:
        print(prompt)


def print_code(code, name=None, force_color=False):
    import sys

    to_print = None
    if sys.stdout.isatty() or force_color:
        try:
            from pygments import highlight
            from pygments.lexers import PythonLexer
            from pygments.formatters import TerminalFormatter
            to_print = highlight(code, PythonLexer(), TerminalFormatter())
        except ImportError:
            pass

    if to_print is None:
        to_print = code

    if name:
        print(f'{name}:\n\n{to_print}\n')
    else:
        print(f'\n\n{to_print}\n')


def load_chat_messages_from_txt(f: Path):
    messages = []
    lines = f.read_text().splitlines()
    current_msg_text = ''
    current_msg_type = None
    signal_words = {
        'Human: ': HumanMessagePromptTemplate,
        'AI: ': AIMessagePromptTemplate,
        'System: ': SystemMessagePromptTemplate
    }

    def flush():
        if current_msg_type is not None:
            messages.append(current_msg_type(prompt=PromptTemplate(
                input_variables=[], validate_template=False, template_format='jinja2',
                template=current_msg_text)))

    for line in lines:
        found_kw = None
        for keyword, t in signal_words.items():
            if line.startswith(keyword):
                flush()
                current_msg_type = t
                found_kw = keyword
        if found_kw:
            current_msg_text = line[len(found_kw):]
        else:
            current_msg_text += '\n' + line
    flush()
    return messages


def cleanup_model_output(model_out: str):
    code_start = model_out.find('```')
    if code_start == -1:
        return model_out
    code_end = model_out.find('```', code_start + 3)
    code_end = None if code_end == -1 else code_end  # -1 would trim the last char. None means no slicing
    sub = model_out[code_start + 3:code_end]
    if sub.startswith('python'):
        sub = sub[len('python'):]
    return sub.strip()


def safe_equals(x, y):
    t1 = type(x)
    t2 = type(y)
    if t1 != t2:
        return False
    if t1 in [int, float, str, bool, NoneType]:
        return x == y
    elif t1 in [list, tuple, set]:
        return (len(x) == len(y)
                and all(safe_equals(a, b) for a, b in zip(x, y)))
    elif t1 == dict:
        return len(x) == len(y) and all(k in y and safe_equals(x[k], y[k]) for k in x.keys())
    elif t1 == np.ndarray:
        return (x.shape == y.shape
                and np.equal(x, y).all())
    else:
        raise TypeError(x)
