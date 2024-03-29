import logging
import shlex
import re

from twitchio.ext import commands
from twitchio.ext.commands import Context
from abc import ABC

logger = logging.getLogger(__name__)

USAGE_REQ = r'<\w+?>'
USAGE_OPT = r'\[\w+?\]'
usage_pattern = re.compile(f"^(({USAGE_REQ})( {USAGE_REQ})*?( {USAGE_OPT})*?)|(({USAGE_OPT})( {USAGE_OPT})*?)")


class CommandFormattingError(Exception):
    pass


class UsageFormattingError(Exception):
    pass


def parse_usage(usage: str) -> dict:
    """Convert the given usage string into a
       dictionary of optional and required args.

    :raises: UsageFormattingError
    """
    args = {}
    if usage:
        match = usage_pattern.fullmatch(usage)
        if not match:
            raise UsageFormattingError(f"Unsupported usage format: {usage}")

        req_match = re.findall(USAGE_REQ, usage)
        opt_match = re.findall(USAGE_OPT, usage)

        args['num_required'] = len(req_match)
        args['names'] = []

        for arg in req_match:
            args['names'].append(arg[1:-1])

        for arg in opt_match:
            args['names'].append(arg[1:-1])

        if len(args['names']) != len(set(args['names'])):
            raise UsageFormattingError(f"Args must have unique names: {usage}")

    return args


class UsageCommand(commands.Command, ABC):
    """A command that encodes how it is meant to be used.
    """

    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._checks.append(self.command_usage_check)
        self._usage = attrs.get('usage', None)

        self._usage_dict = parse_usage(self._usage)

    async def command_usage_check(self, ctx: Context) -> bool:
        """A command check that verifies that usage requirements are met
        """
        if not self._usage:
            return True

        async def failure():
            index = -1

            names = [self.name]
            if self.aliases:
                names += self.aliases

            for name in names:
                index = ctx.content.find(name)
                if index != -1:
                    break

            prefix = ctx.content[:index] if index != -1 else '!'
            await ctx.send(f"usage: {prefix}{self.name} {self.usage}")
            raise CommandFormattingError(f"wrong number of arguments: {ctx.content}")

        try:
            args = shlex.split(ctx.content)[1:]
        except ValueError:
            await failure()

        if len(args) < self._usage_dict['num_required'] or len(args) > len(self._usage_dict['names']):
            await failure()

        return True

    @property
    def usage(self) -> str:
        return self._usage
