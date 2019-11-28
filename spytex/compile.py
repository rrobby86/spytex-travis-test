"""Functions to extract Definitions from JSON-like objects representation."""


from functools import singledispatch
import collections.abc
from typing import Any, Mapping

from .defs import (Definition, ConcreteValue, NameReference, Call, SeqDef,
                   DictDef, ContextValue, ContextBinder, Unpickle)


def _single_key_or_empty(mapping: Mapping[str, Any]) -> str:
    return next(iter(mapping.keys())) if len(mapping) == 1 else ""

def _compile_dict_vals(mapping: Mapping[Any, Any]) -> Mapping[Any, Definition]:
    return {key: compile(val) for key, val in mapping.items()}


@singledispatch
def compile(obj: Any) -> Definition:
    """Extract a definition from a JSON-like object representation."""
    return ConcreteValue(obj)

@compile.register(collections.abc.Sequence)
def _(obj):
    return SeqDef(list, map(compile, obj))

@compile.register(collections.abc.Mapping)
def _(obj):
    if _single_key_or_empty(obj) == "=":
        return ContextValue(next(iter(obj.values())))
    elif _single_key_or_empty(obj) == "@unpickle":
        return Unpickle(next(iter(obj.values())))
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
    elif _single_key_or_empty(obj).startswith("!"):
        key, val = next(iter(obj.items()))
        arg = compile(val)
        return Call(NameReference(key[1:]), [arg], {})
    else:
        return DictDef(_compile_dict_vals(obj))
