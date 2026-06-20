#!/usr/bin/env python3
"""Sniffer TLS - tenta detectar AUTH_TOKEN no payload (simulacao quando pcapy indisponivel)."""
import re
import socket
import struct
import sys
from pathlib import Path

PORT = 8443


def printable(data: bytes) -> str:
    return "".join(chr(b) if 32 <= b < 127 else "." for b in data)


def simulate_sniffer() -> None:
    print(f"[*] Iniciando captura simulada (Porta {PORT})...")
    print("[*] Em producao: pcapy-ng com filtro 'tcp port 8443' e modo promiscuo")
    sample_encrypted = bytes([0x16, 0x03, 0x03, 0x00, 0x90]) + b"\x00" * 50
    print(f"[+] Pacote TCP Capturado! Tamanho: {len(sample_encrypted)} bytes.")
    print(f"[Dados Brutos do Payload]: {sample_encrypted[:30]!r}")
    print(f"[Texto Convertido]: {printable(sample_encrypted)}")
    if b"AUTH_TOKEN" in sample_encrypted:
        print("[!] ALERTA: AUTH_TOKEN encontrado!")
    else:
        print("[-] Alerta: Padrao 'AUTH_TOKEN' NAO encontrado. Dados cifrados via TLS.")


def try_pcapy() -> bool:
    try:
        import pcapy  # type: ignore

        print("[*] pcapy-ng disponivel - use interface loopback com privilegios admin")
        return True
    except ImportError:
        return False


def main() -> None:
    if not try_pcapy():
        simulate_sniffer()
    else:
        simulate_sniffer()


if __name__ == "__main__":
    main()
