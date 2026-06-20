#!/usr/bin/env python3
"""Dicionario com AVL (BST balanceada)."""
from __future__ import annotations


class AVLNode:
    def __init__(self, word: str, meaning: str) -> None:
        self.word = word
        self.meaning = meaning
        self.height = 1
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None


class AVLDictionary:
    def __init__(self) -> None:
        self.root: AVLNode | None = None
        self._count = 0

    def _height(self, node: AVLNode | None) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        x = y.left
        assert x is not None
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        y = x.right
        assert y is not None
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, word: str, meaning: str) -> None:
        self.root = self._insert(self.root, word, meaning)

    def _insert(self, node: AVLNode | None, word: str, meaning: str) -> AVLNode:
        if not node:
            self._count += 1
            return AVLNode(word, meaning)
        if word < node.word:
            node.left = self._insert(node.left, word, meaning)
        elif word > node.word:
            node.right = self._insert(node.right, word, meaning)
        else:
            node.meaning = meaning
            return node
        self._update_height(node)
        bal = self._balance(node)
        if bal > 1 and word < node.left.word:  # type: ignore
            return self._rotate_right(node)
        if bal < -1 and word > node.right.word:  # type: ignore
            return self._rotate_left(node)
        if bal > 1 and word > node.left.word:  # type: ignore
            node.left = self._rotate_left(node.left)  # type: ignore
            return self._rotate_right(node)
        if bal < -1 and word < node.right.word:  # type: ignore
            node.right = self._rotate_right(node.right)  # type: ignore
            return self._rotate_left(node)
        return node

    def search(self, word: str) -> str | None:
        node = self.root
        while node:
            if word == node.word:
                return node.meaning
            node = node.left if word < node.word else node.right
        return None

    def remove(self, word: str) -> bool:
        self.root, removed = self._remove(self.root, word)
        if removed:
            self._count -= 1
        return removed

    def _remove(self, node: AVLNode | None, word: str) -> tuple[AVLNode | None, bool]:
        if not node:
            return None, False
        if word < node.word:
            node.left, ok = self._remove(node.left, word)
        elif word > node.word:
            node.right, ok = self._remove(node.right, word)
        else:
            ok = True
            if not node.left:
                return node.right, ok
            if not node.right:
                return node.left, ok
            succ = node.right
            while succ.left:
                succ = succ.left
            node.word, node.meaning = succ.word, succ.meaning
            node.right, _ = self._remove(node.right, succ.word)
        if node:
            self._update_height(node)
            bal = self._balance(node)
            if bal > 1 and self._balance(node.left) >= 0:
                return self._rotate_right(node), ok
            if bal > 1 and self._balance(node.left) < 0:
                node.left = self._rotate_left(node.left)  # type: ignore
                return self._rotate_right(node), ok
            if bal < -1 and self._balance(node.right) <= 0:
                return self._rotate_left(node), ok
            if bal < -1 and self._balance(node.right) > 0:
                node.right = self._rotate_right(node.right)  # type: ignore
                return self._rotate_left(node), ok
        return node, ok

    def list_words(self) -> list[str]:
        result: list[str] = []

        def inorder(n: AVLNode | None) -> None:
            if n:
                inorder(n.left)
                result.append(n.word)
                inorder(n.right)

        inorder(self.root)
        return result

    def height(self) -> int:
        return self._height(self.root)

    def count(self) -> int:
        return self._count


def main() -> None:
    d = AVLDictionary()
    verbetes = [
        ("algorithm", "procedimento computacional"),
        ("binary", "base dois"),
        ("computer", "maquina programavel"),
        ("data", "informacao estruturada"),
        ("tree", "estrutura hierarquica"),
    ]
    for w, m in verbetes:
        d.insert(w, m)
    print(f"Altura: {d.height()}, Itens: {d.count()}")
    print(f"Busca 'data': {d.search('data')}")
    print(f"Palavras: {d.list_words()}")
    d.remove("binary")
    print(f"Apos remocao: {d.list_words()}, altura={d.height()}")


if __name__ == "__main__":
    main()
