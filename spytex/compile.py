"""Functions to extract Definitions from JSON-like objects representation."""


from functools import singledispatch
import collections.abc
from typing import Any, Mapping

from .defs import (Definition, ConcreteValue, NameReference, Call, SeqDef,
                   DictDef, ContextValue, ContextBinder, RunTask, Unpickle)


_one_val_magics = {
    "run": RunTask,
    "unpickle": Unpickle,
}


def _single_key_or_empty(mapping: Mapping[str, Any]) -> str:
    return next(iter(mapping.keys())) if len(mapping) == 1 else ""

def _compile_dict_vals(mapping: Mapping[Any, Any]) -> Mapping[Any, Definition]:
    return {key: compile(val) for key, val in mapping.items()}


@singledispatch
def compile(obj: Any) -> Definition:
    """Extract a definition from a JSON-like object representation."""
    return ConcreteValue(obj)

@compile.register(list)
@compile.register(tuple)
def _(obj):
    return SeqDef(list, map(compile, obj))

@compile.register(collections.abc.Mapping)
def _(obj):
    if len(obj) == 1:
        key, val = next(iter(obj.items()))
        if key.startswith("!"):
            key = key[1:]
            if key in _one_val_magics:
                arg = compile(val)
                return _one_val_magics[key](arg)
            elif key:
                arg = compile(val)
                return Call(NameReference(key), [arg], {})
        elif key == "=":
            return ContextValue(val)
    elif "=" in obj:
        obj = obj.copy()
        values = _compile_dict_vals(obj.pop("="))
        wrapped = compile(obj)
        return ContextBinder(values, wrapped)
    elif "!" in obj:
        obj = obj.copy()
        callee = obj.pop("!")
        posargs = list(map(compile, obj.pop("*", [])))
        kwargs = _compile_dict_vals(obj)
        return Call(NameReference(callee), posargs, kwargs)
    else:
        return DictDef(_compile_dict_vals(obj))
