from email.mime.image import MIMEImage
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
import matplotlib.pyplot as plt
import pytz
from io import BytesIO
from keep_alive import keep_alive

# SMTP ayarlarını buraya al
email = 'omerddduran@gmail.com'
password = 'qbfl udxd kjya tpiv'

# Fiyat ve hacim değerlerini düzenleyen fonksiyon
def duzenle(deger, para):
    if deger != 0 and isinstance(deger, int):
        return "{:,.0f} {}".format(deger, para).replace(",", ".")
    elif deger != 0 and isinstance(deger, float):
        return "{:,.2f} {}".format(deger, para).replace(",", ".")
    else:
        return ''

def random_stock():
    # Hisse listesi
    hisse_listesi = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK.A', 'BRK.B', 'JPM', 'JNJ', 'V', 'PG', 'NVDA', 'MA', 'HD', 'DIS', 'UNH', 'PYPL', 'BAC', 'CMCSA', 'XOM', 'INTC', 'ADBE', 'NFLX', 'T', 'CRM', 'ABT', 'CSCO', 'VZ', 'KO', 'MRK', 'PFE', 'PEP', 'WMT', 'CVX', 'MCD', 'TMO', 'WFC', 'ABBV', 'ORCL', 'AMGN', 'NKE', 'ACN', 'IBM', 'QCOM', 'TXN', 'COST', 'LLY', 'HON', 'MDT', 'AVGO', 'DHR', 'NEE', 'UPS', 'LIN', 'SBUX', 'LOW', 'UNP', 'BA', 'MO', 'MMM', 'RTX', 'GS', 'BDX', 'CAT', 'ADP', 'LMT', 'CVS', 'CI', 'DE', 'ANTM', 'SO', 'BMY', 'USB', 'AXP', 'GILD', 'MS', 'ISRG', 'CHTR', 'RTX', 'PLD', 'AEP', 'TGT', 'D', 'DUK', 'BKNG', 'SPGI', 'VRTX', 'ZTS', 'CME', 'COF', 'CSX', 'CCI', 'REGN', 'CL']

    # Rastgeele bir hisse seçme
    secilen_hisse = random.choice(hisse_listesi)
    hisse = yf.Ticker(secilen_hisse)
    hisse_bilgileri = hisse.info
    currency = hisse_bilgileri["financialCurrency"] 
    
    email_body = f"📈#{secilen_hisse} {hisse_bilgileri['shortName']} hisse senedinin güncel ve uzun dönemli performansı 👇\n\n"
    email_body += f"Önceki Kapanış: {duzenle(hisse_bilgileri.get('previousClose', 0), currency)}\n"
    email_body += f"Açılış Fiyatı: {duzenle(hisse_bilgileri.get('open', 0), currency)}\n"
    email_body += f"Günlük En Düşük Değer: {duzenle(hisse_bilgileri.get('dayLow', 0), currency)}\n"
    email_body += f"Günlük En Yüksek Değer: {duzenle(hisse_bilgileri.get('dayHigh', 0), currency)}\n"
    anlik_fiyat = hisse_bilgileri.get('regularMarketPrice', (hisse_bilgileri.get('open', 0) + hisse_bilgileri.get('dayHigh', 0)) / 2)
    email_body += f"Anlık Fiyat: {duzenle(anlik_fiyat if anlik_fiyat != 0 else '', currency)}\n"
    email_body += f"52 Haftalık En Düşük Değer: {duzenle(hisse_bilgileri.get('fiftyTwoWeekLow', 0), currency)}\n"
    email_body += f"52 Haftalık En Yüksek Değer: {duzenle(hisse_bilgileri.get('fiftyTwoWeekHigh', 0), currency)}\n"
    email_body += f"Günlük İşlem Hacmi: {duzenle(hisse_bilgileri.get('volume', 'hisse'), currency)}\n"
    email_body += f"Ortalama Günlük İşlem Hacmi (Son 10 Gün): {duzenle(hisse_bilgileri.get('averageDailyVolume10Day', 'hisse'), currency)}\n"
    son_ceyrek_buyume_orani = hisse_bilgileri.get('quarterlyEarningsGrowth', '')
    if son_ceyrek_buyume_orani != '':
        email_body += f"Son Çeyrek Dönem Büyüme Oranı: %{son_ceyrek_buyume_orani:.1f}\n"
    email_body += f"Net Gelir: {duzenle(hisse_bilgileri.get('netIncomeToCommon', 0), currency)}\n"
    email_body += f"Brüt Kar Marjı: %{hisse_bilgileri.get('grossMargins', 0) * 100:.3f}\n"
    email_body += f"Piyasa Değeri: {duzenle(hisse_bilgileri.get('marketCap', 0), currency)}\n"

    # E-posta gönder
    subject = f"{hisse_bilgileri['shortName']} Hissesi Performans Raporu"
    send_email(subject, email_body)
    
