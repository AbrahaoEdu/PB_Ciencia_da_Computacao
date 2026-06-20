#!/bin/bash
# Equivalente Linux: find + redirecionamento
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TP1_DIR="$(dirname "$SCRIPT_DIR")"
if [ -n "$1" ] && [ -d "$1" ]; then
  find "$1" -type f | sort > "$TP1_DIR/data/listagem_arquivos.txt"
  echo "Listagem gerada com find em $1"
else
  python3 "$SCRIPT_DIR/gerar_listagem.py"
fi
