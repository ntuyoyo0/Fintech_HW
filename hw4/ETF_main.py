import Yahoo
import pandas as pd

Yahoo_ETFs_1 = ['VAMO','TVIX','ZIV','VIIX']
Yahoo_ETFs_2 = ['HTUS','FLAG','FTLS','FMF','QAI','MNA','CPI','QMN','MCRO','QLS','QED','RLY','WTMF','DYLS']
Yahoo_ETFs_3 = ['BTAL','MOM','DIVA','SIZ','CHEP','XVZ','HDG','RALS','ALTS','MRGR','SVXY','UVXY','VIXY','VIXM','DIVY']
Yahoo_ETFs = Yahoo_ETFs_1 + Yahoo_ETFs_2 + Yahoo_ETFs_3
dfs = []
INTERVAL = 30

# crawler on Yahoo
for i in Yahoo_ETFs_1:
	dfs.append(Yahoo.find_ETF_value(i))

# remove "Date" column from df
for i in range(len(dfs)):
	dfs[i] = dfs[i].drop(dfs[i].columns[0],axis=1)

# concat + taggging
result = pd.concat(dfs,axis=1,ignore_index=True)
result.columns = Yahoo_ETFs_1

# change to weekly/ monthly
drop_list = []
for i in range(840):
	if i % INTERVAL == 0:
		continue
	else:
		drop_list.append(i)

result = result.drop(result.index[drop_list])

# result df
print(result)