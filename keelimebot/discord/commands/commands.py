import inspect
import logging

from discord.ext import commands
from discord.ext.commands import Context

logger = logging.getLogger(__name__)


def command(*, name: str = None, cls=None, **attrs):
    """Decorator that turns a coroutine into a Command.
    """

    if cls and not inspect.isclass(cls):
        raise TypeError(f'cls must be of type <class> not <{type(cls)}>')

    cls = cls or DefaultCommand

    def decorator(func):
        fname = name or func.__name__
        command = cls(name=fname, func=func, **attrs)

        return command
    return decorator


class DefaultCommand(commands.Command):
    def __init__(self, name: str, func=None, text: str = None, **attrs):
        if func is None:
            assert (text is not None)
            self._func = self.cmd_textcommand
        else:
            self._func = func

        super().__init__(self._func, name=name, **attrs)

        self.text = text
        if self.text is not None:
            assert (func is None)

    async def cmd_textcommand(self, ctx: Context):
        await ctx.send(self.text)

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
        }
