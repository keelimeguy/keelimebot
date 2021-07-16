import threading
import logging

from keelimebot.twitch.twitch_bot import TwitchBot
from keelimebot.discord.discord_bot import DiscordBot

logger = logging.getLogger(__name__)


class Keelimebot(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)

        if args.bot_type == "twitch":
            self.bot = TwitchBot(args)

        elif args.bot_type == "discord":
            self.bot = DiscordBot(args)

        else:
            raise RuntimeError(f'Bad bot_type: "{args.bot_type}"')

    def run(self):
        self.bot.run()
