import threading
import logging

from keelimebot.twitch.twitch_bot import get_twitch_bot
from keelimebot.discord.discord_bot import get_discord_bot

logger = logging.getLogger(__name__)


class Keelimebot(threading.Thread):
    __instance__ = None

    @classmethod
    def get_instance(cls):
        return cls.__instance__

    def __init__(self, args):
        if Keelimebot.__instance__ is None:
            Keelimebot.__instance__ = self
        else:
            raise RuntimeError("You cannot create another instance of Keelimebot")

        threading.Thread.__init__(self)

        if args.bot_type == "twitch":
            self.bot = get_twitch_bot(args)

        elif args.bot_type == "discord":
            self.bot = get_discord_bot(args)

        else:
            raise RuntimeError(f'Bad bot_type: "{args.bot_type}"')

    def run(self):
        self.bot.run_bot()
