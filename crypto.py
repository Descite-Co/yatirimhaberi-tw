import requests

def get_crypto_price(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"{url} adresine yapılan istek başarısız oldu. Hata kodu:", response.status_code)
        return None

def format_price(price):
    return "{:,.2f}".format(float(price))

def format_market_cap(market_cap):
    if market_cap < 1_000_000:
        return f"${market_cap:,.0f}"
    elif market_cap < 1_000_000_000:
        return f"${market_cap / 1_000_000:.2f} Milyon"
    elif market_cap < 1_000_000_000_000:
        return f"${market_cap / 1_000_000_000:.2f} Milyar"
    else:
        return f"${market_cap / 1_000_000_000_000:.2f} Trilyon"

cryptos = {
    "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
    "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
    "BNB": ["https://cryptoprices.cc/BNB/", "https://cryptoprices.cc/BNB/MCAP/"],
    "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"],
    "XRP": ["https://cryptoprices.cc/XRP/", "https://cryptoprices.cc/XRP/MCAP/"]
}

print("🚀 Anlık Kripto Verileri 🚀")
for crypto, urls in cryptos.items():
    print(f"\n🌟 #{crypto} Fiyatı: ${format_price(get_crypto_price(urls[0]))}")
    print(f"💰 #{crypto} Piyasa Değeri: {format_market_cap(float(get_crypto_price(urls[1])))}")
