import json
from argparse import ArgumentParser
import sys

from .compile import compile
from .context import ResolutionContext


def main():
    parser = ArgumentParser()
    parser.add_argument("task_file", nargs="?",
                        help="task specification file")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress output of returned value")
    parser.add_argument("--version", action="store_true",
                        help="print version information and exit")
    args = parser.parse_args()
    if args.version:
        from . import __version__
        print("SPyTEx {}".format(__version__))
        return
    with open(args.task_file, "r") if args.task_file else sys.stdin as f:
        raw_task = json.load(f)
    task_def = compile(raw_task)
    context = ResolutionContext()
    result = task_def.resolve(context)
    if result is not None and not args.quiet:
        print(result)
