import http.client
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import requests
from bs4 import BeautifulSoup

# SMTP ayarlarını buraya al
email = 'omerddduran@gmail.com'
password = 'qbfl udxd kjya tpiv'

cryptos = {
    "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
    "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
    "BNB": ["https://cryptoprices.cc/BNB/", "https://cryptoprices.cc/BNB/MCAP/"],
    "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"],
    "XRP": ["https://cryptoprices.cc/XRP/", "https://cryptoprices.cc/XRP/MCAP/"]
}

def send_email(subject, body):
    # E-posta gönderme işlemi
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = 'trigger@applet.ifttt.com'
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server.send_message(msg)
    server.quit()

def get_gold_price_and_send_email():
    # Altın verilerini alma işlemi
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 1XxDAz4EtnKZ099rPKM8Jj:2se49tU9ttxzlhy1KGI5sW"
    }
    conn.request("GET", "/economy/goldPrice", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)

    # Bugünün tarihini al ve gün ve ayı ayrı değişkenlere at
    today_date = datetime.now()
    day = today_date.strftime("%d")
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık"
    }[month]

    # E-posta oluşturma işlemi
    subject = f"🔴 Altın Fiyatları {day} {turkish_month}"
    body = "🔴 Altın Fiyatları:\n\n"
    for item in parsed_data["result"]:
        if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
            body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

    send_email(subject, body)

def send_bist_open():
    today_date = datetime.now()
    day = today_date.strftime("%d")
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak",
        "February": "Şubat",
        "March": "Mart",
        "April": "Nisan",
        "May": "Mayıs",
        "June": "Haziran",
        "July": "Temmuz",
        "August": "Ağustos",
        "September": "Eylül",
        "October": "Ekim",
        "November": "Kasım",
        "December": "Aralık"
    }[month]
    target_bist = "https://www.google.com/finance/quote/XU100:INDEXIST?hl=tr"
    page = requests.get(target_bist)
    soup = BeautifulSoup(page.content, "html.parser")
    item_bist = soup.find("div", class_="YMlKec fxKbKc").text
    percent_bist = soup.find("div", class_="JwB6zf").text   
    subject = (f"{day} {turkish_month} BIST100 Açılış Verileri 👇")
    body = f"""🔴 {day} {turkish_month} BIST100 Açılış Verileri 👇 \n
            Fiyat: {item_bist} \n
            Yüzde: {percent_bist} \n"""
    send_email(subject, body)

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

def print_crypto_data(cryptos):
    print("🚀 Anlık Kripto Verileri 🚀")
    for crypto, urls in cryptos.items():
        price = get_crypto_price(urls[0])
        market_cap = get_crypto_price(urls[1])
        if price is not None and market_cap is not None:
            print(f"\n🌟 #{crypto} Fiyatı: ${format_price(price)}")
            print(f"💰 #{crypto} Piyasa Değeri: {format_market_cap(float(market_cap))}")
        else:
            print(f"\n🚫 {crypto} verileri alınamadı.")

# İlk çalıştırma
get_gold_price_and_send_email()
send_bist_open()
print_crypto_data(cryptos)

# Haftaiçi saat 13:00'da kontrol ve e-posta gönderme
while True:
    # Şu anki zamanı al
    now = datetime.now()
    # Haftaiçi ise ve saat 13:00 olduğunda çalıştır
    if now.weekday() < 5 and now.hour == 13 and now.minute == 0:
        get_gold_price_and_send_email()
        # iki dakika sonra tekrar kontrol etmek için bekleyin
        time.sleep(120)

    if now.weekday() < 5 and now.hour == 10 and now.minute == 16:
        send_bist_open()
        time.sleep(60)

    else:
        # 1 saniye bekleyin ve tekrar kontrol edin
        time.sleep(1)
