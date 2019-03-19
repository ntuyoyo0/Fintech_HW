from selenium import webdriver
import pandas as pd
import datetime
from pathlib import Path
import time
import os

import requests
from bs4 import BeautifulSoup as bs
import re
import wget

chrome_driver_path = './chromedriver'
etf_alt_file = './source_csv_files/Alternatives ETF List (35).csv'
etf_vol_file = './source_csv_files/Volatility ETF List (18).csv'
info_file = "./csv_files/info.csv"
download_location = './'

etfdb_url = 'https://etfdb.com/etfs/'
etf_prefix_url = 'https://etfdb.com/etf/'

etf_start_inception = datetime.date(2015, 12, 31)

etf_alt = pd.read_csv(etf_alt_file)
etf_vol = pd.read_csv(etf_vol_file)


# ## Filter the ETF 
etf_alt['Inception'] = pd.to_datetime(etf_alt.Inception, format="%Y-%m-%d")
etf_vol['Inception'] = pd.to_datetime(etf_vol.Inception, format="%d/%m/%Y")


etf_alt_filtered = etf_alt[etf_alt['Inception'] < '2015-12-31']
etf_vol_filtered = etf_vol[etf_vol['Inception'] < '2015-12-31']


# ## Collect all symbols
alt_symbols = etf_alt_filtered['Symbol'].tolist()
vol_symbols = etf_vol_filtered['Symbol'].tolist()

all_symbols = []
all_symbols.extend(alt_symbols)
all_symbols.extend(vol_symbols)


# ## info crawler
symbol_list = []
issuer_list = []
hp_url_list = []

count = 0

for symbol in all_symbols:
    target_url = os.path.join(etf_prefix_url, symbol)
    res = requests.get(target_url)
    soup = bs(res.text,features='html.parser')
    
    findHomepage = soup.find("a", text="Home page")
    hp_url = findHomepage.get('href')
    
    findIssuer = soup.find("a", href=re.compile("/issuer/"))
    issuer_text = findIssuer.string
    
    count += 1
    print(str(count) + " " + symbol + ': ' + issuer_text + '    ' + hp_url)
    
    symbol_list.append(symbol)
    issuer_list.append(issuer_text)
    hp_url_list.append(hp_url)
    
    time.sleep(2)


# ## Create a directory
my_file = Path("./csv_files")
if my_file.is_dir():
    print("csv_files/ exists !")
else:
    Path('./csv_files').mkdir(exist_ok=False) 
    print("Create csv_files/")


# ## Create info.csv
df_dict = {'symbol': symbol_list, 'issuer': issuer_list, 'homepage': hp_url_list}
df = pd.DataFrame(data=df_dict)
df.to_csv(info_file)

my_file = Path(info_file)
print(my_file.is_file())
if my_file.is_file():
    print("info.csv exists !")
else:
    df_dict = {'symbol': symbol_list, 'issuer': issuer_list, 'homepage': hp_url_list}
    df = pd.DataFrame(data=df_dict)
    df.to_csv(info_file ,index=0)
    print("Create " + info_file)


