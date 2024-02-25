import http.client
import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

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

    # Gmail hesabınızı ve şifrenizi girin
    email = 'omerddduran@gmail.com'
    password = 'qbfl udxd kjya tpiv'

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

# İlk çalıştırma
get_gold_price_and_send_email()

# Haftaiçi saat 13:00'da kontrol ve e-posta gönderme
while True:
    # Şu anki zamanı al
    now = datetime.now()
    # Haftaiçi ise ve saat 13:00 olduğunda çalıştır
    if now.weekday() < 5 and now.hour == 13 and now.minute == 0:
        get_gold_price_and_send_email()
        # iki dakika sonra tekrar kontrol etmek için bekleyin
        time.sleep(120)
    else:
        # 1 saniye bekleyin ve tekrar kontrol edin
        time.sleep(1)
