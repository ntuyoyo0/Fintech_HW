from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from NER import ner

def crawler(name,start_date,end_date,list_up,list_mid,list_down):
	browser = webdriver.Chrome('./chromedriver.exe')
	url = "https://www.google.com/"
	browser.get(url)

	search = browser.find_element_by_name('q')
	search.send_keys(name)
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
	# search_date.submit()
	time.sleep(3)

	search = browser.find_elements_by_class_name("g")
	#print(search[0].get_attribute('innerHTML'))

	flag = 0
	flag2 = 0
	for item in search:
		news = item.find_element_by_css_selector("h3 a")
		print(news.text)
		#print(news.get_attribute('href'))
		output = ner(news.text,news.get_attribute('href'),list_up,list_mid,list_down)
		print(output)
		if output == "down":
			flag = flag-1
			flag2 = 1
		elif output == "up":
			flag = flag+1

		print("================")

	browser.quit()

	if flag2 == 1:
		return "down"
	else:
		return "up"
	


