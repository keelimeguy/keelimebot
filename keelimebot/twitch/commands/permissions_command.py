import logging

from twitchio.ext import commands
from twitchio.ext.commands import Context
from abc import ABC, abstractmethod

from keelimebot.twitch.permissions import Permissions, check_permissions

logger = logging.getLogger(__name__)


class PermissionsCommand(commands.Command, ABC):
    """A restricted command based on permissions.
    """

    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._checks.append(self.command_permissions_check)

    def command_permissions_check(self, ctx: Context) -> bool:
        """A command check that verifies that the appropriate permissions are met
        """
        return check_permissions(ctx.message, self.required_permissions, self.name)

    @property
    @abstractmethod
    def required_permissions(self) -> Permissions:
        """Returns the required permissions for the command
        """
        pass
