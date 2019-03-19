import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import time
import wget
from selenium import webdriver

#set ChromeDriver options
options = webdriver.ChromeOptions()
prefs = {}
prefs["download.default_directory"] = 'C:\\Users\\AngelYang\\Documents\\GitHub\\Fintech_HW\\hw1'
prefs["profile.default_content_settings"] = { "popups": 1 }
options.add_experimental_option('prefs', prefs)

#crawl historical NAV from fund home page

etf = pd.read_excel('ETF_Vol_Alt_Group16.xlsx', 'Updated ETF list',usecols='A:C')
symbols = etf['Symbol']

df = pd.DataFrame(etf)
df.set_index('Symbol', inplace=True)


for symbol in symbols :
    url = df.at[symbol, 'Home page']
    issuer = df.at[symbol, 'Issuer']
    if issuer == 'ProShares':
        res = requests.get(url)
        soup = bs(res.text,features='html.parser')
        for FindLink in soup.find_all("a", text="NAV History"):
            link = FindLink.get('href')
            wget.download(link, symbol + ".csv")
            print("download: " + symbol)
            
    if issuer == 'AGFiQ Asset Management':
        #wrong links from etfdb.com, replace with correct ones
        url = 'http://www.agfiq.com/agfiq/agfiqweb/us/en/products/'+ symbol.lower() +'/index.jsp'
        res = requests.get(url)
        soup = bs(res.text,features='html.parser')
        for FindLink in soup.find_all("a", text="Historical NAVs & Distribution"):
            link1 = FindLink.get('href')
            link = link1.replace('../../../..','http://www.agfiq.com/agfiq/agfiqweb')
            print("download: " + link)
            wget.download(link, symbol + ".xlsx")
            
    if issuer == 'Barclays Capital':
        #wrong links from etfdb.com, replace with correct ones
        driver = webdriver.Chrome()
        driver.get('http://www.ipathetn.com/US/16/en/home.app')
        driver.implicitly_wait(30)
        driver.find_element_by_id("productSearch").send_keys(symbol)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Search'])[1]/following::div[2]").click()
        driver.find_element_by_xpath('//*[@id="ext-gen13"]/div/table/tbody/tr/td[1]/div/div/a').click()
        driver.find_element_by_link_text("IV/Index History (XLS 1KB)").click()
        print('download:'+ symbol)
        time.sleep(2)
        driver.quit()
        
    if issuer == 'IndexIQ':
        #wrong links from etfdb.com, replace with correct ones
        driver = webdriver.Chrome()
        driver.get('https://www.nylinvestments.com/IQetfs/etfs')
        driver.implicitly_wait(30)
        driver.find_element_by_partial_link_text('('+symbol+')').click()
        driver.find_element_by_id("etfHistoryNav").click()
        print('download:'+ symbol)
        time.sleep(2)
        driver.quit() 
    
    if issuer == 'Reality Shares':
        #right link but they use svg to show NAV data, crawl from yahoo finance instead
        driver = webdriver.Chrome()
        driver.get('https://finance.yahoo.com/')
        driver.implicitly_wait(30)
        driver.find_element_by_name("yfin-usr-qry").send_keys('DIVY')
        time.sleep(5)
        driver.find_element_by_id('search-button').click()
        driver.find_element_by_xpath('//*[@id="quote-nav"]/ul/li[4]/a/span').click()
        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input').click()
        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[7]').click()
        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]').click()
        driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button').click()
        driver.find_element_by_link_text('Download Data').click()
        print('download: DIVY')
        time.sleep(2)
        driver.quit()  

