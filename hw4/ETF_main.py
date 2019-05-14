import Yahoo, calculate
import pandas as pd

Yahoo_ETFs_1 = ['VAMO','TVIX','ZIV','VIIX']
Yahoo_ETFs_2 = ['HTUS','FLAG','FTLS','FMF','QAI','MNA','CPI','QMN','MCRO','QLS','QED','RLY','WTMF','DYLS']
Yahoo_ETFs_3 = ['BTAL','MOM','DIVA','SIZ','CHEP','XVZ','HDG','RALS','ALTS','MRGR','SVXY','UVXY','VIXY','VIXM','DIVY']
Yahoo_ETFs = Yahoo_ETFs_1 + Yahoo_ETFs_2 + Yahoo_ETFs_3
dfs = []
INTERVAL = 7

# crawler on Yahoo
# for i in Yahoo_ETFs:
# 	Yahoo.find_ETF_value(i)
for i in Yahoo_ETFs:
	dfs.append(pd.read_csv("./data/"+i+".csv"))

# remove "Date" column from df
for i in range(len(dfs)):
	dfs[i] = dfs[i].drop(dfs[i].columns[0],axis=1)

# concat + taggging
result = pd.concat(dfs,axis=1,ignore_index=True)
result.columns = Yahoo_ETFs

# change to weekly/ monthly
drop_list = []
rename_list = {}
iterator = 0

for i in range(result.index.size):
	if i % INTERVAL == 0:
		rename_list[i] = iterator
		iterator+=1
	else:
		drop_list.append(i)

result = result.drop(result.index[drop_list])
result = result.rename(index=rename_list)

# result df
# print(result.head(10))

# return value
with_risk = calculate.cal_return(result)
# print(with_risk.head(10))

no_risk = []

if INTERVAL == 30:
	for i in range(40):
		no_risk.append(2.4/12/100)
	excess_return = calculate.minus_no_risk(with_risk,no_risk)

elif INTERVAL == 7:
	for i in range(53*3):
		no_risk.append(2.4/52/100)
	excess_return = calculate.minus_no_risk(with_risk,no_risk)

# print(excess_return.head(10))

# A
mu = calculate.mu_(excess_return)
sigma = calculate.sigma_(excess_return)
skew = calculate.skew_(excess_return)
assr = calculate.assr_(mu,sigma,no_risk,skew)
A_dict = dict(zip(result.columns,assr))
A_rank =  (calculate.sort_by_value(A_dict))
A_rank = A_rank[::-1]
A_last_dict = {}
A_last_dict["A"]=A_rank
A_last = pd.DataFrame.from_dict(A_last_dict)

# B
omega = calculate.omega_(with_risk,no_risk)
B_dict = dict(zip(result.columns,omega))
B_rank =  (calculate.sort_by_value(B_dict))
B_rank = B_rank[::-1]
B_last_dict = {}
B_last_dict["B"]=B_rank
B_last = pd.DataFrame.from_dict(B_last_dict)

# C
Q = calculate.Q_(excess_return)
C_dict = dict(zip(result.columns,Q))
C_rank =  calculate.sort_by_value(C_dict)
C_last_dict = {}
C_last_dict["C"]=C_rank
C_last = pd.DataFrame.from_dict(C_last_dict)

print(A_dict)
print(A_last.head(10))
print(B_dict)
print(B_last.head(10))
print(C_dict)
print(C_last.head(10))