from stock_crawler import crawler
import jieba
import pandas as pd

def num(string):
	if string == "down":
		return 1
	if string == "up":
		return 0

stocks1 = ['台泥','亞泥','統一','台塑','南亞','台化','遠東新','中鋼','正新','和泰車']
stocks2 = ['光寶科','聯電','台達電','鴻海','國巨','台積電','華碩','廣達','研華','南亞科']
stocks3 = ['友達','中華電','聯發科','可成','台灣高鐵','彰銀','中壽','華南金','富邦金','國泰金']
stocks4 = ['開發金','玉山金','元大金','兆豐金','台新金','永豐金','中信金','第一金','統一超','大立光']
stocks5 = ['台灣大','群創','日月光投控','遠傳','和碩','中租-KY','上海商銀','合庫金','台塑化','寶成']

stocks = stocks1 + stocks2

list_up = []
list_mid = []
list_down = []

fp_up = open("up.txt","r",encoding = 'utf8')
fp_mid = open("mid.txt","r",encoding = 'utf8')
fp_down = open("down.txt","r",encoding = 'utf8')

for line in fp_up.readlines():
	list_up.append(line.strip('\n'))
fp_up.close()
for line in fp_mid.readlines():
	list_mid.append(line.strip('\n'))
fp_mid.close()
for line in fp_down.readlines():
	list_down.append(line.strip('\n'))
fp_down.close()

start_time = ['11/1/2018','12/1/2018','1/1/2019','2/1/2019','3/1/2019']
end_time = ['11/30/2018','12/31/2018','1/31/2019','2/28/2019','3/31/2019']

dictionary = {}
for item in stocks:
	col = []
	for i in range(len(start_time)):
		col.append(num(crawler(item,start_time[i],end_time[i],list_up,list_mid,list_down)))
	dictionary.update({item:col})

df = pd.DataFrame(dictionary)
coocc = df.T.dot(df)
print(df)
print(coocc)
coocc.to_csv("./out.csv",encoding="utf_8")
