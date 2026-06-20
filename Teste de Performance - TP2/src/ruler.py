#!/usr/bin/env python3
"""Regua de ordem n no intervalo [0, 2^n]."""


def draw_ruler(n: int, left: int, right: int, depth: int, lines: list[str]) -> None:
    if n == 0:
        return
    mid = (left + right) // 2
    tick = "-" * n
    pos = mid - left
    line = [" "] * (right - left + 1)
    if pos < len(line):
        line[pos] = tick
    lines.append("".join(line))
    draw_ruler(n - 1, left, mid, depth + 1, lines)
    draw_ruler(n - 1, mid, right, depth + 1, lines)


def ruler(n: int) -> list[str]:
    lines: list[str] = []
    draw_ruler(n, 0, 2**n, 0, lines)
    return lines


def main() -> None:
    for order in [2, 3, 4]:
        print(f"Regua ordem {order}:")
        for line in ruler(order):
            print(line)
        print()


if __name__ == "__main__":
    main()
