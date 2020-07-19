import inspect
import logging

from typing import *

from keelimebot.permissions import Permissions
from .permissions_command import PermissionsCommand
from .usage_command import UsageCommand

logger = logging.getLogger(__name__)


def command(*, name: str = None, aliases: Union[list, tuple] = None, cls=None, no_global_checks=False, **kwargs):
    """Decorator that turns a coroutine into a Command.
    """

    if cls and not inspect.isclass(cls):
        raise TypeError(f'cls must be of type <class> not <{type(cls)}>')

    cls = cls or Command

    def decorator(func):
        fname = name or func.__name__
        command = cls(name=fname, func=func, aliases=aliases, no_global_checks=no_global_checks, **kwargs)

        return command
    return decorator


class DefaultCommand(PermissionsCommand, UsageCommand):
    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

        self._func = func

    @property
    def required_permissions(self):
        return Permissions.NONE

    def serialize(self) -> dict:
        return {
            'cls': self.__class__,
            'name': self.name,
            'aliases': self.aliases,
            'func': self._func,
            'no_global_checks': self.no_global_checks,
        }


class StreamerCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.STREAMER


class ModCommand(DefaultCommand):
    def __init__(self, name: str, func, **attrs):
        super().__init__(name, func, **attrs)

    @property
    def required_permissions(self):
        return Permissions.MODERATOR


class SubscriberCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.SUBSCRIBER


class VipCommand(DefaultCommand):
    @property
    def required_permissions(self):
        return Permissions.VIP
