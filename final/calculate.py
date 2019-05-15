import pandas as pd

def cal_cov_list(a,b,mode):
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

	# cov
	sumAll=0

	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x' and mode=="normal":
			sumAll += (a[i]-meanA)*(b[i]-meanB)
		elif a[i]!='x' and b[i]!='x' and mode=="downside":
			sumAll += min((a[i]-meanA),0)*min((b[i]-meanB),0)

	return float(sumAll)/float(numAll)

def cal_cov(df,mode):
	#input:df/string("origin" or "downside")
	#output:df

	output_dict = {}
	for colA in df:
		temp_col = []
		for colB in df:
			covAB = cal_cov_list(df[colA],df[colB],mode)
			temp_col.append(covAB)
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

