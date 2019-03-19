* 你選擇用甚麼樣的套件來做網路爬蟲，為何使用?
    * requests:可以配合BytesIO使用，不用真的下載到local端
    * Selenium:對於動態網頁的爬蟲，比較多reference的套件
    * pandas:用以匯入及整理爬蟲所得資料
    * BytesIO:同requests

* 請用流程圖的方式告訴我們你是怎麼抓到目標資料
![image](https://github.com/leo08260826/Fintech_HW/blob/master/hw1/Diagram.png)

* 5種可能錯誤狀況及解決方法
    * 網站可能有反爬蟲機制，短時間抓取多筆資料造成連線逾時，可用延時方式解決(time.sleep())
    * selenium 有時網頁跑得很慢，須等待他跑完才能執行像 click() 的動作
    * YAHOO會防"用程式滾動"，導致資料不會全部載入，後來不在網頁上用selenium，直接request csv檔
    * YAHOO下載的網址非固定網址，會需要cookie，所以不用requests.get()，改用requests.post()
    * selenium在用css_selector的時候，要注意一下tag的階層(ex:在呼叫<tag_name>.text的時候，會找子階層的text)