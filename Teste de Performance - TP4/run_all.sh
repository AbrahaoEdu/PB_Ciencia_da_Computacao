#!/bin/bash
set -e
TP4="$(cd "$(dirname "$0")" && pwd)"
cd "$TP4/src"
mkdir -p ../output

python3 trie_portugues.py | tee ../output/trie.txt
python3 labirinto.py | tee ../output/labirinto.txt
python3 network/test_network.py | tee ../output/network_tests.txt
echo "TP4 concluido (scheduler e rede: ver src/)."
