"""
Command-line interface for the https-server.
"""

import argparse
import logging
import os
from typing import List

from httpself.security import get_self_signed_certificate
from httpself.server import run_server

logging.basicConfig(format='%(message)s', level=logging.INFO)


def run() -> None:
    """Command wrapper for Poetry."""
    try:
        main(parse_args())
    except KeyboardInterrupt:
        logging.warning('Aborted')


def main(args: argparse.Namespace) -> None:
    """Script entry point."""
    hostname = '0.0.0.0' if args.public else 'localhost'
    address = hostname, args.port
    cert_path = get_self_signed_certificate(hostname)
    try:
        run_server(address, cert_path)
    finally:
        os.remove(cert_path)


def parse_args(args: List[str] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=443)
    parser.add_argument('--public', action='store_true', default=False)
    return parser.parse_args(args)
