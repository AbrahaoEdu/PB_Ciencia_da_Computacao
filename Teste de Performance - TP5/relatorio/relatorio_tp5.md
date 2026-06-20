# Relatorio TP5 - Teste de Performance

**Aluno:** Eduardo De Sa Abrahao  
**Curso:** Engenharia de Software

## Objetivo

Grafos (MST/Dijkstra), heuristica Bin Packing, seguranca TLS/ARP e reconhecimento automatizado.

## Questao 1 - Rede de Fibra

Arquivo: `src/rede_fibra.py`

- Kruskal (MST): custo total = **1065**
- Dijkstra manual: latencias da Cidade 0 ate demais cidades (ex.: Cidade 1 = 3 ms)

## Questao 2 - Bin Packing

Arquivo: `src/bin_packing.py`

| Heuristica | Servidores usados |
|------------|-------------------|
| Next-Fit | 24 |
| First-Fit Decreasing | 20 |

FFD economizou **4 servidores** em relacao a Next-Fit.

## Questao 3 - TLS + Sniffer

Pasta: `src/tls/`

- `servidor.py` — porta 8443, certificado autoassinado
- `cliente.py` — envia AUTH_TOKEN:XYZ123:CMD:REBOOT_SERVER
- `sniffer.py` — padrao AUTH_TOKEN **NAO** encontrado (dados cifrados)

Gerar certificado:
```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

## Questao 4 - ARP Security

Arquivo: `src/arp_security.py`

Scanner ARP (tabela IP->MAC) e detector de ARP spoofing com Scapy.

## Questao 5 - Recon Automation

Arquivo: `src/recon_automation.py`

Integra dnsrecon (zonetransfer.me) e nmap (scanme.nmap.org). Saida: `output/relatorio_recon.json`

## Como Reproduzir

```
cd "Teste de Performance - TP5"
bash run_all.sh
```

**Entrega deste TP:** eduardo_abrahao_PB_TP5.ZIP (codigo + relatorio + outputs)
