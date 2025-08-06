import requests

payload = {
"accountingyear": "111",
"item": "03",
"corn001": " ",
"input803": " ",
"crop": "002",
"city": "00",
"btnSend": '送　出'
}

rs = requests.session()
res = rs.post('https://agr.afa.gov.tw/afa/afa_frame.jsp',data=payload)

with open('cr.html','wt',encoding='utf-8') as ftext:
	print(res.text,file=ftext) 