import sys
from copy import copy
from pathlib import Path
from threading import current_thread

from em.em_tree import HigherLevelSummary, AnyTreeNode


# https://stackoverflow.com/a/57996986
class SysRedirectPerThread(object):
    def __init__(self, file):
        self.terminal = file
        self.log_per_thread = {}

    def _thread_dependent_perform(self, fn, force_console=False):
        ident = current_thread().ident
        if ident in self.log_per_thread and not force_console:
            fn(self.log_per_thread[ident])
        else:
            fn(self.terminal)

    def set_log_for_current_thread(self, log: Path):
        thread = current_thread()
        ident = thread.ident
        # print(f'Redirecting thread {thread.name} ({ident}) to', log, file=self.terminal)
        if ident in self.log_per_thread:
            self.log_per_thread[ident].close()
        self.log_per_thread[ident] = log.open("w") if log else self.terminal

    def isatty(self):
        return current_thread().ident not in self.log_per_thread

    def write(self, message, force_console=False):
        self._thread_dependent_perform(lambda s: s.write(message), force_console)

    def flush(self):
        self._thread_dependent_perform(lambda s: s.flush())

    def close(self):
        for s in self.log_per_thread.values():
            s.close()

    def close_log_for_current_thread(self):
        ident = current_thread().ident
        if ident in self.log_per_thread:
            self.log_per_thread[ident].flush()
            self.log_per_thread[ident].close()
            del self.log_per_thread[ident]

    @staticmethod
    def initialize():
        sys.stdout = SysRedirectPerThread(sys.stdout)
        sys.stderr = SysRedirectPerThread(sys.stderr)


def simplify_summary_node(node: AnyTreeNode):
    if not isinstance(node, HigherLevelSummary):
        return node

    shallow_copy = copy(node)
    children = node.children
    while len(children) == 1 and isinstance(children[0], HigherLevelSummary):
        children = children[0].children
    shallow_copy.children = [
        simplify_summary_node(c)
        for c in children
    ]
    return shallow_copy
