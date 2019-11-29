"""High-level functions."""


import json
from typing import Union, TextIO

from smart_open import open

from .compile import compile
from .context import ResolutionContext


_empty_context = ResolutionContext()


def run(file: Union[str, TextIO], context: ResolutionContext = _empty_context):
    """Run a named task specification file and return the resulting object."""
    if isinstance(file, str):
        with open(file, "r") as f:
            raw_task = json.load(f)
    else:
        raw_task = json.load(file)
    task_def = compile(raw_task)
    return task_def.resolve(context)
