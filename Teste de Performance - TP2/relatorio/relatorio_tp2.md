# Relatorio TP2 - Teste de Performance

**Aluno:** Eduardo De Sa Abrahao  
**Curso:** Engenharia de Software

## Objetivo

Doze exercicios cobrindo OpenMP, asyncio, QuickSort/QuickSelect, listas encadeadas, recursao e programacao dinamica.

## Grupo 1 - OpenMP e asyncio

**Exercicio 1 - Pi:** `src/programa_pi.c` — 100M passos, `reduction(+:sum)`. Comparar OMP_NUM_THREADS=1 e 4.

**Exercicio 2 - Downloads:** `src/download_manager.py` — 5 arquivos em paralelo; `virus.exe` lanca excecao sem interromper os demais.

## Grupo 2 - QuickSort e QuickSelect

| Algoritmo | Complexidade media | Complexidade pior caso |
|-----------|-------------------|------------------------|
| QuickSort | O(n log n) | O(n²) |
| QuickSelect | O(n) | O(n²) |

Testes de n=25 ate n=1000. Graficos: `output/quicksort_graph.png`, `output/quickselect_graph.png`

## Grupo 3 - Listas Duplamente Encadeadas

- `src/linked_list.py` — representacao de texto
- `src/text_editor.py` — comandos I, E, D, L, C, S, A, F

## Grupo 4 - Recursao

- `src/recursive_fs.py` — tamanho total: 5965 bytes
- `src/ruler.py` — regua recursiva ordem n

## Grupo 5 - OpenMP e Produtor-Consumidor

- `src/brightness_openmp.c` — matriz 10000x10000
- `src/producer_consumer.py` — asyncio.Queue(maxsize=10), 10 segundos

## Grupo 6 - Programacao Dinamica

- `src/assembly_line_2.py` — 2 linhas, 20 estacoes, tempo minimo: 158
- `src/assembly_line_3.py` — 3 linhas, 20 estacoes, tempo minimo: 151

## Como Reproduzir

```
cd "Teste de Performance - TP2"
bash run_all.sh
```

Requer gcc com OpenMP (`libomp-dev`).
