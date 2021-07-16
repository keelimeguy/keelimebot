import argparse
import logging
import sys
import io
import os

from keelimebot.webgui.server import Server
from keelimebot.keelimebot import Keelimebot

logger = logging.getLogger(__name__)


def main(args):
    if not os.path.exists(args.channel_data_dir):
        os.makedirs(args.channel_data_dir)

    keelimebot = Keelimebot(args)
    keelimebot.start()
    keelimebot.join()

    server = Server((args.hostname, args.port), use_ssl=args.ssl)
    server.start()

    server.join()


if __name__ == '__main__':
    _border_str = '-' * len(sys.version)
    print(f"{_border_str}\n{sys.version}\n{_border_str}", end='\n\n', flush=True)

    _parser = argparse.ArgumentParser(description='')
    _parser.add_argument('bot_type', help='twitch|discord')
    _parser.add_argument('-v', '--verbose', action='store_true', help='print debug information')
    _parser.add_argument('--prefix', default='k!', help='prefix to use for commands')
    _parser.add_argument('--channel-data-dir', default='./data', help='name of folder to keep channel data')
    _parser.add_argument('--hostname', default='localhost', help='hostname for gui web server')
    _parser.add_argument('--port', type=int, default=8080, help='port for gui web server')
    _parser.add_argument('--ssl', action='store_true', help='run gui webserver over https')
    _parser.add_argument('--manual-mode', action='store_true', help='run with a manual command line message handler')
    _parser.add_argument('--no-sync', action='store_true', help='do not sync discord slash commands')
    _args = _parser.parse_args()

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if _args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(threadName)s.%(name)s:%(lineno)d [%(levelname)s] %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    main(_args)
