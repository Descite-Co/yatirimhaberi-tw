import http.client, json, smtplib, time, requests, yfinance as yf, random, matplotlib.pyplot as plt, pytz;
from datetime import datetime, timedelta;
from email.mime.image import MIMEImage;
from email.mime.text import MIMEText;
from email.mime.multipart import MIMEMultipart;
from bs4 import BeautifulSoup;
from io import BytesIO;
from data.stocks import stocks;
from data.hisse_listesi import hisse_listesi;
from data.cryptos import cryptos;
from data.config import email, password


def send_email(subject, body, image_stream=None):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = 'trigger@applet.ifttt.com'  # Change to the desired recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach image if present
    if image_stream:
        image = MIMEImage(image_stream.getvalue())
        image.add_header('Content-Disposition', 'attachment', filename='bitcoin_price.png')
        msg.attach(image)

    server.send_message(msg)
    server.quit()


# EMTİA FONKSİYONLARI
def format_currency(price, currency):
    if isinstance(price, str):
        return price
    else:
        return f"{price:.2f} {currency}"


def get_commodity_info(ticker, display_name):
    commodity = yf.Ticker(ticker)
    commodity_info = commodity.info
    currency = commodity_info.get("financialCurrency", "USD")

    email_body = f"🔴 {display_name} güncel ve uzun dönemli performansı 👇\n\n"
    current_price = commodity_info.get('regularMarketPrice',
                                       (commodity_info.get('open', 0) + commodity_info.get('dayHigh', 0)) / 2)
    email_body += f"▪️ Anlık Fiyat: {format_currency(current_price, currency)}\n"
    email_body += f"▪️ 52 Haftalık En Yüksek Değer: {format_currency(commodity_info.get('fiftyTwoWeekHigh', 0), currency)}\n"
    email_body += f"▪️ 52 Haftalık En Düşük Değer: {format_currency(commodity_info.get('fiftyTwoWeekLow', 0), currency)}\n"
    return commodity_info, email_body


def plot_commodity_prices(historical_data, commodity_info, display_name):
    plt.figure(figsize=(12, 6))
    plt.plot(historical_data['Close'])
    plt.title(f'{display_name} Değişim Grafiği')
    plt.ylabel('Fiyat Dolar')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    return image_stream


def send_info_by_email(ticker, display_name):
    commodity_info, email_body = get_commodity_info(ticker, display_name)
    historical_data = yf.download(ticker, start=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
                                  end=datetime.now().strftime('%Y-%m-%d'))
    image_stream = plot_commodity_prices(historical_data, commodity_info, display_name)
    # E-posta gönderme işlemi için doğru fonksiyon adını kullan
    send_email(f'Emtia Güncellemesi: {display_name} #crypto', email_body, image_stream)


# CRYPTO FUNCTIONS
def plot_bitcoin_graph():
    # Retrieve historical data for Bitcoin
    btc = yf.Ticker("BTC-USD")
    btc_data = btc.history(period="1mo")  # adjust the period as needed

    # Plot historical prices
    plt.figure(figsize=(10, 5))
    plt.plot(btc_data['Close'], label='Son Fiyat')
    plt.title('Bitcoin Aylık Grafik')
    plt.ylabel('Dolar')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO buffer
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)  # rewind to the beginning of the file
    return image_buffer


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
    body = "🚀 Anlık Kripto Verileri 🚀\n"
    for crypto, urls in cryptos.items():
        price = get_crypto_price(urls[0])
        market_cap = get_crypto_price(urls[1])
        if price is not None and market_cap is not None:
            body += f"\n🌟 #{crypto} Fiyatı: ${format_price(price)}\n"
            body += f"💰 #{crypto} Piyasa Değeri: {format_market_cap(float(market_cap))}\n"
        else:
            print(f"\n🚫 {crypto} verileri alınamadı.")

    # Generate the Bitcoin graph and attach it to the email
    image_stream = plot_bitcoin_graph()
    send_email("Anlık Kripto Verileri #crypto ##crypto #randomstock ##random_stock", body, image_stream)


