#!/usr/bin/env python3
"""Servidor Telnet simplificado."""
import socket
import threading

HOST, PORT = "0.0.0.0", 9003


def session(conn, addr):
    conn.send(b"Login: ")
    user = conn.recv(64).strip()
    conn.send(f"Bem-vindo {user.decode()}\r\n".encode())
    conn.send(b"Comando (quit para sair): ")
    while True:
        cmd = conn.recv(256).decode().strip()
        if cmd.lower() == "quit":
            conn.send(b"Ate logo\r\n")
            break
        conn.send(f"Executado: {cmd}\r\n".encode())
        conn.send(b"Comando: ")
    conn.close()


def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(3)
    print(f"[Telnet Server] Porta {PORT}")
    conn, addr = s.accept()
    session(conn, addr)


if __name__ == "__main__":
    main()
