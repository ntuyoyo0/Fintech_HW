import issuer_crawler
import pandas as pd

chrome_driver_path = './chromedriver'
# etf_alt_file = './source_csv_files/Alternatives ETF List (35).csv'
# etf_vol_file = './source_csv_files/Volatility ETF List (18).csv'
# info_file = './csv_files/info.csv'
# download_location = './'

# df_info = pd.read_csv(info_file)

issuer_crawler.WisdomTree(df_info)
issuer_crawler.IndexIQ(df_info)
issuer_crawler.SPDR(df_info)
issuer_crawler.FirstTrust(df_info)
issuer_crawler.ETC(df_info)


