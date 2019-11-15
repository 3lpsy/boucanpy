#!/usr/bin/env python
import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from sys import exit


async def call_command(command, args):
    result = await command.make(args).call()
    return result


if __name__ == "__main__":
    from boucanpy.cli import commands
    from boucanpy.cli.parser import make_parser

    loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    parser = make_parser()
    args = parser.parse_args()
    for command in commands:
        if command.has_command(args.command):
            result = loop.run_until_complete(call_command(command, args))
            exit(result)
    parser.print_help()
    exit(1)