def get_data_sil(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_data_cur(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

cryptos = {
    "BTC": ["https://cryptoprices.cc/BTC/", "https://cryptoprices.cc/BTC/MCAP/"],
    "ETH": ["https://cryptoprices.cc/ETH/", "https://cryptoprices.cc/ETH/MCAP/"],
    "BNB": ["https://cryptoprices.cc/BNB/", "https://cryptoprices.cc/BNB/MCAP/"],
    "SOL": ["https://cryptoprices.cc/SOL/", "https://cryptoprices.cc/SOL/MCAP/"],
    "XRP": ["https://cryptoprices.cc/XRP/", "https://cryptoprices.cc/XRP/MCAP/"]
}

def currency_send():
    # Döviz kurlarını al
    json_data = get_data_cur('https://api.genelpara.com/embed/para-birimleri.json')

    # E-posta için içerik oluştur
    if json_data:
        email_body = "🌍 Döviz Kurları 🌍\n\n"
        for currency in ['USD', 'EUR', 'GBP']:
            data = json_data.get(currency)
            if data:
                email_body += f'#{currency}:\nFiyat: {data["satis"]}\nDeğişim: {data["degisim"]}%\n\n'
            else:
                email_body += f'{currency} verisi bulunamadı.\n\n'

        # E-posta gönder
        send_email("Güncel Döviz Kurları", email_body)
    else:
        print("Döviz kurları alınamadı.")


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
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
    
    gold = yf.Ticker('GC=F')
    hist_data = gold.history(period='max')
    
    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data['Close'])
    plt.title('Ons Altın Grafiği')
    plt.xlabel('Tarih')
    plt.ylabel('Fiyat')
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
            
            
    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # E-posta oluşturma işlemi
    subject = f"🔴 Altın Fiyatları {day} {turkish_month}"
    body = "🔴 Altın Fiyatları:\n\n"
    for item in parsed_data["result"]:
        if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
            body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

    send_email(subject, body)
    #print(body)

def send_bist_open():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
    #print(body)
    
def send_bist_close():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
    xu100_data = xu100.history(period='max')
    xu100_current = xu100_data['Close'][-1]
    xu100_prev = xu100_data['Close'][-2]
    xu100_current_change = (((xu100_current - xu100_prev) / xu100_prev) * 100)
    xu100_current_change = round(xu100_current_change, 2)
    emo = '📈' if xu100_current_change > 0 else '📉'
    text = 'yükseliş' if xu100_current_change > 0 else 'düşüş'
    subject = ("send_bist100_open")
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde günü %{xu100_current_change} {text} ile kapattı.
    
{emo} Kapanış Fiyatı: {xu100_current} \n
    """
    
    send_email(subject, body)
    #print(body)

def get_crypto_price(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"{url} adresine yapılan istek başarısız oldu. Hata kodu:", response.status_code)
        return None

def format_price(price):
    return "{:,.2f}".format(float(price))

def silver():
    # Gümüş verilerini al
    json_data = get_data_sil('https://api.genelpara.com/embed/para-birimleri.json')

    # E-posta için içerik oluştur
    if json_data:
        data = json_data.get('GAG')
        if data:
            email_body = "🔴 #Gümüş:\n"
            email_body += f'Fiyat: ₺{data["satis"]}\nDeğişim: {data["degisim"]}%\n'
            
            
            silver = yf.Ticker('SI=F')
            hist_data = silver.history(period='max')
            
            # Plot historical prices
            plt.figure(figsize=(12, 6))
            plt.plot(hist_data['Close'])
            plt.title('Gümüş Grafiği')
            plt.xlabel('Tarih')
            plt.ylabel('Fiyat')
            plt.grid(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            
            # Save the plot as a BytesIO object
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
            image_stream.seek(0)
            

            # E-posta gönder
            send_email("Güncel Gümüş Fiyatları", email_body)
            #print(email_body)
            
        else:
            print('Gümüş verisi bulunamadı.')
    else:
        print("Veri alınamadı.")

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
    body = "🚀 Anlık Kripto Verileri 🚀\n"
    for crypto, urls in cryptos.items():
        price = get_crypto_price(urls[0])
        market_cap = get_crypto_price(urls[1])
        if price is not None and market_cap is not None:
            body += f"\n🌟 #{crypto} Fiyatı: ${format_price(price)}\n"
            body += f"💰 #{crypto} Piyasa Değeri: {format_market_cap(float(market_cap))}\n"
        else:
            print(f"\n🚫 {crypto} verileri alınamadı.")
    send_email("Anlık Kripto Verileri", body)
    #print(body)

def bist_by_time():
    stocks = ['ACSEL', 'ADEL', 'ADESE', 'AEFES', 'AFYON', 'AGYO', 'AKBNK', 'AKCNS', 'AKENR', 'AKFGY', 'AKGRT', 'AKMGY', 'AKSA', 'AKSEN', 'AKSGY', 'AKSUE', 'ALARK', 'ALBRK', 'ALCAR', 'ALCTL', 'ALGYO', 'ALKIM', 'ANELE', 'ANHYT', 'ANSGR', 'ARCLK', 'ARENA', 'ARSAN', 'ASELS', 'ASUZU', 'ATAGY', 'ATEKS', 'ATLAS', 'ATSYH', 'AVGYO', 'AVHOL', 'AVOD', 'AVTUR', 'AYCES', 'AYEN', 'AYES', 'AYGAZ', 'BAGFS', 'BAKAB', 'BALAT', 'BANVT', 'BASCM', 'BEYAZ', 'BFREN', 'BIMAS', 'BIZIM', 'BJKAS', 'BLCYT', 'BNTAS', 'BOSSA', 'BRISA', 'BRKSN', 'BRMEN', 'BRSAN', 'BRYAT', 'BSOKE', 'BTCIM', 'BUCIM', 'BURCE', 'BURVA', 'CCOLA', 'CELHA', 'CEMAS', 'CEMTS', 'CIMSA', 'CLEBI', 'CMBTN', 'CMENT', 'COSMO', 'CRDFA', 'CRFSA', 'CUSAN', 'DAGHL', 'DAGI', 'DARDL', 'DENGE', 'DERIM', 'DEVA', 'DGATE', 'DGGYO', 'DIRIT', 'DITAS', 'DMSAS', 'DOAS', 'DOBUR', 'DOCO', 'DOGUB', 'DOHOL', 'DURDO', 'DYOBY', 'DZGYO', 'ECILC', 'ECZYT', 'EDIP', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EKGYO', 'EKIZ', 'EMKEL', 'EMNIS', 'ENKAI', 'EPLAS', 'ERBOS', 'EREGL', 'ERSU', 'ESCOM', 'ETILR', 'ETYAT', 'EUHOL', 'EUKYO', 'EUYO', 'FENER', 'FLAP', 'FMIZP', 'FRIGO', 'FROTO', 'GARAN', 'GARFA', 'GEDIK', 'GEDZA', 'GENTS', 'GEREL', 'GLBMD', 'GLRYH', 'GLYHO', 'GOLTS', 'GOODY', 'GOZDE', 'GRNYO', 'GSDDE', 'GSDHO', 'GSRAY', 'GUBRF', 'HALKB', 'HATEK', 'HDFGS', 'HEKTS', 'HLGYO', 'HURGZ', 'ICBCT', 'IDGYO', 'IEYHO', 'IHEVA', 'IHGZT', 'IHLAS', 'IHYAY', 'INDES', 'INFO', 'INTEM', 'IPEKE', 'ISBIR', 'ISBTR', 'ISCTR', 'ISDMR', 'ISFIN', 'ISGSY', 'ISGYO', 'ISMEN', 'ISYAT', 'IZFAS', 'IZMDC', 'JANTS', 'KAPLM', 'KAREL', 'KARSN', 'KARTN', 'KATMR', 'KCHOL', 'KENT', 'KERVN', 'KERVT', 'KLGYO', 'KLMSN', 'KLNMA', 'KNFRT', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMA', 'KRDMB', 'KRDMD', 'KRGYO', 'KRONT', 'KRSTL', 'KRTEK', 'KSTUR', 'KUTPO', 'KUYAS', 'LIDFA', 'LINK', 'LKMNH', 'LOGO', 'LUKSK', 'MAALT', 'MAKTK', 'MARTI', 'MEGAP', 'MEPET', 'MERIT', 'MERKO', 'METAL', 'METRO', 'METUR', 'MGROS', 'MIPAZ', 'MMCAS', 'MNDRS', 'MRGYO', 'MRSHL', 'MZHLD', 'NETAS', 'NIBAS', 'NTHOL', 'NUGYO', 'NUHCM', 'ODAS', 'ORGE', 'ORMA', 'OSMEN', 'OSTIM', 'OTKAR', 'OYAYO', 'OYLUM', 'OZGYO', 'OZKGY', 'OZRDN', 'PAGYO', 'PARSN', 'PEGYO', 'PENGD', 'PETKM', 'PETUN', 'PGSUS', 'PINSU', 'PKART', 'PKENT', 'PNSUT', 'POLHO', 'POLTK', 'PRKAB', 'PRKME', 'PRZMA', 'PSDTC', 'RAYSG', 'RODRG', 'RTALB', 'RYGYO', 'RYSAS', 'SAHOL', 'SAMAT', 'SANEL', 'SANFM', 'SARKY', 'SASA', 'SAYAS', 'SEKFK', 'SEKUR', 'SELEC', 'SELGD', 'SEYKM', 'SILVR', 'SISE', 'SKBNK', 'SKTAS', 'SNGYO', 'SNKRN', 'SNPAM', 'SODSN', 'SONME', 'SRVGY', 'TATGD', 'TAVHL', 'TBORG', 'TCELL', 'TEKTU', 'TGSAS', 'THYAO', 'TKFEN', 'TKNSA', 'TMPOL', 'TMSN', 'TOASO', 'TRCAS', 'TRGYO', 'TSKB', 'TSPOR', 'TTKOM', 'TTRAK', 'TUCLK', 'TUKAS', 'TUPRS', 'TURGG', 'ULAS', 'ULKER', 'ULUSE', 'ULUUN', 'UMPAS', 'USAK', 'USAS', 'UZERB', 'VAKBN', 'VAKFN', 'VAKKO', 'VANGD', 'VERTU', 'VERUS', 'VESBE', 'VESTL', 'VKFYO', 'VKGYO', 'VKING', 'YAPRK', 'YATAS', 'YAYLA', 'YBTAS', 'YESIL', 'YGGYO', 'YGYO', 'YKBNK', 'YONGA', 'YUNSA', 'YYAPI', 'ZOREN']
    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + '.IS'
    chosen_stock_info = yf.Ticker(stock_code)
    
    # Retrieve historical data
    hist_data = chosen_stock_info.history(period='max')

    # Get the latest price
    today = chosen_stock_info.info.get('currentPrice', '0')

    # Calculate percentage changes
    month_1_close = hist_data['Close'].iloc[-31]
    month_1_change_percent = (((today - month_1_close) / month_1_close) * 100).round(1)
    
    day_5_close = hist_data['Close'].iloc[-6]
    day_5_change_percent = (((today - day_5_close) / day_5_close) * 100).round(1)
    
    month_6_close = hist_data['Close'].iloc[-181]
    month_6_change_percent = (((today - month_6_close) / month_6_close) * 100).round(1)
    
    month_1_date = hist_data.index[-31].strftime('%d/%m/%Y')
    day_5_date = hist_data.index[-6].strftime('%d/%m/%Y')
    month_6_date = hist_data.index[-181].strftime('%d/%m/%Y')
    
    determine = lambda x: 'arttı' if x > 0 else 'azaldı'
    
    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data['Close'])
    plt.title(f'{chosen_stock} Hisse Senedi Grafiği')
    plt.xlabel('Tarih')
    plt.ylabel('Fiyat')
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # Construct the message
    body = f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇

⬛ Güncel Fiyat: {today}
⬛ {day_5_date} tarihinden beri %{day_5_change_percent} {determine(day_5_change_percent)}
⬛ {month_1_date} tarihinden beri %{month_1_change_percent} {determine(month_1_change_percent)}
⬛ {month_6_date} tarihinden beri %{month_6_change_percent} {determine(month_6_change_percent)}

#yatırım #borsa #hisse #hisseanaliz #bist #bist100 #bist30 #borsaistanbul
          """
    subject = ("bist_by_time")

    send_email(subject, body)
    
def bist30_change():
    stocks = ['ADEL', 'AFYON', 'AKBNK', 'AKSA', 'AKSEN', 'ALARK', 'ALBRK', 'ALCTL', 'ANELE', 'ARCLK', 'ASELS', 'AYGAZ', 'BIMAS', 'BRSAN', 'CCOLA', 'CEYLN', 'CRDFA', 'DEVA', 'DGKLB', 'DOAS', 'ECILC', 'EGEEN', 'ENJSA', 'ENKAI', 'ESCOM', 'FROTO', 'GOLTS', 'GOODY', 'ICBCT', 'IEYHO', 'KCHOL', 'KLMSN', 'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS', 'SASA', 'SISE', 'SKTAS', 'SODA', 'TAVHL', 'THYAO', 'TOASO', 'TTRAK', 'ULKER', 'VESTL', 'YATAS']
    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + ".IS"
    
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day
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
    hisse = yf.Ticker(stock_code)
    hisse_data = hisse.history(period='max')
    hisse_current = hisse.info.get('currentPrice', '0')
    hisse_prev = hisse.info.get('previousClose', '0')
    hisse_current_change = (((hisse_current - hisse_prev) / hisse_prev) * 100)
    hisse_current_change = round(hisse_current_change, 2)
    emo = '📈' if hisse_current_change > 0 else '📉'
    text = 'yükseldi' if hisse_current_change > 0 else 'düştü'
    subject = ("send_bist30_stock")
    body = f"""🔴 #{chosen_stock} bugün %{hisse_current_change} {text}
    
{emo} Anlık Fiyatı: {hisse_current} \n
    """
    
    #print(body)
    send_email(subject, body)

def halka_arz ():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day # BUNU HER DAY KULLANILAN YERDE KULLANALIM
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
    stocks = ['ENTRA', 'ODINE', 'MOGAN', 'ARTMS', 'ALVES', "LMKDC"]
    change_rates = []
    stock_prices = []
    subject = ("halka_arz_tablosu")
    body = f"""🔴 {day} {turkish_month} Halka Arz Tablosu \n
"""
    for stock in stocks[::-1]:
        stock_code = stock + '.IS'
        hisse = yf.Ticker(stock_code)
        hisse_data = hisse.history(period='max')
        hisse_current = hisse_data['Close'][-1]
        hisse_prev = hisse_data['Close'][-2]
        hisse_current_change = (((hisse_current - hisse_prev) / hisse_prev) * 100)
        hisse_current_change = round(hisse_current_change, 2)
        change_rates.append(hisse_current_change)
        stock_prices.append(hisse_current)
        emo = '📈' if hisse_current_change > 0 else '📉'
        text = 'yükseldi' if hisse_current_change > 0 else 'düştü'
        tavan_check = " - Hisse Tavanda" if hisse_current_change > 9.5 else ""
        message = f"{emo} #{stock} bugün %{hisse_current_change} {text}"
        body += f"{message + tavan_check}\n"
    
    #print(body)
    send_email(subject, body)

def sektor_hisse_bilgi(sektor):
    stocks = {
    "Enerji": ["TCELL", "TUPRS", "TSPOR", "HALKB", "GARAN"],
    "Banka": ["TRCAS", "BIMAS", "TKFEN", "SASA", "SISE"]
    }
    subject = ("sektor_hisse_bilgi")
    body = f"""🔴 {sektor} Hisselerinin 5 Günlük Performansları 👇 
    \n"""
    for stock in stocks[sektor]:
        stock_code = stock + ".IS"
        stock_info = yf.Ticker(stock_code)
        stock_data = stock_info.history(period='max')
        current = stock_info.info.get('currentPrice', '0')
        day_5_close = stock_data['Close'].iloc[-6]
        day_5_change_percent = (((current - day_5_close) / day_5_close) * 100).round(1)
        emo = '📈' if day_5_change_percent > 0 else '📉' 
        body += f"{emo} #{stock} {stock_info.info.get('longName', '')} %{day_5_change_percent}\n"

    #print(body)
    send_email(subject, body)

def sektor_endeks_bilgi():
    endeksler = {
    "Banka": "XBANK"
    }
    subject = ("sektor_hisse_bilgi")
    body = f"""🔴 Borsa İstanbul Endekslerinin 5 Günlük Performansları 👇 
    \n"""
    for k in endeksler:
        stock_code = endeksler[k] + ".IS"
        endeks = yf.Ticker(stock_code)
        endeks_data = endeks.history(period='max')
        current = endeks_data['Close'][-1]
        day5 = endeks_data['Close'][-5]
        change = (((current - day5) / day5) * 100)
        change = round(change, 2)
        text = 'Yükseldi' if change > 0 else 'Düştü'
        emo = '📈' if change > 0 else '📉' 
        body += f"{emo} #{endeksler[k]} {endeks.info.get('longName')} 5 Günde %{change} {text}"
    

    #print(body)
    send_email(subject, body)

# İlk çalıştırma

#get_gold_price_and_send_email()
#send_bist_open()
#send_bist_close()
#print_crypto_data(cryptos)   
#bist_by_time()
#bist30_change()
#halka_arz()
#currency_send()
#silver()
random_stock()
#sektor_hisse_bilgi("Banka") #SAAT BELİRLENECEK
#sektor_endeks_bilgi() #SAAT BELİRLENECEK

keep_alive()

while True:
    tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(tz)

    if now.weekday() < 5 and now.hour == 11 and now.minute == 00:
        silver()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 16 and now.minute == 00:
        silver()
        time.sleep(120)
        continue
   
    if now.weekday() < 7 and now.hour == 9 and now.minute == 00:
        print_crypto_data(cryptos)
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 19 and now.minute == 00:
        print_crypto_data(cryptos)
        time.sleep(120)
        continue
    

    if now.weekday() < 5 and now.hour == 10 and now.minute == 30:
        currency_send()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 17 and now.minute == 30:
        currency_send()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 11 and now.minute == 30:
        get_gold_price_and_send_email()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 17 and now.minute == 30:
        get_gold_price_and_send_email()
        time.sleep(120) 
        continue

    if now.weekday() < 5 and now.hour == 10 and now.minute == 15:
        send_bist_open()
        time.sleep(120) 
        continue
    
    if now.weekday() < 5 and now.hour == 18 and now.minute == 00:
        send_bist_close()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 9 and now.minute == 30:
        bist_by_time()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 15 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 18 and now.minute == 30:
        bist_by_time()
        time.sleep(120)    
        continue

    if now.weekday() < 5 and now.hour == 11 and now.minute == 35:
        bist30_change()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 13 and now.minute == 30:
        bist30_change()
        time.sleep(120)
        continue   

    if now.weekday() < 5 and now.hour == 17 and now.minute == 00:
        bist30_change()
        time.sleep(120)  
        continue    
    
    if now.weekday() < 5 and now.hour == 20 and now.minute == 00:
        halka_arz()
        time.sleep(120)
        continue
        
    else:
        time.sleep(1)
        continue
