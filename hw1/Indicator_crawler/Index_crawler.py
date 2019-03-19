import requests
import csv
import pandas as pd
from io import BytesIO
import datetime

#=======================================
#function for adding date 
def last_day(year,month):
	day_list=[0,31,28,31,30,31,30,31,31,30,31,30,31]
	if month!=2:
		return day_list[month]
	if year%400==0:
		return 29
	if year%100==0:
		return 28
	if year%4==0:
		return 29
	return 28
#========================================

################### Imortant!!!#####################################################  
#                                                                                  #
#  Attention users! This page will be decommissioned on March 19th.                #
#  This sentence is shown on the web page, so the url may be wrong in the future.  #
#                                                                                  #
####################################################################################
url = 'https://www.census.gov/wholesale/xls/mwts/timeseries1.xlsx'
download = requests.get(url)
df = pd.read_excel(BytesIO(download.content),header=None,sheet_name="Inventories")

#change to dict to modify the format
df_list = df.to_dict('list')
df_list.pop(0, None)
df = pd.DataFrame.from_dict(df_list)
#change back to dataframe to modify the format
df = df.drop(df.index[:17])
df = df.drop(df.columns[2:],axis=1)
#change to dict again to modify the format
df_list = df.to_dict('list')

#modify the date to python.datetime
year = -1
month = -1
temp_list = {}
temp_list_1 = []
for item in df_list[1]:
	if item != year:
		month = 12
		year = item
	temp_list_1.append(datetime.date(year, month,last_day(year,month)))
	month = month-1
temp_list[1]=temp_list_1
df_list.update(temp_list)

#change back to dataframe
df = pd.DataFrame(df_list)
df.columns = ['Date', 'Value',]
df = df[::-1]

print(df.head(20))



