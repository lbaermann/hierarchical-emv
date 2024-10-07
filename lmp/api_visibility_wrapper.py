from typing import Any, Iterable


def group(group_name: str):
    """
    Use this as a decorator on a function of an API object to mark it as part of a specific group.

    E.g.
    @group('low_level')
    def grab(self, object: str) -> str:
        ...
    """

    def _apply(f):
        f.__api_group__ = group_name
        return f

    return _apply


class ApiVisibilityWrapper:

    def __init__(self,
                 api,
                 include_all=False,
                 include_groups=(),
                 include_names=()
                 ) -> None:
        super().__init__()
        self._api = api
        if include_all:
            self._names_to_export = dir(api)
        else:
            self._names_to_export = list(include_names)
            for name in dir(api):
                f = getattr(api, name)
                if hasattr(f, '__api_group__') and f.__api_group__ in include_groups:
                    self._names_to_export.append(name)

    def __dir__(self) -> Iterable[str]:
        return self._names_to_export

    def __getattribute__(self, __name: str) -> Any:
        if __name.startswith('_'):
            return super().__getattribute__(__name)
        if __name in self._names_to_export:
            return getattr(self._api, __name)
        return super().__getattribute__(__name)
