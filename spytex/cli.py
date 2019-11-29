import pickle
from argparse import ArgumentParser
import sys

from smart_open import open

from .api import run


def main():
    parser = ArgumentParser()
    parser.add_argument("task_file", nargs="?",
                        help="task specification file")
    parser.add_argument("-p", "--pickle", metavar="FILE",
                        help="pickle returned object to specified file")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress output of returned value")
    parser.add_argument("--version", action="store_true",
                        help="print version information and exit")
    args = parser.parse_args()
    if args.version:
        from . import __version__
        print("SPyTEx {}".format(__version__))
        return
    result = run(args.task_file or sys.stdin)
    if result is not None and not args.quiet:
        print(result)
    if args.pickle:
        with open(args.pickle, "wb") as f:
            pickle.dump(result, f)
