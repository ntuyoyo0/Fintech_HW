import readcsv
import datetime
import pandas as pd
import calculate

CSV_NAME = '平衡型基金.csv'
test_num = 3
test_list_of_fund=['00971976','42334401A','42334401B']
test_ratio_of_fund = [0.2,0.5,0.3]

if __name__=='__main__':
	start = datetime.datetime.strptime("2016/5/6","%Y/%m/%d")
	end = datetime.datetime.strptime("2019/4/26","%Y/%m/%d")
	
	df = readcsv.readcsv(CSV_NAME,start,end)
	corr = df.corr()
	cov = df.cov()

	risk = calculate.cal_co_risk(test_num,test_list_of_fund,test_ratio_of_fund,cov)
	print(risk)