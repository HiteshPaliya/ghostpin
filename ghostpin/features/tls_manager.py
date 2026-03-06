"""
GhostPin v5 Phase 2 — Feature: HTTPS with Self-Signed Certificate
Generates a self-signed cert on first run and stores it in ~/.ghostpin/certs/.
"""
import os, ssl
from pathlib import Path

CERT_DIR = Path.home() / '.ghostpin' / 'certs'
CERT_FILE = CERT_DIR / 'ghostpin.crt'
KEY_FILE  = CERT_DIR / 'ghostpin.key'

def generate_self_signed_cert():
    """Generate a self-signed TLS cert using cryptography or openssl fallback."""
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    if CERT_FILE.exists() and KEY_FILE.exists():
        return  # already exists

    try:
        # Preferred: use cryptography library
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        import datetime

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'GhostPin Enterprise'),
            x509.NameAttribute(NameOID.COMMON_NAME, 'localhost'),
        ])
        now = datetime.datetime.utcnow()
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject).issuer_name(subject)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=3650))
            .add_extension(x509.SubjectAlternativeName([
                x509.DNSName('localhost'),
                x509.IPAddress(__import__('ipaddress').IPv4Address('127.0.0.1')),
            ]), critical=False)
            .sign(key, hashes.SHA256(), default_backend())
        )
        KEY_FILE.write_bytes(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
        CERT_FILE.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        print(f'[GhostPin] TLS cert generated: {CERT_FILE}')

    except ImportError:
        # Fallback: use openssl CLI
        import subprocess
        subprocess.run([
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', str(KEY_FILE), '-out', str(CERT_FILE),
            '-days', '3650', '-nodes', '-subj',
            '/C=US/O=GhostPin Enterprise/CN=localhost',
        ], check=True, capture_output=True)
        print(f'[GhostPin] TLS cert generated via openssl: {CERT_FILE}')

def get_ssl_context() -> ssl.SSLContext:
    """Return an SSL context for Flask's SSL support."""
    generate_self_signed_cert()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(CERT_FILE), str(KEY_FILE))
    return ctx

def get_cert_paths():
    generate_self_signed_cert()
    return str(CERT_FILE), str(KEY_FILE)

def cert_fingerprint() -> str:
    """Return SHA-256 fingerprint of the cert for browser display."""
    try:
        import hashlib
        cert_bytes = CERT_FILE.read_bytes()
        return hashlib.sha256(cert_bytes).hexdigest().upper()
    except Exception:
        return ''
