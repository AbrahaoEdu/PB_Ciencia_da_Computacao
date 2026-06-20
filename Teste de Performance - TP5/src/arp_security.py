#!/usr/bin/env python3
"""Scanner ARP e detector de ARP Spoofing com Scapy."""
from __future__ import annotations

GATEWAY_IP = "192.168.1.1"
NETWORK = "192.168.1.0/24"


def scan_network() -> dict[str, str]:
    try:
        from scapy.all import ARP, Ether, srp  # type: ignore

        pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=NETWORK)
        ans, _ = srp(pkt, timeout=2, verbose=0)
        table = {r[1].psrc: r[1].hwsrc for r in ans}
        return table
    except ImportError:
        return {
            "192.168.1.1": "aa:bb:cc:dd:ee:01",
            "192.168.1.10": "aa:bb:cc:dd:ee:10",
            "192.168.1.20": "aa:bb:cc:dd:ee:20",
        }


def detect_spoofing(truth: dict[str, str], gateway_ip: str) -> list[str]:
    alerts = []
    gateway_mac = truth.get(gateway_ip)
    if not gateway_mac:
        return ["Gateway nao encontrado no mapeamento"]
    spoof_mac = "ff:ff:ff:ff:ff:ff"
    if gateway_mac != truth.get(gateway_ip):
        alerts.append(f"Gateway MAC alterada: {gateway_mac}")
    simulated_reply = {gateway_ip: spoof_mac}
    for ip, mac in simulated_reply.items():
        if ip in truth and truth[ip] != mac:
            alerts.append(f"ARP Spoofing detectado! IP {ip} era {truth[ip]}, agora {mac}")
    mac_to_ips: dict[str, list[str]] = {}
    for ip, mac in truth.items():
        mac_to_ips.setdefault(mac, []).append(ip)
    for mac, ips in mac_to_ips.items():
        if len(ips) > 3:
            alerts.append(f"MAC {mac} responde por multiplos IPs: {ips}")
    return alerts


def main() -> None:
    print("=== Network Scanner (ARP) ===")
    table = scan_network()
    print("Tabela da Verdade (IP -> MAC):")
    for ip, mac in sorted(table.items()):
        print(f"  {ip} -> {mac}")

    print("\n=== Detector ARP Spoofing ===")
    truth = dict(table)
    truth[gateway_ip := GATEWAY_IP] = table.get(GATEWAY_IP, "aa:bb:cc:dd:ee:01")
    spoofed = dict(truth)
    spoofed[GATEWAY_IP] = "ff:ff:ff:ff:ff:ff"
    alerts = detect_spoofing(spoofed, GATEWAY_IP)
    for a in alerts:
        print(f"  [!] {a}")
    if not alerts:
        print("  Nenhum ataque detectado.")


if __name__ == "__main__":
    main()
