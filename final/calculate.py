import pandas as pd
import numpy as np
import math
from math import sqrt

import matplotlib.pyplot as plt
from itertools import permutations
from itertools import combinations

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster
import scipy.spatial.distance as ssd
import pylab

import scipy.spatial.distance as ssd

def cal_cor_list(a,b,mode="normal"):
	# input:list/list
	# output:float

	# mean 
	temp_sumA = 0
	temp_sumB = 0
	numAll = 0
	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x':
			temp_sumA += a[i]
			temp_sumB += b[i]
			numAll += 1

	# no intersection
	if numAll == 0:
		return 0

	meanA = float(temp_sumA)/float(numAll)
	meanB = float(temp_sumB)/float(numAll)

	# cor
	sumAll=0
	sumA = 0
	sumB = 0

	for i in range(len(a)):
		if a[i]!='x' and b[i]!='x' and mode=="normal":
			sumAll += (a[i]-meanA)*(b[i]-meanB)
			sumA += (a[i]-meanA)*(a[i]-meanA)
			sumB += (b[i]-meanB)*(b[i]-meanB)
		elif a[i]!='x' and b[i]!='x' and mode=="downside":
			sumAll += min((a[i]-meanA),0)*min((b[i]-meanB),0)
			sumA += min((a[i]-meanA),0)*min((a[i]-meanA),0)
			sumB += min((b[i]-meanB),0)*min((b[i]-meanB),0)

	# no downside relation
	if sumA==0 or sumB==0:
		return 0


	return float(sumAll)/sqrt(float(sumA)*float(sumB))

def cal_cor(df,mode):
	#input:df/string("origin" or "downside")
	#output:df

	output_dict = {}
	for colA in df:
		temp_col = []
		for colB in df:
			corAB = cal_cor_list(df[colA],df[colB],mode)
			temp_col.append(corAB)
		output_dict[colA] = temp_col
		print(colA)

	output_df = pd.DataFrame.from_dict(output_dict)
	
	row_name = {}
	i = 0
	for colA in df:
		row_name[i] = colA
		i += 1
	
	output_df = output_df.rename(index=row_name)

	return output_df

def cal_cov_list(colA,colB,meanA,meanB,useful,mode):
	covAB = 0
	for i in useful:
		if mode == "normal":
			covAB += (colA[i]-meanA)*(colB[i]-meanB)
		elif mode == "downside":
			covAB += min((colA[i]-meanA),0)*min((colB[i]-meanB),0)
	return covAB


def cal_co_risk(list_of_fund,ratio_of_fund,raw_data,mode="normal"):
	# input:list(str)/list(float)/df
	# output: float
	
	fund_num = len(list_of_fund)
	data_num = len(raw_data[list_of_fund[0]])

	#useful data
	useful = []
	for i in range(data_num):
		flag = 0
		for col in list_of_fund:
			if raw_data[col][i] == 'x':
				flag+=1
			print(col,i)
		if flag == 0:
			useful.append(i)

	#mean list
	mean = []
	for col in list_of_fund:
		temp_sum = 0
		for j in useful:
			temp_sum += raw_data[col][j]
		mean.append(float(temp_sum)/float(len(useful)))

	#calculate
	risk=0
	for i in range(fund_num):
		for j in range(fund_num):
			colA = raw_data[list_of_fund[i]]
			colB = raw_data[list_of_fund[j]]
			covAB = cal_cov_list(colA,colB,mean[i],mean[j],useful,mode)
			risk += ratio_of_fund[i]*ratio_of_fund[j]*covAB

	return risk

def cal_co_return(list_of_fund,ratio_of_fund,raw_data):
	# input:list(str)/list(float)/df
	# output: float
	
	fund_num = len(list_of_fund)
	data_num = len(raw_data[list_of_fund[0]])

	#useful data
	useful = []
	for i in range(data_num):
		flag = 0
		for col in list_of_fund:
			print(col,i)
			if raw_data[col][i] == 'x':
				flag+=1

		if flag == 0:
			useful.append(i)

	#mean list
	mean = []
	for col in list_of_fund:
		temp_sum = 0
		for j in useful:
			temp_sum += raw_data[col][j]
		mean.append(float(temp_sum)/float(len(useful)))

	# calculate return
	all_return = 0
	for i in range(fund_num):
		all_return += ratio_of_fund[i]*mean[i]

	return all_return


def cor2dist(cor, amp_factor):
    
    col_num = len(cor.columns)
    
    for col in cor.columns:
        cor[col] = cor[col].mask(cor[col] > 1, 1)
    
    dist = (1-cor) * amp_factor
      
    for col in cor.columns:
        dist[col][col] = 0
    
    return dist

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             size=50,
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

def gen_Z(df_cor):
    dist = cor2dist(df_cor, 10)
    distArray = ssd.squareform(dist) 
    Z = linkage(distArray, 'average')
    return Z

