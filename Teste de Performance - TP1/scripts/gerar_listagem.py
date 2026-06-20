#!/usr/bin/env python3
"""Gera listagem sintética com 10000+ caminhos de arquivos (equivalente ao find Linux)."""
import os
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
OUTPUT = DATA_DIR / "listagem_arquivos.txt"

EXTENSIONS = [".txt", ".py", ".c", ".h", ".json", ".log", ".cfg", ".md", ".csv", ".dat"]
DIRS = ["docs", "src", "lib", "tests", "bin", "config", "logs", "backup", "cache", "tmp"]


def gerar_listagem(total: int = 12000) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    random.seed(42)
    paths = set()
    while len(paths) < total:
        depth = random.randint(1, 5)
        parts = [random.choice(DIRS) for _ in range(depth)]
        name = f"arquivo_{random.randint(1, 999999)}{random.choice(EXTENSIONS)}"
        paths.add("/".join(parts + [name]))
    ordered = sorted(paths)
    OUTPUT.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Gerados {len(ordered)} arquivos em {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    gerar_listagem()
