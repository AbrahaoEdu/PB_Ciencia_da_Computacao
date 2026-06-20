#!/bin/bash
set -e
TP1="$(cd "$(dirname "$0")" && pwd)"
cd "$TP1"
bash scripts/gerar_listagem.sh
python3 src/sort_algorithms.py
python3 src/data_structures.py
echo "TP1 executado. Ver output/"