# Uzun Dönem Performans Random Stock
def duzenle(deger, para):
    if deger != 0 and isinstance(deger, int):
        return "{:,.0f} {}".format(deger, para).replace(",", ".")
    elif deger != 0 and isinstance(deger, float):
        return "{:,.2f} {}".format(deger, para).replace(",", ".")
    else:
        return ''


def random_stock():
    secilen_hisse = random.choice(hisse_listesi)
    hisse = yf.Ticker(secilen_hisse)
    hisse_bilgileri = hisse.info
    currency = hisse_bilgileri["financialCurrency"]

    email_body = f"📈#{secilen_hisse} {hisse_bilgileri['shortName']} hisse senedinin güncel ve uzun dönemli performansı 👇\n\n"
    anlik_fiyat = hisse_bilgileri.get('regularMarketPrice',
                                      (hisse_bilgileri.get('open', 0) + hisse_bilgileri.get('dayHigh', 0)) / 2)
    email_body += f"▪️ Anlık Fiyat: {duzenle(anlik_fiyat if anlik_fiyat != 0 else '', currency)}\n"
    email_body += f"▪️ 52 Haftalık En Yüksek Değer: {duzenle(hisse_bilgileri.get('fiftyTwoWeekHigh', 0), currency)}\n"
    email_body += f"▪️ Ortalama Günlük İşlem Hacmi (Son 10 Gün): {duzenle(hisse_bilgileri.get('averageDailyVolume10Day', 'hisse'), currency)}\n"
    email_body += f"▪️ Piyasa Değeri: {duzenle(hisse_bilgileri.get('marketCap', 0), currency)}\n"

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    # Download historical stock data for the last year
    stock_data1 = yf.download(secilen_hisse, start=start_date, end=end_date)

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data1['Close'], label='Son Fiyat')
    y_min = stock_data1['Close'].min()
    y_max = stock_data1['Close'].max()
    y_ticks = range(int(y_min), int(y_max) + 1, 10)
    plt.yticks(y_ticks)
    plt.title(f'{hisse_bilgileri["shortName"]} Değişim Grafiği ')
    plt.ylabel('Fiyat')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # E-posta gönder
    subject = f"{hisse_bilgileri['shortName']} Hissesi Performans Raporu ##randomstock ##randomstock"
    send_email(subject, email_body, image_stream)
    #print(email_body)


# BIST OPEN AND CLOSE
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
    xu100_open = round(xu100_open, 2)
    emo = '📈' if xu100_change > 0 else '📉'
    text = 'yükseliş' if xu100_change > 0 else 'düşüş'
    subject = ("send_bist100_open #randomstock ##randomstock #crypto ##crypto")
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde güne %{xu100_change} {text} ile başladı.

{emo} Açılış Fiyatı: {xu100_open} \n
    """

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    stock_data = yf.download('XU100.IS', start=start_date, end=end_date, interval='15m')

    # Resample the data to 3-hour intervals and interpolate to fill missing values
    stock_data_3h = stock_data['Close'].resample('1h').mean().interpolate(method='time')

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle='-')
    plt.title('BIST 100 7-Day Graph (3-Hour Intervals)')
    plt.xlabel('Date')
    plt.ylabel('Price (TL)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    send_email(subject, body, image_stream)
    #print(body)
    #plt.show()


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
    xu100_current = round(xu100_current, 2)
    emo = '📈' if xu100_current_change > 0 else '📉'
    text = 'yükseliş' if xu100_current_change > 0 else 'düşüş'
    subject = ("send_bist100_close #randomstock ##randomstock #crypto ##crypto")
    body = f"""🔴 #BIST100 {day} {turkish_month} tarihinde günü %{xu100_current_change} {text} ile kapattı.

