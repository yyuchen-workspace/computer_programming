import urllib.request as ur
resp = ur.urlopen('http://python.org/')
html = resp.read()
print(html)
with open('cr_python.html','wt',encoding='utf-8') as ftext:
	print(html,file=ftext) 