import random
import yfinance as yf

def bist_by_time():
    stocks = ['ACSEL', 'ADEL', 'ADESE', 'AEFES', 'AFYON', 'AGYO', 'AKBNK', 'AKCNS', 'AKENR', 'AKFGY', 'AKGRT', 'AKMGY', 'AKSA', 'AKSEN', 'AKSGY', 'AKSUE', 'ALARK', 'ALBRK', 'ALCAR', 'ALCTL', 'ALGYO', 'ALKIM', 'ANELE', 'ANHYT', 'ANSGR', 'ARCLK', 'ARENA', 'ARSAN', 'ASELS', 'ASUZU', 'ATAGY', 'ATEKS', 'ATLAS', 'ATSYH', 'AVGYO', 'AVHOL', 'AVOD', 'AVTUR', 'AYCES', 'AYEN', 'AYES', 'AYGAZ', 'BAGFS', 'BAKAB', 'BALAT', 'BANVT', 'BASCM', 'BEYAZ', 'BFREN', 'BIMAS', 'BIZIM', 'BJKAS', 'BLCYT', 'BNTAS', 'BOSSA', 'BRISA', 'BRKSN', 'BRMEN', 'BRSAN', 'BRYAT', 'BSOKE', 'BTCIM', 'BUCIM', 'BURCE', 'BURVA', 'CCOLA', 'CELHA', 'CEMAS', 'CEMTS', 'CIMSA', 'CLEBI', 'CMBTN', 'CMENT', 'COSMO', 'CRDFA', 'CRFSA', 'CUSAN', 'DAGHL', 'DAGI', 'DARDL', 'DENGE', 'DERIM', 'DEVA', 'DGATE', 'DGGYO', 'DIRIT', 'DITAS', 'DMSAS', 'DOAS', 'DOBUR', 'DOCO', 'DOGUB', 'DOHOL', 'DURDO', 'DYOBY', 'DZGYO', 'ECILC', 'ECZYT', 'EDIP', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EKGYO', 'EKIZ', 'EMKEL', 'EMNIS', 'ENKAI', 'EPLAS', 'ERBOS', 'EREGL', 'ERSU', 'ESCOM', 'ETILR', 'ETYAT', 'EUHOL', 'EUKYO', 'EUYO', 'FENER', 'FLAP', 'FMIZP', 'FRIGO', 'FROTO', 'GARAN', 'GARFA', 'GEDIK', 'GEDZA', 'GENTS', 'GEREL', 'GLBMD', 'GLRYH', 'GLYHO', 'GOLTS', 'GOODY', 'GOZDE', 'GRNYO', 'GSDDE', 'GSDHO', 'GSRAY', 'GUBRF', 'HALKB', 'HATEK', 'HDFGS', 'HEKTS', 'HLGYO', 'HURGZ', 'ICBCT', 'IDGYO', 'IEYHO', 'IHEVA', 'IHGZT', 'IHLAS', 'IHYAY', 'INDES', 'INFO', 'INTEM', 'IPEKE', 'ISBIR', 'ISBTR', 'ISCTR', 'ISDMR', 'ISFIN', 'ISGSY', 'ISGYO', 'ISMEN', 'ISYAT', 'IZFAS', 'IZMDC', 'JANTS', 'KAPLM', 'KAREL', 'KARSN', 'KARTN', 'KATMR', 'KCHOL', 'KENT', 'KERVN', 'KERVT', 'KLGYO', 'KLMSN', 'KLNMA', 'KNFRT', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMA', 'KRDMB', 'KRDMD', 'KRGYO', 'KRONT', 'KRSTL', 'KRTEK', 'KSTUR', 'KUTPO', 'KUYAS', 'LIDFA', 'LINK', 'LKMNH', 'LOGO', 'LUKSK', 'MAALT', 'MAKTK', 'MARTI', 'MEGAP', 'MEPET', 'MERIT', 'MERKO', 'METAL', 'METRO', 'METUR', 'MGROS', 'MIPAZ', 'MMCAS', 'MNDRS', 'MRGYO', 'MRSHL', 'MZHLD', 'NETAS', 'NIBAS', 'NTHOL', 'NUGYO', 'NUHCM', 'ODAS', 'ORGE', 'ORMA', 'OSMEN', 'OSTIM', 'OTKAR', 'OYAYO', 'OYLUM', 'OZGYO', 'OZKGY', 'OZRDN', 'PAGYO', 'PARSN', 'PEGYO', 'PENGD', 'PETKM', 'PETUN', 'PGSUS', 'PINSU', 'PKART', 'PKENT', 'PNSUT', 'POLHO', 'POLTK', 'PRKAB', 'PRKME', 'PRZMA', 'PSDTC', 'RAYSG', 'RODRG', 'RTALB', 'RYGYO', 'RYSAS', 'SAHOL', 'SAMAT', 'SANEL', 'SANFM', 'SARKY', 'SASA', 'SAYAS', 'SEKFK', 'SEKUR', 'SELEC', 'SELGD', 'SEYKM', 'SILVR', 'SISE', 'SKBNK', 'SKTAS', 'SNGYO', 'SNKRN', 'SNPAM', 'SODSN', 'SONME', 'SRVGY', 'TATGD', 'TAVHL', 'TBORG', 'TCELL', 'TEKTU', 'TGSAS', 'THYAO', 'TKFEN', 'TKNSA', 'TMPOL', 'TMSN', 'TOASO', 'TRCAS', 'TRGYO', 'TSKB', 'TSPOR', 'TTKOM', 'TTRAK', 'TUCLK', 'TUKAS', 'TUPRS', 'TURGG', 'ULAS', 'ULKER', 'ULUSE', 'ULUUN', 'UMPAS', 'USAK', 'USAS', 'UZERB', 'VAKBN', 'VAKFN', 'VAKKO', 'VANGD', 'VERTU', 'VERUS', 'VESBE', 'VESTL', 'VKFYO', 'VKGYO', 'VKING', 'YAPRK', 'YATAS', 'YAYLA', 'YBTAS', 'YESIL', 'YGGYO', 'YGYO', 'YKBNK', 'YONGA', 'YUNSA', 'YYAPI', 'ZOREN']
    chosen_stock = random.choice(stocks)
    stock_code = chosen_stock + '.IS'
    chosen_stock_info = yf.Ticker(stock_code)
    today = chosen_stock_info.info.get('currentPrice', '')
    month_1_close = chosen_stock_info.history(period='max').iloc[-22]['Close']
    month_1_change_percent = (((today - month_1_close) / today) * 100).round(1)
    day_5_close = chosen_stock_info.history(period='max').iloc[-5]['Close']
    day_5_change_percent = (((today - day_5_close) / today) * 100).round(1)
    month_3_close = chosen_stock_info.history(period='max').iloc[-66]['Close']
    month_3_change_percent = (((today - month_3_close) / today) * 100).round(1)
    
    print(f"""🔴 #{chosen_stock} Hissesinin Zamana Bağlı Performansı 👇
          
⬛ Güncel Fiyat: {today}
⬛ 5 Günlük Fiyat Değişimi: %{day_5_change_percent}
⬛ 1 Aylık Fiyat Değişimi: %{month_1_change_percent}
⬛ 3 Aylık Fiyat Değişimi: %{month_3_change_percent}

#yatırım #borsa #hisse #hisseanaliz #bist #bist100 #bist30 #borsaistanbul
          """)
    
bist_by_time()