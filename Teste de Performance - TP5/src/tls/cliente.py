#!/usr/bin/env python3
import socket
import ssl
from pathlib import Path

BASE = Path(__file__).resolve().parent
CERT = BASE / "cert.pem"
PORT = 8443
MSG = "AUTH_TOKEN:XYZ123:CMD:REBOOT_SERVER"


def main() -> None:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with ctx.wrap_socket(sock, server_hostname="localhost") as ssock:
        ssock.connect(("127.0.0.1", PORT))
        ssock.send(MSG.encode())
        print(f"[Cliente] Enviado: {MSG}")


if __name__ == "__main__":
    main()
