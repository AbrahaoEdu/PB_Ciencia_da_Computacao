#!/usr/bin/env python3
"""QuickSort com analise de complexidade e graficos."""
import random
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "output"


def quicksort(arr: list[int]) -> list[int]:
    """QuickSort: particiona em torno do pivot e ordena recursivamente."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)


def medir(n: int, repeticoes: int = 3) -> float:
    random.seed(n)
    tempos = []
    for _ in range(repeticoes):
        data = [random.randint(0, 100000) for _ in range(n)]
        t0 = time.perf_counter()
        quicksort(data)
        tempos.append(time.perf_counter() - t0)
    return sum(tempos) / len(tempos)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tamanhos = list(range(25, 1001, 25))
    resultados = []
    print("QuickSort - Complexidade media O(n log n), pior O(n²)")
    for n in tamanhos:
        t = medir(n)
        resultados.append((n, t))
        print(f"n={n}: {t:.6f}s")

    lines = ["n | tempo_s"] + [f"{n} | {t:.6f}" for n, t in resultados]
    (OUTPUT / "quicksort_results.txt").write_text("\n".join(lines), encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 5))
        plt.plot([r[0] for r in resultados], [r[1] for r in resultados], "b-o", markersize=3)
        plt.xlabel("Tamanho da lista")
        plt.ylabel("Tempo (s)")
        plt.title("QuickSort - Tempo vs Tamanho")
        plt.grid(True)
        plt.savefig(OUTPUT / "quicksort_graph.png", dpi=120)
    except ImportError:
        pass


if __name__ == "__main__":
    main()
