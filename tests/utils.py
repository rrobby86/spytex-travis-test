import os

import pytest

from spytex import run


def file(*path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)


def task_returns(task, expected):
    def testfun():
        assert run(file(task)) == expected
    return testfun


def task_raises(task, exception_type):
    def testfun():
        with pytest.raises(exception_type):
            run(file(task))
