import os

from spytex import run
print(os.path.abspath("."))

def file(*path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)


def task_returns(task, expected):
    def testfun():
        assert run(file(task)) == expected
    return testfun
