import itertools
import datetime
import inspect
import logging

from twitchio.ext import commands as basecommands
from twitchio import Context, Message
from typing import *

from .commands import commands
from .globalnames import BOTNAME
from .permissions import Permissions, PermissionsError, get_author_permissions
from .serializer import json_deserialize_from_file, json_serialize_to_string

logger = logging.getLogger(__name__)


class Keelimebot(basecommands.Bot):
    def __init__(self, irc_token: str, client_id: str, channel_data_dir: str = '.'):
        self.channel_data_dir = channel_data_dir
        self.lock_json = True

        super().__init__(
            irc_token=irc_token,
            client_id=client_id,
            nick=BOTNAME,
            prefix='!',
            initial_channels=['keelimebot']
        )

        self.add_commands_from_json_file(f"{self.channel_data_dir}/commands.json")
        self.lock_json = False
        self.dump_commands_to_json_file()

    async def event_ready(self):
        """Called once when the bot goes online.
        """

        logger.info(f'Ready | {self.nick}')
        for channel in self.initial_channels:
            await self._ws.send_privmsg(channel, f"/me has landed!")

    async def event_message(self, message: Message):
        """Called once when a message is posted in chat.
        """

        author_permissions = get_author_permissions(message)

        timestamp = int(datetime.datetime.now().timestamp()*1000)
        if message.tags:
            if abs(message.tags['tmi-sent-ts'] - timestamp) >= 10000:
                logger.warning(f"timestamp is off by more than 10s: tags={message.tags['tmi-sent-ts']}ms, now={timestamp}ms")
            timestamp = message.tags['tmi-sent-ts']
        else:
            timestamp = str(timestamp)[:-4]+'XXXX'

        if author_permissions == Permissions.NONE:
            logger.info(f"{timestamp} [#{message.channel}] {message.author.name}: {message.content}")
        else:
            logger.info(f"{timestamp} [#{message.channel}] {message.author.name}({author_permissions.name}): {message.content}")

        await self.handle_commands(message)

    async def event_command_error(self, ctx: Context, error: Exception):
        """Called once when an error occurs during command handling
        """

        logger.info(error)
        logger.debug('', exc_info=True)

    def add_commands_from_json_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                command_dict = json_deserialize_from_file(f)

                for name, args in command_dict.items():
                    if name in self.commands:
                        del self.commands[name]

                    if isinstance(args['func'], basecommands.Command):
                        command = args['cls'](name=args['name'], aliases=args['aliases'], func=args['func']._func, no_global_checks=args['no_global_checks'], usage=args['usage'])
                    else:
                        command = args['cls'](name=args['name'], aliases=args['aliases'], func=args['func'], no_global_checks=args['no_global_checks'], usage=args['usage'])
                    self.add_command(command)

        except FileNotFoundError:
            pass

    def dump_commands_to_json_file(self):
        if self.lock_json:
            return

        with open(f"{self.channel_data_dir}/commands.json", 'w') as f:
            f.write(json_serialize_to_string(self.commands))

    async def _handle_checks(self, ctx, no_global_checks=False):
        command = ctx.command

        if no_global_checks:
            checks = [predicate for predicate in command._checks]
        else:
            checks = [predicate for predicate in itertools.chain(self._checks, command._checks)]

        if not checks:
            return True

        for predicate in checks:
            if inspect.iscoroutinefunction(predicate):
                result = await predicate(ctx)
            else:
                result = predicate(ctx)
            if not result:
                return predicate

        return True

    def add_command(self, command: commands.DefaultCommand):
        super().add_command(command)
        self.dump_commands_to_json_file()

    def remove_command(self, command: commands.DefaultCommand):
        super().remove_command(command)
        self.dump_commands_to_json_file()

    def command(self, *, name: str = None, cls=commands.DefaultCommand, **kwargs):
        """Decorator which registers a command on the bot.

        Commands must be a coroutine.
        """

        if not inspect.isclass(cls):
            raise TypeError(f"cls must be of type <class> not <{type(cls)}>")

        def decorator(func):
            cmd_name = name or func.__name__

            command = cls(name=cmd_name, func=func, aliases=aliases, instance=None, **kwargs)
            self.add_command(command)

            return command
        return decorator

    @commands.command(name='bottest', cls=commands.ModCommand)
    async def cmd_bottest(ctx: Context):
        """Check that the bot is connected
        """

        await ctx.send('/me is surviving and thriving MrDestructoid')

    @commands.command(name='addcommand', cls=commands.ModCommand,
                      usage='<new_cmd> <action>')
    async def cmd_addcommand(ctx: Context):
        """Add a command in the channel
        """

        await ctx.send('command was not added!')
