import readcsv
import datetime
import pandas as pd
import calculate

CSV_NAME = '平衡型基金_NAV_Return.csv'
test_list_of_fund=['00971976','42334401A','42334401B']
test_ratio_of_fund = [0.2,0.5,0.3]
CD_NUMBER = 0.6/52 #better to depend on real number, not a stable one 

if __name__=='__main__':
	# start = datetime.datetime.strptime("2016/5/6","%Y/%m/%d")
	# end = datetime.datetime.strptime("2019/4/26","%Y/%m/%d")

	start = datetime.datetime.strptime("2016/5/6","%Y/%m/%d")
	end = datetime.datetime.strptime("2016/12/6","%Y/%m/%d")
	
	df = readcsv.readcsv(CSV_NAME,start,end,CD_NUMBER)
	print("finish df")

	# cor = calculate.cal_cor(df,"normal")
	# print(cor.head(10))
	# print("===============")
	# cov_down = calculate.cal_cov(df,"downside")
	# print(cov_down.head(10))
	# print("finish cor")

	risk = calculate.cal_co_risk(test_list_of_fund,test_ratio_of_fund,df)
	print(risk)