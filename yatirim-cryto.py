import http.client
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import random

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
    xu100 = yf.Ticker('XU100.IS')
    xu100_open = xu100.info.get('open', '')
    xu100_last_close = xu100.info.get('previousClose', '')
    xu100_change = (((xu100_open - xu100_last_close) / xu100_last_close) * 100)
    xu100_change = round(xu100_change, 2)
    emo = '📈' if xu100_change > 0 else '📉'
    text = 'yükseliş' if xu100_change > 0 else 'düşüş'
    subject = ("send_bist100_open")
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde güne %{xu100_change} {text} ile başladı.
{emo} Açılış Fiyatı: {xu100_open} \n
    """
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

def bist_by_time():
    stocks = ['ACSEL', 'ADEL', 'ADESE', 'AEFES', 'AFYON', 'AGYO', 'AKBNK', 'AKCNS', 'AKENR', 'AKFGY', 'AKGRT', 'AKMGY', 'AKSA', 'AKSEN', 'AKSGY', 'AKSUE', 'ALARK', 'ALBRK', 'ALCAR', 'ALCTL', 'ALGYO', 'ALKIM', 'ANELE', 'ANHYT', 'ANSGR', 'ARCLK', 'ARENA', 'ARSAN', 'ASELS', 'ASUZU', 'ATAGY', 'ATEKS', 'ATLAS', 'ATSYH', 'AVGYO', 'AVHOL', 'AVOD', 'AVTUR', 'AYCES', 'AYEN', 'AYES', 'AYGAZ', 'BAGFS', 'BAKAB', 'BALAT', 'BANVT', 'BASCM', 'BEYAZ', 'BFREN', 'BIMAS', 'BIZIM', 'BJKAS', 'BLCYT', 'BNTAS', 'BOSSA', 'BRISA', 'BRKSN', 'BRMEN', 'BRSAN', 'BRYAT', 'BSOKE', 'BTCIM', 'BUCIM', 'BURCE', 'BURVA', 'CCOLA', 'CELHA', 'CEMAS', 'CEMTS', 'CIMSA', 'CLEBI', 'CMBTN', 'CMENT', 'COSMO', 'CRDFA', 'CRFSA', 'CUSAN', 'DAGHL', 'DAGI', 'DARDL', 'DENGE', 'DERIM', 'DEVA', 'DGATE', 'DGGYO', 'DIRIT', 'DITAS', 'DMSAS', 'DOAS', 'DOBUR', 'DOCO', 'DOGUB', 'DOHOL', 'DURDO', 'DYOBY', 'DZGYO', 'ECILC', 'ECZYT', 'EDIP', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EKGYO', 'EKIZ', 'EMKEL', 'EMNIS', 'ENKAI', 'EPLAS', 'ERBOS', 'EREGL', 'ERSU', 'ESCOM', 'ETILR', 'ETYAT', 'EUHOL', 'EUKYO', 'EUYO', 'FENER', 'FLAP', 'FMIZP', 'FRIGO', 'FROTO', 'GARAN', 'GARFA', 'GEDIK', 'GEDZA', 'GENTS', 'GEREL', 'GLBMD', 'GLRYH', 'GLYHO', 'GOLTS', 'GOODY', 'GOZDE', 'GRNYO', 'GSDDE', 'GSDHO', 'GSRAY', 'GUBRF', 'HALKB', 'HATEK', 'HDFGS', 'HEKTS', 'HLGYO', 'HURGZ', 'ICBCT', 'IDGYO', 'IEYHO', 'IHEVA', 'IHGZT', 'IHLAS', 'IHYAY', 'INDES', 'INFO', 'INTEM', 'IPEKE', 'ISBIR', 'ISBTR', 'ISCTR', 'ISDMR', 'ISFIN', 'ISGSY', 'ISGYO', 'ISMEN', 'ISYAT', 'IZFAS', 'IZMDC', 'JANTS', 'KAPLM', 'KAREL', 'KARSN', 'KARTN', 'KATMR', 'KCHOL', 'KENT', 'KERVN', 'KERVT', 'KLGYO', 'KLMSN', 'KLNMA', 'KNFRT', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMA', 'KRDMB', 'KRDMD', 'KRGYO', 'KRONT', 'KRSTL', 'KRTEK', 'KSTUR', 'KUTPO', 'KUYAS', 'LIDFA', 'LINK', 'LKMNH', 'LOGO', 'LUKSK', 'MAALT', 'MAKTK', 'MARTI', 'MEGAP', 'MEPET', 'MERIT', 'MERKO', 'METAL', 'METRO', 'METUR', 'MGROS', 'MIPAZ', 'MMCAS', 'MNDRS', 'MRGYO', 'MRSHL', 'MZHLD', 'NETAS', 'NIBAS', 'NTHOL', 'NUGYO', 'NUHCM', 'ODAS', 'ORGE', 'ORMA', 'OSMEN', 'OSTIM', 'OTKAR', 'OYAYO', 'OYLUM', 'OZGYO', 'OZKGY', 'OZRDN', 'PAGYO', 'PARSN', 'PEGYO', 'PENGD', 'PETKM', 'PETUN', 'PGSUS', 'PINSU', 'PKART', 'PKENT', 'PNSUT', 'POLHO', 'POLTK', 'PRKAB', 'PRKME', 'PRZMA', 'PSDTC', 'RAYSG', 'RODRG', 'RTALB', 'RYGYO', 'RYSAS', 'SAHOL', 'SAMAT', 'SANEL', 'SANFM', 'SARKY', 'SASA', 'SAYAS', 'SEKFK', 'SEKUR', 'SELEC', 'SELGD', 'SEYKM', 'SILVR', 'SISE', 'SKBNK', 'SKTAS', 'SNGYO', 'SNKRN', 'SNPAM', 'SODSN', 'SONME', 'SRVGY', 'TATGD', 'TAVHL', 'TBORG', 'TCELL', 'TEKTU', 'TGSAS', 'THYAO', 'TKFEN', 'TKNSA', 'TMPOL', 'TMSN', 'TOASO', 'TRCAS', 'TRGYO', 'TSKB', 'TSPOR', 'TTKOM', 'TTRAK', 'TUCLK', 'TUKAS', 'TUPRS', 'TURGG', 'ULAS', 'ULKER', 'ULUSE', 'ULUUN', 'UMPAS', 'USAK', 'USAS', 'UZERB', 'VAKBN', 'VAKFN', 'VAKKO', 'VANGD', 'VERTU', 'VERUS', 'VESBE', 'VESTL', 'VKFYO', 'VKGYO', 'VKING', 'YAPRK', 'YATAS', 'YAYLA', 'YBTAS', 'YESIL', 'YGGYO', 'YGYO', 'YKBNK', 'YONGA', 'YUNSA', 'YYAPI', 'ZOREN']
    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + '.IS'
    chosen_stock_info = yf.Ticker(stock_code)
    today = chosen_stock_info.info.get('currentPrice', '')
    month_1_close = chosen_stock_info.history(period='max').iloc[-30]['Open']
    month_1_change_percent = (((today - month_1_close) / today) * 100).round(1)
    day_5_close = chosen_stock_info.history(period='max').iloc[-5]['Open']
    day_5_change_percent = (((today - day_5_close) / today) * 100).round(1)
    month_3_close = chosen_stock_info.history(period='max').iloc[-180]['Open']
    month_3_change_percent = (((today - month_3_close) / today) * 100).round(1)
    
    body = f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇
          
⬛ Güncel Fiyat: {today}
⬛ 5 Günlük Fiyat Değişimi: %{day_5_change_percent}
⬛ 1 Aylık Fiyat Değişimi: %{month_1_change_percent}
⬛ 6 Aylık Fiyat Değişimi: %{month_3_change_percent}

#yatırım #borsa #hisse #hisseanaliz #bist #bist100 #bist30 #borsaistanbul
          """
    subject = ("bist_by_time")
    
    send_email(subject, body)

# İlk çalıştırma
#get_gold_price_and_send_email()
#send_bist_open()
#print_crypto_data(cryptos)
bist_by_time()

# Haftaiçi saat 13:00'da kontrol ve e-posta gönderme
while True:
    # Şu anki zamanı al
    now = datetime.now()

    if now.weekday() < 5 and now.hour == 10 and now.minute == 16:
        send_bist_open()
        time.sleep(120)
    
    if now.weekday() < 5 and now.hour == 11 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
    
    # Haftaiçi ise ve saat 13:00 olduğunda çalıştır
    if now.weekday() < 5 and now.hour == 13 and now.minute == 0:
        get_gold_price_and_send_email()
        # iki dakika sonra tekrar kontrol etmek için bekleyin
        time.sleep(120)
    
    if now.weekday() < 5 and now.hour == 14 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
    
    if now.weekday() < 5 and now.hour == 17 and now.minute == 00:
        bist_by_time()
        time.sleep(120)

    else:
        # 1 saniye bekleyin ve tekrar kontrol edin
        time.sleep(1)
