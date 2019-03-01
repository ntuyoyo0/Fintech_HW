from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# input date and the lxml obj of "list of news published at that day"
# output parsed data(in list of dictionaries)
def process_doc(doc,date):
	nodes = doc.select('ul.list > li')
	data = list()

	# for every news happened at "date"
	for li in nodes:
		# no more news
		if li.select_one('a') == None:
			continue;

		# get the lxml of the news
		li_link = 'http://news.ltn.com.tw/' + li.select_one('a')['href']
		li_res = requests.get(li_link)
		li_doc = bs(li_res.text,'lxml')

		# parse the news into li_date/li_title/li_content
		li_date = datetime.strptime(date,"%Y%m%d").strftime('%Y-%m-%d')
		li_title = li.select_one('p').get_text()
		li_content = ""
		for ele in li_doc.select('div.text > p'):
			li_content += ele.get_text()

		data.append({
            'date' : li_date,
			'title': li_title,
			'link' : li_link,
			'content' : li_content,
		})
	
	return data

#  make dates a list of date form start_date to stop_date
start_date = "2018-07-01"
stop_date = "2018-07-05"

start = datetime.strptime(start_date,"%Y-%m-%d")
stop = datetime.strptime(stop_date,"%Y-%m-%d")

dates = list()
while start <= stop:
	dates.append(start.strftime('%Y%m%d'))
	start = start + timedelta(days=1)

all_data = list()
# crawling data by dates
for date in dates:
    print('start crawling :', date)
    # get the lxml obj of "list of news published at <date>"
    res = requests.get('https://news.ltn.com.tw/list/newspaper/politics/' + date)
    doc = bs(res.text, 'lxml')
    # adding to the list of dictionaries 
    all_data += process_doc(doc, date)

# make it into table-like, whose columns are date and title
table = pd.DataFrame(all_data)[['date', 'title']]
print(table)





