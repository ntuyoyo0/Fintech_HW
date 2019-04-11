# HW2
此作業我們實作兩種質化分析方式
1. 以股票為單位，判斷不同時間區間內，用新聞標題和內文來判斷其股票狀況（下跌or其他），若狀況為下跌，則紀錄為1，其他為0，以此做出x軸為各股票，y軸為時間區間的matrix，再使用這個matrix做出co-occurrence matrix。其意義為，相關性越高的兩個股票，越容易同時下跌。
2. 對每篇新聞文章，搜索公司名單內各個公司名字是否出現，若有出現則在矩陣內對應 element 加 1，以此方式分析各個公司之間的相關性，並用 Gephi 呈現共線圖

執行方式
1. 第一種實作
`$ python3 stock_anay_main.py`
會產生一個 out.csv 的檔案 （co-occurence matrix) 
可藉由 Gephi 產生共線圖

2. 第二種實作
`$ python3 stock_crawler_ntuyoyo0.py`
會產生一個 df.csv 的檔案 （co-occurence matrix) 
可藉由 Gephi 產生共線圖
    * out_ntuyoyo0.csv 為此實作的範例
    * cor_graph_ntuyoyo0.png 為此實作透過 Genphi 的共現圖範例
    ![image](https://github.com/leo08260826/Fintech_HW/blob/master/hw2/cor_graph_ntuyoyo0.png)

