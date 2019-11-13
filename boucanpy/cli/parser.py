import argparse
from boucanpy.cli import commands


def make_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(help="command", dest="command")
    for command in commands:
        command.apply_parser(sub_parser)
    return parser
