#!/bin/bash
set -e
TP5="$(cd "$(dirname "$0")" && pwd)"
cd "$TP5/src"
mkdir -p ../output tls

python3 rede_fibra.py | tee ../output/rede_fibra.txt
python3 bin_packing.py | tee ../output/bin_packing.txt
python3 arp_security.py | tee ../output/arp.txt
python3 recon_automation.py | tee ../output/recon.txt

if [ ! -f tls/cert.pem ]; then
  openssl req -x509 -newkey rsa:2048 -keyout tls/key.pem -out tls/cert.pem \
    -days 365 -nodes -subj "/CN=localhost" 2>/dev/null || true
fi
python3 tls/sniffer.py | tee ../output/sniffer.txt

echo "TP5 concluido."
