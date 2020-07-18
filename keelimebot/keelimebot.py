import logging

from twitchio.ext import commands
from .permissions import Permissions

logger = logging.getLogger(__name__)


class Keelimebot(commands.Bot):

    def __init__(self, irc_token, client_id):
        super().__init__(
            irc_token=irc_token,
            client_id=client_id,
            nick='keelimebot',
            prefix='!',
            initial_channels=['keelimebot']
        )

    def get_author_permissions(self, ctx):
        """Returns the permissions of the given message's author

        :param ctx: message context, such as given to event_message(self, ctx)
        :rtype: Permissions
        """
        if ctx.tags and ctx.tags['room-id'] == ctx.author.id:
            return Permissions.STREAMER

        elif ctx.author.name.lower() == self.nick.lower():
            return Permissions.BOT

        elif ctx.author.is_mod:
            return Permissions.MODERATOR

        elif ctx.author.is_subscriber:
            return Permissions.SUBSCRIBER

        return Permissions.NONE

    async def event_ready(self):
        """Called once when the bot goes online.
        """
        logger.info(f'Ready | {self.nick}')
        for channel in self.initial_channels:
            await self._ws.send_privmsg(channel, f"/me has landed!")

    async def event_message(self, ctx):
        """Called once when a message is posted in chat.
        """
        permissions = self.get_author_permissions(ctx)
        if permissions == Permissions.NONE:
            logger.info(f"[#{ctx.channel}]{ctx.author.name}: {ctx.content}")
        else:
            logger.info(f"[#{ctx.channel}]{ctx.author.name}({permissions.name}): {ctx.content}")

        await self.handle_commands(ctx)

    @commands.command(name='bottest')
    async def cmd_bottest(self, ctx):
        """Check that the bot is connected
        """
        await ctx.send(f'/me is surviving and thriving MrDestructoid')
