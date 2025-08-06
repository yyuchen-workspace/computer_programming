import requests
from urllib.parse import urljoin, unquote  #配合結合URL
from bs4 import BeautifulSoup
import time
import re #用到re.compile處理下一頁
from urllib.parse import urlencode, quote_plus
from pathlib import Path  #處理路徑

city_map = {
    # 直轄市
    "臺北市": [
        "中正區","大同區","中山區","松山區","大安區","萬華區",
        "信義區","士林區","北投區","內湖區","南港區","文山區"
    ],
    "新北市": [
        "萬里區","金山區","板橋區","汐止區","深坑區","石碇區","瑞芳區",
        "平溪區","雙溪區","貢寮區","新店區","坪林區","烏來區",
        "永和區","中和區","土城區","三峽區","樹林區","鶯歌區",
        "三重區","新莊區","泰山區","林口區","蘆洲區","五股區",
        "八里區","淡水區","三芝區","石門區"
    ],
    "桃園市": [
        "中壢區","平鎮區","龍潭區","楊梅區","新屋區","觀音區",
        "桃園區","龜山區","八德區","大溪區","復興區","大園區","蘆竹區"
    ],
    "臺中市": [
        "中區","東區","南區","西區","北區","北屯區","西屯區","南屯區",
        "太平區","大里區","霧峰區","烏日區","豐原區","后里區","石岡區",
        "東勢區","和平區","新社區","潭子區","大雅區","神岡區","大肚區",
        "沙鹿區","龍井區","梧棲區","清水區","大甲區","外埔區","大安區"
    ],
    "臺南市": [
        "中西區","東區","南區","北區","安平區","安南區","永康區",
        "歸仁區","新化區","左鎮區","玉井區","楠西區","南化區","仁德區",
        "關廟區","龍崎區","官田區","麻豆區","佳里區","西港區","七股區",
        "將軍區","學甲區","北門區","新營區","後壁區","白河區","東山區",
        "六甲區","下營區","柳營區","鹽水區","善化區","大內區","山上區",
        "新市區","安定區"
    ],
    "高雄市": [
        "楠梓區","左營區","鼓山區","三民區","鹽埕區","前金區","新興區",
        "苓雅區","前鎮區","旗津區","小港區","鳳山區","大寮區","鳥松區",
        "林園區","仁武區","大樹區","大社區","岡山區","路竹區","橋頭區",
        "梓官區","彌陀區","永安區","燕巢區","田寮區","阿蓮區","茄萣區",
        "茂林區","桃源區","那瑪夏區"
    ],

    # 省轄市
    "基隆市": ["仁愛區","信義區","中正區","中山區","安樂區","暖暖區","七堵區"],
    "新竹市": ["東區","北區","香山區"],
    "嘉義市": ["東區","西區"],

    # 縣
    "宜蘭縣": [
        "宜蘭市","頭城鎮","礁溪鄉","壯圍鄉","員山鄉",
        "羅東鎮","五結鄉","冬山鄉","蘇澳鎮","南澳鄉","釣魚臺列嶼"
    ],
    "新竹縣": [  # 新竹縣行政區劃 :contentReference[oaicite:0]{index=0}
        "竹北市","竹東鎮","新埔鎮","關西鎮","湖口鄉","新豐鄉",
        "芎林鄉","橫山鄉","寶山鄉","北埔鄉","峨眉鄉","尖石鄉","五峰鄉"
    ],
    "苗栗縣": [  # 苗栗縣行政區劃 :contentReference[oaicite:1]{index=1}
        "苗栗市","頭份市","竹南鎮","後龍鎮","通霄鎮","苑裡鎮","卓蘭鎮",
        "造橋鄉","西湖鄉","頭屋鄉","公館鄉","銅鑼鄉","三義鄉","大湖鄉",
        "獅潭鄉","三灣鄉","南庄鄉","泰安鄉"
    ],
    "彰化縣": [  # 彰化縣行政區劃 :contentReference[oaicite:2]{index=2}
        "彰化市","員林市","和美鎮","鹿港鎮","溪湖鎮","二林鎮","田中鎮","北斗鎮",
        "花壇鄉","芬園鄉","大村鄉","永靖鄉","伸港鄉","線西鄉","福興鄉","秀水鄉",
        "埔心鄉","埔鹽鄉","大城鄉","芳苑鄉","竹塘鄉","社頭鄉","二水鄉","田尾鄉",
        "埤頭鄉","溪州鄉"
    ],
    "南投縣": [  # 南投縣行政區劃 :contentReference[oaicite:3]{index=3}
        "南投市","埔里鎮","草屯鎮","竹山鎮","集集鎮",
        "名間鄉","中寮鄉","鹿谷鄉","水里鄉","魚池鄉",
        "國姓鄉","信義鄉","仁愛鄉"
    ],
    "雲林縣": [  # 雲林縣行政區劃 :contentReference[oaicite:4]{index=4}
        "斗六市","斗南鎮","虎尾鎮","西螺鎮","土庫鎮","北港鎮",
        "崙背鄉","二崙鄉","莿桐鄉","林內鄉","古坑鄉","大埤鄉",
        "麥寮鄉","臺西鄉","東勢鄉","褒忠鄉","四湖鄉","元長鄉",
        "口湖鄉","水林鄉"
    ],
    "嘉義縣": [  # 嘉義縣行政區劃 :contentReference[oaicite:5]{index=5}
        "太保市","朴子市","布袋鎮","大林鎮",
        "民雄鄉","溪口鄉","新港鄉","六腳鄉","東石鄉","義竹鄉",
        "鹿草鄉","水上鄉","中埔鄉","竹崎鄉","梅山鄉","番路鄉",
        "大埔鄉","阿里山鄉"
    ],
    "屏東縣": [  # 屏東縣等縣市行政區劃 :contentReference[oaicite:6]{index=6}
        "屏東市","潮州鎮","東港鎮","恆春鎮",
        "三地門鄉","霧臺鄉","瑪家鄉","九如鄉","里港鄉","高樹鄉",
        "鹽埔鄉","長治鄉","麟洛鄉","竹田鄉","內埔鄉","萬丹鄉",
        "泰武鄉","來義鄉","萬巒鄉","崁頂鄉","新園鄉","新埤鄉",
        "南州鄉","林邊鄉","琉球鄉","佳冬鄉","枋寮鄉","枋山鄉",
        "春日鄉","獅子鄉","車城鄉","牡丹鄉","滿州鄉"
    ],
    "花蓮縣": [  # 花蓮縣行政區劃 :contentReference[oaicite:7]{index=7}
        "花蓮市","鳳林鎮","玉里鎮",
        "新城鄉","秀林鄉","吉安鄉","壽豐鄉","光復鄉",
        "豐濱鄉","瑞穗鄉","萬榮鄉","卓溪鄉","富里鄉"
    ],
    "臺東縣": [  # 臺東縣行政區劃 :contentReference[oaicite:8]{index=8}
        "臺東市","關山鎮","成功鎮",
        "綠島鄉","蘭嶼鄉","延平鄉","卑南鄉","鹿野鄉",
        "海端鄉","池上鄉","東河鄉","長濱鄉","太麻里鄉",
        "金峰鄉","大武鄉","達仁鄉"
    ],
    "澎湖縣": [  # 澎湖縣行政區劃 :contentReference[oaicite:9]{index=9}
        "馬公市","西嶼鄉","望安鄉","七美鄉","白沙鄉","湖西鄉"
    ],
    "金門縣": [  # 金門縣行政區劃 :contentReference[oaicite:10]{index=10}
        "金沙鎮","金湖鎮","金城鎮",
        "金寧鄉","烈嶼鄉","烏坵鄉"
    ],
    "連江縣": [  # 連江縣行政區劃 :contentReference[oaicite:11]{index=11}
        "南竿鄉","北竿鄉","莒光鄉","東引鄉"
    ]
}


