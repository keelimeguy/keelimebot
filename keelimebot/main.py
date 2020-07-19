import argparse
import logging
import sys
import os

from .keelimebot import Keelimebot

logger = logging.getLogger(__name__)


def main(args):
    if not os.path.exists(args.channel_data_dir):
        os.makedirs(args.channel_data_dir)

    keelimebot = Keelimebot(args.irc_token, args.client_id, args.channel_data_dir)
    keelimebot.run()


if __name__ == '__main__':
    border_str = '-' * len(sys.version)
    print(f"{border_str}\n{sys.version}\n{border_str}", end='\n\n', flush=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    parser.add_argument('--irc_token', default='', help='Twitch IRC OAuth token')
    parser.add_argument('--client_id', default='', help='Twitch API Client ID')
    parser.add_argument('--channel_data_dir', default='./data', help='Name of folder to keep channel data')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(args)
