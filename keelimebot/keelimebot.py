import threading
import logging

from keelimebot.twitch.twitch_core import TwitchCore
from keelimebot.discord.discord_core import DiscordCore

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
            self.core = TwitchCore(prefix=args.prefix, channel_data_dir=args.channel_data_dir)

        elif args.bot_type == "discord":
            self.core = DiscordCore(prefix=args.prefix, channel_data_dir=args.channel_data_dir)

        else:
            raise RuntimeError(f'Bad bot_type: "{args.bot_type}"')

    def run(self):
        self.core.run_bot()
