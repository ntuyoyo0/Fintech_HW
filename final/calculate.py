import pandas as pd

def cal_mean(df):
	# input:df
	# output:dict

	mean={}
	for col in df:
		temp_sum = 0
		temp_num = 0
		for item in df[col]:
			if item != 'x':
				temp_sum += float(item)
				temp_num +=1
		temp_mean = float(temp_sum)/float(temp_num)
		mean[col] = temp_mean
	return mean

def cal_inner_list(a,b):
	# input:list/list
	# output:float
	sumAll=0
	numAll=0
	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x':
			sumAll += a[i]*b[i]
			numAll += 1
	
	if numAll == 0:
		return 0
	else:
		return float(sumAll)/float(numAll)

def cal_cov(df,mode):
	#input:df/string("origin" or "downside")
	#output:df
	
	# mean
	mean = cal_mean(df)

	# origin num - mean
	new_df = {}
	for col in df:
		temp_col = []
		for item in df[col]:
			if item == 'x':
				temp_col.append('x')
			elif mode=="downside": #downside
				temp_col.append(item-mean[col])
			else: #origin
				temp_col.append(min(item-mean[col],0))
		new_df[col] = temp_col

	# cov
	output_dict = {}
	for colA in df:
		temp_col = []
		for colB in df:
			covAB = cal_inner_list(new_df[colA],new_df[colB])
			temp_col.append(covAB)
		output_dict[colA] = temp_col

	output_df = pd.DataFrame.from_dict(output_dict)
	
	row_name = {}
	i = 0
	for colA in df:
		row_name[i] = colA
		i += 1
	
	output_df = output_df.rename(index=row_name)

	return output_df


def cal_co_risk(list_of_fund,ratio_of_fund,cov):
	# input:list(str)/list(float)/df
	# output: float
	risk=0
	num = len(list_of_fund)

	for i in range(num):
		weight = ratio_of_fund[i]
		variance = cov.at[list_of_fund[i],list_of_fund[i]]
		risk += weight*weight*variance

	for i in range(num):
		for j in range(num):
			if i==j:
				continue
			weight_i=ratio_of_fund[i]
			weight_j=ratio_of_fund[j]
			covariance = cov.at[list_of_fund[i],list_of_fund[j]]
			risk += weight_j*weight_i*covariance

	return risk

