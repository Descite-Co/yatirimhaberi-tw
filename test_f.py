import requests
from bs4 import BeautifulSoup
import random

def bist_by_time():
    bist_hisseler = ['ACSEL', 'ADEL', 'ADESE', 'AEFES', 'AFYON', 'AGYO', 'AKBNK', 'AKCNS', 'AKENR', 'AKFGY', 'AKGRT', 'AKMGY', 'AKSA', 'AKSEN', 'AKSGY', 'AKSUE', 'ALARK', 'ALBRK', 'ALCAR', 'ALCTL', 'ALGYO', 'ALKIM', 'ANELE', 'ANHYT', 'ANSGR', 'ARCLK', 'ARENA', 'ARSAN', 'ASELS', 'ASUZU', 'ATAGY', 'ATEKS', 'ATLAS', 'ATSYH', 'AVGYO', 'AVHOL', 'AVOD', 'AVTUR', 'AYCES', 'AYEN', 'AYES', 'AYGAZ', 'BAGFS', 'BAKAB', 'BALAT', 'BANVT', 'BASCM', 'BEYAZ', 'BFREN', 'BIMAS', 'BIZIM', 'BJKAS', 'BLCYT', 'BNTAS', 'BOSSA', 'BRISA', 'BRKSN', 'BRMEN', 'BRSAN', 'BRYAT', 'BSOKE', 'BTCIM', 'BUCIM', 'BURCE', 'BURVA', 'CCOLA', 'CELHA', 'CEMAS', 'CEMTS', 'CIMSA', 'CLEBI', 'CMBTN', 'CMENT', 'COSMO', 'CRDFA', 'CRFSA', 'CUSAN', 'DAGHL', 'DAGI', 'DARDL', 'DENGE', 'DERIM', 'DEVA', 'DGATE', 'DGGYO', 'DIRIT', 'DITAS', 'DMSAS', 'DOAS', 'DOBUR', 'DOCO', 'DOGUB', 'DOHOL', 'DURDO', 'DYOBY', 'DZGYO', 'ECILC', 'ECZYT', 'EDIP', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EKGYO', 'EKIZ', 'EMKEL', 'EMNIS', 'ENKAI', 'EPLAS', 'ERBOS', 'EREGL', 'ERSU', 'ESCOM', 'ETILR', 'ETYAT', 'EUHOL', 'EUKYO', 'EUYO', 'FENER', 'FLAP', 'FMIZP', 'FRIGO', 'FROTO', 'GARAN', 'GARFA', 'GEDIK', 'GEDZA', 'GENTS', 'GEREL', 'GLBMD', 'GLRYH', 'GLYHO', 'GOLTS', 'GOODY', 'GOZDE', 'GRNYO', 'GSDDE', 'GSDHO', 'GSRAY', 'GUBRF', 'HALKB', 'HATEK', 'HDFGS', 'HEKTS', 'HLGYO', 'HURGZ', 'ICBCT', 'IDGYO', 'IEYHO', 'IHEVA', 'IHGZT', 'IHLAS', 'IHYAY', 'INDES', 'INFO', 'INTEM', 'IPEKE', 'ISBIR', 'ISBTR', 'ISCTR', 'ISDMR', 'ISFIN', 'ISGSY', 'ISGYO', 'ISMEN', 'ISYAT', 'IZFAS', 'IZMDC', 'JANTS', 'KAPLM', 'KAREL', 'KARSN', 'KARTN', 'KATMR', 'KCHOL', 'KENT', 'KERVN', 'KERVT', 'KLGYO', 'KLMSN', 'KLNMA', 'KNFRT', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL', 'KRDMA', 'KRDMB', 'KRDMD', 'KRGYO', 'KRONT', 'KRSTL', 'KRTEK', 'KSTUR', 'KUTPO', 'KUYAS', 'LIDFA', 'LINK', 'LKMNH', 'LOGO', 'LUKSK', 'MAALT', 'MAKTK', 'MARTI', 'MEGAP', 'MEPET', 'MERIT', 'MERKO', 'METAL', 'METRO', 'METUR', 'MGROS', 'MIPAZ', 'MMCAS', 'MNDRS', 'MRGYO', 'MRSHL', 'MZHLD', 'NETAS', 'NIBAS', 'NTHOL', 'NUGYO', 'NUHCM', 'ODAS', 'ORGE', 'ORMA', 'OSMEN', 'OSTIM', 'OTKAR', 'OYAYO', 'OYLUM', 'OZGYO', 'OZKGY', 'OZRDN', 'PAGYO', 'PARSN', 'PEGYO', 'PENGD', 'PETKM', 'PETUN', 'PGSUS', 'PINSU', 'PKART', 'PKENT', 'PNSUT', 'POLHO', 'POLTK', 'PRKAB', 'PRKME', 'PRZMA', 'PSDTC', 'RAYSG', 'RODRG', 'RTALB', 'RYGYO', 'RYSAS', 'SAHOL', 'SAMAT', 'SANEL', 'SANFM', 'SARKY', 'SASA', 'SAYAS', 'SEKFK', 'SEKUR', 'SELEC', 'SELGD', 'SEYKM', 'SILVR', 'SISE', 'SKBNK', 'SKTAS', 'SNGYO', 'SNKRN', 'SNPAM', 'SODSN', 'SONME', 'SRVGY', 'TATGD', 'TAVHL', 'TBORG', 'TCELL', 'TEKTU', 'TGSAS', 'THYAO', 'TKFEN', 'TKNSA', 'TMPOL', 'TMSN', 'TOASO', 'TRCAS', 'TRGYO', 'TSKB', 'TSPOR', 'TTKOM', 'TTRAK', 'TUCLK', 'TUKAS', 'TUPRS', 'TURGG', 'ULAS', 'ULKER', 'ULUSE', 'ULUUN', 'UMPAS', 'USAK', 'USAS', 'UZERB', 'VAKBN', 'VAKFN', 'VAKKO', 'VANGD', 'VERTU', 'VERUS', 'VESBE', 'VESTL', 'VKFYO', 'VKGYO', 'VKING', 'YAPRK', 'YATAS', 'YAYLA', 'YBTAS', 'YESIL', 'YGGYO', 'YGYO', 'YKBNK', 'YONGA', 'YUNSA', 'YYAPI', 'ZOREN']
    chosen = random.choice(bist_hisseler)
    BASE_URL_5D = f'https://www.google.com/finance/quote/{chosen}:IST?hl=tr&window=5D'
    page_5d = requests.get(BASE_URL_5D)
    soup_5d = BeautifulSoup(page_5d.content, "html.parser") 
    percent_5d = soup_5d.find("span", class_="P2Luy Ez2Ioe ZYVHBb")
    
    print(f"""
          🔴 #{chosen} hissesi için zaman aralığına göre analizler: 👇
          
          ⬛ 5 Günlük Yüzde: {percent_5d}
          """)

bist_by_time()