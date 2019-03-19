import Yahoo
import pandas as pd

Yahoo_ETFs = ['VAMO','TVIX','ZIV','VIIX']
dfs = []

# crawler on Yahoo
for i in Yahoo_ETFs:
	dfs.append(Yahoo.find_ETF_value(i))

# remove "Date" column from df
for i in range(len(dfs)):
	if i != 0:
		dfs[i] = dfs[i].drop(dfs[i].columns[0],axis=1)

# concat + taggging
result = pd.concat(dfs,axis=1,ignore_index=True)
result.columns = ['Date']+Yahoo_ETFs

# result df
print(result)