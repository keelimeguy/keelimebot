import threading
import logging

from keelimebot.twitchcore import TwitchCore
from keelimebot.discordcore import DiscordCore

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
            self.core = TwitchCore(args.irc_token, args.client_id, channel_data_dir=args.channel_data_dir)

        elif args.bot_type == "discord":
            self.core = DiscordCore()

        else:
            raise RuntimeError(f'Bad bot_type: "{args.bot_type}"')

    def start(self):
        self.core.start()
