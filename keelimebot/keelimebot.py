import datetime
import logging

from twitchio import Context, Message
from twitchio.ext import commands
from typing import *

from .permissions import Permissions, PermissionsError, ModCommand, get_author_permissions
from .globalnames import BOTNAME

logger = logging.getLogger(__name__)


class Keelimebot(commands.Bot):
    def __init__(self, irc_token: str, client_id: str, channel_data_dir: str = '.'):
        super().__init__(
            irc_token=irc_token,
            client_id=client_id,
            nick=BOTNAME,
            prefix='!',
            initial_channels=['keelimebot']
        )

        self.channel_data_dir = channel_data_dir

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

    @commands.command(name='bottest', cls=ModCommand)
    async def cmd_bottest(self, ctx: Context):
        """Check that the bot is connected
        """

        await ctx.send(f'/me is surviving and thriving MrDestructoid')

    @commands.command(name='addcommand', cls=ModCommand)
    async def cmd_addcommand(self, ctx: Context):
        """Add a command in the channel
        """

        await self._ws.send_privmsg(ctx.channel.name, f"command was not added!")
