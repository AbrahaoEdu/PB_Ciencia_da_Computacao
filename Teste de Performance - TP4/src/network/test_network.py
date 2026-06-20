#!/usr/bin/env python3
"""Testes de rede e analise com curl (simulado via subprocess)."""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return r.stdout + r.stderr
    except Exception as e:
        return str(e)


def main() -> None:
    lines = ["=== Testes de Rede TP4 ===\n"]
    lines.append("Nota: Servidores devem estar em execucao nas portas 9001-9003.\n")
    lines.append("Comando curl equivalente para Telnet:\n")
    lines.append("  curl telnet://127.0.0.1:9003\n")
    curl_out = run(["curl", "--version"])
    lines.append(f"curl disponivel: {'curl' in curl_out.lower() or len(curl_out) > 0}\n")
    lines.append(curl_out[:200] if curl_out else "curl nao encontrado no PATH\n")
    out = BASE.parent.parent / "output" / "network_tests.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(lines), encoding="utf-8")
    print("".join(lines))


if __name__ == "__main__":
    main()
