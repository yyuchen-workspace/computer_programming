import requests # 引入requests模組
from bs4 import BeautifulSoup # 引入BeautifulSoup模組

# 登入表單的資料
payload = {
    'from': '/bbs/HatePolitics/index1.html', 
    'yes': 'yes' # 檢查網頁原始碼
}

# 取自chatgpt:使用 session 保持會話
rs = requests.session()
# 登入頁面，確認成年
rs.post('https://www.ptt.cc/ask/over18', data=payload)

#取得目標頁面的內容
def get_pagecontent(url):
    res = rs.get(url)
    #打開頁面
    soup = BeautifulSoup(res.text, 'html.parser') #將抓回的HTML頁面傳入BeautifulSoup，使用html.parser解析

 #開啟一個文檔
file = open("PTT-HatePolitics.txt", mode="w", encoding="utf-8")

# 爬取多頁標題及內文
def getData(pageURL, numberpages): # 創建函數
    with open("PTT-HatePolitics.txt", mode="w", encoding="utf-8") as file:
        for i in range(numberpages): # 利用for迴圈重複運行代碼並可在之後限制要跑幾頁 
            file.write(f"第 {i+1} 頁\n") #寫入第幾頁
            soup2 = get_pagecontent(pageURL) #引入函數get_pagecontent來獲得解析後的網頁
        
        # 找到標題並寫入檔案
            div_tags = soup2.find_all('div', {'class': 'title'}) # 獲取所有<div>標籤下面的class屬性值title
            for div_tag in div_tags: # 用for迴圈重複執行
                a_tag = div_tag.find('a') # 獲取第一個<a>標籤
                if a_tag != None: # 若<a>標籤下面不是空白
                    file.write(a_tag.text.strip() + "\n") # 取自chatgpt:將 <a> 標籤的文本內容使用 a_tag.text 獲取，並使用 strip() 方法去除文本內容的首尾空白，然後寫入到文件 (file) 中，並在末尾加上換行符 (\n)。
                    article_url = 'https://www.ptt.cc' + a_tag.get('href') # 獲取<a>標籤下面的'href'屬性值，藉此跳轉到該標題的文章內容頁面
                
                # 取得文章內文
                    articlesoup = get_pagecontent(article_url) # 引入函數get_pagecontent來獲得解析後的網頁
                    maincontent = articlesoup.find(id="main-content").text.strip() # 獲取第一個id屬性值為"main-content"的文本內容並去除文本內容的首尾空白
                    file.write(maincontent + '\n') # 寫入文檔
        
            # 找到下一頁連結
            nextLink=soup2.find("a",string="‹ 上頁") #找到內文的上頁標籤
            # print(nextLink["href"])
            pageURL = 'https://www.ptt.cc'+ nextLink["href"]
            return pageURL


# 主程式
pageURL = "https://www.ptt.cc/bbs/HatePolitics/index.html"
numberpages = 301
getData(pageURL, numberpages)
