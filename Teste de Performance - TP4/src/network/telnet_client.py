#!/usr/bin/env python3
import socket

s = socket.socket()
s.connect(("127.0.0.1", 9003))
print(s.recv(64).decode())
s.send(b"eduardo\n")
print(s.recv(128).decode())
s.send(b"help\n")
print(s.recv(128).decode())
s.send(b"quit\n")
s.close()
