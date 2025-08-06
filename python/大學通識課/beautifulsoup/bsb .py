import requests
from bs4 import BeautifulSoup
payload = {
'from': '/bbs/Gossiping/index.html',
'yes': 'yes'
}
rs = requests.session()
res = rs.post('https://www.ptt.cc/ask/over18',data=payload)
res = rs.get('http://www.ptt.cc/bbs/Gossiping/index.html')

soup = BeautifulSoup(res.text, 'html.parser') #將抓回的HTML頁面傳入BeautifulSoup，使用html.parser解析

# 使用 find_all()
div_tags = soup.find_all('div', {'class': 'title'}) #找到網頁中全部的 <div class="title">
for div_tag in div_tags:
    a_tag = div_tag.find('a') #找到 <div class="title"> 下的 <a>
    if a_tag is not None: #或文章被刪除會是None，所以要排除None
        print(a_tag.text)
        # print(a_tag.get('href'))  

        # 抓取內文使用
        rs2 = requests.session()
        res2 = rs2.post('https://www.ptt.cc/ask/over18',data=payload)
        res2 = rs2.get('http://www.ptt.cc/'+ a_tag.get('href'))
        soup2 = BeautifulSoup(res2.text, 'html.parser') 
        main_content = soup2.find(id="main-content").text
        # print(div_tags2[0])
        print(main_content)

