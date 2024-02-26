import requests
from bs4 import BeautifulSoup
import random
import yfinance as yf

def bist_by_time():
    stocks = []
    chosen_stock = 'TARKM.IS'
    chosen_stock_info = yf.Ticker(chosen_stock)
    today = chosen_stock_info.history(period='1d').iloc[-1]['Close']
    month_1_close = chosen_stock_info.history(period='max').iloc[-25]['Close']
    month_1_change_percent = (((today - month_1_close) / today) * 100).round(1)
    print('%' ,month_1_change_percent)
    
        
    
    # print(f"""
    #       🔴 #{chosen} hissesi için zaman aralığına göre analizler: 👇
          
    #       ⬛ 5 Günlük Yüzde: {percent_5d}
    #       """)
bist_by_time()