#!/usr/bin/env python3
"""Funcao recursiva para somar tamanhos em sistema de arquivos aninhado."""

sistema_arquivos = {
    "Documentos": {
        "Trabalho": {"projeto1.pdf": 500, "projeto2.pdf": 300},
        "Pessoal": {"receitas.txt": 10},
    },
    "Imagens": {
        "Ferias": {"foto1.jpg": 2000, "foto2.jpg": 3000},
        "logo.png": 150,
    },
    "README.txt": 5,
}


def tamanho_total(no) -> int:
    if isinstance(no, int):
        return no
    if isinstance(no, dict):
        return sum(tamanho_total(v) for v in no.values())
    return 0


def main() -> None:
    total = tamanho_total(sistema_arquivos)
    print(f"Tamanho total: {total} bytes")
    assert total == 5965


if __name__ == "__main__":
    main()
