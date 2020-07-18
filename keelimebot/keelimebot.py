import logging

from twitchio.ext import commands

logger = logging.getLogger(__name__)


class Keelimebot(commands.Bot):

    def __init__(self, irc_token):
        super().__init__(
            irc_token=irc_token,
            nick='keelimebot',
            prefix='!',
            initial_channels=['keelimebot']
        )

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def test_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')
