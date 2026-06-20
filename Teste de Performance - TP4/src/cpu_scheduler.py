#!/usr/bin/env python3
"""Simulador de escalonamento CPU com heaps minimas manuais."""
import time
from dataclasses import dataclass, field
from enum import Enum


class State(Enum):
    NEW = "Nova"
    READY = "Pronta"
    WAITING = "Suspensa"
    RUNNING = "Executando"
    TERMINATED = "Terminada"


@dataclass(order=True)
class HeapItem:
    priority: int
    pid: int = field(compare=False)
    obj: object = field(compare=False, default=None)


class MinHeap:
    """Heap minima manual (array-based)."""

    def __init__(self) -> None:
        self._data: list[HeapItem] = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _heapify_up(self, i: int) -> None:
        while i > 0 and self._data[i].priority < self._data[self._parent(i)].priority:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _heapify_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            smallest = i
            l, r = self._left(i), self._right(i)
            if l < n and self._data[l].priority < self._data[smallest].priority:
                smallest = l
            if r < n and self._data[r].priority < self._data[smallest].priority:
                smallest = r
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    def push(self, item: HeapItem) -> None:
        self._data.append(item)
        self._heapify_up(len(self._data) - 1)

    def pop(self) -> HeapItem | None:
        if not self._data:
            return None
        if len(self._data) == 1:
            return self._data.pop()
        root = self._data[0]
        self._data[0] = self._data.pop()
        self._heapify_down(0)
        return root

    def __len__(self) -> int:
        return len(self._data)

    def peek(self) -> HeapItem | None:
        return self._data[0] if self._data else None


@dataclass
class Process:
    pid: int
    burst: int
    remaining: int
    io_time: int = 0
    state: State = State.NEW
    times_scheduled: int = 0


def simulate(processes: list[Process], quantum: int = 2) -> list[str]:
    ready = MinHeap()
    waiting = MinHeap()
    log: list[str] = []
    clock = 0
    running: Process | None = None
    quantum_left = 0

    for p in processes:
        p.state = State.READY
        ready.push(HeapItem(p.burst, p.pid, p))

    log.append(f"{'Tempo':<6} | {'PID':<4} | {'Estado':<12} | Ready | Wait | Running")
    log.append("-" * 60)

    while running or ready or waiting:
        if not running and ready:
            item = ready.pop()
            running = item.obj
            running.state = State.RUNNING
            running.times_scheduled += 1
            quantum_left = quantum

        if running:
            log.append(
                f"{clock:<6} | P{running.pid:<3} | Executando   | {len(ready):<5} | {len(waiting):<4} | P{running.pid}"
            )
            time.sleep(0.05)
            running.remaining -= 1
            quantum_left -= 1
            clock += 1

            if running.remaining == 0:
                running.state = State.TERMINATED
                log.append(f"{clock:<6} | P{running.pid:<3} | Terminada    | {len(ready):<5} | {len(waiting):<4} | -")
                running = None
            elif quantum_left == 0 and running.io_time > 0:
                running.state = State.WAITING
                running.io_time -= 1
                waiting.push(HeapItem(running.burst, running.pid, running))
                running = None
            elif quantum_left == 0:
                running.state = State.READY
                ready.push(HeapItem(running.remaining, running.pid, running))
                running = None
        else:
            clock += 1

        done = []
        temp = []
        while waiting:
            item = waiting.pop()
            p = item.obj
            if p.io_time <= 0:
                p.state = State.READY
                ready.push(HeapItem(p.remaining, p.pid, p))
            else:
                temp.append(item)
        for item in temp:
            waiting.push(item)

        if not running and not ready and waiting:
            break

    return log


def main() -> None:
    procs = [
        Process(1, burst=8, remaining=8, io_time=1),
        Process(2, burst=4, remaining=4, io_time=0),
        Process(3, burst=9, remaining=9, io_time=2),
        Process(4, burst=5, remaining=5, io_time=1),
        Process(5, burst=3, remaining=3, io_time=0),
        Process(6, burst=7, remaining=7, io_time=1),
        Process(7, burst=2, remaining=2, io_time=0),
        Process(8, burst=6, remaining=6, io_time=2),
        Process(9, burst=4, remaining=4, io_time=0),
        Process(10, burst=5, remaining=5, io_time=1),
    ]
    quantum = 2
    log = simulate(procs, quantum)
    for line in log:
        print(line)
    for p in procs:
        print(f"P{p.pid}: execucoes CPU = {p.times_scheduled}")


if __name__ == "__main__":
    main()
