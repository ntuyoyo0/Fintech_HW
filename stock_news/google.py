from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup as bs
from models import News
import pandas as pd

def crawler(name,start_date,end_date,month):

	browser = webdriver.Chrome('./chromedriver.exe')
	url = "https://www.google.com/"
	browser.get(url)

	search = browser.find_element_by_name('q')
	search.send_keys(name + " " + "鉅亨網")
	search.send_keys(Keys.RETURN)
	time.sleep(3)

	search = browser.find_elements_by_css_selector("a")
	for item in search:
		if item.text == "新聞":
			item.click()
			break
	time.sleep(3)

	advances = browser.find_elements_by_css_selector("a")
	for item in advances:
		if item.text == "工具":
			advance = item
			break
	advance.click()
	time.sleep(1)

	arounds = browser.find_elements_by_class_name("hdtb-mn-hd")
	for item in arounds:
		if item.text == "最近":
			around = item
			break
	around.click()
	time.sleep(1)

	customizes = browser.find_elements_by_class_name("q")
	for item in customizes:
		if item.text == "自訂日期範圍...":
			customize = item
			break
	customize.click()
	time.sleep(1)

	start = browser.find_element_by_id("cdr_min")
	end = browser.find_element_by_id("cdr_max")
	search_date = browser.find_element_by_class_name("cdr_go")
	start.send_keys(start_date)
	end.send_keys(end_date)	
	end.send_keys(Keys.ENTER)
	time.sleep(3)


	flag=0
	stock_news = []

	while flag <10:
		flag=0
		search = browser.find_elements_by_class_name("g")

		for item in search:
			news = item.find_element_by_css_selector("h3 a")
			url = news.get_attribute('href')
			if 'cnyes' in url:
				# print(news.text)
				res = requests.get(url)
				doc = bs(res.text,"lxml")
				content = []
				try:
					paras = doc.find_all('p')
					for item in paras:
						content.append(item.get_text())
					timestamp = doc.find_all("time")
					stock_news.append(News(news.text,content,timestamp[0].get_text(),url))
				except:
					pass

				# print("================")
			else:
				flag = flag+1

		nexts = browser.find_elements_by_tag_name('span')
		for item in nexts:
			if item.text == "下一頁":
				item.click()
				break
		else:
			break


	browser.quit()
	# for item in stock_news:
	# 	print(item.title,item.timestamp,item.link)
	# 	print("=======")

	pd_file = pd.DataFrame.from_records([i.to_dict() for i in stock_news])
	pd_file.to_csv("./result/" + name +"_" + month + ".txt")
	pd_file.to_csv("./result/" + name +"_" + month + ".csv")
	


