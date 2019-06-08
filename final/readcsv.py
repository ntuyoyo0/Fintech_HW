import csv
import datetime
import pandas as pd


# def readminus(csv_name):
# 	#input:string
# 	#output:dict
# 	fp = open(csv_name,"r")
# 	flag = 1
# 	year_month_to_CD = {}
# 	for item in csv.reader(fp):
# 		if flag:
# 			flag = 0
# 			continue
# 		print(item)
# 		print(item[0])
# 		temp_datetime = datetime.datetime.strptime(item[0],"%YM%m")
# 		print(temp_datetime)
# 		temp_tuple = (temp_datetime.year,temp_datetime.month)
# 		print(temp_tuple)
# 		temp_CD = float(item[1])/52
# 		year_month_to_CD[temp_tuple] = temp_CD

# 	print(year_month_to_CD)
# 	return year_month_to_CD


def create_date_index(csv_name,start,end):
    #create date to index for the dataframe
    #input:string/datetime/datetime
    #output:dict(datetime->int)
    
    skip_row_num = 3

    fp = open(csv_name,'r', encoding='big5')
    date_to_index = {}
    index = 0

    flag = skip_row_num
    for item in csv.reader(fp):
        if flag:
            flag -= 1
            continue

        temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
        if temp_datetime < start :
            break
        elif temp_datetime > end:
            continue

        if not(temp_datetime in date_to_index):
            date_to_index[temp_datetime] = index
            index+=1

    fp.close()
    return date_to_index

def readcsv(csv_name,start,end,CD_NUMBER):
    #create dataframe of net value
    #input:string/datetime/datetime
    #output:dataframe(time,fund name)

    skip_row_num = 3
    nav_change_fieldIndex = 5
    
    date_to_index=create_date_index(csv_name,start,end)

    #create dictionary for dataframe
    date_to_dict ={}

    fp = open(csv_name,'r', encoding='big5')
    flag = skip_row_num
    for item in csv.reader(fp):
        if flag:
            flag -= 1
            continue

        temp_datetime = datetime.datetime.strptime(item[1],"%Y/%m/%d")
        #print(temp_datetime,start,end)
        if temp_datetime < start :
            break
        elif temp_datetime > end:
            continue

        if not(item[2] in date_to_dict):
            temp_list = []
            for i in range(len(date_to_index)):
                temp_list.append('x')
            try:
                temp_float = float(item[nav_change_fieldIndex]) - CD_NUMBER
            except:
                temp_float = float(0) - CD_NUMBER
            temp_list[date_to_index[temp_datetime]]=temp_float

            temp_dict = {item[2]:temp_list}
            date_to_dict.update(temp_dict)

        else:
            try:
                temp_float = float(item[nav_change_fieldIndex]) - CD_NUMBER
            except:
                temp_float = float(0) - CD_NUMBER
            date_to_dict[item[2]][date_to_index[temp_datetime]]=temp_float


    fp.close()

    #create dataframe
    df = pd.DataFrame.from_dict(date_to_dict)
    return  df


def get_closedfunds(closedfund_csv, df_nav):
    
    skip_row_num = 3
    
    fp = open(closedfund_csv,'r', encoding='utf-8')
    flag = skip_row_num
    closed_items = []
    
    for item in csv.reader(fp):
        
        if flag:
            flag -= 1
            continue
            
        if item[8] != '' and item[2] != '':
            closed_items.append(item)
    
    tmp_closed_funds = []
    for items in closed_items:
        tmp_closed_funds.append(items[2])
        
    closed_funds = [] = []
    for tmp_closed_fund in tmp_closed_funds:
        if tmp_closed_fund in df_nav.columns:
            closed_funds.append(tmp_closed_fund)
    
    return closed_funds

def readcsv_preproc(fundnav_csv, closedfund_csv, start, end, CD_NUMBER):
    
    skip_row_num = 3
    nav_change_fieldIndex = 5
    x_existRate = 0.2
    
    df = readcsv(fundnav_csv,start,end,CD_NUMBER)
    closed_funds = get_closedfunds(closedfund_csv, df)
    df = df.drop(columns=closed_funds)
    
    drop_funds = []
    n = len(df[df.columns[0]])
    for col in df.columns:
        if len(df[df[col].astype(str) == 'x']) > x_existRate * n:
            drop_funds.append(col)
    
    df = df.drop(columns=drop_funds)
    
    return df

def read_df(csv_filename):
    df_cor = pd.read_csv(csv_filename)
    df_cor = df_cor.set_index('Unnamed: 0')
    return df_cor

