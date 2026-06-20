#!/bin/bash
set -e
TP3="$(cd "$(dirname "$0")" && pwd)"
cd "$TP3/src"
mkdir -p ../output

python3 bst_dictionary.py | tee ../output/bst.txt
python3 ip_trie.py | tee ../output/ip_trie.txt

TP1_LIST="$TP3/../Teste de Performance - TP1/data/listagem_arquivos.txt"
gcc -fopenmp kway_merge_parallel.c -o ../output/kway_merge
../output/kway_merge "$TP1_LIST" | tee ../output/kway_merge.txt

gcc -fopenmp quadtree_openmp.c -o ../output/quadtree -lm
../output/quadtree | tee ../output/quadtree.txt

echo "TP3 concluido."
