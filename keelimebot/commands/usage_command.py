import logging

from twitchio.ext import commands
from twitchio import Context
from typing import *
from abc import ABC

logger = logging.getLogger(__name__)


class UsageFormattingError(Exception):
    pass


def parse_usage(usage: str) -> dict:
    """Convert the given usage string into a
       dictionary of optional and required args.

    :raises: UsageFormattingError
    """
    args = {}
    if usage:
        # raise UsageFormattingError(f"Usage parsing not yet implemented: {usage}")
        pass

    return args


class UsageCommand(commands.Command, ABC):
    """A command that encodes how it is meant to be used.
    """

    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._checks.append(self.command_usage_check)
        self._usage = attrs.get('usage', None)

        self._usage_dict = parse_usage(self._usage)

    def command_usage_check(self, ctx: Context) -> bool:
        """A command check that verifies that usage requirements are met
        """
        if not self.usage:
            return True

        # TODO
        return True

    @property
    def usage(self) -> str:
        return self._usage
