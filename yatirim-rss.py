import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

# RSS ve e-posta yapılandırma değişkenleri
RSS_URL = "https://bigpara.hurriyet.com.tr/rss/"
CHECK_INTERVAL = 60  # Kontrol aralığı 10 dakika olarak ayarlandı
EMAIL = "omerddduran@gmail.com"
PASSWORD = "qbfl udxd kjya tpiv"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
TWITTER_CHAR_LIMIT = 280  # Twitter karakter limiti

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL, EMAIL, text)
    server.quit()

def check_feed():
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries
    for entry in entries:
        description = "🔴 " + entry.description
        if len(description) <= TWITTER_CHAR_LIMIT:
            send_email("New RSS Feed Item #test ##test", description)

if __name__ == "__main__":
    while True:
        check_feed()
        time.sleep(CHECK_INTERVAL)
