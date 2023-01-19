import logging
import asyncio
from threading import Thread

from keelimebot.twitch.twitch_bot import TwitchBot
from keelimebot.discord.discord_bot import DiscordBot

logger = logging.getLogger(__name__)


class Keelimebot():
    def __init__(self, args):
        if args.bot_type == "twitch":
            self.bot = TwitchBot(args)

        elif args.bot_type == "discord":
            self.bot = DiscordBot(args)

        else:
            raise RuntimeError(f'Bad bot_type: "{args.bot_type}"')

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.bot.run())
        self.thread = Thread(target=self.loop.run_forever)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()
