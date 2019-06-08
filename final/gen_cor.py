import readcsv
import calculate
import datetime
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm

CSV_NAME = '平衡型基金_NAV_Return.csv'
FUNDS_CSV_NAME = 'Funds_NAV_Return.csv'
CLOSED_FUNDS_CSV_NAME = 'Funds_delete.csv'
CORR_CSV_NAME = 'cor_downside.csv'


CD_NUMBER = 0.6/52 #better to depend on real number, not a stable one 

start = datetime.datetime.strptime("2016/5/31","%Y/%m/%d")
end = datetime.datetime.strptime("2019/5/31","%Y/%m/%d")

df = readcsv.readcsv_preproc(FUNDS_CSV_NAME, CLOSED_FUNDS_CSV_NAME, start, end, CD_NUMBER)
print('len(df.columns):', len(df.columns))
print("finish df")

cor_downside = calculate.cal_cor(df,"downside")
cor_downside.to_csv(CORR_CSV_NAME)

## Skip calculating the correlation
# cor_downside = readcsv.read_df(CORR_CSV_NAME)
# print('len(cor_downside.columns):', len(cor_downside.columns))
# print("finish df")

index = 'downside'
size = 100
fig, ax = plt.subplots(figsize=(size, size))
ax.matshow(cor_downside,cmap=cm.get_cmap('coolwarm'), vmin=-1,vmax=1)
plt.xticks(range(len(cor_downside.columns)), cor_downside.columns, rotation='vertical', fontsize=30);
plt.yticks(range(len(cor_downside.columns)), cor_downside.columns, fontsize=30);
plt.savefig('correlation matrix_'+index+'.png')