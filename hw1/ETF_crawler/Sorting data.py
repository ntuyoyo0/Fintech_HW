import pandas as pd
import datetime

etf = pd.read_excel('ETF_Vol_Alt_Group16.xlsx', 'Updated ETF list',usecols='A,C',header=0)
df = pd.DataFrame(etf)
df.set_index('Issuer', inplace=True)
print(df)

dates = {'Date': pd.date_range(start='2015-12-31', end='2019-03-15')}
data = pd.DataFrame(data=dates)
data['Date'] = pd.to_datetime(data['Date']) 


print (data)


#Symbols by issuer
ProShares=df.at['ProShares','Symbol']
print(ProShares)

AGFiQ=df.at['AGFiQ Asset Management','Symbol']
print(AGFiQ)

Barclays=df.at['Barclays Capital','Symbol']
print(Barclays)

Reality=df.at['Reality Shares','Symbol']
print(Reality)


#ProShares
for symbol in ProShares:
    etf= pd.read_csv(symbol+'.csv',usecols = ['Date', 'NAV'])
    df = pd.DataFrame(etf)
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df.set_index('Date')
    df.rename(columns={'NAV': symbol}, inplace=True)
    df=(df.truncate(after = '2015-12-31'))
    print(df.head(5))

    data = pd.merge(data,df,on = 'Date')  
    
print(data.head(5))

#AGFiQ:
etf= pd.read_excel('BTAL.xlsx','Sheet1',usecols = 'A:F')
df = pd.DataFrame(etf)
df['Date'] = pd.to_datetime(df['Date']) 
df = df.set_index('Date')
df.rename(columns={'MOM NAV': 'MOM','SIZ NAV': 'SIZ','CHEP NAV': 'CHEP','BTAL NAV': 'BTAL'}, inplace=True)
print(df.head(5))

data = pd.merge(data,df,on = 'Date')
print(data.head(5))

#Barclays
etf= pd.read_csv( 'XVZ.csv',usecols=['Date', 'Note IV*'])
df = pd.DataFrame(etf)
df['Date'] = pd.to_datetime(df['Date'],format='%Y/%m/%d', errors='coerce')
df.rename(columns={'Note IV*': 'XVZ'}, inplace=True)
df = df.set_index('Date')
print(df.head(5))

data = pd.merge(data,df,on = 'Date')
print(data.head(5))

#Reality
etf= pd.read_csv( 'DIVY.csv',usecols=['Date', 'Adj Close'])
df = pd.DataFrame(etf)
df['Date'] = pd.to_datetime(df['Date'],format='%Y/%m/%d', errors='coerce')
df.rename(columns={'Adj Close': 'DIVY'}, inplace=True)
df = df.set_index('Date')
print(df.head(5))

data = pd.merge(data,df,on = 'Date')
print(data.head(5))

data.to_excel('NAV.xlsx', sheet_name='NAV')

