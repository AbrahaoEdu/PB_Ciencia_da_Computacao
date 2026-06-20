#!/usr/bin/env python3
"""Servidor TLS na porta 8443."""
import socket
import ssl
from pathlib import Path

BASE = Path(__file__).resolve().parent
CERT = BASE / "cert.pem"
KEY = BASE / "key.pem"
PORT = 8443


def main() -> None:
    if not CERT.exists():
        print("Execute: openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'")
        return
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(CERT), str(KEY))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", PORT))
    sock.listen(1)
    print(f"[Servidor] TLS escutando na porta {PORT}")
    conn, addr = sock.accept()
    with ctx.wrap_socket(conn, server_side=True) as ssock:
        data = ssock.recv(4096).decode()
        print(f"[Servidor] Comando Seguro Recebido: {data.strip()}")


if __name__ == "__main__":
    main()
