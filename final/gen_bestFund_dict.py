import readcsv
import datetime
import pandas as pd
import pickle
import calculate

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster
import pylab

import scipy.spatial.distance as ssd

import matplotlib.pyplot as plt
from itertools import permutations
from itertools import combinations
import numpy as np
import math

FUNDS_CSV_NAME = 'Funds_NAV_Return.csv'
CLOSED_FUNDS_CSV_NAME = 'Funds_delete.csv'
FUNDS_PREPROC_CSV_NAME = 'Funds_preproc.csv'
CORR_CSV_NAME = 'cor_downside.csv'
CD_NUMBER = 0.6/52 #better to depend on real number, not a stable one 

max_d_downside = 4.9
ivt_loop_num = 15
candidate_num = 5


df = readcsv.read_df(FUNDS_PREPROC_CSV_NAME)
print("finish df")
print('')

df_cor_downside = readcsv.read_df(CORR_CSV_NAME)
Z_downside = calculate.gen_Z(df_cor_downside)
clusters_downside = fcluster(Z_downside, max_d_downside, criterion='distance')
clusters_downside_dict = calculate.cluster_grouping(clusters_downside, df_cor_downside)
print('original number of the groups:', len(clusters_downside_dict))

original_cluster_dict = {}
for i in range(len(clusters_downside_dict)):
    original_cluster_dict[i] = clusters_downside_dict[i+1]

with open('original_cluster_dict' + '.pkl', 'wb') as f:
        pickle.dump(original_cluster_dict, f, pickle.HIGHEST_PROTOCOL)
print('generate original_cluster_dict.pkl')

bestFund_dict = calculate.pick_bestFund(original_cluster_dict, df, ivt_loop_num)
with open('bestFund_dict' + '.pkl', 'wb') as f:
        pickle.dump(bestFund_dict, f, pickle.HIGHEST_PROTOCOL)
print('generate bestFund_dict.pkl')
