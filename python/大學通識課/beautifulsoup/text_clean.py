import re
import urllib.request as req
import bs4

url="https://www.ptt.cc/bbs/movie/M.1685633533.A.003.html"#要抓的那一篇的網址
request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
})#讓網頁覺得我們是正常人類，所以建立Request物件並附加Request Headers

with req.urlopen(request) as response:
    data=response.read().decode("utf-8")#中文編碼

root=bs4.BeautifulSoup(data, "html.parser")
contents=root.find_all("div",class_="bbs-screen bbs-content") #bbs-screen bbs-content #尋找class="bbs-screen bbs-content"的div標籤

file=open("PTT-Text-NEW.txt",mode="w",encoding="utf-8") #開啟一個文檔

# 使用 text.split() 方法 
txt=contents[0].text
# postext=txt.split('2023')[1]
# pretext=postext.split('※ 發信站')[0]
# print(pretext)
# print(txt)

# 正規表示式 - 取代 \n, \s
# txt2=re.sub('\n*', "", txt)
# txt=re.sub('\s*', "", txt2)
# # print(txt)

# 正規表示式 - 搜尋 (符合的片段)
# target=re.compile(r"2023.*--※")
target=re.compile(r".*")
result = target.findall(txt)
print(result)

# for i in range(len(result)):
#     result2 =re.sub(r"推 .*: ", r"", result[i])
#     print(result[i], file=file)
#     print(result[i])

# 寫入檔案
# file.write(result[0])

file.close()