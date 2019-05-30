import pandas as pd
from math import sqrt

def cal_cor_list(a,b,mode="normal"):
	# input:list/list
	# output:float

	# mean 
	temp_sumA = 0
	temp_sumB = 0
	numAll = 0
	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x':
			temp_sumA += a[i]
			temp_sumB += b[i]
			numAll += 1

	# no intersection
	if numAll == 0:
		return 0

	meanA = float(temp_sumA)/float(numAll)
	meanB = float(temp_sumB)/float(numAll)

	# cor
	sumAll=0
	sumA = 0
	sumB = 0

	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x' and mode=="normal":
			sumAll += (a[i]-meanA)*(b[i]-meanB)
			sumA += (a[i]-meanA)*(a[i]-meanA)
			sumB += (b[i]-meanB)*(b[i]-meanB)
		elif a[i]!='x' and b[i]!='x' and mode=="downside":
			sumAll += min((a[i]-meanA),0)*min((b[i]-meanB),0)
			sumA += min((a[i]-meanA),0)*min((a[i]-meanA),0)
			sumB += min((b[i]-meanB),0)*min((b[i]-meanB),0)

	# no downside relation
	if sumA==0 or sumB==0:
		return 0


	return float(sumAll)/sqrt(float(sumA)*float(sumB))

def cal_cor(df,mode):
	#input:df/string("origin" or "downside")
	#output:df

	output_dict = {}
	for colA in df:
		temp_col = []
		for colB in df:
			corAB = cal_cor_list(df[colA],df[colB],mode)
			temp_col.append(corAB)
		output_dict[colA] = temp_col
		print(colA)

	output_df = pd.DataFrame.from_dict(output_dict)
	
	row_name = {}
	i = 0
	for colA in df:
		row_name[i] = colA
		i += 1
	
	output_df = output_df.rename(index=row_name)

	return output_df

def cal_cov_list(colA,colB,meanA,meanB,useful,mode):
	covAB = 0
	for i in useful:
		if mode == "normal":
			covAB += (colA[i]-meanA)*(colB[i]-meanB)
		elif mode == "downside":
			covAB += min((colA[i]-meanA),0)*min((colB[i]-meanB),0)
	return covAB


def cal_co_risk(list_of_fund,ratio_of_fund,raw_data,mode="normal"):
	# input:list(str)/list(float)/df
	# output: float
	
	fund_num = len(list_of_fund)
	data_num = len(raw_data[list_of_fund[0]])

	#useful data
	useful = []
	for i in range(data_num):
		flag = 0
		for j in range(fund_num):
			if raw_data.iat[i,j] == 'x':
				flag+=1

		if flag == 0:
			useful.append(i)

	#mean list
	mean = []
	for i in range(fund_num):
		temp_sum = 0
		for j in useful:
			temp_sum += raw_data.iat[j,i]
		mean.append(float(temp_sum)/float(len(useful)))

	#calculate
	risk=0
	for i in range(fund_num):
		for j in range(fund_num):
			colA = raw_data[list_of_fund[i]]
			colB = raw_data[list_of_fund[j]]
			covAB = cal_cov_list(colA,colB,mean[i],mean[j],useful,mode)
			risk += ratio_of_fund[i]*ratio_of_fund[j]*covAB

	return risk

