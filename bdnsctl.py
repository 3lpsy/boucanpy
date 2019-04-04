#!/usr/bin/env python
import asyncio
from sys import exit
from bountydns.core.utils import load_env

load_env("core")


async def call_command(command, args):
    result = await command.make(args).call()
    return result


if __name__ == "__main__":
    from bountydns.cli import make_parser, commands

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    parser = make_parser()
    args = parser.parse_args()
    for command in commands:
        if command.has_command(args.command):
            result = loop.run_until_complete(call_command(command, args))
            exit(result)
    parser.print_help()
    exit(1)
