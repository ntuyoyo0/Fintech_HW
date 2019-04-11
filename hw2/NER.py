from bs4 import BeautifulSoup as bs
import requests
from hanziconv import HanziConv
import jieba

def udn(title,url):
	res = requests.get(url)
	doc = bs(res.text,"lxml")
	try:
		news_content = doc.find(id="story_body_content")
		paras = news_content.find_all('p')
		content = ""
		for item in paras:
			content = content + item.get_text()
		return content
	except:
		return ""

def yahoo(title,url):
	res = requests.get(url)
	doc = bs(res.text,"lxml")
	try:
		news_content = doc.find_all("td",class_="yui-text-left")
		paras = news_content[0].find_all('p')
		content = ""
		for item in paras:
			content = content + item.get_text()
		return content
	except:
		return ""

def chinatimes(title,url):
	res = requests.get(url)
	doc = bs(res.text,"lxml")
	try:
		news_content = doc.find_all("div",class_="article-body")
		paras = news_content[0].find_all('p')
		content = ""
		for item in paras:
			content = content + item.get_text()
		return content
	except:
		return ""

def ltn(title,url):
	res = requests.get(url)
	doc = bs(res.text,"lxml")
	try:
		news_content = doc.find_all("div",class_="text")
		paras = news_content[0].find_all('p')
		content = ""
		for item in paras:
			content = content + item.get_text()
		return content
	except:
		return ""

def ner(title,url,list_up,list_mid,list_down):
	if "udn" in url:
		content = udn(title,url)
	elif "yahoo" in url:
		content = yahoo(title,url)
	elif "chinatimes" in url:
		content = chinatimes(title,url)
	elif "ltn" in url:
		content = ltn(title,url)
	else:
		content = ""

	seg_list = jieba.cut(HanziConv.toSimplified(title+content))
	words = []
	delete_list = ["、","-","：","，","。"]
	for item in seg_list:
		if item in delete_list:
			continue
		else:
			words.append(HanziConv.toTraditional(item))

	count_up = 0
	count_mid = 0
	count_down = 0

	for item in words:
		if item in list_up:
			count_up = count_up + 1
		elif item in list_mid:
			count_mid = count_mid + 1
		elif item in list_down:
			count_down = count_down + 1
	print("{0},{1},{2}".format(count_up,count_mid,count_down))

	if count_up==0 and count_mid==0 and count_down==0:
		return "mid"
	elif count_down>count_up and count_down>count_mid:
		return "down"
	else:
		return "up"
	