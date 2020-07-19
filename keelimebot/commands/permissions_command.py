import logging

from twitchio.ext import commands
from twitchio import Context
from typing import *
from abc import ABC, abstractmethod

from keelimebot.permissions import check_permissions

logger = logging.getLogger(__name__)


class PermissionsCommand(commands.Command, ABC):
    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._checks.append(self.command_permissions_check)
        self._func = func

    def serialize(self):
        return {
            'cls': self.__class__,
            'name': self.name,
            'aliases': self.aliases,
            'func': self._func,
            'no_global_checks': self.no_global_checks,
        }

    def command_permissions_check(self, ctx: Context) -> bool:
        """A command check that verifies that the appropriate permissions are met
        """
        return check_permissions(ctx.message, self.required_permissions, self.name)

    @property
    @abstractmethod
    def required_permissions(self):
        """Returns the required permissions for the command
        """
        pass
