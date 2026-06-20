#!/bin/bash
set -e
TP2="$(cd "$(dirname "$0")" && pwd)"
cd "$TP2/src"
mkdir -p ../output

echo "=== Exercicio 1: Pi OpenMP ==="
gcc -fopenmp programa_pi.c -o ../output/programa_pi
export OMP_NUM_THREADS=1; ../output/programa_pi | tee ../output/pi_1thread.txt
export OMP_NUM_THREADS=4; ../output/programa_pi | tee ../output/pi_4threads.txt

echo "=== Exercicio 2: Downloads ==="
python3 download_manager.py | tee ../output/downloads.txt

echo "=== Exercicios 3-4: QuickSort/QuickSelect ==="
python3 quicksort.py
python3 quickselect.py

echo "=== Exercicios 5-6: Lista encadeada / Editor ==="
python3 linked_list.py | tee ../output/linked_list.txt
python3 text_editor.py --demo | tee ../output/editor_demo.txt

echo "=== Exercicios 7-8: Recursao ==="
python3 recursive_fs.py | tee ../output/recursive_fs.txt
python3 ruler.py | tee ../output/ruler.txt

echo "=== Exercicio 9: Brilho OpenMP ==="
gcc -fopenmp brightness_openmp.c -o ../output/brightness
export OMP_NUM_THREADS=4; ../output/brightness | tee ../output/brightness.txt

echo "=== Exercicio 10: Produtor-Consumidor ==="
timeout 12 python3 producer_consumer.py | tee ../output/producer_consumer.txt || true

echo "=== Exercicios 11-12: Linha de Montagem ==="
python3 assembly_line_2.py | tee ../output/assembly_2.txt
python3 assembly_line_3.py | tee ../output/assembly_3.txt

echo "TP2 concluido."