# 在程式最上方，city_map 載入完後就做這件事
# district_to_city: key 是區名，value 是對應的縣市
district_to_city = {
    dis: city
    for city, districts in city_map.items()
    for dis in districts
}

# 也可以保留一個所有區名的 set（如果只需要驗證，不需要知道所屬縣市）
#all_districts = set(district_to_city)



def find_city(city_name):
    while city_name not in city_map:
        city_name = input("請輸入正確縣市名: ").strip().replace("台", "臺")
    return city_name


def find_district(district_name):
    # 清洗輸入
    district_name = district_name.strip().replace("台", "臺")
    # 不在就請使用者重輸
    while district_name not in district_to_city:
        district_name = input("請輸入正確鄉鎮市區名: ").strip().replace("台", "臺")
    city_name = district_to_city[district_name]
    return city_name, district_name


def create_city_folder(city_name):
    # 2. 建立完整的檔案路徑物件
    #    Path(city_name)     → 新北市
    #    / "data"            → 新北市/data
    #    / f"{district_name}.txt" → 新北市/data/中山區.txt
    city_folder = Path(city_name)
    city_folder.mkdir(parents=True, exist_ok=True)


base_url = "http://group.lifego.tw"
headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }


def find_data(url, city_name, district_name, seperate):
    if seperate == "否":
        file_path = Path(city_name) / f"{city_name}.txt"
    else:
        # city 資料夾下，建立 district.txt 並寫入 content。
        file_path = Path(city_name) / f"{district_name}.txt"

    with file_path.open(mode = "w", encoding = "utf-8") as file:
        page = 1
        while True:
            print(f"🔎 第{page}頁")
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


