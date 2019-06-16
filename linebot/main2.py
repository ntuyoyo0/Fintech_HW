import datetime, pickle
import calculate, readcsv

import pandas as pd
import numpy as np
import scipy.spatial.distance as ssd

from models import Portfolio
from operator import attrgetter
from itertools import permutations, combinations
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster

from linebot.models import *

FUNDS_PREPROC_CSV_NAME = 'Funds_preproc.csv'
ivt_loop_num = 15
candidate_num = 5

start = datetime.datetime.strptime("2016/5/31","%Y/%m/%d")
end = datetime.datetime.strptime("2019/5/31","%Y/%m/%d")

def recommend(user_input,line_bot_api,user_id):
    #### User Input ####
    extraPortfolio_ratio = user_input.extraPortfolio_ratio 
    user_selectFunds = user_input.user_selectFunds
    user_selectFund_weights = user_input.user_selectFund_weights
    user_recommend_num = user_input.user_recommend_num

    #### Transform user_selectFund_weights to user_portfolio_weights_arr ####
    ## Description: Multiply (1-extraPortfolio_ratio) to user_selectFund_weights
    user_portfolio_weights_arr = (1-extraPortfolio_ratio) * np.array(user_selectFund_weights)
    user_portfolio_weights = user_portfolio_weights_arr.tolist()

    #### Get the Funds' data ####
    ## Note: Has removed the funds that were closed or have few data
    message = TextSendMessage(text="讀取基金資料\U0010005E...")
    line_bot_api.push_message(user_id,message)
    df = readcsv.read_df(FUNDS_PREPROC_CSV_NAME)

    ## Check if user_selectFunds are in df.columns
    for fund in user_selectFunds:
        if not (fund in df.columns):
            return None,None

    #### Get the original_cluster_dict information ####
    original_cluster_dict = {}
    with open('original_cluster_dict' + '.pkl', 'rb') as f:
        original_cluster_dict = pickle.load(f)


    #### Get the bestFund_dict information ####
    bestFund_dict = {}
    new_bestFund_dict = {}
    with open('bestFund_dict' + '.pkl', 'rb') as f:
        bestFund_dict = pickle.load(f)

    #### Get the bestFund_dict excluding the groups that user_selectFund was in ####
    message = TextSendMessage(text="Pre-processing\U0010005E...")
    line_bot_api.push_message(user_id,message)
    new_bestFund_dict = calculate.cluster_preproc(original_cluster_dict, bestFund_dict, user_selectFunds)

    #### Pick the top 5 of bestFunds ####
    candidate_list = calculate.pick_candidate(new_bestFund_dict, candidate_num)

    #### Calculate the orginal protfolio ####
    portfolio_list = []
    new_returns = calculate.newFund_return(df, user_selectFunds, user_selectFund_weights)
    orginal_q = calculate.index_q(new_returns, ivt_loop_num)

    co_risk = calculate.cal_co_risk(user_selectFunds,user_selectFund_weights,df,"downside")
    co_return = calculate.cal_co_return(user_selectFunds,user_selectFund_weights,df)
    # print(co_risk,co_return)
    orginal_protfolio = Portfolio(orginal_q, user_selectFunds, user_selectFund_weights,co_return/co_risk)
    portfolio_list.append(orginal_protfolio)

    #### Calculate protfolios with extra funds ####
    message = TextSendMessage(text="計算中(這可能會花點時間\U0010005E)...")
    line_bot_api.push_message(user_id,message)
    for i in range(1, user_recommend_num + 1):
        portfolio = calculate.portfolio_alloc(df, candidate_list, i, user_selectFunds, user_portfolio_weights, extraPortfolio_ratio, ivt_loop_num)
        if portfolio != None:
            portfolio_list.append(portfolio)
        
    recommend_portfolio = min(portfolio_list,key=attrgetter('index_q'))


    number_to_name = {}
    with open('label2name_dict' + '.pkl', 'rb') as f:
        number_to_name = pickle.load(f)

    temp_labels = []
    for item in orginal_protfolio.labels:
        temp_labels.append(number_to_name.get(item,"Unkown name") + "(" + item + ")")
    orginal_protfolio.labels = temp_labels

    # ori = rec
    if len(orginal_protfolio.labels) == len(recommend_portfolio.labels):
        return orginal_protfolio, recommend_portfolio

    temp_labels = []
    for item in recommend_portfolio.labels:
        temp_labels.append(number_to_name.get(item,"Unkown name") + "(" + item + ")")
    recommend_portfolio.labels = temp_labels

    return orginal_protfolio, recommend_portfolio