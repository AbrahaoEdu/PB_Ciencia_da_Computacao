#!/usr/bin/env python3
"""Programa 2: hashtable, pilha e fila com medicoes de tempo e memoria."""
import sys
import time
import tracemalloc
from collections import deque
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LISTAGEM = BASE / "data" / "listagem_arquivos.txt"
OUTPUT = BASE / "output"


class Pilha:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str:
        return self._items.pop()

    def peek(self, index: int) -> str:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)


class Fila:
    def __init__(self) -> None:
        self._items: deque[str] = deque()

    def enqueue(self, item: str) -> None:
        self._items.append(item)

    def dequeue(self) -> str:
        return self._items.popleft()

    def get(self, index: int) -> str:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)


class HashTable:
    def __init__(self, size: int = 10007) -> None:
        self.size = size
        self.buckets: list[list[tuple[str, int]]] = [[] for _ in range(size)]

    def _hash(self, key: str) -> int:
        return hash(key) % self.size

    def insert(self, key: str, value: int) -> None:
        h = self._hash(key)
        for i, (k, _) in enumerate(self.buckets[h]):
            if k == key:
                self.buckets[h][i] = (key, value)
                return
        self.buckets[h].append((key, value))

    def get(self, key: str) -> int | None:
        h = self._hash(key)
        for k, v in self.buckets[h]:
            if k == key:
                return v
        return None

    def remove(self, key: str) -> bool:
        h = self._hash(key)
        for i, (k, _) in enumerate(self.buckets[h]):
            if k == key:
                del self.buckets[h][i]
                return True
        return False

    def get_by_index(self, index: int, keys_ordered: list[str]) -> str:
        return keys_ordered[index]


def medir_estrutura(nome: str, func) -> tuple[float, int, str]:
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = func()
    fim = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fim - inicio, peak, resultado


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not LISTAGEM.exists():
        sys.path.insert(0, str(BASE / "scripts"))
        from gerar_listagem import gerar_listagem

        gerar_listagem()

    with open(LISTAGEM, encoding="utf-8") as f:
        dados = [line.strip() for line in f if line.strip()]

    ordenados = sorted(dados)
    posicoes = [0, 99, 999, 4999, len(dados) - 1]
    labels = ["1a", "100a", "1000a", "5000a", "ultima"]

    linhas = ["Estrutura | Operacao | Tempo (s) | Memoria (bytes) | Detalhes"]
    linhas.append("-" * 80)

    def testar_hashtable():
        ht = HashTable()
        for i, item in enumerate(dados):
            ht.insert(item, i)
        vals = [ht.get_by_index(p, ordenados) for p in posicoes]
        ht.remove(dados[0])
        ht.insert("novo_arquivo.txt", len(dados))
        return ", ".join(f"{l}={v[:25]}" for l, v in zip(labels, vals))

    def testar_pilha():
        p = Pilha()
        for item in dados:
            p.push(item)
        vals = [p.peek(len(p) - 1 - p_idx) if p_idx < len(p) else "" for p_idx in posicoes]
        p.pop()
        p.push("novo_arquivo.txt")
        return ", ".join(f"{l}={v[:25]}" for l, v in zip(labels, vals))

    def testar_fila():
        q = Fila()
        for item in dados:
            q.enqueue(item)
        vals = [q.get(p) for p in posicoes]
        q.dequeue()
        q.enqueue("novo_arquivo.txt")
        return ", ".join(f"{l}={v[:25]}" for l, v in zip(labels, vals))

    for nome, func in [
        ("Hashtable", testar_hashtable),
        ("Pilha", testar_pilha),
        ("Fila", testar_fila),
    ]:
        tempo, mem, det = medir_estrutura(nome, func)
        linha = f"{nome} | insert+query+add/remove | {tempo:.4f} | {mem} | {det}"
        linhas.append(linha)
        print(linha)

    out = OUTPUT / "structures_results.txt"
    out.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Resultados em {out}")


if __name__ == "__main__":
    main()
