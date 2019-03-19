from selenium import webdriver
import pandas as pd
import datetime
from pathlib import Path
import time
import os
import csv
import glob

import requests
from bs4 import BeautifulSoup as bs
import pandas_datareader.data as web   
import re
import wget

chrome_driver_path = './chromedriver'
etf_alt_file = './source_csv_files/Alternatives ETF List (35).csv'
etf_vol_file = './source_csv_files/Volatility ETF List (18).csv'
info_file = './csv_files/info.csv'
download_location = './'
csv_filepath=r'./csv_files/'

# df_info = pd.read_csv(info_file)

def IndexIQ_csv_proc(symbol):
    
    symbol_filename = symbol + '.csv'
    
    symbol_csvfile = os.path.join('./csv_files', symbol_filename)
    tmp_csvfile = os.path.join('./csv_files', 'output.csv')
    
    with open(symbol_csvfile) as csvfile:
        rows = csv.reader(csvfile)
        next(csvfile, None)
        next(csvfile, None)
        next(csvfile, None)

        with open(tmp_csvfile, 'w') as writefile:
            writer = csv.writer(writefile)
            for row in rows:
                writer.writerow(row)

    os.remove(symbol_csvfile)
    os.rename(tmp_csvfile, symbol_csvfile)


def WisdomTree(symbols):
    
    # df_WisdomTree = df_info[df_info['issuer'] == 'WisdomTree']
    # symbols = df_WisdomTree['symbol'].tolist()
    
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_location}
    options.add_experimental_option("prefs", prefs)
    
    for symbol in symbols:
    
        xpath_pattern = "//a[contains(text(),'View NAV and Premium/Discount History')]"
        rename_command = "mv *.csv "
        move_command = "mv XXX.csv ./csv_files"

        target_url = os.path.join('https://www.wisdomtree.com/etfs/alternative', symbol)
        driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)
        driver.minimize_window()
        driver.get(target_url)

        data_element = driver.find_element_by_xpath(xpath_pattern)
        data_link = data_element.get_attribute("data-href")

        html_filename = symbol + ".html"
        wget.download(data_link, out=html_filename)
        df_list = pd.read_html(html_filename)
        df = df_list[0]
        df = df[['Date', 'Nav']]
        df.to_csv(csv_filepath + symbol + ".csv" ,index=0)
        print('\n')
        print(symbol + " is downloaded")
        
        os.remove(html_filename)

        driver.quit()

def IndexIQ(symbols):
    
    # df_IndexIQ = df_info[df_info['issuer'] == 'IndexIQ']
    # symbols = df_IndexIQ['symbol'].tolist()

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_location}
    options.add_experimental_option("prefs", prefs)

    for symbol in symbols:

        xpath_pattern = "//a[contains(text(), 'XXX')]"

        target_url = os.path.join('https://www.nylinvestments.com/IQetfs', 'etfs')
        driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)
        driver.minimize_window()
        driver.get(target_url)

        xpath_pattern = xpath_pattern.replace('XXX', symbol)

        time.sleep(1)
        
        driver.find_element_by_xpath(xpath_pattern).click()
        driver.find_element_by_partial_link_text('Download Historical').click()

        time.sleep(3)

        filename_list = glob.glob('./*.csv')
        filename = filename_list[0]
        os.rename(filename, os.path.join('./csv_files', symbol+'.csv'))
        
        IndexIQ_csv_proc(symbol)

        print(symbol + " is downloaded")
        driver.quit()

def SPDR(symbols):
    df_SSS = df_info[df_info['issuer'] == 'State Street SPDR']
    symbols = df_SSS['symbol'].tolist()
    for symbol in symbols:
        start = datetime.datetime(2015,12,31)
        end = datetime.date.today()
        df_nav = web.DataReader(symbol, "yahoo", start, end)
        df_nav.to_csv(csv_filepath + symbol + ".csv" ,index=0)
        print(symbol + " is downloaded")

def FirstTrust(symbols):
    # df_FT = df_info[df_info['issuer'] == 'First Trust']
    # symbols = df_FT['symbol'].tolist()
    
    for symbol in symbols:
        start = datetime.datetime(2015,12,31)
        end = datetime.date.today()
        df_nav = web.DataReader(symbol, "yahoo", start, end)
        df_nav.to_csv(csv_filepath + symbol + ".csv" ,index=0)
        print(symbol + " is downloaded")

def ETC(symbols):
    # df_ETC = df_info[df_info['issuer'] == 'Exchange Traded Concepts']
    # symbols = df_ETC['symbol'].tolist()
    
    for symbol in symbols:
        start = datetime.datetime(2015,12,31)
        end = datetime.date.today()
        df_nav = web.DataReader(symbol, "yahoo", start, end)
        df_nav.to_csv(csv_filepath + symbol + ".csv" ,index=0)
        print(symbol + " is downloaded")


