#!/usr/bin/env python3
import socket

HOST, PORT = "127.0.0.1", 9001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(s.recv(1024).decode())
s.send(b"Mensagem do cliente TCP")
print(s.recv(1024).decode())
s.close()
