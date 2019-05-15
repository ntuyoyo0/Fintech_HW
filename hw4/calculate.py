import pandas as pd
import numpy as np
from scipy import stats
from math import sqrt, exp
from sympy import symbols, solve

def sort_by_value(d): 
	items=d.items() 
	backitems=[[v[1],v[0]] for v in items] 
	backitems.sort() 
	return [ backitems[i][1] for i in range(0,len(backitems))] 

def cal_return(df):
	#input:df
	#output:df
	newdf = df.copy()
	for col in df:
		flag = 0
		pre_num = df.at[0,col]
		for row in df.index:
			if flag == 0:
				newdf.at[row,col] = 0
				flag = 1
			elif pre_num == 0:
				newdf.at[row,col] = 0
			else:
				newdf.at[row,col] = float(df.at[row,col]-pre_num)/float(pre_num)
			pre_num = df.at[row,col]

	return newdf

def minus_no_risk(df,risk_list):
	#input:df
	#output:df
	newdf = df.copy()
	for col in df:
		for row in df.index:
			newdf.at[row,col] = df.at[row,col] - risk_list[row]

	return newdf

def mu_(excess_return):
	temp = []
	for col in excess_return:
		temp.append(np.mean(excess_return[col]))
	return temp

def sigma_(excess_return):
	temp = []
	for col in excess_return:
		temp.append(np.std(excess_return[col]))
	return temp

def skew_(excess_return):
	temp = []
	for col in excess_return:
		temp.append(stats.skew(excess_return[col]))
	return temp


def assr_(mu,sigma,no_risk,skew):
	temp =[]
	for i in range(len(mu)):
		SR = (mu[i]-no_risk[i])/sigma[i];
		assr = SR*sqrt(1+2*skew[i]*SR/3)
		temp.append(assr)
	return temp

def omega_(with_risk,no_risk):
	temp = []
	for col in with_risk:
		plus = 0
		plus_num = 0
		minus = 0
		minus_num = 0
		for row in with_risk.index:
			if with_risk.at[row,col] > no_risk[row]:
				plus += with_risk.at[row,col] - no_risk[row]
				plus_num += 1
			elif with_risk.at[row,col] < no_risk[row]:
				minus += no_risk[row] - with_risk.at[row,col]
				minus_num +=1
		sharp = (plus/plus_num)/(minus/minus_num) - 1
		temp.append(sharp)
	return temp

def Q_(df):
	temp = []
	for col in df:
		function = "0"
		x = symbols('x')
		num = 0
		for row in df.index:
			data = round(df.at[row,col],5)
			function += "+x**"+str(data)
			num += 1

		function += "-" + str(num)
		print(function)
		ans = solve(function+"-"+str(num),x)
		print(ans)
		# temp.append(ans)

	return temp
	

