#!/usr/bin/env python3
"""Automatizacao de reconhecimento com dnsrecon e nmap."""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "output"
DEFAULT_DNS_TARGET = "zonetransfer.me"
DEFAULT_NMAP_TARGET = "scanme.nmap.org"


def run_cmd(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except FileNotFoundError:
        return -1, f"Comando nao encontrado: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -1, "Timeout"


def dns_recon(target: str) -> dict:
    code, out = run_cmd(["dnsrecon", "-d", target, "-t", "std"])
    if code != 0:
        code, out = run_cmd(["nslookup", target])
    return {"target": target, "output": out[:5000], "status": "ok" if code == 0 else "fallback"}


def nmap_scan(target: str) -> dict:
    try:
        import nmap  # type: ignore

        nm = nmap.PortScanner()
        nm.scan(target, arguments="-Pn -sV --top-ports 100")
        hosts = []
        for host in nm.all_hosts():
            entry = {"host": host, "ports": []}
            for proto in nm[host].all_protocols():
                for port in nm[host][proto]:
                    entry["ports"].append(
                        {
                            "port": port,
                            "state": nm[host][proto][port]["state"],
                            "service": nm[host][proto][port].get("product", ""),
                        }
                    )
            hosts.append(entry)
        return {"target": target, "hosts": hosts}
    except ImportError:
        code, out = run_cmd(["nmap", "-Pn", "-sV", "--top-ports", "20", target])
        return {"target": target, "raw": out[:5000], "status": "cli" if code == 0 else "simulated"}


def simulate_report(dns_target: str, nmap_target: str) -> dict:
    return {
        "timestamp": datetime.now().isoformat(),
        "dns": {
            "target": dns_target,
            "mx": f"mail.{dns_target}",
            "subdomains": [f"www.{dns_target}", f"ns1.{dns_target}"],
            "note": "Resultado simulado quando dnsrecon/nmap indisponiveis",
        },
        "nmap": {
            "target": nmap_target,
            "ports": [
                {"port": 22, "service": "OpenSSH", "state": "open"},
                {"port": 80, "service": "Apache httpd", "state": "open"},
            ],
        },
    }


def main() -> None:
    dns_target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DNS_TARGET
    nmap_target = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_NMAP_TARGET

    print("=" * 50)
    print("RELATORIO AUTOMATIZADO DE SUPERFICIE DE ATAQUE")
    print("=" * 50)
    print(f"\n[+] Alvo analisado: {nmap_target}\n")

    dns_result = dns_recon(dns_target)
    nmap_result = nmap_scan(nmap_target)

    if dns_result.get("status") != "ok" and nmap_result.get("status") not in ("cli", None):
        report = simulate_report(dns_target, nmap_target)
    else:
        report = {
            "timestamp": datetime.now().isoformat(),
            "dns_recon": dns_result,
            "nmap_scan": nmap_result,
        }

    OUTPUT.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT / "relatorio_recon.json"
    out_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("[1] RESULTADOS DNS (dnsrecon):")
    print(f"- Alvo: {dns_target}")
    print(f"- Status: {dns_result.get('status', 'ok')}")

    print("\n[2] RESULTADOS DA VARREDURA (Nmap):")
    print(f"- Alvo: {nmap_target}")
    if "hosts" in nmap_result:
        for h in nmap_result["hosts"]:
            print(f"  Host: {h['host']}")
            for p in h.get("ports", [])[:5]:
                print(f"    Porta {p['port']}: {p['state']} | {p.get('service', '')}")
    else:
        print(f"- Output: {str(nmap_result)[:300]}")

    print(f"\n[+] Arquivo salvo em: {out_file}")


if __name__ == "__main__":
    main()
