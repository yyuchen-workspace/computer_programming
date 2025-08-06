from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin


# 1. 在全域建立並讀取 robots.txt
rp = RobotFileParser()
robots_url = "https://www.iyp.com.tw/robots.txt"
rp.set_url(robots_url)
rp.read()


def can_fetch_url(url: str) -> bool:
    """檢查 robots.txt 是否允許爬蟲抓取這個 URL"""
    return rp.can_fetch("*", url)


def safe_get(driver, url: str):
    """包一層檢查：只有在 robots.txt 允許時才 driver.get"""
    if not can_fetch_url(url):
        print(f"🚫 robots.txt 禁止存取：{url}")
        return False
    driver.get(url)
    return True


# Selenium Chrome 選項，關閉各種 log
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")  # 只保留 fatal
options.add_argument("--disable-logging")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--blink-settings=imagesEnabled=false")  # 不載入圖片
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")


# 建立 ChromeDriver
CHROMEDRIVER_PATH = r"E:\version\Chrome_tools\chromedriver-win64\chromedriver.exe"  # <- 改成你的實際位置

#清理icon標籤
def clean_icon_text(text):
    parts = text.strip().split(maxsplit=1)
    return parts[1] if len(parts) > 1 else text.strip()


def select_area_location():
    
    while True:
        print("請選擇類型(輸入:縣市/區域):")
        select_function = input().strip()
        if select_function == "縣市":
            print("請輸入縣市名稱(不須輸入縣市，如:台北): ")
            location = input().strip()
            if location:
                return location
            break
        elif select_function == "區域":
            print("請輸入區域名稱(全區/北區/南區/西區/東區): ")
            district = input().strip()
            if district:
                return district
            break
        print("⚠️ 輸入有誤，請重新輸入")


def find_area_url(driver, initial_url, area):
    if not safe_get(driver, initial_url):
        return None
    try:
        select_elem = Select(driver.find_element(By.ID, "search-range"))
        select_elem.select_by_visible_text(area)
    except NoSuchElementException:
        print(f"❌ 找不到選項：『{area}』，請確認輸入是否正確")
        return None
    value = select_elem.first_selected_option.get_attribute("value")
    search_url = f"{initial_url}&city={value}"
    return search_url


def get_area_map(driver, url):
    if not safe_get(driver, url):
        return None
    area_map = {}
    select_elem = driver.find_element(By.ID, "search-range")
    optgroups = select_elem.find_elements(By.TAG_NAME, "optgroup")
    for group in optgroups:
        label = group.get_attribute("label")
        cities = group.find_elements(By.TAG_NAME, "option")
        area_map[label] = [city.text.strip() for city in cities]
    return area_map



def Traverse_the_location_data(initial_url, location, base_url):
    # 🆕 每次新建 driver
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)


    # 先找 search_url
    search_url = find_area_url(driver, initial_url, location)
    if not search_url:
        driver.quit()
        exit()


    # 檢查並載入 search_url
    if not safe_get(driver, search_url):
        driver.quit()
        return
    
    
    output_file = f"{location}公司資料列表.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        page = 1
        while True:
            print(f"🔎 第 {page} 頁")
            
            # 等待公司名稱元素出現
            try:
                WebDriverWait(driver, 10).until(
                    #用於需等待的動態內容  #等待條件成立 
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.text-xl"))
                    
                )
            except:
                print("❌ 等待元素失敗，可能資料載入異常")
                break

            # 抓公司卡片
            cards = driver.find_elements(By.CSS_SELECTOR, "div.relative.mb-4")#回傳list
            if not cards:
                print("⚠️ 沒有公司資料，結束")
                break

            for card in cards:
                try:
                    name = card.find_element(By.CSS_SELECTOR, "a.text-xl").text.strip()
                    '''去除<mark>標籤內容
                    from bs4 import BeautifulSoup
                    # 抓到 <a> 元素
                    a_tag = card.find_element(By.CSS_SELECTOR, "a.text-xl")
                    # 取 innerHTML，保留 <mark> 標籤
                    html = a_tag.get_attribute("innerHTML")
                    # 用 BeautifulSoup 分析、移除 <mark>
                    soup = BeautifulSoup(html, "html.parser")
                    # 刪掉 <mark> 標籤
                    for mark in soup.find_all("mark"):
                        mark.decompose()
                    # 剩下的純文字
                    clean_text = soup.get_text(strip=True)
                    '''
                    if not name:
                        print("非公司資料")
                        break
                    # 地址與電話都包在 text-neutral-700 裡
                    info_block = card.find_element(By.CSS_SELECTOR, "div.text-sm.text-neutral-700")
                    details = info_block.find_elements(By.CSS_SELECTOR, "div.flex")
                    
                    addr = clean_icon_text(details[0].text) if len(details) > 0 else ""
                    tel = clean_icon_text(details[1].text) if len(details) > 1 else ""
                    if addr == "" and tel == "":
                        continue
        
                    #print(f"公司名稱: {name}\n📍地址: {addr}\n📞電話: {tel}\n")#印出檢查進度
                    f.write(f"公司名稱: {name}\n📍地址: {addr}\n📞電話: {tel}\n\n")

                except Exception as e:
                    pass
                    ##rint("⚠️ 卡片處理錯誤（換頁可忽略）:", e)

            # 嘗試找「下一頁」連結（<a>）
            try:
                next_link = driver.find_element(By.XPATH, "//a[span[contains(text(),'下一頁')]]")
                next_href = next_link.get_attribute("href")
                if not next_href:
                    print("✅ 沒有下一頁，結束")
                    break
                full_url = next_href if next_href.startswith("http") else base_url + next_href


                if not safe_get(driver, full_url):
                    break


                page += 1
                driver.get(full_url)
                time.sleep(2)
            except Exception as e:
                print("✅ 找不到下一頁，結束")
                break

    driver.quit()
    print(f"\n📄 所有結果已寫入：{output_file}")


if __name__ == "__main__":
    base_url = "https://www.iyp.com.tw"
    initial_url = f"{base_url}/search?q=股份有限公司&type=keywords"
    area = select_area_location()
    
    # 建立暫時的 driver 來取得區域 map
    driver_temp = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    area_map = get_area_map(driver_temp, initial_url)
    driver_temp.quit()

    if area in area_map:
        for city in area_map[area]:
            print(f"🌐 開始抓取：{city}")
            Traverse_the_location_data(initial_url, city, base_url)
    else:
        Traverse_the_location_data(initial_url, area, base_url)
