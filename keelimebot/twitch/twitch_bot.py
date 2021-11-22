import logging

from keelimebot.twitch.twitch_core import TwitchCore

logger = logging.getLogger(__name__)


class TwitchBot:
    core = None

    @classmethod
    def get_core(cls) -> TwitchCore:
        return cls.core

    @classmethod
    def run(cls):
        cls.core.run_bot()

    def __init__(self, args):
        if TwitchBot.core is None:
            TwitchBot.core = TwitchCore(prefix=args.prefix, data_dir=args.data_dir)

        else:
            raise RuntimeError("You cannot create another instance of TwitchBot")
