import pandas as pd

def cal_co_risk(num,list_of_fund,ratio_of_fund,cov):
	risk=0

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

