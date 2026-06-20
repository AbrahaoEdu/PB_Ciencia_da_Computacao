#!/usr/bin/env python3
"""Servidor TCP simples."""
import socket
import threading

HOST, PORT = "0.0.0.0", 9001


def handle(conn, addr):
    print(f"[TCP Server] Conexao de {addr}")
    conn.send(b"Bem-vindo ao servidor TCP\n")
    data = conn.recv(1024)
    print(f"[TCP Server] Recebido: {data.decode().strip()}")
    conn.send(b"Eco: " + data)
    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[TCP Server] Escutando em {PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
