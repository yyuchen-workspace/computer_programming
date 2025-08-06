import requests# 引入requests模組
from bs4 import BeautifulSoup# 引入BeautifulSoup模組
import time

# 登入表單的資料
payload = {
    'from': '/bbs/HatePolitics/index1.html',
    'yes': 'yes' # 檢查網頁原始碼
}

# 取自chatgpt:使用 session 保持會話
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18', data=payload) # 登入頁面，確認成年

# 初始頁面
pageURL = 'https://www.ptt.cc/bbs/HatePolitics/index.html'

# 打開文檔
file = open("PTT-HatePolitics.txt", mode="w", encoding="utf-8")

# 抓取多個頁面的標題和內文
for pages in range(300):  # 抓取300頁

    # 寫入頁數
    file.write(f"第 {pages+1} 頁\n")
    
    # 發送 GET 請求獲取頁面內容
    res = rs.get(pageURL)
    soup = BeautifulSoup(res.text, 'html.parser')# 將抓回的HTML頁面傳入BeautifulSoup，使用html.parser解析

    # 使用 find_all() 尋找標題並抓取內容，獲取所有<div>標籤下面的class屬性值title
    div_tags = soup.find_all('div', {'class': 'title'})
    for div_tag in div_tags:
        a_tag = div_tag.find('a') # 找到 <div class="title"> 下的 <a>
        if a_tag != None: # 如果標題包含 <a> 標籤

            # 寫入標題到文件
            file.write(a_tag.text + "\n")

            # 抓取內文
            res2 = rs.get('http://www.ptt.cc/'+ a_tag.get('href'))
            soup2 = BeautifulSoup(res2.text, 'html.parser') 
            main_content = soup2.find(id="main-content").text
            file.write(main_content + '\n\n') # 寫入內文到文件

    # 找到下一頁連結
    nextLink = soup.find("a", string="‹ 上頁") # 找到內文的上頁標籤
    if nextLink and nextLink.get("href") != None:  # 取自chatgpt:若找不到下一頁連結或者無效的 href 屬性，跳出迴圈停止爬取
        pageURL = 'https://www.ptt.cc' + nextLink["href"] # 更新下一頁 URL
    else:
        break

    time.sleep(1)
   

# 關閉文
file.close()
