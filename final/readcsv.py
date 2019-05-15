import csv
import datetime
import pandas as pd

# def readminus(csv_name):
# 	#input:string
# 	#output:dict
# 	fp = open(csv_name,"r")
# 	flag = 1
# 	year_month_to_CD = {}
# 	for item in csv.reader(fp):
# 		if flag:
# 			flag = 0
# 			continue
# 		print(item)
# 		print(item[0])
# 		temp_datetime = datetime.datetime.strptime(item[0],"%YM%m")
# 		print(temp_datetime)
# 		temp_tuple = (temp_datetime.year,temp_datetime.month)
# 		print(temp_tuple)
# 		temp_CD = float(item[1])/52
# 		year_month_to_CD[temp_tuple] = temp_CD

# 	print(year_month_to_CD)
# 	return year_month_to_CD


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

def readcsv(csv_name,start,end,CD_NUMBER):
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
				temp_list.append('x')
			temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
			try:
				temp_float = float(item[6]) - CD_NUMBER
			except:
				temp_float = float(0) - CD_NUMBER
			temp_list[date_to_index[temp_datetime]]=temp_float

			temp_dict = {item[2]:temp_list}
			date_to_dict.update(temp_dict)
		else:
			temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
			try:
				temp_float = float(item[6]) - CD_NUMBER
			except:
				temp_float = float(0) - CD_NUMBER
			date_to_dict[item[2]][date_to_index[temp_datetime]]=temp_float

	fp.close()

	#create dataframe
	df = pd.DataFrame.from_dict(date_to_dict)
	return  df

