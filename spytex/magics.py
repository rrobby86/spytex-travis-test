"""Magic functions available in task specifications."""


import pickle

from smart_open import open


def get_magic(name):
    """Get a magic function by name or None if not exists."""
    return globals().get("do_" + name)


def accepts_context(fun):
    fun._pass_context = True
    return fun


@accepts_context
def do_run(filename, context):
    """Runs the task specified in the given file."""
    from .api import run   # here to avoid circular import
    return run(filename, context)


def do_unpickle(filename):
    """Unpickles an object from a given file."""
    with open(filename, "rb") as f:
        return pickle.load(f)
