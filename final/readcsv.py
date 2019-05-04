import csv
import datetime
import pandas as pd

def create_date_index(csv_name):
	#create date to index for the dataframe
	#input:string
	#output:dict(datetime->int)

	fp = open(csv_name,'r')
	date_to_index = {}
	index = 0

	flag = 1
	for item in csv.reader(fp):
		if flag:
			flag=0
			continue

		temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
		if not(temp_datetime in date_to_index):
			date_to_index[temp_datetime] = index
			index+=1
	fp.close()
	return date_to_index

def current(current_name):
	#cuculate current ratio
	#input:str
	#output:float

	if current_name=="NTD":
		return 1
	if current_name=="USD":
		return 30.87
	if current_name=="RMB":
		return 4.58
	if current_name=="AUD":
		return 21.67
	if current_name=="ZAR":
		return 2.15
		
	return 1

def readcsv(csv_name,start,end):
	#create dataframe of net value
	#input:string/datetime/datetime
	#output:dataframe(time,fund name)

	date_to_index=create_date_index(csv_name)

	#create dictionary for dataframe
	date_to_dict ={}

	fp = open(csv_name,'r')
	flag = 1
	for item in csv.reader(fp):
		if flag:
			flag=0
			continue

		if not(item[2] in date_to_dict):
			temp_list = []
			for i in range(len(date_to_index)):
				temp_list.append(float(0))
			temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
			temp_float = current(item[3]) * float(item[4].replace(',',''))
			temp_list[date_to_index[temp_datetime]]=temp_float

			temp_dict = {item[2]:temp_list}
			date_to_dict.update(temp_dict)
		else:
			temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
			temp_float = current(item[3]) * float(item[4].replace(',',''))
			date_to_dict[item[2]][date_to_index[temp_datetime]]=temp_float

	fp.close()

	#create dataframe
	df = pd.DataFrame.from_dict(date_to_dict)
	return  df