def plot_clusterTree(Z, labels, mode):
    index = mode
    plt.figure(figsize=(80, 25))
    labelsize=20
    ticksize=15
    plt.title('Hierarchical Clustering Dendrogram for '+index, fontsize=labelsize)
    plt.xlabel('fund', fontsize=labelsize)
    plt.ylabel('distance', fontsize=labelsize)
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=18.,  # font size for the x axis labels
        labels = labels
    )
    pylab.yticks(fontsize=ticksize)
    pylab.xticks(rotation=-90, fontsize=ticksize)
    plt.savefig('dendogram_'+index+'.png')
    plt.show()
    
def plot_clusterTree_withThreshold(Z, labels, max_d, mode):
    index = mode
    plt.figure(figsize=(80, 25))
    labelsize=50
    ticksize=50
    plt.title('Hierarchical Clustering Dendrogram for '+index, fontsize=labelsize)
    plt.xlabel('fund', fontsize=labelsize)
    plt.ylabel('distance', fontsize=labelsize)
    fancy_dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=800.,  # font size for the x axis labels
        labels = labels,
        show_contracted=True,
        max_d = max_d
    )
    pylab.yticks(fontsize=ticksize)
    pylab.xticks(rotation=-90, fontsize=ticksize)
    plt.savefig('dendogram_' + index + 'withThreshold' +'.png')
    plt.show()
    
def cluster_grouping(clusters_array, df_data):
    clusters_dict = {key: [] for key in range(1, clusters_array.max() + 1)}
    for i in range(clusters_array.size):
        clusters_dict[clusters_array[i]].append(df_data.columns[i])
    return clusters_dict

def cluster_preproc(original_cluster_dict, best_fund_dict, user_selectFunds):
    
    new_bestFund_dict = {}
    for i in range(len(original_cluster_dict)):

        saved_flag = 1
        for user_selectFund in user_selectFunds:
            if user_selectFund in original_cluster_dict[i]:
                saved_flag = 0
                break

        if saved_flag == 1:
            new_bestFund_dict[i] = best_fund_dict[i]
            
    return new_bestFund_dict


def const_func(x, c):
    return c * np.ones(len(x))

def risk_index(x, a_list):
    
    result = 0
    for a in a_list:
        result += x ** a

    return result

def get_step(upper_bound, lower_bound, slice_num):
    
    tmp_step = (upper_bound - lower_bound) / slice_num
    
    if tmp_step < 1:
        exponent = math.ceil(abs(math.log(step) / math.log(10)))
        final_step = 10 ** (-exponent)
    else:
        exponent = math.floor(abs(math.log(step) / math.log(10)))
        final_step = 10 ** exponent
    
    return final_step

def IVT(start_point, step, func, a_list, c, loop_num):
    left_x = start_point
    right_x = start_point + step
    
    for i in range(loop_num):
        mid_x = (left_x + right_x) / 2
        left_value = func(left_x, a_list)
        right_value = func(right_x, a_list)
        mid_value = func(mid_x, a_list)
        
        if func(mid_x, a_list) == c:
            break
        elif (left_value < c and mid_value > c) or (left_value > c and mid_value < c):
            right_x = mid_x
        elif (mid_value < c and right_value > c) or (mid_value > c and right_value < c):
            left_x = mid_x
    sol = (left_x + right_x) / 2
    
    return sol

def get_step(upper_bound, lower_bound, slice_num):
    
    tmp_step = (upper_bound - lower_bound) / slice_num
    
    if tmp_step < 1:
        exponent = math.ceil(abs(math.log(tmp_step) / math.log(10)))
        final_step = 10 ** (-exponent)
    else:
        exponent = math.floor(abs(math.log(tmp_step) / math.log(10)))
        final_step = 10 ** exponent
    
    return final_step

def index_q(data_list, ivt_loop_num):
    
    new_a_list = []
    amp_factor = 100000
    
    for a in data_list:
        if a != 'x':
            new_a_list.append(float(a))
    
    c = len(new_a_list)
    avg = float(sum(new_a_list)) / float(len(new_a_list))
    total = 0
    for a in new_a_list:
        total += float((a - avg)**2)
    var = float(total) /  float(len(new_a_list))
    
    root = -1 * 2 * float(avg) / float(var)
            
    first_bound = math.exp(root * 1.5)
    second_bound = math.exp(root * 0.5)
    upper_bound = max(first_bound, second_bound)
    lower_bound = min(first_bound, second_bound)
    
    
    sol_list = []
    sol = 1
    slice_num = 1000
    
    step = get_step(upper_bound, lower_bound, slice_num)
    
    for x in np.arange(lower_bound, upper_bound, step):
        left_value = risk_index(x, new_a_list)
        right_value = risk_index(x + step, new_a_list)
        
        if (left_value < c and right_value > c) or (left_value > c and right_value < c):
            sol_list.append(x)
    
    if len(sol_list) == 2:
        sol_list_arr = np.array(sol_list)
        sol_list_arr = sol_list_arr * amp_factor
        sol_list_arr = abs(sol_list_arr - 1*amp_factor)
        cmp_list = list(sol_list_arr)
        max_index = cmp_list.index(max(cmp_list))
        sol = sol_list[max_index]
    else:
        sol = sol_list[0]
        
    if step > 10:
        exponent = math.floor(abs(math.log(step) / math.log(10)))
        ivt_loop_num *= exponent
    
    sol = IVT(sol, step, risk_index, new_a_list, c, ivt_loop_num)
   
    return sol