{emo} Kapanış Fiyatı: {xu100_current} \n
    """

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    stock_data = yf.download('XU100.IS', start=start_date, end=end_date, interval='15m')

    # Resample the data to 3-hour intervals and interpolate to fill missing values
    stock_data_3h = stock_data['Close'].resample('1h').mean().interpolate(method='time')

    # Plotting the graph
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data_3h.index, stock_data_3h.values, linestyle='-')
    plt.title('BIST 100 7-Day Graph (3-Hour Intervals)')
    plt.xlabel('Date')
    plt.ylabel('Price (TL)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    send_email(subject, body, image_stream)
    #print(body)


# ABD Borsa Açılış/Kapanış
def us_open():
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
    subject = ("send_us_open #test ##test")
    body = f"""🔴 {day} {turkish_month} ABD Endeksleri Açılış Verileri 👇

    """
    nasdaq = "^IXIC"
    nasdaq_name = "Nasdaq"
    nasdaq_ticker = yf.Ticker(nasdaq)
    nasdaq_open = nasdaq_ticker.info.get('open', '')
    nasdaq_last_close = nasdaq_ticker.info.get('previousClose', '')
    nasdaq_change = (((nasdaq_open - nasdaq_last_close) / nasdaq_last_close) * 100)
    nasdaq_change = round(nasdaq_change, 2)
    nasdaq_open = round(nasdaq_open, 2)
    nasdaq_emo = '📈' if nasdaq_change > 0 else '📉'
    body += f"\n{nasdaq_emo} {nasdaq_name}: %{nasdaq_change}"

    sp500 = "^GSPC"
    sp500_name = "S&P 500"
    sp500_ticker = yf.Ticker(sp500)
    sp500_open = sp500_ticker.info.get('open', '')
    sp500_last_close = sp500_ticker.info.get('previousClose', '')
    sp500_change = (((sp500_open - sp500_last_close) / sp500_last_close) * 100)
    sp500_change = round(sp500_change, 2)
    sp500_open = round(sp500_open, 2)
    sp500_emo = '📈' if sp500_change > 0 else '📉'
    body += f"\n{sp500_emo} {sp500_name}: %{sp500_change}"

    dowjones = "^DJI"
    dowjones_name = "Dow Jones Industrial Average"
    dowjones_ticker = yf.Ticker(dowjones)
    dowjones_open = dowjones_ticker.info.get('open', '')
    dowjones_last_close = dowjones_ticker.info.get('previousClose', '')
    dowjones_change = (((dowjones_open - dowjones_last_close) / dowjones_last_close) * 100)
    dowjones_change = round(dowjones_change, 2)
    dowjones_open = round(sp500_open, 2)
    dowjones_emo = '📈' if dowjones_change > 0 else '📉'
    body += f"\n{dowjones_emo} {dowjones_name}: %{dowjones_change}"

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"

    send_email(subject, body)
    #print(body)


def us_close():
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
    subject = ("send_us_close #test ##test")
    body = f"""🔴 {day} {turkish_month} ABD Endeksleri Kapanış Verileri 👇
    
    """
    nasdaq = "^IXIC"
    nasdaq_name = "NASDAQ"
    nasdaq_data = yf.Ticker(nasdaq).history(period='max')
    nasdaq_current = nasdaq_data['Close'][-1]
    nasdaq_prev = nasdaq_data['Close'][-2]
    nasdaq_current_change = (((nasdaq_current - nasdaq_prev) / nasdaq_prev) * 100)
    nasdaq_current_change = round(nasdaq_current_change, 2)
    emo_nasdaq = '📈' if nasdaq_current_change > 0 else '📉'
    body += f"\n{emo_nasdaq} {nasdaq_name}: %{nasdaq_current_change}"

    sp500 = "^GSPC"
    sp500_name = "S&P 500"
    sp500_data = yf.Ticker(sp500).history(period='max')
    sp500_current = sp500_data['Close'][-1]
    sp500_prev = sp500_data['Close'][-2]
    sp500_current_change = (((sp500_current - sp500_prev) / sp500_prev) * 100)
    sp500_current_change = round(sp500_current_change, 2)
    emo_sp500 = '📈' if sp500_current_change > 0 else '📉'
    body += f"\n{emo_sp500} {sp500_name}: %{sp500_current_change}"

    dowjones = "^DJI"
    dowjones_name = "Dow Jones"
    dowjones_data = yf.Ticker(dowjones).history(period='max')
    dowjones_current = dowjones_data['Close'][-1]
    dowjones_prev = dowjones_data['Close'][-2]
    dowjones_current_change = (((dowjones_current - dowjones_prev) / dowjones_prev) * 100)
    dowjones_current_change = round(dowjones_current_change, 2)
    emo_dowjones = '📈' if dowjones_current_change > 0 else '📉'
    body += f"\n{emo_dowjones} {dowjones_name}: %{dowjones_current_change}"

    body += "\n\n#yatırım #borsa #hisse #ekonomi #nasdaq #sp500 #dowjones #amerika"

    send_email(subject, body)
    #print(body)


# DÖVİZ KURLARI VE SILVER
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
        btc = yf.Ticker("TRY=X")
        btc_data = btc.history(period="3mo")  # adjust the period as needed

        # Plot historical prices
        plt.figure(figsize=(10, 5))
        plt.plot(btc_data['Close'], label='Son Fiyat')
        plt.title('Dolar TL 3 Aylık Grafik')
        plt.xlabel('')
        plt.ylabel('TL')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        image_buffer = BytesIO()
        plt.savefig(image_buffer, format='png')
        image_buffer.seek(0)

        send_email("Güncel Döviz Kurları #crypto", email_body, image_buffer)
    else:
        print("Döviz kurları alınamadı.")


def silver():
    # Gümüş verilerini al
    json_data = get_data_cur('https://api.genelpara.com/embed/para-birimleri.json')

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
            plt.plot(hist_data['Close'], label='Son Fiyat')
            plt.title('Gümüş Dolar Grafiği')
            plt.xlabel('')
            plt.ylabel('Fiyat')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save the plot as a BytesIO object
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
            image_stream.seek(0)

            # E-posta gönder
            send_email("Güncel Gümüş Fiyatları #crypto", email_body, image_stream)
            #print(email_body)

        else:
            print('Gümüş verisi bulunamadı.')
    else:
        print("Veri alınamadı.")


# GOLD PRICE FUNCTIONS
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
    hist_data = gold.history(period='1y')

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data['Close'], label='Son Fiyat')
    plt.legend()
    plt.title('Ons Altın Grafiği')
    plt.ylabel('Fiyat Dolar')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # E-posta oluşturma işlemi
    subject = f"🔴 Altın Fiyatları {day} {turkish_month} #crypto"
    body = "🔴 Altın Fiyatları:\n\n"
    for item in parsed_data["result"]:
        if item["name"] in ["Gram Altın", "ONS Altın", "Çeyrek Altın"]:
            body += f"💰 {item['name']}: Alış - {item['buying']}, Satış - {item['selling']}\n"

    send_email(subject, body, image_stream)
    #print(body)


def bist_by_time():
    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + '.IS'
    chosen_stock_info = yf.Ticker(stock_code)

    # Retrieve historical data
    hist_data = chosen_stock_info.history(period='1y')

    # Get the latest price
    today = chosen_stock_info.info.get('currentPrice', '0')

    # Calculate percentage changes
    month_1_close = hist_data['Close'].iloc[-31]
    month_1_change_percent = (((today - month_1_close) / month_1_close) * 100).round(1)

    day_5_close = hist_data['Close'].iloc[-6]
    day_5_change_percent = (((today - day_5_close) / day_5_close) * 100).round(1)

    month_6_close = hist_data['Close'].iloc[-181]
    month_6_change_percent = (((today - month_6_close) / month_6_close) * 100).round(1)

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
    }
    month_1_day = hist_data.index[-31].strftime('%d')
    month_1_month = hist_data.index[-31].strftime("%B")
    turkish_month_1 = turkish_month[month_1_month]
    month_1_year = hist_data.index[-31].strftime('%Y')

    day_5_day = hist_data.index[-6].strftime('%d')
    day_5_year = hist_data.index[-6].strftime('%Y')
    day_5_month = hist_data.index[-6].strftime("%B")
    turkish_day_5 = turkish_month[day_5_month]

    month_6_day = hist_data.index[-181].strftime('%d')
    month_6_year = hist_data.index[-181].strftime('%Y')
    month_6_month = hist_data.index[-181].strftime("%B")
    turkish_month_6 = turkish_month[month_6_month]

    determine = lambda x: 'arttı' if x > 0 else 'azaldı'

    # Plot historical prices
    plt.figure(figsize=(12, 6))
    plt.plot(hist_data['Close'], label='Son Fiyat')
    plt.title(f'{chosen_stock} Hisse Senedi Grafiği')
    plt.xlabel('')
    plt.ylabel('Fiyat')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')  # Save the plot as PNG image to the BytesIO object
    image_stream.seek(0)

    # Construct the message
    body = f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇

⬛ Güncel Fiyat: {today}
⬛ {day_5_day} {turkish_day_5} {day_5_year} tarihinden beri %{day_5_change_percent} {determine(day_5_change_percent)}.
⬛ {month_1_day} {turkish_month_1} {month_1_year} tarihinden beri %{month_1_change_percent} {determine(month_1_change_percent)}.
⬛ {month_6_day} {turkish_month_6} {month_6_year} tarihinden beri %{month_6_change_percent} {determine(month_6_change_percent)}.

          """
    subject = ("bist_by_time #crypto ##crypto")

    #print(body)
    send_email(subject, body, image_stream)


