import pickle
import sys
import traceback

from llm_emv.setup import setup_llm_emv
from lmp.repl.code_execution import ReplExecutionEnvironment


def _safe_run(lmp, command):
    try:
        lmp(command)
    except BaseException as e:
        if isinstance(e, KeyboardInterrupt):
            raise
        print('Error. Waiting for next command.')
        traceback.print_exc()
        lmp.code_execution_env.namespace.api.say('Sorry, an error occurred. Please try again.')
        lmp.reset()


def _load_history():
    from pathlib import Path
    history_cache = Path(__file__).parent.parent / 'data' / 'armarx_lt_mem' / f'2024-a7a-merged-summary.pkl'
    return pickle.loads(history_cache.read_bytes())


def main(config: str):
    import langchain.globals
    import langchain_community.callbacks
    from langchain_community.cache import SQLiteCache
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
    langchain.globals.set_verbose(True)

    def _exit_lmp_tts(text):
        print('Answer:', text)
        raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, None))

    lmp = setup_llm_emv(config, history=_load_history(), tts=_exit_lmp_tts)
    with langchain_community.callbacks.get_openai_callback() as cb:
        try:
            while True:
                print(f'Top-level waiting for trigger...')
                t = lmp.code_execution_env.namespace.api.wait_for_trigger()
                _safe_run(lmp, t)
        finally:
            print(cb)


if __name__ == '__main__':
    main(sys.argv[1])
