import logging

from keelimebot.twitch.twitch_core import TwitchCore

logger = logging.getLogger(__name__)


def get_twitch_bot(args) -> TwitchCore:
    core = TwitchCore(prefix=args.prefix, channel_data_dir=args.channel_data_dir)
    return core
