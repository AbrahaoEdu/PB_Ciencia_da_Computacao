#!/usr/bin/env python3
"""Trie com 100+ palavras portuguesas: search, remove, autocomplete, autocorrect."""
from __future__ import annotations


PALAVRAS_PT = """
de a o que e do da em um para com nao uma os no se na por mais as dos como mas foi ao ele das tem a sua ou ser quando muito ha nos ja esta eu tambem so pelo pode mes isso ele esta voce ano entre ate porque ela era depois sem mesmo aos ter seus quem nas meu me sua ou eram era voce tinha sao meu sao foi ter seu sua tem nos ja la onde foi la la la
casa tempo pessoa mundo trabalho vida cidade agua comida escola familia amor paz liberdade justica verdade saber pensar falar ouvir ver sentir caminhar correr aprender ensinar estudar ler escrever palavra frase texto livro pagina capitulo historia futuro presente passado memoria sonho esperanca coragem forca vontade desejo plano meta objetivo resultado sucesso fracasso erro acerto tentativa esforco dedicacao persistencia paciencia calma raiva alegria tristeza medo coragem amizade confianca respeito honestidade bondade generosidade humildade orgulho vaidade egoismo altruismo solidariedade cooperacao competicao rivalidade conflito paz guerra dialogo acordo consenso divergencia opiniao ideia pensamento reflexao analise sintese conclusao argumento prova evidencia fato dado informacao conhecimento ciencia tecnologia inovacao descoberta invento maquina computador programa codigo algoritmo estrutura funcao variavel constante loop condicao iteracao recursao compilador interpretador sistema operacional processo thread memoria arquivo diretorio rede protocolo socket cliente servidor conexao pacote roteador switch firewall criptografia seguranca ataque defesa vulnerabilidade
""".split()


class TrieNode:
    __slots__ = ("children", "is_end", "word")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end = False
        self.word: str | None = None


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
        self._size = 0

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.word = word.lower()

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def remove(self, word: str) -> bool:
        word = word.lower()

        def _remove(node: TrieNode, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.word = None
                return len(node.children) == 0
            ch = word[depth]
            if ch not in node.children:
                return False
            should_delete = _remove(node.children[ch], depth + 1)
            if should_delete:
                del node.children[ch]
                return not node.is_end and len(node.children) == 0
            return False

        if _remove(self.root, 0):
            self._size -= 1
            return True
        if self.search(word) is False and word:
            self._size -= 1
        return self.search(word) is False

    def list_words(self) -> list[str]:
        result: list[str] = []

        def dfs(node: TrieNode) -> None:
            if node.is_end and node.word:
                result.append(node.word)
            for child in node.children.values():
                dfs(child)

        dfs(self.root)
        return sorted(result)

    def autocomplete(self, prefix: str) -> list[str]:
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return []
            node = node.children[ch]
        result: list[str] = []

        def dfs(n: TrieNode) -> None:
            if n.is_end and n.word:
                result.append(n.word)
            for c in n.children.values():
                dfs(c)

        dfs(node)
        return sorted(result)[:10]

    def autocorrect(self, word: str, max_dist: int = 2) -> str | None:
        candidates = self.list_words()

        def dist(a: str, b: str) -> int:
            if abs(len(a) - len(b)) > max_dist:
                return max_dist + 1
            dp = list(range(len(b) + 1))
            for i, ca in enumerate(a, 1):
                prev = dp[0]
                dp[0] = i
                for j, cb in enumerate(b, 1):
                    cur = dp[j]
                    dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (ca != cb))
                    prev = cur
            return dp[-1]

        best = None
        best_d = max_dist + 1
        for c in candidates:
            d = dist(word.lower(), c)
            if d < best_d:
                best_d = d
                best = c
        return best if best_d <= max_dist else None


def main() -> None:
    trie = Trie()
    words = list(dict.fromkeys(PALAVRAS_PT))[:120]
    for w in words:
        if len(w) > 1:
            trie.insert(w)
    print(f"Palavras inseridas: {len(trie.list_words())}")
    print(f"Busca 'casa': {trie.search('casa')}")
    print(f"Autocomplete 'ca': {trie.autocomplete('ca')[:5]}")
    print(f"Autocorrect 'caza': {trie.autocorrect('caza')}")
    trie.remove("caza") if trie.search("caza") else None
    if trie.search("casa"):
        trie.remove("casa")
        print(f"Apos remover 'casa': {trie.search('casa')}")


if __name__ == "__main__":
    main()
