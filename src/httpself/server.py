"""
A thin wrapper around the built-in http.server module.
"""

import http.server
import logging
import ssl
from typing import Tuple


def run_server(address: Tuple[str, str], cert_path: str) -> None:
    """Start an HTTP server over SSL/TLS using the given PEM certificate."""

    logging.info('Running server at https://%s:%d', *address)

    httpd = http.server.HTTPServer(address, http.server.SimpleHTTPRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=cert_path, server_side=True)
    httpd.serve_forever()
