#!/usr/bin/env python3
"""Trie binaria para roteamento IP com LPM e path compression basica."""
from __future__ import annotations


class TrieNode:
    __slots__ = ("left", "right", "route_id", "skip", "prefix")

    def __init__(self) -> None:
        self.left: TrieNode | None = None
        self.right: TrieNode | None = None
        self.route_id: int | None = None
        self.skip: int = 0
        self.prefix: str = ""


def parse_cidr(cidr: str) -> tuple[list[int], int]:
    ip, mask = cidr.split("/")
    bits = []
    for part in ip.split("."):
        v = int(part)
        for i in range(7, -1, -1):
            bits.append((v >> i) & 1)
    if ":" in cidr:
        return bits, int(mask)
    return bits[: int(mask)], int(mask)


def ip_to_bits(ip: str) -> list[int]:
    if ":" in ip:
        return parse_cidr(ip + "/128")[0]
    bits = []
    for part in ip.split("."):
        v = int(part)
        for i in range(7, -1, -1):
            bits.append((v >> i) & 1)
    return bits


class IPTrie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, prefix: str, route_id: int) -> None:
        bits, _ = parse_cidr(prefix) if "/" in prefix else (ip_to_bits(prefix), len(ip_to_bits(prefix)) * 8)
        node = self.root
        for b in bits:
            if b == 0:
                if node.left is None:
                    node.left = TrieNode()
                node = node.left
            else:
                if node.right is None:
                    node.right = TrieNode()
                node = node.right
        node.route_id = route_id

    def lookup(self, ip: str) -> int | None:
        bits = ip_to_bits(ip)
        node = self.root
        best: int | None = None
        i = 0
        while node and i < len(bits):
            if node.route_id is not None:
                best = node.route_id
            b = bits[i]
            node = node.left if b == 0 else node.right
            i += 1
        if node and node.route_id is not None:
            best = node.route_id
        return best

    def compress(self, node: TrieNode | None = None) -> None:
        if node is None:
            node = self.root
        if node.left and node.left.route_id is None and not node.left.left and not node.left.right:
            if node.left.left is None and node.left.right:
                pass
        for child in (node.left, node.right):
            if child:
                self.compress(child)
                if (
                    child.route_id is None
                    and ((child.left and not child.right) or (child.right and not child.left))
                ):
                    grand = child.left or child.right
                    if grand:
                        child.skip += 1 + grand.skip
                        child.route_id = grand.route_id
                        child.left = grand.left
                        child.right = grand.right


def main() -> None:
    trie = IPTrie()
    routes = [
        ("192.168.0.0/16", 1),
        ("192.168.1.0/24", 2),
        ("10.0.0.0/8", 3),
    ]
    for p, rid in routes:
        trie.insert(p, rid)

    tests = [
        ("192.168.1.5", 2),
        ("192.168.2.1", 1),
        ("10.1.2.3", 3),
    ]
    print("Longest Prefix Match:")
    for ip, expected in tests:
        got = trie.lookup(ip)
        status = "OK" if got == expected else "FAIL"
        print(f"  {ip} -> rota {got} (esperado {expected}) [{status}]")


if __name__ == "__main__":
    main()
