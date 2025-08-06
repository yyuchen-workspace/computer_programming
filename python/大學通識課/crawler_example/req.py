import requests
# url = 'https://www.ptt.cc/bbs/Food/index.html'
url = 'http://www.ptt.cc/bbs/Gossiping/index.html'
# 模擬使用者瀏覽器
payload = {
'from': '/bbs/Gossiping/index.html',
'yes': 'yes'
}
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
res = rs.get(url)
with open('cr.html','wt',encoding='utf-8') as ftext:
	print(res.text,file=ftext) 