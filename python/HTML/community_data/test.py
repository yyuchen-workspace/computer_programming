import requests
from urllib.parse import urljoin, unquote  #配合結合URL
from bs4 import BeautifulSoup
import time
import re #用到re.compile處理下一頁
from pathlib import Path  #處理路徑
import logging

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


base_url = "https://group.lifego.tw/" 
headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }


def create_city_folder(city_name):
    # 2. 建立完整的檔案路徑物件
    #    Path(city_name)     → 新北市
    #    / "data"            → 新北市/data
    #    / f"{district_name}.txt" → 新北市/data/中山區.txt
    city_folder = Path(city_name)
    city_folder.mkdir(parents=True, exist_ok=True)


def find_data(url, city_name, district_name, count, do_dis):
    if do_dis == "否":
        file_path = Path(city_name) / f"{city_name}全部社區資料(共有{count}筆).txt"
    elif do_dis == "是":
        file_path = Path(city_name) / f"{city_name}{district_name}社區資料(共有{count}筆).txt"

    with file_path.open( mode = "w", encoding = "utf-8") as file:
        page = 1
        while True:
            logger.info(f"[{city_name}{'-'+district_name if do_dis else ''}] 第{page}頁 {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            div_tags = soup.find_all('div', {'class' : 'product-info'})
            for div_tag in div_tags:
                a_title = div_tag.find('a')#找到<a>標籤
                title = a_title.text.strip().replace('\xa0', '')
                if title != None:
                    file.write(f"{title}\n")#寫入標題
                    phone = address = ""#避免空白或無資料
                    spans = div_tag.find('span')#找到<span>標籤
                    for label in spans.find_all('label'):#找到label
                        label_name = label.get_text(strip=True).replace('\xa0','')#取得label內文字#去除&nbsp;（不換行空格）
                        label_text = label.next_sibling
                        if not label_text:#空白或換行
                            continue
                        value = label_text.strip().replace('\xa0', '')#去除&nbsp;（不換行空格)、頭尾空白
                        if label_name == "電話":
                            phone = value
                        elif label_name == "地址":
                            address = value
                    file.write(f"電話: {phone}\n地址: {address}\n\n")
        
            a_tag = soup.find('a',class_='btn btn-primary',string=re.compile(r'下一頁'))
            '''
            if a_tag and a_tag.get('href') != None:
                next_page_url = base_url + a_tag['href']
            else:
                break
            '''
            #urljoin套件
            href = a_tag and a_tag.get('href')#利用and避免a_tag為None
            if not href:
                print("已無下一頁，結束")
                break
            url = urljoin(base_url, unquote(href))#更完整，可以自動結合連結
            #
            page+=1
            time.sleep(2)


def seperate_name(text):
    name_part, sep, num_part = text.partition('(')#如"台北市 (4776)"
    name = name_part.strip()               # 拿到「台北市」
    count = num_part.rstrip(')').strip() #拿到4776
    return name, count

if __name__ == "__main__":
    response = requests.get(base_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    city_tree = soup.find_all('li', {'class' : 'treeview'})#全國縣市樹
    found_city = found_district = False#用於後面確認是否查找到該縣市、區名
    city_name = input("請輸入縣市名: ").strip()
    if city_name == "全部":
        found_city = True
        found_district = True
        do_dis = input("是否分區: ").strip()
        while True:
            if do_dis == "是":#全部縣市-全區分類  
                for tree in city_tree:
                    #取出 <span> 內的城市名稱
                    span = tree.find('span')
                    if not span:
                        continue

                    city_text = span.get_text(strip = True)
                    city_n, _ = seperate_name(city_text)# 拿到「台北市」
                    create_city_folder(city_n)
                    #處理此城市下的所有子選單（ul.treeview-menu）
                    for city in tree.find_all('ul', {'class' : 'treeview-menu'}):
                        for dis in city.find_all('li'):#遍歷子選單
                            a_tag = dis.find('a')
                            a_text = a_tag.get_text(strip=True)#<a>標籤下的字串#全部或是區名(筆數)
                            if a_text.startswith('全部'):#遇到全部就跳過
                                continue
                            district_n, count = seperate_name(a_text)                               
                            href = a_tag['href']
                            url =  urljoin(base_url, unquote(href))  #結合連結
                            find_data(url, city_n, district_n, count, do_dis)
                break
            elif do_dis == "否":#全部縣市-全區不分類
                #逐一處理每個城市節點
                for tree in city_tree:
                    #取出 <span> 內的城市名稱
                    span = tree.find('span')
                    if not span:
                        continue
                    city_text = span.get_text(strip = True)
                    city_n, count = seperate_name(city_text)
                    create_city_folder(city_n)
                    #處理此城市下的所有子選單（ul.treeview-menu）
                    for city in tree.find_all('ul', {'class' : 'treeview-menu'}):
                        a_tag = city.find('a')#只找第一個(全部)
                        href = a_tag['href']
                        url =  urljoin(base_url, unquote(href))  
                        find_data(url, city_n, None, count, do_dis)             
                break
            do_dis = input("錯誤輸入!請輸入是/否:").strip()
    else:
        district_name = input("請輸入鄉鎮市區名: ").strip()
        if district_name == "全部":
            found_district = True
            do_dis = input("是否分區: ").strip()
            while True:
                if do_dis == "是":#單一縣市-全區分類
                    for tree in city_tree:
                        #取出 <span> 內的城市名稱
                        span = tree.find('span')
                        if not span:
                            continue

                        city_text = span.get_text(strip = True)
                        city_n, _ = seperate_name(city_text)# 拿到「台北市」
                        if city_n == city_name:
                            found_city == True
                            #處理此城市下的所有子選單（ul.treeview-menu）
                            for city in tree.find_all('ul', {'class' : 'treeview-menu'}):
                                for dis in city.find_all('li'):#遍歷子選單
                                    a_tag = dis.find('a')
                                    a_text = a_tag.get_text(strip=True)#<a>標籤下的字串#全部或是區名(筆數)
                                    if a_text.startswith('全部'):#遇到全部就跳過
                                        continue
                                    district_n, count = seperate_name(a_text)                               
                                    href = a_tag['href']
                                    url =  urljoin(base_url, unquote(href))  #結合連結
                                    find_data(url, city_n, district_n, count, do_dis) 
                    break                  
                elif do_dis == "否":#單一縣市-全區不分類
                    #逐一處理每個城市節點
                    for tree in city_tree:
                        #取出 <span> 內的城市名稱
                        span = tree.find('span')
                        if not span:
                            continue
                        city_text = span.get_text(strip = True)
                        city_n, count = seperate_name(city_text)
                        if city_n == city_name:
                            found_city == True
                            create_city_folder(city_n)
                            #處理此城市下的所有子選單（ul.treeview-menu）
                            for city in tree.find_all('ul', {'class' : 'treeview-menu'}):
                                a_tag = city.find('a')#只找第一個(全部)
                                href = a_tag['href']
                                url =  urljoin(base_url, unquote(href))  
                                find_data(url, city_n, None, count, do_dis)             
                    break
                do_dis = input("錯誤輸入!請輸入是/否:").strip()

        else:  #單一縣市-單一區
            for tree in city_tree:
                #取出 <span> 內的城市名稱
                span = tree.find('span')
                if not span:
                    continue

                city_text = span.get_text(strip = True)
                city_n, _ = seperate_name(city_text)# 拿到「台北市」
                if city_n == city_name:
                    found_city == True
                #處理此城市下的所有子選單（ul.treeview-menu）
                    for city in tree.find_all('ul', {'class' : 'treeview-menu'}):
                    
                        for dis in city.find_all('li'):#遍歷子選單
                            a_tag = dis.find('a')
                            a_text = a_tag.get_text(strip=True)#<a>標籤下的字串#全部或是區名(筆數)
                            dis_n, count = seperate_name(a_text)   
                            if dis_n == district_name:
                                found_district == True
                                create_city_folder(city_n)
                                href = a_tag['href']
                                url =  urljoin(base_url, unquote(href))  #結合連結
                                find_data(url, city_n, dis_n, count, "是")
                else:
                    continue

        if not found_city:
            print("查無此縣市資料或輸入縣市名稱錯誤")
        elif not found_district:
            print("查無此鄉鎮市區資料或輸入鄉鎮市區名稱錯誤")