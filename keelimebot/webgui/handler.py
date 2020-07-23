import http.server
import logging

logger = logging.getLogger(__name__)


class Handler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logger.debug(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")
        self._set_response()
        self.wfile.write(f"GET request for {self.path}".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logger.debug(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}"
                     f"\n\nBody:\n{post_data.decode('utf-8')}\n")

        self._set_response()
        self.wfile.write(f"POST request for {self.path}".encode('utf-8'))
