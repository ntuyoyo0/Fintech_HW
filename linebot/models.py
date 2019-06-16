class Portfolio:
    def __init__(self, index_q, labels, weights,sortino=0):
        self.index_q = index_q
        self.labels = labels
        self.weights = weights
        self.sortino = sortino
    
    def __str__(self):
        return 'index: ' + str(self.index_q) + '\n' + \
            'labels: ' + str(self.labels) + '\n' + \
            'weights: ' + str(self.weights)
    
    def output_portfolio(self):
        ans = ""
        for i in range(len(self.labels)):
            ans += self.labels[i]
            ans += " : "
            ans += "{0:.2f}".format(self.weights[i])
            ans += "\n"
        ans += "indexQ : "
        ans += "{0:.5f}".format(self.index_q)
        ans += "\n"
        ans += "sortino : "
        ans += "{0:.5f}".format(self.sortino)

        return ans


class Input:
	def __init__(self,extraPortfolio_ratio,user_selectFunds,user_selectFund_weights,user_recommend_num):
		self.extraPortfolio_ratio = extraPortfolio_ratio
		self.user_selectFunds = user_selectFunds
		self.user_selectFund_weights = user_selectFund_weights
		self.user_recommend_num = user_recommend_num


