from selenium import webdriver
import time, datetime
import requests
import csv, xlrd
import pandas as pd
from io import BytesIO

def find_ETF_value(ETF_NAME):

	# for caculating start time and end time
	time1 = datetime.datetime(2015,12,31,0,0,0,0) - datetime.datetime(1970,1,1,0,0,0,0)
	start_time = int(time1.total_seconds())
	time2 = datetime.datetime.now() - datetime.datetime(1970,1,1,0,0,0,0)
	end_time = int(time2.total_seconds())
	#print(start_time,end_time)

	# activate chrome driver
	browser = webdriver.Chrome("./chromedriver.exe")
	url = "https://finance.yahoo.com/quote/"+ETF_NAME+"/history?period1="+str(start_time)+"&period2="+str(end_time)+"&interval=1d&filter=history&frequency=1d"
	browser.get(url)

	# get the url of csv
	a_s = browser.find_elements_by_css_selector("a")
	for i in a_s:
		if i.get_attribute("download")==ETF_NAME+".csv":
			csv_url = i.get_attribute("href")
			break
	#print(csv_url)

	# download csv to dataframe
	download = requests.post(csv_url)
	df = pd.read_csv(BytesIO(download.content))
	df = df.drop(df.columns[[1,2,3,4,6]],axis=1)

	#print(df.head(20))

	browser.quit()

	return df




	# no use
	"""
	#browser.execute_script("window.scrollTo(0, 5000)") 
	table = browser.find_element_by_css_selector("table")
	innertable = table.find_element_by_css_selector("tbody")
	trs = innertable.find_elements_by_css_selector("tr")
	for i in trs:
		#print(i.text)
		tds = i.find_elements_by_css_selector("td")
		for j in tds:
			print(j.text)
	#print(innertable.text)
	"""



