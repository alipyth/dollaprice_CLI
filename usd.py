import requests
from bs4 import BeautifulSoup

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

def fetch_price(cur):
    url = supported[cur]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    price_div = soup.select_one(
        'body > main > section.container.mostPopularRate > div > div > div:nth-child(1) > div > div > div > div'
    )
    price_text = price_div.get_text(strip=True) if price_div else "Price not found"
    
    # Remove everything after "٪" to keep only the price
    if "٪" in price_text:
        price_text = price_text.split("٪")[0]
    
    return price_text

# Main loop
while True:
    cur = input("Enter currency (help, all, exit): ").lower().strip()
    if cur == 'exit':
        print("Bye!")
        break
    if cur == 'help':
        print("Supported currencies:")
        for c in supported:
            print(f" - {c}")
        print(" - all (show all prices)\n")
        continue
    if cur == 'all':
        print("Fetching all prices...\n")
        for c in supported:
            try:
                price = fetch_price(c)
                print(f"{c.upper()} price: {price}")
            except Exception as e:
                print(f"{c.upper()} price: Error ({e})")
        print()
        continue
    if cur not in supported:
        print(f"Currency '{cur}' not supported. Type 'help' to see available currencies.\n")
        continue

    # Single currency
    price = fetch_price(cur)
    print(f"{cur.upper()} price: {price}\n")
