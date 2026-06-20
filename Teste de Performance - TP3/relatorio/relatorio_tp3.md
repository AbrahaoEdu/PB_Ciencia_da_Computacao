# Relatorio TP3 - Teste de Performance

**Aluno:** Eduardo De Sa Abrahao  
**Curso:** Engenharia de Software

## Objetivo

Quatro exercicios com arvores e OpenMP, executaveis em Docker (Ubuntu + gcc + libomp).

## Exercicio 1 - Dicionario AVL

Arquivo: `src/bst_dictionary.py`

BST balanceada (AVL) com inserir, buscar, listar, remover, altura e contagem de itens.

Resultado exemplo: altura=3, 5 verbetes inseridos; busca e remocao validadas.

## Exercicio 2 - k-way Merge Paralelo

Arquivo: `src/kway_merge_parallel.c`

16 listas ordenadas fundidas via merge tree com `#pragma omp task`. Reutiliza listagem do TP1.

## Exercicio 3 - Quadtree OpenMP

Arquivo: `src/quadtree_openmp.c`

100.000 particulas em espaco 1000x1000. Insercao paralela com tasks e cutoff; consultas por raio com `parallel for`.

## Exercicio 4 - Roteador IP (LPM)

Arquivo: `src/ip_trie.py`

| IP | Rota esperada | Resultado |
|----|---------------|-----------|
| 192.168.1.5 | 2 (/24) | OK |
| 192.168.2.1 | 1 (/16) | OK |
| 10.1.2.3 | 3 (/8) | OK |

## Docker

```
cd "Teste de Performance - TP3"
docker build -t tp3 docker
docker run -v "$(pwd)":/tp3 tp3 bash run_all.sh
```

## Como Reproduzir (WSL)

```
cd "Teste de Performance - TP3"
bash run_all.sh
```
