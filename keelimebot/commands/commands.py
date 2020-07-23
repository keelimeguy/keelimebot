import inspect
import logging

from twitchio import Context
from typing import Union

from keelimebot.permissions import Permissions
from .permissions_command import PermissionsCommand
from .usage_command import UsageCommand

logger = logging.getLogger(__name__)


def command(*, name: str = None, aliases: Union[list, tuple] = None, cls=None, no_global_checks=False, **kwargs):
    """Decorator that turns a coroutine into a Command.
    """

    if cls and not inspect.isclass(cls):
        raise TypeError(f'cls must be of type <class> not <{type(cls)}>')

    cls = cls or DefaultCommand

    def decorator(func):
        fname = name or func.__name__
        command = cls(name=fname, func=func, aliases=aliases, no_global_checks=no_global_checks, **kwargs)

        return command
    return decorator


class DefaultCommand(PermissionsCommand, UsageCommand):
    def __init__(self, name: str, func=None, text: str = None, **attrs):
        if func is None:
            assert(text is not None)
            self._func = self.cmd_textcommand
        else:
            self._func = func

        super().__init__(name, self._func, **attrs)

        self.text = text
        if self.text is not None:
            assert(func is None)

    async def cmd_textcommand(self, ctx: Context):
        await ctx.send(self.text)

    @property
    def required_permissions(self):
        return Permissions.NONE

    def serialize(self) -> dict:

        if self.text is None:
            func = self._func
        else:
            func = None

        return {
            'cls': self.__class__,
            'name': self.name,
            'aliases': self.aliases,
            'func': func,
            'text': self.text,
            'no_global_checks': self.no_global_checks,
            'usage': self._usage,
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