def bist30_change():
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
    subject = ("send_bist30_stock #test ##test")
    body = f"""🔴 #{chosen_stock} bugün %{hisse_current_change} {text}

{emo} Anlık Fiyatı: {hisse_current} \n
    """

    #print(body)
    send_email(subject, body)


def halka_arz():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d")
    day = day[1:] if day.startswith('0') else day  # BUNU HER DAY KULLANILAN YERDE KULLANALIM
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
    stocks = ['RGYAS', 'ODINE', 'MOGAN', 'ARTMS', 'ALVES', 'LMKDC']
    change_rates = []
    stock_prices = []
    subject = ("halka_arz_tablosu #test ##test")
    body = f"""🔴 {day} {turkish_month} Halka Arz Tablosu \n
"""
    for stock in stocks[::-1]:
        stock_code = stock + '.IS'
        hisse = yf.Ticker(stock_code)
        hisse_data = hisse.history(period='Max')
        hisse_close_list = hisse_data['Close'][-3:].tolist()
        print(hisse_close_list)
        hisse_current = hisse_close_list[2]
        hisse_prev = hisse_close_list[1]
        hisse_current_change = (((hisse_current - hisse_prev) / hisse_prev) * 100)
        hisse_current_change = round(hisse_current_change, 2)
        change_rates.append(hisse_current_change)
        stock_prices.append(hisse_current)
        emo = '📈' if hisse_current_change > 0 else '📉'
        text = 'yükseldi' if hisse_current_change > 0 else 'düştü'
        tavan_check = " - Hisse Tavanda" if hisse_current_change > 9.5 else ""
        message = f"{emo} #{stock} bugün %{hisse_current_change} {text}"
        body += f"{message + tavan_check}\n"

    print(body)
    #send_email(subject, body)


