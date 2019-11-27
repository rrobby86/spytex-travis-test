"""Basic object definitions."""


from abc import ABC, abstractmethod
from pydoc import locate
import pickle
from typing import Any, Iterable, Sequence, Mapping, Type

from .context import ResolutionContext


class Definition(ABC):
    """Base class for definitions of Python objects to be created."""

    @abstractmethod
    def resolve(self, context: ResolutionContext):
        pass

    def __call__(self, context: ResolutionContext):
        return self.resolve(context)


class ConcreteValue(Definition):
    """Definition wrapping an actual Python object."""

    __slots__ = "obj"

    def __init__(self, obj: Any):
        self.obj = obj

    def resolve(self, context: ResolutionContext):
        return self.obj


class NameReference(Definition):
    """Reference by dotted path to a Python object."""

    __slots__ = "name"

    def __init__(self, name: str):
        self.name = name

    def resolve(self, context: ResolutionContext):
        return locate(self.name)


class Call(Definition):
    """Definition of object obtained by callable invocation."""

    __slots__ = "callee", "posargs", "kwargs"

    def __init__(self, callee: Definition, posargs: Iterable[Definition] = (),
                 kwargs: Mapping[str, Definition] = {}):
        self.callee = callee
        self.posargs = tuple(posargs)
        self.kwargs = dict(kwargs)

    def resolve(self, context: ResolutionContext):
        callee = self.callee.resolve(context)
        posargs = [arg.resolve(context) for arg in self.posargs]
        kwargs = {name: arg.resolve(context)
                  for name, arg in self.kwargs.items()}
        return callee(*posargs, **kwargs)


class SeqDef(Definition):
    """Definition of a sequence with values expressed as definitions."""

    __slots__ = "type", "items"

    def __init__(self, type: Type[Sequence], items: Iterable[Definition]):
        self.type = type
        self.items = tuple(items)

    def resolve(self, context: ResolutionContext):
        return self.type(item.resolve(context) for item in self.items)


class DictDef(Definition):
    """Definition of a dictionary with values expressed as definitions."""

    __slots__ = "items"

    def __init__(self, items: Mapping[Any, Definition]):
        self.items = items

    def resolve(self, context: ResolutionContext):
        return {key: val.resolve(context) for key, val in self.items.items()}


class ContextValue(Definition):
    """Reference to a context-bound value."""

    __slots__ = "name"

    def __init__(self, name: str):
        self.name = name

    def resolve(self, context: ResolutionContext):
        return context.vals[self.name]


class ContextBinder(Definition):
    """Wraps a definition with added context-bound values."""

    __slots__ = "values", "wrapped"

    def __init__(self, values: Mapping[str, Definition], wrapped: Definition):
        self.values = dict(values)
        self.wrapped = wrapped

    def resolve(self, context: ResolutionContext):
        resolved_vals = {key: val.resolve(context)
                         for key, val in self.values.items()}
        inner_context = context.update_vals(resolved_vals)
        return self.wrapped.resolve(inner_context)