def pick_bestFund(cluster_dict, df_data, ivt_loop_num):
    
    num_of_group = len(cluster_dict)
    bestFund_dict = {}
    
    for i in range(0, num_of_group):
        index_q_dict = {}
        print('find the best fund in group', i)
        for label in cluster_dict[i]:
            index_q_dict[label] = index_q(df_data[label], ivt_loop_num)
        index_q_items = index_q_dict.items()
        inverse_items=[[v[1],v[0]] for v in index_q_items] 
        min_q, min_label = min(inverse_items)
        bestFund_dict[i] = [min_label, min_q]
    return bestFund_dict

def pick_candidate(bestFund_dict, candidate_num):
    
    items = bestFund_dict.items()
    backitems = []
    for group_index, bestFund in bestFund_dict.items():
        bestFund_label, bestFund_q = bestFund
        backitems.append([bestFund_q, bestFund_label, group_index])
    backitems.sort() 
    
    candidate_list = []
    for candidate_data in backitems[0:candidate_num]:
        u, v, w = candidate_data
        candidate_list.append(v)
    return candidate_list

def combinationSum(candidates, target):
    candidates.sort()
    res=set()
    intermedia=[]
    recursion(candidates,target,res,intermedia)
    return [list(i) for i in res]

def recursion(candidates,target,res,intermedia):
    for i in candidates:
        if target==i:
            temp=intermedia+[i]
            temp.sort()
            if temp is not None:
                res.add(tuple(temp))
            return
        elif target>i:
            recursion(candidates,target-i,res,intermedia+[i])
        else:
            return

def weight_alloc(candidate_num, exist_sum, step, side_num):
    amp_factor = 10000
    weight_candidate_list = []
    weight_alloc_list = []
    
    mid_num = int(((100 - exist_sum) * amp_factor / candidate_num))
    weight_candidate_list.append(mid_num)
    
    for i in range(1, side_num+1):
        weight_candidate_list.append(mid_num + (i * step)*amp_factor)
        weight_candidate_list.append(mid_num - (i * step)*amp_factor)    
        
    new_weight_candidate_list = []
    for e in weight_candidate_list:
        if e < 0:
            continue
        else:
            new_weight_candidate_list.append(e)
    
    # print('np.array(new_weight_candidate_list) / amp_factor')
    for e in combinationSum(new_weight_candidate_list,mid_num * candidate_num):
        if len(e) == candidate_num:
            e_arr = np.array(e)
            e_arr = e_arr / amp_factor
            e_arr = e_arr / 100
            weight_alloc_list.append(e_arr.tolist())
    return weight_alloc_list

def newFund_return(df_data, labels, weights):
    
    n = len(df_data[labels[0]])
    new_returns = []
    
    for i in range(n):
        is_fieldValid = 1
        for label in labels:
            if df_data[label][i] == 'x':
                is_fieldValid = 0
        
        if is_fieldValid == 1:
            new_return = 0
            for label, weight in zip(labels, weights):
                new_return += float(df_data[label][i]) * weight
            new_returns.append(new_return)
    return new_returns

def portfolio_alloc(raw_data, candidate_list, candidate_pick_num, user_selectFund, user_selectFund_weights, extraPortfolio_ratio, ivt_loop_num):
    
    minimum_weight = 0.1
    candidate_combs = list(combinations(candidate_list, candidate_pick_num))
    weight_alloc_combs = weight_alloc(candidate_pick_num, (1-extraPortfolio_ratio)*100, 3, 3)

    new_weight_alloc_combs = []
    for weight_comb in weight_alloc_combs:
        if min(weight_comb) > minimum_weight:
            new_weight_alloc_combs.append(weight_comb)

    print(new_weight_alloc_combs)
    
    portfolio_alloc_list = []
    if len(new_weight_alloc_combs) > 0:
        for candidate_comb in candidate_combs: 
            print(candidate_comb)
            for weight_alloc_comb in new_weight_alloc_combs:
                new_return_list = []
                weight_alloc_comb_perms = set(list(permutations(weight_alloc_comb)))
                for weight_alloc_comb_perm in weight_alloc_comb_perms:
                    final_candidate_comb = candidate_comb + tuple(user_selectFund)
                    final_weight_alloc_comb_perm = weight_alloc_comb_perm + tuple(user_selectFund_weights)
                    new_return_list = newFund_return(raw_data, final_candidate_comb, final_weight_alloc_comb_perm)
                    q = index_q(new_return_list, ivt_loop_num)
                    portfolio_alloc_list.append([q, final_candidate_comb, final_weight_alloc_comb_perm])
    return portfolio_alloc_list