import urllib.request as req
file=open("PTT-Gossip.txt",mode="w",encoding="utf-8") #開啟一個文檔

def getData(url):
    #讓網頁覺得我們是正常瀏覽器，所以附加Request Headers
    request=req.Request(url,headers={
        "cookie":"over18=1", #給自己套上已滿18
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data=response.read().decode("utf-8") #中文編碼

    #解析原始碼，取的每篇文章的標題
    import bs4
    root=bs4.BeautifulSoup(data, "html.parser")
    titles=root.find_all("div",class_="title") #尋找class="title"的div標籤
    for title in titles:
        if title.a != None: #如果標題包含a標籤(沒有被刪除)，印出來
            # print(title.a.string)
            file.write(title.a.string + "\n") #寫入資料

    #抓上一頁
    nextLink=root.find("a",string="‹ 上頁") #找到內文的上頁標籤
    # print(nextLink["href"])
    return nextLink["href"]

#主程式(抓取多個頁面標題)
pageURL="https://www.ptt.cc/bbs/Gossiping/index.html"
count=0
while count<3: #設定要抓的頁數
    file.write("第" + str(count+1) + "頁" + "\n")
    pageURL="https://www.ptt.cc"+getData(pageURL)
    # print(pageURL)
    count = count + 1

file.close() #關閉文檔