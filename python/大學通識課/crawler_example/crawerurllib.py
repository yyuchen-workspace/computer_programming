import urllib.request as req
# url = 'https://www.ptt.cc/bbs/Food/index.html'
url = 'http://www.ptt.cc/bbs/Gossiping/index.html'
# 模擬網站使用者
url = req.Request(url, headers={
	"cookie":"over18=1",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
})
with req.urlopen(url) as response:
	data=response.read().decode('utf-8')
#寫入檔案
with open('cr.html','wt',encoding='utf-8') as ftext:
	print(data,file=ftext)  
print(data)
