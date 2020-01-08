"""
A generator of self-signed certificates for the given hostname.
"""

import tempfile
from typing import Tuple

import OpenSSL


def get_self_signed_certificate(hostname: str) -> str:
    """Return path to a temporary file with a PEM certificate.

    Note: the resulting file won't be removed automatically.
    """

    private_key, certificate = _generate_self_signed_certificate(hostname)

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.file.write(private_key)
    temp.file.write(certificate)
    temp.file.flush()

    return temp.name


def _generate_self_signed_certificate(hostname: str) -> Tuple[bytes, bytes]:
    """Return a tuple comprised of the private key and the corresponding certificate."""
    public_key = OpenSSL.crypto.PKey()
    public_key.generate_key(OpenSSL.crypto.TYPE_RSA, 1024)

    certificate = OpenSSL.crypto.X509()

    subject = certificate.get_subject()
    subject.CN = hostname
    subject.C = 'US'
    subject.ST = 'California'
    subject.L = 'Palo Alto'
    subject.O = 'My Company'
    subject.OU = 'My Organization'

    certificate.set_serial_number(1000)
    certificate.gmtime_adj_notBefore(0)
    certificate.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    certificate.set_issuer(subject)
    certificate.set_pubkey(public_key)
    certificate.sign(public_key, 'sha256')

    return (
        OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, public_key),
        OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
    )
