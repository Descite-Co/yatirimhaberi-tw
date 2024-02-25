import yfinance as yf
import random

# Hisse listesi
hisseler = ['ACSEL.IS', 'ADEL.IS', 'ADESE.IS', 'AEFES.IS', 'AFYON.IS', 'AGYO.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKENR.IS', 'AKFGY.IS', 'AKGRT.IS', 'AKMGY.IS', 'AKSA.IS', 'AKSEN.IS', 'AKSGY.IS', 'AKSUE.IS', 'ALARK.IS', 'ALBRK.IS', 'ALCAR.IS', 'ALCTL.IS', 'ALGYO.IS', 'ALKIM.IS', 'ANELE.IS', 'ANHYT.IS', 'ANSGR.IS', 'ARCLK.IS', 'ARENA.IS', 'ARSAN.IS', 'ASELS.IS', 'ASUZU.IS', 'ATAGY.IS', 'ATEKS.IS', 'ATLAS.IS', 'ATSYH.IS', 'AVGYO.IS', 'AVHOL.IS', 'AVOD.IS', 'AVTUR.IS', 'AYCES.IS', 'AYEN.IS', 'AYES.IS', 'AYGAZ.IS', 'BAGFS.IS', 'BAKAB.IS', 'BALAT.IS', 'BANVT.IS', 'BASCM.IS', 'BEYAZ.IS', 'BFREN.IS', 'BIMAS.IS', 'BIZIM.IS', 'BJKAS.IS', 'BLCYT.IS', 'BNTAS.IS', 'BOSSA.IS', 'BRISA.IS', 'BRKSN.IS', 'BRMEN.IS', 'BRSAN.IS', 'BRYAT.IS', 'BSOKE.IS', 'BTCIM.IS', 'BUCIM.IS', 'BURCE.IS', 'BURVA.IS', 'CCOLA.IS', 'CELHA.IS', 'CEMAS.IS', 'CEMTS.IS', 'CIMSA.IS', 'CLEBI.IS', 'CMBTN.IS', 'CMENT.IS', 'COSMO.IS', 'CRDFA.IS', 'CRFSA.IS', 'CUSAN.IS', 'DAGHL.IS', 'DAGI.IS', 'DARDL.IS', 'DENGE.IS', 'DERIM.IS', 'DEVA.IS', 'DGATE.IS', 'DGGYO.IS', 'DIRIT.IS', 'DITAS.IS', 'DMSAS.IS', 'DOAS.IS', 'DOBUR.IS', 'DOCO.IS', 'DOGUB.IS', 'DOHOL.IS', 'DURDO.IS', 'DYOBY.IS', 'DZGYO.IS', 'ECILC.IS', 'ECZYT.IS', 'EDIP.IS', 'EGEEN.IS', 'EGGUB.IS', 'EGPRO.IS', 'EGSER.IS', 'EKGYO.IS', 'EKIZ.IS', 'EMKEL.IS', 'EMNIS.IS', 'ENKAI.IS', 'EPLAS.IS', 'ERBOS.IS', 'EREGL.IS', 'ERSU.IS', 'ESCOM.IS', 'ETILR.IS', 'ETYAT.IS', 'EUHOL.IS', 'EUKYO.IS', 'EUYO.IS', 'FENER.IS', 'FLAP.IS', 'FMIZP.IS', 'FRIGO.IS', 'FROTO.IS', 'GARAN.IS', 'GARFA.IS', 'GEDIK.IS', 'GEDZA.IS', 'GENTS.IS', 'GEREL.IS', 'GLBMD.IS', 'GLRYH.IS', 'GLYHO.IS', 'GOLTS.IS', 'GOODY.IS', 'GOZDE.IS', 'GRNYO.IS', 'GSDDE.IS', 'GSDHO.IS', 'GSRAY.IS', 'GUBRF.IS', 'HALKB.IS', 'HATEK.IS', 'HDFGS.IS', 'HEKTS.IS', 'HLGYO.IS', 'HURGZ.IS', 'ICBCT.IS', 'IDGYO.IS', 'IEYHO.IS', 'IHEVA.IS', 'IHGZT.IS', 'IHLAS.IS', 'IHYAY.IS', 'INDES.IS', 'INFO.IS', 'INTEM.IS', 'IPEKE.IS', 'ISBIR.IS', 'ISBTR.IS', 'ISCTR.IS', 'ISDMR.IS', 'ISFIN.IS', 'ISGSY.IS', 'ISGYO.IS', 'ISMEN.IS', 'ISYAT.IS', 'IZFAS.IS', 'IZMDC.IS', 'JANTS.IS', 'KAPLM.IS', 'KAREL.IS', 'KARSN.IS', 'KARTN.IS', 'KATMR.IS', 'KCHOL.IS', 'KENT.IS', 'KERVN.IS', 'KERVT.IS', 'KLGYO.IS', 'KLMSN.IS', 'KLNMA.IS', 'KNFRT.IS', 'KONYA.IS', 'KORDS.IS', 'KOZAA.IS', 'KOZAL.IS', 'KRDMA.IS', 'KRDMB.IS', 'KRDMD.IS', 'KRGYO.IS', 'KRONT.IS', 'KRSTL.IS', 'KRTEK.IS', 'KSTUR.IS', 'KUTPO.IS', 'KUYAS.IS', 'LIDFA.IS', 'LINK.IS', 'LKMNH.IS', 'LOGO.IS', 'LUKSK.IS', 'MAALT.IS', 'MAKTK.IS', 'MARTI.IS', 'MEGAP.IS', 'MEPET.IS', 'MERIT.IS', 'MERKO.IS', 'METAL.IS', 'METRO.IS', 'METUR.IS', 'MGROS.IS', 'MIPAZ.IS', 'MMCAS.IS', 'MNDRS.IS', 'MRGYO.IS', 'MRSHL.IS', 'MZHLD.IS', 'NETAS.IS', 'NIBAS.IS', 'NTHOL.IS', 'NUGYO.IS', 'NUHCM.IS', 'ODAS.IS', 'ORGE.IS', 'ORMA.IS', 'OSMEN.IS', 'OSTIM.IS', 'OTKAR.IS', 'OYAYO.IS', 'OYLUM.IS', 'OZGYO.IS', 'OZKGY.IS', 'OZRDN.IS', 'PAGYO.IS', 'PARSN.IS', 'PEGYO.IS', 'PENGD.IS', 'PETKM.IS', 'PETUN.IS', 'PGSUS.IS', 'PINSU.IS', 'PKART.IS', 'PKENT.IS', 'PNSUT.IS', 'POLHO.IS', 'POLTK.IS', 'PRKAB.IS', 'PRKME.IS', 'PRZMA.IS', 'PSDTC.IS', 'RAYSG.IS', 'RODRG.IS', 'RTALB.IS', 'RYGYO.IS', 'RYSAS.IS', 'SAHOL.IS', 'SAMAT.IS', 'SANEL.IS', 'SANFM.IS', 'SARKY.IS', 'SASA.IS', 'SAYAS.IS', 'SEKFK.IS', 'SEKUR.IS', 'SELEC.IS', 'SELGD.IS', 'SEYKM.IS', 'SILVR.IS', 'SISE.IS', 'SKBNK.IS', 'SKTAS.IS', 'SNGYO.IS', 'SNKRN.IS', 'SNPAM.IS', 'SODSN.IS', 'SONME.IS', 'SRVGY.IS', 'TATGD.IS', 'TAVHL.IS', 'TBORG.IS', 'TCELL.IS', 'TEKTU.IS', 'TGSAS.IS', 'THYAO.IS', 'TKFEN.IS', 'TKNSA.IS', 'TMPOL.IS', 'TMSN.IS', 'TOASO.IS', 'TRCAS.IS', 'TRGYO.IS', 'TSKB.IS', 'TSPOR.IS', 'TTKOM.IS', 'TTRAK.IS', 'TUCLK.IS', 'TUKAS.IS', 'TUPRS.IS', 'TURGG.IS', 'ULAS.IS', 'ULKER.IS', 'ULUSE.IS', 'ULUUN.IS', 'UMPAS.IS', 'USAK.IS', 'USAS.IS', 'UZERB.IS', 'VAKBN.IS', 'VAKFN.IS', 'VAKKO.IS', 'VANGD.IS', 'VERTU.IS', 'VERUS.IS', 'VESBE.IS', 'VESTL.IS', 'VKFYO.IS', 'VKGYO.IS', 'VKING.IS', 'YAPRK.IS', 'YATAS.IS', 'YAYLA.IS', 'YBTAS.IS', 'YESIL.IS', 'YGGYO.IS', 'YGYO.IS', 'YKBNK.IS', 'YONGA.IS', 'YUNSA.IS', 'YYAPI.IS', 'ZOREN.IS', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'BRK.A', 'BRK.B', 'JPM', 'JNJ', 'V', 'PG', 'NVDA', 'MA', 'HD', 'DIS', 'UNH', 'PYPL', 'BAC', 'CMCSA', 'XOM', 'INTC', 'ADBE', 'NFLX', 'T', 'CRM', 'ABT', 'CSCO', 'VZ', 'KO', 'MRK', 'PFE', 'PEP', 'WMT', 'CVX', 'MCD', 'TMO', 'WFC', 'ABBV', 'ORCL', 'AMGN', 'NKE', 'ACN', 'IBM', 'QCOM', 'TXN', 'COST', 'LLY', 'HON', 'MDT', 'AVGO', 'DHR', 'NEE', 'UPS', 'LIN', 'SBUX', 'LOW', 'UNP', 'BA', 'MO', 'MMM', 'RTX', 'GS', 'BDX', 'CAT', 'ADP', 'LMT', 'CVS', 'CI', 'DE', 'ANTM', 'SO', 'BMY', 'USB', 'AXP', 'GILD', 'MS', 'ISRG', 'CHTR', 'RTX', 'PLD', 'AEP', 'TGT', 'D', 'DUK', 'BKNG', 'SPGI', 'VRTX', 'ZTS', 'CME', 'COF', 'CSX', 'CCI', 'REGN', 'CL']

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
anlik_fiyat = hisse_bilgileri.get('regularMarketPrice', (hisse_bilgileri.get('open', 0) + hisse_bilgileri.get('dayHigh', 0)) / 2)
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
