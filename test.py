import yfinance as yf
import random

# Hisse listesi
hisse_listesi = ['ACSEL.IS']

# Rastgeele bir hisse seçme
secilen_hisse = random.choice(hisse_listesi)

# Para birimini belirleme fonksiyonu
def para_birimi(hisse_kodu):
    if hisse_kodu.endswith('.IS'):
        return 'TRY'
    else:
        return 'USD'

# Seçilen hisse için verileri al
hisse = yf.Ticker(secilen_hisse)
hisse_bilgileri = hisse.info

# Fiyat ve hacim değerlerini düzenleyen fonksiyon
def duzenle(deger, para):
    if deger != 0 and isinstance(deger, int):
        return "{:,.0f} {}".format(deger, para).replace(",", ".")
    elif deger != 0 and isinstance(deger, float):
        return "{:,.2f} {}".format(deger, para).replace(",", ".")
    else:
        return ''

# Bilgileri yazdırma
print("📈 {} hisse senedinin güncel ve uzun dönemli performansı şu şekildedir:".format(hisse_bilgileri['shortName']))
print("\nÖnceki Kapanış: {}".format(duzenle(hisse_bilgileri.get('previousClose', ''), para_birimi(secilen_hisse))))
print("Açılış Fiyatı: {}".format(duzenle(hisse_bilgileri.get('open', ''), para_birimi(secilen_hisse))))
print("Günlük En Düşük Değer: {}".format(duzenle(hisse_bilgileri.get('dayLow', ''), para_birimi(secilen_hisse))))
print("Günlük En Yüksek Değer: {}".format(duzenle(hisse_bilgileri.get('dayHigh', ''), para_birimi(secilen_hisse))))

# Eğer 'regularMarketPrice' bilgisi mevcutsa, kullan. Değilse 'open' ve 'dayHigh' değerlerinden ortalama al.
anlik_fiyat = hisse_bilgileri
hisse_bilgileri.get('regularMarketPrice', (hisse_bilgileri.get('open', 0) + hisse_bilgileri.get('dayHigh', 0)) / 2)
print("Anlık Fiyat: {}".format(duzenle(anlik_fiyat, para_birimi(secilen_hisse)) if anlik_fiyat != 0 else ''))

print("52 Haftalık En Düşük Değer: {}".format(duzenle(hisse_bilgileri.get('fiftyTwoWeekLow', ''), para_birimi(secilen_hisse))))
print("52 Haftalık En Yüksek Değer: {}".format(duzenle(hisse_bilgileri.get('fiftyTwoWeekHigh', ''), para_birimi(secilen_hisse))))
print("Günlük İşlem Hacmi: {}".format(duzenle(hisse_bilgileri.get('volume', ''), 'hisse')))
print("Ortalama Günlük İşlem Hacmi (Son 10 Gün): {}".format(duzenle(hisse_bilgileri.get('averageDailyVolume10Day', ''), 'hisse')))
son_ceyrek_buyume_orani = hisse_bilgileri.get('quarterlyEarningsGrowth', '')
if son_ceyrek_buyume_orani != '':
    print("Son Çeyrek Dönem Büyüme Oranı: %{:.1f}".format(son_ceyrek_buyume_orani))
print("Net Gelir: {}".format(duzenle(hisse_bilgileri.get('netIncomeToCommon', ''), para_birimi(secilen_hisse))))
print("Brüt Kar Marjı: %{:.3f}".format(hisse_bilgileri.get('grossMargins', 0) * 100))
print("Piyasa Değeri: {}".format(duzenle(hisse_bilgileri.get('marketCap', ''), para_birimi(secilen_hisse))))