import argparse
import logging
import sys

from .keelimebot import Keelimebot

logger = logging.getLogger(__name__)


def main(args):
    keelimebot = Keelimebot(args.irc_token)
    keelimebot.run()


if __name__ == '__main__':
    border_str = '-' * len(sys.version)
    print(f"{border_str}\n{sys.version}\n{border_str}", end='\n\n', flush=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('irc_token', help='IRC OAuth token')
    parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(args)