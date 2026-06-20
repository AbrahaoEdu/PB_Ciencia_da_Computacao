#!/usr/bin/env python3
"""Gerenciador de downloads assincrono com asyncio."""
import asyncio
import random
import time

ARQUIVOS = [
    "documento.pdf",
    "foto.jpg",
    "video.mp4",
    "musica.mp3",
    "virus.exe",
    "relatorio.xlsx",
]


async def baixar_arquivo(nome_arquivo: str) -> str:
    print(f"[INICIO] Download de {nome_arquivo}")
    if nome_arquivo == "virus.exe":
        raise ValueError(f"Arquivo bloqueado: {nome_arquivo}")
    tempo = random.uniform(1, 5)
    await asyncio.sleep(tempo)
    print(f"[FIM] Download de {nome_arquivo} concluido ({tempo:.2f}s)")
    return nome_arquivo


async def main() -> None:
    random.seed(42)
    inicio = time.perf_counter()
    tarefas = [baixar_arquivo(a) for a in ARQUIVOS]
    resultados = await asyncio.gather(*tarefas, return_exceptions=True)
    fim = time.perf_counter()

    baixados = [r for r in resultados if isinstance(r, str)]
    erros = [r for r in resultados if isinstance(r, Exception)]

    print(f"\nTempo total: {fim - inicio:.2f}s")
    print(f"Arquivos baixados: {baixados}")
    print(f"Erros tratados: {len(erros)}")


if __name__ == "__main__":
    asyncio.run(main())