def sektor_hisse_bilgi(sektor):
    stocks = {
        "Banka": ["AKBNK", "ALBRK", "GARAN", "HALKB", "ICBCT", "ISATR", "ISBTR", "ISCTR", "ISKUR", "KLNMA", "QNBFB",
                  "SKBNK", "TSKB", "VAKBN", "YKBNK"],
        "Aracı Kurum": ["A1CAP", "GEDIK", "GLBMD", "INFO", "ISMEN", "OSMEN", "OYYAT", "SKYMD", "TERA"],
        "Savunma": ["ASELS", "SDTTR"],
        "Perakende Ticaret": ["BIMAS", "BIZIM", "CASA", "CRFSA", "EBEBK", "GMTAS", "KIMMR", "MAVI", "MEPET", "MGROS",
                              "MIPAZ", "SOKM", "SUWEN", "TKNSA", "VAKKO"],
        "Bilişim": ["ALCTL", "ARDYZ", "ARENA", "ATATP", "AZTEK", "DESPC", "DGATE", "EDATA", "ESCOM", "FONET", "FORTE",
                    "HTTBT", "INDES", "INGRM", "KAREL", "KFEIN",
                    "KRONT", "LINK", "LOGO", "MANAS", "MIATK", "MOBTL", "MTRKS", "NETAS", "OBASA", "ODINE", "PAPIL",
                    "PATEK", "PENTA", "PKART", "REEDR", "SMART", "VBTYZ"],
        "Gayrimenkul Yatırım Ortaklığı": ["ADGYO", "AGYO", "AKFGY", "AKMGY", "AKSGY", "ALGYO", "ASGYO", "ATAGY",
                                          "AVGYO", "AVPGY", "BASGZ", "BEGYO", "DGGYO", "DZGYO", "EKGYO",
                                          "EYGYO", "FZLGY", "HLGYO", "IDGYO", "ISGYO", "KGYO", "KLGYO", "KRGYO",
                                          "KZBGY", "KZGYO", "MHRGY", "MRGYO", "MSGYO", "NUGYO", "OZGYO",
                                          "OZKGY", "PAGYO", "PEGYO", "PEKGY", "PSGYO", "RYGYO", "SEGYO", "SNGYO",
                                          "SRVGY", "SURGY", "TDGYO", "TRGYO", "TSGYO", "VKGYO", "VRGYO",
                                          "YGGYO", "YGYO", "ZRGYO"]
    }
    subject = ("sektor_hisse_bilgi #crypto ##crypto")
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


