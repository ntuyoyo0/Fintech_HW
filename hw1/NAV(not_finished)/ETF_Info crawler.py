mport requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time
import wget
from selenium import webdriver

#read excel files for the list of ETFs, get symbol
etf = pd.read_excel('ETF_Vol_Alt_list_Group16.xlsx', 'ETF list',usecols='A')
symbols=etf['Symbol']

#use symbols to crawl etfdb.com and get info of issuer and link of fund homepage

data = list()
all_data = list()

for symbol in symbols :
    print(symbol)
    url='https://etfdb.com/etf/'+symbol
    res = requests.get(url)
    soup = bs(res.text,features='html.parser')
    for FindHomepage in soup.find_all("a", text="Home page"):
        homepage = FindHomepage.get('href')
    for FindIssuer in soup.find_all(href=re.compile("/issuer/")):
        issuer = FindIssuer.string
    data.append({'Symbol' : symbol,
                 'Issuer' : issuer, 
                 'Home page' : homepage})
    time.sleep(2)
    

df = pd.DataFrame(data)
df.set_index('Symbol', inplace=True)

df.to_excel('ETF_Vol_Alt_Group16.xlsx', sheet_name='Updated ETF list')

