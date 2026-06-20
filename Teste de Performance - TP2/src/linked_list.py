#!/usr/bin/env python3
"""Lista duplamente encadeada para representacao de texto."""
from __future__ import annotations


class Node:
    def __init__(self, text: str = "") -> None:
        self.text = text
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.current: Node | None = None

    def append(self, text: str) -> Node:
        node = Node(text)
        if not self.head:
            self.head = self.tail = self.current = node
        else:
            node.prev = self.tail
            self.tail.next = node  # type: ignore
            self.tail = node
        return node

    def insert_after(self, ref: Node | None, lines: list[str]) -> None:
        if ref is None:
            ref = self.current or self.tail
        for line in lines:
            node = Node(line)
            nxt = ref.next
            node.prev = ref
            ref.next = node
            node.next = nxt
            if nxt:
                nxt.prev = node
            else:
                self.tail = node
            ref = node

    def delete_range(self, start: Node, end: Node) -> None:
        while start and start != end.next:
            nxt = start.next
            prev = start.prev
            if prev:
                prev.next = nxt
            else:
                self.head = nxt
            if nxt:
                nxt.prev = prev
            else:
                self.tail = prev
            if self.current == start:
                self.current = prev or nxt
            start = nxt

    def to_list(self) -> list[str]:
        result = []
        node = self.head
        while node:
            result.append(node.text)
            node = node.next
        return result

    def line_at(self, n: int) -> Node | None:
        node = self.head
        i = 1
        while node and i < n:
            node = node.next
            i += 1
        return node


def demo() -> None:
    dll = DoublyLinkedList()
    for line in ['"A natureza,', "dizem-nos,", 'e apenas o habito..."', "(Rousseau)"]:
        dll.append(line)
    print("Texto representado:")
    for i, t in enumerate(dll.to_list(), 1):
        print(f"  {i}: {t}")


if __name__ == "__main__":
    demo()
