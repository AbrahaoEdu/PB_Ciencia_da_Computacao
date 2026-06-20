#!/usr/bin/env python3
import socket

HOST, PORT = "0.0.0.0", 9002

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print(f"[UDP Server] Escutando em {PORT}")
data, addr = s.recvfrom(1024)
print(f"[UDP Server] De {addr}: {data.decode()}")
s.sendto(b"Resposta UDP OK", addr)
s.close()