def make_url(area, t, page, a1, a2):
    params = {
        't':      t,   
        'page':   page,          # 縣市
        'a1':     a1,          # 鄉鎮市區
        'a2':     a2,          # 你看到有的時候還會多一個 a2
        'q':      area,          # 關鍵字，你可以放 "" 或不放
                    # 第幾頁
    }
    # urlencode 會自動做 UTF-8 編碼＆百分比轉碼
    return f"{base_url}/Litem.aspx?{urlencode(params, quote_via=quote_plus)}"




if __name__ == "__main__":
    select_area = input("請選擇查找方式(輸入全國/縣市/區): ")
    while True:
        if select_area == "全國":
            seperate = input("請輸入是否分區(是/否): " )
            while True:
                if seperate == "是":
                    for city_name in city_map:
                        create_city_folder(city_name)        
                        for district_name in city_map[city_name]:              
                            url = make_url(district_name, t="", page=1, a1="", a2="")
                            print(f"🔎 {city_name}{district_name}社區資料")
                            find_data(url, city_name, district_name, "")
                    break
                elif seperate == "否":
                    for city_name in city_map:
                        create_city_folder(city_name)     
                        url = make_url(city_name, t="", page=1, a1="", a2="")
                        print(f"🔎 {city_name}資料")
                        find_data(url, city_name, "", seperate)
                    break
                else:
                    seperate = input("輸入錯誤，請輸入是或否: " ).strip()
            break            


            
                
            

        elif select_area == "縣市":
            city_name = input("請輸入縣市名: ").strip().replace("台", "臺")
            city_name = find_city(city_name)
            create_city_folder(city_name) 
            seperate = input("請輸入是否分區(是/否): " )
            while True:
                if seperate == "是":       
                    for district_name in city_map[city_name]:              
                        url = make_url(district_name, t="", page=1, a1="", a2="")
                        print(f"🔎 {city_name}{district_name}社區資料")
                        find_data(url, city_name, district_name, "")
                    break
                elif seperate == "否":
                    url = make_url(city_name, t="", page=1, a1="", a2="")
                    print(f"🔎 {city_name}資料")
                    find_data(url, city_name, "", seperate)
                    break
                else:
                    seperate = input("輸入錯誤，請輸入是或否: " ).strip()
            break

        elif select_area == "區":
            district_name = input("請輸入鄉鎮市區名: ")
            city_name, district_name = find_district(district_name)
            create_city_folder(city_name)

            url = make_url(district_name, t="", page=1, a1="", a2="")
            print(f"🔎 {city_name}{district_name}資料")
            find_data(url, city_name, district_name, "")
            break

        else:
            select_area = input("輸入錯誤，請輸入(縣市/區): ").strip()