def sektor_endeks_bilgi(start, end):
    tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(tz)
    endeksler = ["XUSIN", "XUHIZ", "XUMAL", "XUTEK", "XBANK", "XAKUR", "XBLSM", "XELKT", "XFINK", "XGMYO", "XGIDA",
                 "XHOLD",
                 "XILTM", "XINSA", "XKAGT", "XKMYA", "XMADN", "XYORT", "XMANA", "XMESY", "XSGRT", "XSPOR", "XTAST",
                 "XTEKS",
                 "XTCRT", "XTRZM", "XULAS"]
    endeksler = endeksler[start:end + 1]
    subject = "sektor_hisse_bilgi"
    body = "🔴 Borsa İstanbul Endekslerinin 5 Günlük Performansları 👇\n"

    for index in endeksler:
        try:
            stock_code = index + ".IS"
            endeks = yf.Ticker(stock_code)
            endeks_data = endeks.history(period='5d')
            if len(endeks_data) >= 5:
                current = endeks_data['Close'].iloc[-1]
                day5 = endeks_data['Close'].iloc[-5]
                change = (((current - day5) / day5) * 100)
                change = round(change, 2)
                text = 'Yükseldi' if change > 0 else 'Düştü'
                emo = '📈' if change > 0 else '📉'
                body += f"{emo} #{index} {endeks.info.get('longName', 'Bilgi Yok')} 5 Günde %{change} {text}\n"
            else:
                body += f"🔍 #{index} Yeterli veri yok\n"
        except Exception as e:
            body += f"⚠️ #{index} Veri alınırken hata: {str(e)}\n"

    #print(body)
    send_email(subject, body)


