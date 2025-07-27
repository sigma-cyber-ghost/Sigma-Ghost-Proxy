#!/usr/bin/env python3
import os, time, requests, concurrent.futures, socks, socket
from collections import defaultdict
from rich.console import Console
from rich.prompt import Prompt
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.box import HEAVY, ROUNDED
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn

console = Console()

BANNER_ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀
⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢸⣦⠀⠀⠀⠀⠀⠸⠛⠻⡿⣳⡄
⠰⠉⡯⢽⡀⠀⠀⣀⣀⠀⠀⠘⣏⠀⠀⣀⡀⠀⠀⠀⠀⠇⢨⢻
⡀⠀⠀⢸⡇⠀⢸⠁⠀⠁⢀⣀⣻⣄⣾⠯⠋⠛⠁⠀⠀⠀⠀⣿
⣿⡆⣠⡟⠀⡀⠈⠢⡀⣴⣿⢏⢼⡟⢿⠻⠲⠦⣤⣤⣤⠴⠚⠇
⣼⠀⣿⣇⠈⠓⢒⣶⣿⣿⣿⣿⣿⡗⢸⣧⠀⠀⠀⠀⠂⠀⠀⠀
⢹⡄⠁⢙⢲⣾⣿⣿⣾⣿⣿⣿⣿⡤⣾⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠘⠛⢷⠞⣛⣭⣿⣿⣿⣿⣿⡟⣿⣟⣙⡆⠀⠀⠀⠀⠀⠀⠀⠀
⣤⣦⠸⠘⠀⣸⣿⣿⣿⣿⣿⢧⣿⣿⠻⡇⠀⠀⠀⠀⠀⠀⠀⠀
⡽⠀⠀⠀⣰⡟⠽⢹⣿⣿⣿⣄⠸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣷⣦⣴⢾⠋⠁⠀⢸⣿⣿⣿⣿⡇⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠘⠀⠀⠀⢸⣿⣿⢻⣿⣿⡘⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣧⢿⣿⣧⢿⣿⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠘⡈⣿⣿⡜⣿⣿⡀⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠃⠸⣿⣧⢿⡿⠟⠷⢗⣦⣄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣇⠀⠀⠹⣿⣿⠒⠒⠒⢸⠗⣽⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣧⣟⣿⣿⣆⠀⠀⢹⣿⣦⠀⠀⠀⠀⠻⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⢻⣝⡿⣿⣆⠀⠀⢹⣿⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠃⠀⠀⠙⡛⠃⠀⠀⠀⠀⠀
"""

SOCIAL = """
[bright_white]Follow Sigma Ghost:[/bright_white]
[cyan]Telegram:[/] https://t.me/Sigma_Cyber_Ghost
[red]YouTube:[/] https://www.youtube.com/@sigma_ghost_hacking
[magenta]Instagram:[/] https://www.instagram.com/safderkhan0800_
[blue]Twitter:[/] https://twitter.com/safderkhan0800_
[green]GitHub:[/] https://github.com/sigma-cyber-ghost
"""

def show_banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = Text(BANNER_ART, style="bold cyan")
    console.print(Panel(Align.center(banner_text), box=HEAVY, border_style="cyan"))
    console.print(Panel(Align.center("[bold red]SIGMA GHOST PROXY TOOL — BLACK HAT EDITION[/bold red]"), style="bright_white", box=ROUNDED))
    console.print(Panel(SOCIAL, box=ROUNDED, border_style="bright_black"))

def ensure_dirs():
    os.makedirs("proxy_results", exist_ok=True)
    os.makedirs("checked_proxies", exist_ok=True)

def test_raw_proxy(proxy, proto, timeout=6):
    ip, port = proxy.split(":")
    sock = socks.socksocket()
    if proto == "socks4":
        sock.set_proxy(socks.SOCKS4, ip, int(port))
    elif proto == "socks5":
        sock.set_proxy(socks.SOCKS5, ip, int(port))
    else:
        return test_http_proxy(proxy, proto, timeout)
    try:
        sock.settimeout(timeout)
        start = time.time()
        sock.connect(("ifconfig.me", 80))
        sock.send(b"GET /ip HTTP/1.1\r\nHost: ifconfig.me\r\n\r\n")
        resp = sock.recv(128)
        latency = int((time.time() - start) * 1000)
        return {"ip": ip, "port": port, "country": "??", "ms": str(latency), "status": "LIVE"}
    except:
        return {"status": "DEAD"}

def test_http_proxy(proxy, proto, timeout=6):
    try:
        ip, port = proxy.split(":")
        proxies = {"http": f"{proto}://{proxy}", "https": f"{proto}://{proxy}"}
        start = time.time()
        r = requests.get("http://ip-api.com/json", proxies=proxies, timeout=timeout)
        latency = int((time.time() - start) * 1000)
        if r.ok:
            j = r.json()
            return {"ip": ip, "port": port, "country": j.get("countryCode", "??"), "ms": str(latency), "status": "LIVE"}
    except:
        pass
    return {"status": "DEAD"}

def scan_proxies(path):
    if not os.path.exists(path):
        console.print(Panel(f"[red]✘ File not found: {path}[/red]", box=ROUNDED))
        return

    proxies = list(set([l.strip() for l in open(path, encoding="utf8", errors="ignore") if ":" in l]))
    table = Table(title="[bold cyan]Live Proxy Scan Feed[/bold cyan]", show_header=True, expand=True, box=HEAVY)
    for col in ["PROTO", "STATUS", "IP", "PORT", "COUNTRY", "TIME(ms)", "RATING"]:
        table.add_column(col, justify="center")

    console.print(Panel(f"[cyan]Scanning {len(proxies)} entries...[/cyan]", box=ROUNDED))
    live = []

    with Live(table, refresh_per_second=8):
        with concurrent.futures.ThreadPoolExecutor(max_workers=80) as pool:
            futures = []
            for proxy in proxies:
                for proto in ["http", "https", "socks4", "socks5"]:
                    futures.append(pool.submit(test_raw_proxy if proto.startswith("socks") else test_http_proxy, proxy, proto))

            for fut in concurrent.futures.as_completed(futures):
                res = fut.result()
                if res.get("status") == "LIVE":
                    row = [proto.upper(), "[green]LIVE[/green]", res["ip"], res["port"], res["country"], res["ms"], "High" if int(res["ms"]) < 200 else "Medium"]
                    table.add_row(*row)
                    live.append(f"{proto}://{res['ip']}:{res['port']}")
                else:
                    table.add_row(proto.upper(), "[red]DEAD[/red]", "-", "-", "-", "-", "-")

    ensure_dirs()
    byproto = defaultdict(list)
    for entry in live:
        proto, rest = entry.split("://", 1)
        byproto[proto].append(rest)
    for proto, lst in byproto.items():
        with open(f"checked_proxies/{proto}_proxies.txt", "w") as f:
            f.write("\n".join(lst))
    console.print(Panel(f"[bold green]✔ {len(live)} live proxies saved in checked_proxies/[/bold green]", box=ROUNDED))

def generate_proxies():
    ensure_dirs()
    sources = [f"https://www.proxy-list.download/api/v1/get?type={t}" for t in ["http", "https", "socks4", "socks5"]]
    allp = set()
    console.print(Panel("[magenta]Generating proxies...[/magenta]", border_style="magenta", box=ROUNDED))

    with Progress(SpinnerColumn(), BarColumn(), TimeElapsedColumn(), console=console, transient=True) as pr:
        pr.add_task("", total=None)
        for url in sources:
            try:
                resp = requests.get(url, timeout=10)
                if resp.ok:
                    allp.update(resp.text.splitlines())
            except:
                pass
            time.sleep(0.1)

    out = os.path.join("proxy_results", "generated_proxies.txt")
    with open(out, "w", encoding="utf8") as f:
        f.write("\n".join(sorted(allp)))
    console.print(Panel(f"[bold green]✔ Generated {len(allp)} proxies to {out}[/bold green]", box=ROUNDED))
    input("Press Enter to continue...")

def main():
    ensure_dirs()
    show_banner()
    while True:
        console.print("\n[1] Generate Proxies\n[2] Check Proxies (Live Feed)\n[3] Exit\n")
        choice = Prompt.ask("Choose option", choices=["1", "2", "3"], default="1")
        if choice == "1":
            generate_proxies()
        elif choice == "2":
            default = "proxy_results/generated_proxies.txt"
            path = Prompt.ask("Proxy file path", default=default).strip().strip("'\"")
            scan_proxies(path)
        else:
            console.print(Panel("[red]☠ Ghost logged out.[/red]", box=ROUNDED))
            break

if __name__ == "__main__":
    main()
