#!/usr/bin/env python3
"""Programa 1: ordenação Bubble, Selection e Insertion Sort com medição de tempo."""
import copy
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LISTAGEM = BASE / "data" / "listagem_arquivos.txt"
OUTPUT = BASE / "output"


def bubble_sort(arr: list[str]) -> list[str]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(arr: list[str]) -> list[str]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: list[str]) -> list[str]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def medir(nome: str, func, dados: list[str]) -> tuple[float, list[str]]:
    d = copy.deepcopy(dados)
    inicio = time.perf_counter()
    resultado = func(d)
    fim = time.perf_counter()
    return fim - inicio, resultado


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not LISTAGEM.exists():
        from gerar_listagem import gerar_listagem

        gerar_listagem()

    with open(LISTAGEM, encoding="utf-8") as f:
        dados = [line.strip() for line in f if line.strip()]

    print(f"Total de arquivos: {len(dados)}")
    algoritmos = [
        ("Bubble Sort", bubble_sort, "O(n²)"),
        ("Selection Sort", selection_sort, "O(n²)"),
        ("Insertion Sort", insertion_sort, "O(n²)"),
    ]

    linhas = ["Algoritmo | Tempo (s) | Complexidade | Primeiro | Ultimo"]
    linhas.append("-" * 70)
    resultados = []

    for nome, func, big_o in algoritmos:
        tempo, ordenado = medir(nome, func, dados)
        resultados.append((nome, tempo, big_o))
        linhas.append(
            f"{nome} | {tempo:.4f} | {big_o} | {ordenado[0][:30]} | {ordenado[-1][:30]}"
        )
        print(f"{nome}: {tempo:.4f}s ({big_o})")

    out_file = OUTPUT / "sort_results.txt"
    out_file.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Resultados salvos em {out_file}")

    try:
        import matplotlib.pyplot as plt

        nomes = [r[0] for r in resultados]
        tempos = [r[1] for r in resultados]
        plt.figure(figsize=(8, 5))
        plt.bar(nomes, tempos, color=["#4C72B0", "#55A868", "#C44E52"])
        plt.ylabel("Tempo (s)")
        plt.title("Comparacao de Algoritmos de Ordenacao - TP1")
        plt.tight_layout()
        plt.savefig(OUTPUT / "sort_comparison.png", dpi=120)
        print(f"Grafico salvo em {OUTPUT / 'sort_comparison.png'}")
    except ImportError:
        print("matplotlib nao instalado; grafico omitido")


if __name__ == "__main__":
    main()
