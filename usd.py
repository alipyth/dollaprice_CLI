import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box
from datetime import datetime

console = Console()

# Supported currencies
supported = {
    'usd': 'https://alanchand.com/currencies-price/usd',
    'eur': 'https://alanchand.com/currencies-price/eur',
    'aed': 'https://alanchand.com/currencies-price/aed',
    'try': 'https://alanchand.com/currencies-price/try',
    'gbp': 'https://alanchand.com/currencies-price/gbp',
    'cny': 'https://alanchand.com/currencies-price/cny',
    'iqd': 'https://alanchand.com/currencies-price/iqd',
    'aud': 'https://alanchand.com/currencies-price/aud',
}

# ✅ Session (Proxy-safe)
SESSION = requests.Session()
SESSION.trust_env = False  # ✅ ignore system/env proxies


def fetch_price(cur: str, timeout=15) -> str:
    url = supported[cur]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://alanchand.com/',
        'Connection': 'close',
    }

    # ✅ force no-proxy (extra safety)
    resp = SESSION.get(
        url,
        headers=headers,
        timeout=timeout,
        proxies={"http": None, "https": None}
    )
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Your original selector
    price_div = soup.select_one(
        'body > main > section.container.mostPopularRate > div > div > div:nth-child(1) > div > div > div > div'
    )
    price_text = price_div.get_text(strip=True) if price_div else ""

    if not price_text:
        return "Price not found"

    # Remove everything after "٪"
    if "٪" in price_text:
        price_text = price_text.split("٪")[0].strip()

    return price_text


def header():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = Text(" Currency Price Fetcher ", style="bold black on cyan")
    subtitle = Text(f"Updated: {now}", style="dim")
    console.print(Panel.fit(Text.assemble(title, "\n", subtitle), border_style="cyan"))


def show_help():
    t = Table(title="Commands", box=box.SIMPLE_HEAVY)
    t.add_column("Command", style="bold cyan")
    t.add_column("Description", style="white")
    t.add_row("help", "Show this help")
    t.add_row("all", "Fetch all supported currencies")
    t.add_row("usd / eur / ...", "Fetch a single currency")
    t.add_row("exit", "Quit")
    console.print(t)
    console.print()


def show_all():
    table = Table(title="Live Prices", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Currency", style="bold cyan", no_wrap=True)
    table.add_column("Price", style="bold green")
    table.add_column("Status", style="yellow")

    with console.status("[bold blue]Fetching prices...[/bold blue]"):
        for c in supported:
            try:
                price = fetch_price(c)
                table.add_row(c.upper(), price, "OK")
            except Exception as e:
                table.add_row(c.upper(), "-", f"Error: {type(e).__name__}")

    console.print(table)
    console.print()


def show_one(cur: str):
    with console.status(f"[bold blue]Fetching {cur.upper()}...[/bold blue]"):
        price = fetch_price(cur)

    console.print(
        Panel(
            f"[bold cyan]{cur.upper()}[/bold cyan] price is:\n\n[bold green]{price}[/bold green]",
            title="Result",
            border_style="green",
        )
    )
    console.print()


def main():
    console.clear()
    header()

    # ✅ Default show USD on start
    try:
        show_one("usd")
    except Exception as e:
        console.print(Panel(f"[red]Error loading USD:[/red] {e}", border_style="red"))
        console.print()

    console.print("[dim]Type [bold cyan]help[/bold cyan] to see commands.[/dim]\n")

    while True:
        cur = Prompt.ask("[bold cyan]Enter currency[/bold cyan] (help/all/exit)").lower().strip()

        if cur == "exit":
            console.print("\n[bold green]Bye![/bold green]")
            break

        if cur == "help":
            show_help()
            continue

        if cur == "all":
            show_all()
            continue

        if cur not in supported:
            console.print(f"[bold red]Currency '{cur}' not supported.[/bold red] Type [bold cyan]help[/bold cyan].\n")
            continue

        try:
            show_one(cur)
        except Exception as e:
            console.print(Panel(f"[red]Error:[/red] {e}", title="Failed", border_style="red"))
            console.print()


if __name__ == "__main__":
    main()
