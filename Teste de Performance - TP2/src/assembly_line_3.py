#!/usr/bin/env python3
"""Problema da Linha de Montagem - 3 linhas, programacao dinamica recursiva."""
import random
from functools import lru_cache

NUM_LINHAS = 3


def gerar_instancia(n: int = 20, seed: int = 42):
    random.seed(seed)
    e = [random.randint(1, 10) for _ in range(NUM_LINHAS)]
    x = [random.randint(1, 10) for _ in range(NUM_LINHAS)]
    a = [[random.randint(1, 20) for _ in range(n)] for _ in range(NUM_LINHAS)]
    t = [[random.randint(1, 10) for _ in range(n)] for _ in range(NUM_LINHAS)]
    return e, x, a, t


@lru_cache(maxsize=None)
def dp(linha: int, estacao: int, n: int, e_t, x_t, a_t, t_t) -> int:
    a = [list(row) for row in a_t]
    t = [list(row) for row in t_t]
    x = list(x_t)
    if estacao == n - 1:
        return a[linha][estacao] + x[linha]
    opcoes = [a[linha][estacao] + dp(linha, estacao + 1, n, e_t, x_t, a_t, t_t)]
    for outra in range(NUM_LINHAS):
        if outra != linha:
            opcoes.append(
                a[linha][estacao] + t[linha][estacao] + dp(outra, estacao + 1, n, e_t, x_t, a_t, t_t)
            )
    return min(opcoes)


def tempo_minimo(n: int = 20) -> int:
    e, x, a, t = gerar_instancia(n)
    e_t = tuple(e)
    x_t = tuple(x)
    a_t = tuple(tuple(row) for row in a)
    t_t = tuple(tuple(row) for row in t)
    return min(e[i] + dp(i, 0, n, e_t, x_t, a_t, t_t) for i in range(NUM_LINHAS))


def main() -> None:
    n = 20
    tempo = tempo_minimo(n)
    print(f"Linha de montagem (3 linhas, {n} estacoes): tempo minimo = {tempo}")


if __name__ == "__main__":
    main()
