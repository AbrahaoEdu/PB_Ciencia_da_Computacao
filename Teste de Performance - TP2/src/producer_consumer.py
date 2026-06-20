#!/usr/bin/env python3
"""Produtor-Consumidor com asyncio.Queue (hospital)."""
import asyncio
import random
import time


async def produtor(fila: asyncio.Queue, stop: asyncio.Event) -> None:
    while not stop.is_set():
        batimento = random.randint(40, 180)
        await fila.put(batimento)
        await asyncio.sleep(0.5)


async def consumidor(fila: asyncio.Queue, stop: asyncio.Event) -> None:
    while not stop.is_set() or not fila.empty():
        try:
            batimento = await asyncio.wait_for(fila.get(), timeout=0.3)
        except asyncio.TimeoutError:
            continue
        if batimento > 120:
            print(f"ALERTA: Batimento em {batimento}!")
        else:
            print(f"Normal: {batimento}")
        fila.task_done()


async def main() -> None:
    fila: asyncio.Queue = asyncio.Queue(maxsize=10)
    stop = asyncio.Event()
    prod = asyncio.create_task(produtor(fila, stop))
    cons = asyncio.create_task(consumidor(fila, stop))
    await asyncio.sleep(10)
    stop.set()
    await prod
    await cons
    print("Encerramento elegante concluido.")


if __name__ == "__main__":
    asyncio.run(main())
