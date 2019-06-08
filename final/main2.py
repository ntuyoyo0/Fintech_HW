import readcsv
import datetime
import pandas as pd
import pickle
import calculate
from operator import attrgetter

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster
import pylab

import scipy.spatial.distance as ssd

from itertools import permutations
from itertools import combinations
import numpy as np
import math

class Portfolio:
    def __init__(self, index_q, labels, weights):
        self.index_q = index_q
        self.labels = labels
        self.weights = weights
    def __str__(self):
        return 'index: ' + str(self.index_q) + '\n' + \
            'labels: ' + str(self.labels) + '\n' + \
                'weights: ' + str(self.weights)


FUNDS_CSV_NAME = 'Funds_NAV_Return.csv'
FUNDS_PREPROC_CSV_NAME = 'Funds_preproc.csv'
CLOSED_FUNDS_CSV_NAME = 'Funds_delete.csv'
CORR_CSV_NAME = 'cor_downside.csv'
CD_NUMBER = 0.6/52 #better to depend on real number, not a stable one 

max_d_downside = 4.9
ivt_loop_num = 15
candidate_num = 5

start = datetime.datetime.strptime("2016/5/31","%Y/%m/%d")
end = datetime.datetime.strptime("2019/5/31","%Y/%m/%d")

#### User Input ####
extraPortfolio_ratio = 0.25    ## the ratio that the user allow us to hold
user_selectFunds = ['26396604B', '26286281F', '26331835G']
user_selectFund_weights = [0.1, 0.3, 0.6]
user_recommend_num = 3

#### Transform user_selectFund_weights to user_portfolio_weights_arr ####
## Description: Multiply (1-extraPortfolio_ratio) to user_selectFund_weights
user_portfolio_weights_arr = (1-extraPortfolio_ratio) * np.array(user_selectFund_weights)
user_portfolio_weights = user_portfolio_weights_arr.tolist()

#### Get the Funds' data ####
## Note: Has removed the funds that were closed or have few data
df = readcsv.read_df(FUNDS_PREPROC_CSV_NAME)
print("finish df")
print('')

## TODO: Check if user_selectFunds are in df.columns

#### Get the original_cluster_dict information ####
original_cluster_dict = {}
with open('original_cluster_dict' + '.pkl', 'rb') as f:
    original_cluster_dict = pickle.load(f)
print('original number of the groups:', len(original_cluster_dict))

#### Get the bestFund_dict information ####
bestFund_dict = {}
new_bestFund_dict = {}
with open('bestFund_dict' + '.pkl', 'rb') as f:
    bestFund_dict = pickle.load(f)

#### Get the bestFund_dict excluding the groups that user_selectFund was in ####
new_bestFund_dict = calculate.cluster_preproc(original_cluster_dict, bestFund_dict, user_selectFunds)
print('number of the groups after preproc:', len(new_bestFund_dict))
print('')

#### Pick the top 5 of bestFunds ####
candidate_list = calculate.pick_candidate(new_bestFund_dict, candidate_num)

#### Calculate the orginal protfolio ####
portfolio_list = []
new_returns = calculate.newFund_return(df, user_selectFunds, user_selectFund_weights)
orginal_q = calculate.index_q(new_returns, ivt_loop_num)
orginal_protfolio = Portfolio(orginal_q, user_selectFunds, user_selectFund_weights)
portfolio_list.append(orginal_protfolio)

#### Calculate protfolios with extra funds ####
for i in range(1, user_recommend_num + 1):
    portfolios = calculate.portfolio_alloc(df, candidate_list, i, user_selectFunds, user_portfolio_weights, extraPortfolio_ratio, ivt_loop_num)
    if len(portfolios) > 0:
        min_portfolio = min(portfolios)
        portfolio_list.append(Portfolio(min_portfolio[0], min_portfolio[1], min_portfolio[2]))

recommend_portfolio = min(portfolio_list,key=attrgetter('index_q'))

#### Print the results ####
for portfolio in portfolio_list:
    print(portfolio)
    print('')

print("recommend_portfolio:")
print(recommend_portfolio)