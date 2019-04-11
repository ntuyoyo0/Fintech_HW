import requests
import csv
import pandas as pd
from io import BytesIO
import datetime
from selenium import webdriver
import re
from bs4 import BeautifulSoup
# import jieba    ## https://github.com/APCLab/jieba-tw
import numpy as np


def news_link_crawler(cmp_list, page_num):
    
    browser = webdriver.Chrome("./chromedriver")
    news_urls_dict = {}
    
    for cmp_name in cmp_list:
        
        url = "https://tw.stock.yahoo.com/"
        browser.get(url)
        
        browser.find_element_by_xpath("//input[@placeholder='搜尋']").send_keys(cmp_name + "\n")
        browser.find_element_by_xpath("//a[contains(@class,'t1 c-black-h td-n td-n-h c-dgray')][contains(text(),'新聞')]").click()
    
        news_urls = []
    
        news_elements = browser.find_elements_by_class_name("fz-m")
        for e in news_elements:
            news_urls.append(e.get_attribute('href'))
        
        if page_num > 1:

            for i in range(2, page_num + 1):
                browser.find_element_by_link_text(str(i)).click()
                news_elements = browser.find_elements_by_class_name("fz-m")
                for e in news_elements:
                    news_urls.append(e.get_attribute('href'))
        
        news_urls_dict[cmp_name] = news_urls
                
    browser.close()
    
    return news_urls_dict



# ## 針對新聞網址爬內容

def create_df(cmp_list):
    columns_list=[cmp for cmp in cmp_list]
    columns_list = columns_list + ['0']
    
    df = pd.DataFrame(np.zeros((len(cmp_list), len(cmp_list) + 1)), columns=columns_list)
    df['0'] = cmp_list
    df = df.set_index('0')
    
    return df


def df_record(df, src_cmp, cmp_list, source_str):
    for cmp in cmp_list:
        findword = u"(" + re.escape(cmp) + u"+)"
        pattern = re.compile(findword)
        results =  pattern.findall(source_str)
        if len(results) > 0:
            df.loc[src_cmp][cmp] += 1

def url2str(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    json_data = soup.find('script', text=re.compile("window.location.replace") )
    refer_url_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', json_data.string)
    r = requests.get(refer_url_list[0], verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    p_tags = soup.find_all('p')
    str_all = ""
    
    for s in p_tags:
        if s.string == None:
            continue
        str_all = str_all + s.string
        
    return str_all

def main_crawler(cmp_list):
    
    df = create_df(cmp_list)
    
    news_urls_dict = {}
    news_urls_list = news_link_crawler(cmp_list, 3)
    
    for cmp in cmp_list:
        
        print('cmp: ' + cmp)
        
        ## collect news content
        print('collect news content')
        comp_str_list = []
        for url in news_urls_list[cmp]:
            s = url2str(url)

            if len(s) > 0:
                comp_str_list.append(s)
        
        ## record to df
        count = 1
        print('sizeof comp_str_list: ' + str(len(comp_str_list)))
        print('record to df')
        for comp_str in comp_str_list:
            print(count)
            df_record(df, cmp, cmp_list, comp_str)
            count += 1
    
    return df


cmp_list = []

browser = webdriver.Chrome("./chromedriver")
tw_comp_list_url = "https://www.taifex.com.tw/cht/9/futuresQADetail?fbclid=IwAR3pJIIO6ANLaKSOWM_gKIuCUqkvsSe32FcHW7odYqaw8onsXnYAETcfy00"
browser.get(tw_comp_list_url)

for i in range(2, 22):
    element = browser.find_element_by_xpath("//tr[{0}]//td[3]".format(i))
    cmp_list.append(element.text)
browser.close()

for cmp in cmp_list:
    jieba.suggest_freq(cmp, True)

print('size of cmp_list: ' + str(len(cmp_list)))


df = main_crawler(cmp_list)
df.to_csv('df.csv')

'''
new_df = pd.read_csv("df_20.csv")
new_df.set_index('0')

'''