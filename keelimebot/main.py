import argparse
import logging
import sys
import os

from .webgui.server import Server
from .keelimebot import Keelimebot

logger = logging.getLogger(__name__)


def main(args):
    if not os.path.exists(args.channel_data_dir):
        os.makedirs(args.channel_data_dir)

    keelimebot = Keelimebot(args.irc_token, args.client_id, channel_data_dir=args.channel_data_dir)
    keelimebot.start()

    server = Server((args.hostname, args.port), use_ssl=args.ssl)
    server.start()


if __name__ == '__main__':
    border_str = '-' * len(sys.version)
    print(f"{border_str}\n{sys.version}\n{border_str}", end='\n\n', flush=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    parser.add_argument('--irc_token', default='', help='the Twitch IRC OAuth token')
    parser.add_argument('--client_id', default='', help='the Twitch API Client ID')
    parser.add_argument('--channel_data_dir', default='./data', help='name of folder to keep channel data')
    parser.add_argument('--hostname', default='localhost', help='hostname for gui web server')
    parser.add_argument('--port', type=int, default=8080, help='port for gui web server')
    parser.add_argument('--ssl', action='store_true', help='run gui webserver over https')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(args)
