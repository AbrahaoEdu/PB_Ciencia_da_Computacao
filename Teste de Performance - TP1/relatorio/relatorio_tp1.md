# Relatorio TP1 - Teste de Performance

**Aluno:** Eduardo De Sa Abrahao  
**Curso:** Engenharia de Software

## Objetivo

Listagem de arquivos em Linux, ordenacao com Bubble/Selection/Insertion Sort e analise de hashtable, pilha e fila com medicao de tempo e memoria.

## Parte 1 - Manipulacao de Arquivos Linux

Listagem de 12.000 arquivos gerada com `scripts/gerar_listagem.sh` (equivalente a `find ... | sort > data/listagem_arquivos.txt`).

Arquivo: `data/listagem_arquivos.txt`

## Parte 2 - Programa 1: Algoritmos de Ordenacao

Arquivo: `src/sort_algorithms.py`

| Algoritmo | Tempo (s) | Complexidade |
|-----------|-----------|--------------|
| Bubble Sort | 9.4082 | O(n²) |
| Selection Sort | 5.5504 | O(n²) |
| Insertion Sort | 0.0022 | O(n²) |

**Analise:** Bubble e Selection confirmam comportamento quadratico. Insertion Sort foi rapido porque a listagem ja estava parcialmente ordenada (melhor caso O(n)).

Grafico: `output/sort_comparison.png`

## Parte 3 - Programa 2: Estruturas de Dados

Arquivo: `src/data_structures.py`

| Estrutura | Tempo (s) | Memoria (bytes) |
|-----------|-----------|-----------------|
| Hashtable | 0.0928 | 1873597 |
| Pilha | 0.0009 | 109187 |
| Fila | 0.0021 | 101437 |

Posicoes consultadas: 1a, 100a, 1000a, 5000a e ultima. Operacoes de insercao e remocao executadas em cada estrutura.

## Como Reproduzir

```
cd "Teste de Performance - TP1"
bash run_all.sh
```

## Arquivos Entregues

- data/listagem_arquivos.txt
- src/sort_algorithms.py
- src/data_structures.py
- output/sort_results.txt
- output/structures_results.txt
- output/sort_comparison.png
