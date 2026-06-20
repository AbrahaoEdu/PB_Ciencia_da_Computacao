#!/usr/bin/env python3
"""QuickSelect - busca do k-esimo elemento em O(n) medio."""
import random
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "output"


def partition(arr: list[int], left: int, right: int, pivot_idx: int) -> int:
    pivot = arr[pivot_idx]
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    store = left
    for i in range(left, right):
        if arr[i] < pivot:
            arr[store], arr[i] = arr[i], arr[store]
            store += 1
    arr[store], arr[right] = arr[right], arr[store]
    return store


def quickselect(arr: list[int], k: int) -> int:
    """Retorna o k-esimo menor elemento (0-indexed)."""
    a = arr[:]
    left, right = 0, len(a) - 1
    while left <= right:
        pivot_idx = random.randint(left, right)
        pivot = partition(a, left, right, pivot_idx)
        if k == pivot:
            return a[k]
        if k < pivot:
            right = pivot - 1
        else:
            left = pivot + 1
    return a[k]


def medir(n: int) -> float:
    random.seed(n)
    data = [random.randint(0, 100000) for _ in range(n)]
    k = random.randint(0, n - 1)
    t0 = time.perf_counter()
    quickselect(data, k)
    return time.perf_counter() - t0


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tamanhos = list(range(25, 1001, 25))
    resultados = []
    print("QuickSelect - Complexidade media O(n), pior O(n²)")
    for n in tamanhos:
        t = medir(n)
        resultados.append((n, t))
        print(f"n={n}: {t:.6f}s")

    lines = ["n | tempo_s"] + [f"{n} | {t:.6f}" for n, t in resultados]
    (OUTPUT / "quickselect_results.txt").write_text("\n".join(lines), encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 5))
        plt.plot([r[0] for r in resultados], [r[1] for r in resultados], "g-o", markersize=3)
        plt.xlabel("Tamanho da lista")
        plt.ylabel("Tempo (s)")
        plt.title("QuickSelect - Tempo vs Tamanho")
        plt.grid(True)
        plt.savefig(OUTPUT / "quickselect_graph.png", dpi=120)
    except ImportError:
        pass


if __name__ == "__main__":
    main()
