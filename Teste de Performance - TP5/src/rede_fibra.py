#!/usr/bin/env python3
"""Rede de fibra: MST (Kruskal) + Dijkstra (latencia da cidade 0)."""
from __future__ import annotations

NUM_CIDADES = 30
CONEXOES = [
    (0, 1, 45, 3), (0, 2, 60, 8), (0, 3, 75, 12), (1, 2, 20, 2), (1, 4, 55, 6),
    (2, 3, 35, 4), (2, 5, 40, 5), (3, 6, 80, 10), (4, 5, 15, 1), (4, 7, 90, 14),
    (5, 6, 30, 3), (5, 8, 50, 7), (6, 9, 65, 9), (7, 8, 25, 2), (7, 10, 70, 11),
    (8, 9, 45, 5), (8, 11, 60, 8), (9, 12, 85, 13), (10, 11, 15, 1), (10, 13, 50, 6),
    (11, 12, 40, 4), (11, 14, 55, 7), (12, 15, 75, 10), (13, 14, 30, 3), (13, 16, 65, 9),
    (14, 15, 35, 4), (14, 17, 45, 6), (15, 18, 90, 15), (16, 17, 20, 2), (16, 19, 55, 8),
    (17, 18, 40, 5), (17, 20, 60, 9), (18, 21, 80, 12), (19, 20, 25, 3), (19, 22, 70, 11),
    (20, 21, 35, 4), (20, 23, 50, 7), (21, 24, 75, 10), (22, 23, 15, 1), (22, 25, 60, 8),
    (23, 24, 45, 6), (23, 26, 55, 7), (24, 27, 90, 14), (25, 26, 30, 3), (25, 28, 65, 9),
    (26, 27, 40, 5), (26, 29, 70, 11), (27, 29, 50, 6), (28, 29, 25, 2), (0, 4, 110, 18),
    (1, 5, 85, 11), (2, 6, 95, 14), (3, 9, 120, 22), (4, 8, 70, 9), (5, 9, 60, 8),
    (6, 12, 110, 16), (7, 11, 65, 9), (8, 12, 80, 11), (9, 15, 130, 24), (10, 14, 55, 7),
    (11, 15, 70, 9), (12, 18, 115, 19), (13, 17, 60, 8), (14, 18, 75, 10), (15, 21, 140, 25),
    (16, 20, 65, 9), (17, 21, 85, 12), (18, 24, 125, 20), (19, 23, 60, 8), (20, 24, 80, 11),
    (21, 27, 135, 23), (22, 26, 55, 7), (23, 27, 75, 10), (24, 29, 110, 17), (0, 7, 200, 35),
    (3, 12, 180, 28), (10, 19, 150, 22), (13, 22, 140, 21), (16, 25, 160, 26), (1, 8, 95, 13),
    (2, 9, 105, 15), (7, 13, 85, 12), (11, 17, 90, 13), (19, 25, 80, 12), (20, 26, 85, 13),
]


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(n: int, edges: list[tuple]) -> tuple[list[tuple], int]:
    sorted_edges = sorted(edges, key=lambda e: e[2])
    uf = UnionFind(n)
    mst = []
    total = 0
    for u, v, cost, lat in sorted_edges:
        if uf.union(u, v):
            mst.append((u, v, cost, lat))
            total += cost
        if len(mst) == n - 1:
            break
    return mst, total


def dijkstra(n: int, graph: list[list[tuple]], source: int = 0) -> list[int]:
    INF = 10**9
    dist = [INF] * n
    dist[source] = 0
    visited = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not visited[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def build_graph(edges: list[tuple]) -> list[list[tuple]]:
    n = NUM_CIDADES
    g: list[list[tuple]] = [[] for _ in range(n)]
    for u, v, _, lat in edges:
        g[u].append((v, lat))
        g[v].append((u, lat))
    return g


def main() -> None:
    mst, custo = kruskal(NUM_CIDADES, CONEXOES)
    print("=== Rede de Menor Custo (Kruskal) ===")
    for u, v, c, lat in mst:
        print(f"  {u} -- {v} | custo={c} latencia={lat}")
    print(f"Custo total: {custo}")

    graph = build_graph(CONEXOES)
    dist = dijkstra(NUM_CIDADES, graph, 0)
    print("\n=== Latencia acumulada da Cidade 0 ===")
    for i, d in enumerate(dist):
        print(f"  Cidade {i}: {d} ms")


if __name__ == "__main__":
    main()
