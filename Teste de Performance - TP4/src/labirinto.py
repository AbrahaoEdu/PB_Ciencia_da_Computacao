#!/usr/bin/env python3
"""Labirinto como grafo com DFS (pilha) e BFS (fila)."""
from collections import deque
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Labirinto: # = parede, . = corredor, S = inicio, E = saida
LABIRINTO = [
    "#############",
    "#S#...#...#.#",
    "#.#.#.#.#.#.#",
    "#...#...#...#",
    "#.#######.#.#",
    "#.....#...#.#",
    "###.#.#.###.#",
    "#...#.#.....#",
    "#.###.#####.#",
    "#.....#.....#",
    "###########E#",
    "#############",
]


def parse_maze(maze: list[str]) -> tuple[dict, tuple, tuple]:
    graph: dict[tuple, list[tuple]] = {}
    start = end = None
    rows, cols = len(maze), len(maze[0])
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] in ".SE":
                pos = (r, c)
                if maze[r][c] == "S":
                    start = pos
                if maze[r][c] == "E":
                    end = pos
                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#":
                        neighbors.append((nr, nc))
                graph[pos] = neighbors
    assert start and end
    return graph, start, end


def dfs_path(graph: dict, start: tuple, end: tuple) -> list[tuple] | None:
    stack = [(start, [start])]
    visited = {start}
    while stack:
        node, path = stack.pop()
        if node == end:
            return path
        for nb in reversed(graph.get(node, [])):
            if nb not in visited:
                visited.add(nb)
                stack.append((nb, path + [nb]))
    return None


def bfs_path(graph: dict, start: tuple, end: tuple) -> list[tuple] | None:
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return None


def main() -> None:
    graph, start, end = parse_maze(LABIRINTO)
    path_dfs = dfs_path(graph, start, end)
    path_bfs = bfs_path(graph, start, end)
    print(f"Inicio: {start}, Saida: {end}")
    print(f"DFS: caminho com {len(path_dfs)} passos" if path_dfs else "DFS: sem caminho")
    print(f"BFS: caminho com {len(path_bfs)} passos" if path_bfs else "BFS: sem caminho")
    if path_dfs and path_bfs:
        print(f"BFS encontra caminho minimo: {len(path_bfs) <= len(path_dfs)}")

    out = BASE / "output" / "labirinto_results.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"DFS passos: {len(path_dfs) if path_dfs else 0}\nBFS passos: {len(path_bfs) if path_bfs else 0}\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
