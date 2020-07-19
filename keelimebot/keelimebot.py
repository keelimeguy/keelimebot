import datetime
import logging
import sys

from twitchio import Context, Message
from twitchio.ext import commands
from typing import *

from .permissions import Permissions, PermissionsError, ModCommand, get_author_permissions
from .globalnames import BOTNAME
from .serializer import json_deserialize_from_file, json_serialize_to_string

logger = logging.getLogger(__name__)


class Keelimebot(commands.Bot):
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
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if author_permissions == Permissions.NONE:
            logger.info(f"{timestamp} [#{message.channel}]{message.author.name}: {message.content}")
        else:
            logger.info(f"{timestamp} [#{message.channel}]{message.author.name}({author_permissions.name}): {message.content}")

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

                    if isinstance(args['func'], commands.Command):
                        command = args['cls'](name=args['name'], aliases=args['aliases'], func=args['func']._func, no_global_checks=args['no_global_checks'])
                    else:
                        command = args['cls'](name=args['name'], aliases=args['aliases'], func=args['func'], no_global_checks=args['no_global_checks'])
                    self.add_command(command)

        except FileNotFoundError:
            pass

    def dump_commands_to_json_file(self):
        if self.lock_json:
            return

        with open(f"{self.channel_data_dir}/commands.json", 'w') as f:
            f.write(json_serialize_to_string(self.commands))

    def add_command(self, command: commands.Command):
        super().add_command(command)
        self.dump_commands_to_json_file()

    def remove_command(self, command: commands.Command):
        super().remove_command(command)
        self.dump_commands_to_json_file()

    @commands.command(name='bottest', cls=ModCommand)
    async def cmd_bottest(ctx: Context):
        """Check that the bot is connected
        """

        await ctx.send(f'/me is surviving and thriving MrDestructoid')

    @commands.command(name='addcommand', cls=ModCommand)
    async def cmd_addcommand(ctx: Context):
        """Add a command in the channel
        """

        await ctx.send(f"command was not added!")
