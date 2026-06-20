#!/usr/bin/env python3
"""Editor de textos com lista duplamente encadeada."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from linked_list import DoublyLinkedList


class TextEditor:
    def __init__(self) -> None:
        self.doc = DoublyLinkedList()
        self.doc.append("")

    def cmd_i(self, n: int | None, lines: list[str]) -> None:
        ref = self.doc.line_at(n) if n else self.doc.current
        self.doc.insert_after(ref, lines)

    def cmd_e(self, i: int | None, f: int | None) -> None:
        start = self.doc.line_at(i) if i else self.doc.current
        end = self.doc.line_at(f) if f else start
        if start and end:
            self.doc.delete_range(start, end)

    def cmd_l(self, i: int | None = None, f: int | None = None) -> None:
        lines = self.doc.to_list()
        if i is None:
            for idx, line in enumerate(lines, 1):
                print(f"{idx}: {line}")
        else:
            for idx in range(i, (f or i) + 1):
                if 1 <= idx <= len(lines):
                    print(f"{idx}: {lines[idx - 1]}")

    def cmd_c(self, arq: str, n: int | None) -> None:
        with open(arq, encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f]
        ref = self.doc.line_at(n) if n else self.doc.current
        self.doc.insert_after(ref, lines)

    def cmd_s(self, arq: str, i: int | None, f: int | None) -> None:
        lines = self.doc.to_list()
        if i is None:
            sel = lines
        else:
            sel = lines[i - 1 : f]
        with open(arq, "w", encoding="utf-8") as f:
            f.write("\n".join(sel) + "\n")

    def cmd_a(self, n: int, text: str) -> None:
        node = self.doc.line_at(n)
        if node:
            node.text = text

    def run_interactive(self) -> None:
        print("Editor de Textos - Comandos: I, E, D, L, C, S, A, F")
        while True:
            try:
                cmd = input("> ").strip()
            except EOFError:
                break
            if not cmd:
                continue
            op = cmd[0].upper()
            if op == "F":
                break
            parts = cmd.split(maxsplit=1)
            args = parts[1] if len(parts) > 1 else ""
            self._dispatch(op, args)

    def _dispatch(self, op: str, args: str) -> None:
        if op == "L":
            if not args:
                self.cmd_l()
            else:
                nums = [int(x) for x in args.replace(" ", "").split(",") if x]
                self.cmd_l(nums[0], nums[1] if len(nums) > 1 else None)
        elif op == "I":
            if args:
                n = int(args.split()[0]) if args[0].isdigit() else None
                print("Modo insercao (linha vazia para terminar):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                self.cmd_i(n, lines)
        elif op == "A" and args:
            n, _, text = args.partition(" ")
            self.cmd_a(int(n), text)


def demo() -> None:
    ed = TextEditor()
    ed.cmd_i(None, ["Linha 1", "Linha 2", "Linha 3"])
    ed.cmd_l()
    ed.cmd_a(2, "Linha 2 alterada")
    ed.cmd_l()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo()
    else:
        TextEditor().run_interactive()