def bist_karsilastirma():
    tz = pytz.timezone('Europe/Istanbul')
    today_date = datetime.now(tz)
    day = today_date.strftime("%d").lstrip('0')
    month = today_date.strftime("%B")
    turkish_month = {
        "January": "Ocak", "February": "Şubat", "March": "Mart", "April": "Nisan",
        "May": "Mayıs", "June": "Haziran", "July": "Temmuz", "August": "Ağustos",
        "September": "Eylül", "October": "Ekim", "November": "Kasım", "December": "Aralık"
    }[month]

    xu100 = yf.Ticker('XU100.IS')
    xu100_data = xu100.history(period='max')
    xu100_current = xu100_data['Close'].iloc[-1]
    xu100_prev = xu100_data['Close'].iloc[-2]
    xu100_current_change = (((xu100_current - xu100_prev) / xu100_prev) * 100)
    xu100_current = round(xu100_current, 2)
    xu100_current_change = round(xu100_current_change, 2)
    emo100 = '📈' if xu100_current_change > 0 else '📉'

    xu30 = yf.Ticker('XU030.IS')
    xu30_data = xu30.history(period='max')
    xu30_current = xu30_data['Close'].iloc[-1]
    xu30_prev = xu30_data['Close'].iloc[-2]
    xu30_current_change = (((xu30_current - xu30_prev) / xu30_prev) * 100)
    xu30_current = round(xu30_current, 2)
    xu30_current_change = round(xu30_current_change, 2)
    emo30 = '📈' if xu30_current_change > 0 else '📉'

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    stock_data1 = yf.download('XU030.IS', start=start_date, end=end_date)
    stock_data2 = yf.download('XU100.IS', start=start_date, end=end_date)

    plt.figure(figsize=(12, 6))
    plt.plot(stock_data1['Close'], label='XU030.IS', color='blue')
    plt.plot(stock_data2['Close'], label='XU100.IS', color='orange')
    plt.legend()
    plt.title('BIST100 - BIST30 Karşılaştırması')
    plt.xlabel('')
    plt.ylabel('Fiyat (TL)')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    subject = "BIST100 - BIST30 Karşılaştırması #crypto ##crypto"
    body = f"""🔴 BIST100 - BIST30 Karşılaştırması 👇

#BIST30
💸 Anlık Fiyat: {xu30_current} TL
{emo30} Günlük Değişim: %{xu30_current_change}

#BIST100
💸 Anlık Fiyat: {xu100_current} TL
{emo100} Günlük Değişim: %{xu100_current_change}
    """
    # Ensure your email sending functionality is correctly configured
    send_email(subject, body, image_stream)


# İlk çalıştırma

#sektor_hisse_bilgi("Gayrimenkul Yatırım Ortaklığı") #SAAT BELİRLENECEK - Perakende , GYO ve Bilişimde sıkıntı çıkıyor bakıcam
#sektor_endeks_bilgi(0,26) #SAAT BELİRLENECEK
#bist_karsilastirma() #SAAT BELİRLENECEK

#halka_arz()
bist30_change()
bist_by_time()
#send_bist_open()
#send_bist_close()
#us_open()
#us_close()
currency_send()
#silver()
#get_gold_price_and_send_email()
random_stock()
print_crypto_data(cryptos)
#send_info_by_email('CL=F', 'Ham Petrol')  # Crude Oil
#send_info_by_email('HO=F', 'Kalorifer Yakıtı')  # Heating Oil
#send_info_by_email('NG=F', 'Doğal Gaz')  # Natural Gas

while True:
    tz = pytz.timezone('Europe/Istanbul')
    now = datetime.now(tz)

    if now.weekday() < 5 and now.hour == 10 and now.minute == 20:
        halka_arz()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 20 and now.minute == 30:
        bist30_change()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 16 and now.minute == 00:
        bist30_change()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 19 and now.minute == 30:
        bist30_change()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 11 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
        continue
    if now.weekday() < 7 and now.hour == 15 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 19 and now.minute == 00:
        bist_by_time()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 10 and now.minute == 17:
        send_bist_open()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 18 and now.minute == 17:
        send_bist_close()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 12 and now.minute == 30:
        currency_send()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 11 and now.minute == 30:
        silver()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 10 and now.minute == 30:
        get_gold_price_and_send_email()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 16 and now.minute == 30:
        get_gold_price_and_send_email()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 17 and now.minute == 30:
        random_stock()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 23 and now.minute == 49:
        random_stock()
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 6 and now.minute == 30:
        print_crypto_data(cryptos)
        time.sleep(120)
        continue

    if now.weekday() < 7 and now.hour == 18 and now.minute == 00:
        print_crypto_data(cryptos)
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 13 and now.minute == 30:
        send_info_by_email('NG=F', 'Doğal Gaz')
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 23 and now.minute == 30:
        send_info_by_email('HO=F', 'Kalorifer Yakıtı')
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 20 and now.minute == 00:
        send_info_by_email('CL=F', 'Ham Petrol')
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 16 and now.minute == 46:
        us_open()
        time.sleep(120)
        continue

    if now.weekday() < 5 and now.hour == 23 and now.minute == 16:
        us_close()
        time.sleep(120)
        continue

    else:
        time.sleep(1)
        continue
