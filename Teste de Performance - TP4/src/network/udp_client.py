#!/usr/bin/env python3
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b"Ping UDP", ("127.0.0.1", 9002))
data, _ = s.recvfrom(1024)
print(f"[UDP Client] {data.decode()}")
s.close()
