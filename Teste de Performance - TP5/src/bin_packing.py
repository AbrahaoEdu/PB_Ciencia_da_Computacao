#!/usr/bin/env python3
"""Bin Packing: Next-Fit vs First-Fit Decreasing."""
CAPACIDADE_SERVIDOR = 100
VMS_SOLICITADAS = [
    48, 12, 35, 22, 17, 65, 8, 42, 53, 29,
    14, 38, 47, 19, 25, 61, 33, 9, 55, 23,
    44, 16, 50, 31, 11, 28, 58, 41, 13, 37,
    62, 21, 45, 18, 26, 52, 34, 7, 49, 20,
    39, 15, 57, 32, 12, 27, 54, 43, 10, 36,
    60, 24, 46, 16, 22, 51, 30, 8, 40, 25,
]


def next_fit(vms: list[int], cap: int) -> list[list[int]]:
    servers: list[list[int]] = []
    current: list[int] = []
    used = 0
    for vm in vms:
        if used + vm <= cap:
            current.append(vm)
            used += vm
        else:
            if current:
                servers.append(current)
            current = [vm]
            used = vm
    if current:
        servers.append(current)
    return servers


def first_fit_decreasing(vms: list[int], cap: int) -> list[list[int]]:
    sorted_vms = sorted(vms, reverse=True)
    servers: list[list[int]] = []
    usage: list[int] = []
    for vm in sorted_vms:
        placed = False
        for i, u in enumerate(usage):
            if u + vm <= cap:
                servers[i].append(vm)
                usage[i] += vm
                placed = True
                break
        if not placed:
            servers.append([vm])
            usage.append(vm)
    return servers


def report(name: str, servers: list[list[int]]) -> None:
    print(f"\n[Heuristica {name}]")
    print(f"- Servidores utilizados: {len(servers)} servidores")
    if servers:
        total = sum(servers[0])
        print(f"- Exemplo Servidor 1: {servers[0]} (Total: {total}/{CAPACIDADE_SERVIDOR} GB)")


def main() -> None:
    print("=== RESULTADO DA ALOCACAO (HEURISTICAS) ===")
    nf = next_fit(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
    ffd = first_fit_decreasing(VMS_SOLICITADAS, CAPACIDADE_SERVIDOR)
    report("Next-Fit", nf)
    report("First-Fit Decreasing", ffd)
    print(f"\nConclusao: FFD economizou {len(nf) - len(ffd)} servidores em relacao a Next-Fit.")


if __name__ == "__main__":
    main()
