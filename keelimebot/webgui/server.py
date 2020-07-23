import http.server
import threading
import logging
import ssl

from typing import Tuple

from .handler import Handler

logger = logging.getLogger(__name__)


class Server(http.server.HTTPServer, threading.Thread):
    def __init__(self, server_address: Tuple[str, int], use_ssl: bool = False):
        threading.Thread.__init__(self)

        super().__init__(server_address, Handler)

        if use_ssl:
            self.socket = ssl.wrap_socket(
                self.socket,
                server_side=True,
                certfile='certificate.pem',
                keyfile='key.pem',
                ssl_version=ssl.PROTOCOL_TLS
            )

    def run(self):
        logger.info(f"GUI webserver started at {self.server_address[0]}:{self.server_address[1]}")
        self.serve_forever()
