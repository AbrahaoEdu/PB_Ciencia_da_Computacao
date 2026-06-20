#!/usr/bin/env python3
"""Problema da Linha de Montagem - 2 linhas, programacao dinamica recursiva."""
import random
from functools import lru_cache


def gerar_instancia(n: int = 20, seed: int = 42):
    random.seed(seed)
    e = [random.randint(1, 10) for _ in range(2)]
    x = [random.randint(1, 10) for _ in range(2)]
    a = [[random.randint(1, 20) for _ in range(n)] for _ in range(2)]
    t = [[random.randint(1, 10) for _ in range(n)] for _ in range(2)]
    return e, x, a, t


@lru_cache(maxsize=None)
def dp(linha: int, estacao: int, n: int, e_t, x_t, a_t, t_t) -> int:
    e = list(e_t)
    x = list(x_t)
    a = [list(row) for row in a_t]
    t = [list(row) for row in t_t]
    if estacao == n - 1:
        return a[linha][estacao] + x[linha]
    permanece = a[linha][estacao] + dp(linha, estacao + 1, n, e_t, x_t, a_t, t_t)
    troca = a[linha][estacao] + t[linha][estacao] + dp(1 - linha, estacao + 1, n, e_t, x_t, a_t, t_t)
    return min(permanece, troca)


def tempo_minimo(n: int = 20) -> int:
    e, x, a, t = gerar_instancia(n)
    e_t = tuple(e)
    x_t = tuple(x)
    a_t = tuple(tuple(row) for row in a)
    t_t = tuple(tuple(row) for row in t)
    return min(
        e[0] + dp(0, 0, n, e_t, x_t, a_t, t_t),
        e[1] + dp(1, 0, n, e_t, x_t, a_t, t_t),
    )


def main() -> None:
    n = 20
    tempo = tempo_minimo(n)
    print(f"Linha de montagem (2 linhas, {n} estacoes): tempo minimo = {tempo}")


if __name__ == "__main__":
    main()
