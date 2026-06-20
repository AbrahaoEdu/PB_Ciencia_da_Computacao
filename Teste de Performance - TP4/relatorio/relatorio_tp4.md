# Relatorio TP4 - Teste de Performance

**Aluno:** Eduardo De Sa Abrahao  
**Curso:** Engenharia de Software

## Objetivo

Simulador de CPU, Trie em portugues, labirinto com DFS/BFS e aplicacoes cliente-servidor TCP/UDP/Telnet.

## 1. Simulador de CPU

Arquivo: `src/cpu_scheduler.py`

- 10 processos com bursts distintos
- Quantum = 2 (cada processo executa CPU >= 3 vezes)
- Heaps minimas manuais para filas ready e waiting
- Temporizacao real e tabela de estados na saida

## 2. Trie Portugues

Arquivo: `src/trie_portugues.py`

117 palavras inseridas. Funcoes: insert, search, remove, list, autocomplete, autocorrect.

Exemplo: autocorrect('caza') -> 'casa'

## 3. Labirinto (DFS vs BFS)

Arquivo: `src/labirinto.py`

| Algoritmo | Passos no caminho |
|-----------|-------------------|
| DFS (pilha) | 32 |
| BFS (fila) | 28 |

BFS encontra caminho minimo (menor numero de passos).

## 4. Redes

Pasta: `src/network/`

| Protocolo | Porta | Arquivos |
|-----------|-------|----------|
| TCP | 9001 | tcp_server.py, tcp_client.py |
| UDP | 9002 | udp_server.py, udp_client.py |
| Telnet | 9003 | telnet_server.py, telnet_client.py |

Testes: `output/network_tests.txt`. Analise curl documentada em `test_network.py`.

## Como Reproduzir

```
cd "Teste de Performance - TP4"
bash run_all.sh
```

Para rede: iniciar servidores em terminais separados antes dos clientes.
