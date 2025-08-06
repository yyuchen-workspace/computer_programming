#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Data Scraper Module
Contains all the web scraping logic from the original script
Modified to support incremental updates
"""

import requests
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
from typing import Callable, Optional, Dict, List, Tuple
import os
from datetime import datetime
import difflib


class CommunityDataScraper:
    def __init__(self, progress_callback: Optional[Callable] = None, status_callback: Optional[Callable] = None, output_folder: Optional[str] = None):
        self.base_url = "https://group.lifego.tw/"  # 目標網站的基礎URL  
        # 設定HTTP請求標頭，模擬瀏覽器行為
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        self.session = self._build_session()  # 建立支援重試的Session物件
        self.progress_callback = progress_callback  # 儲存進度回調函式
        self.status_callback = status_callback  # 儲存狀態回調函式
        self.should_stop = False  # 控制爬取是否停止的標誌
        self.output_folder = output_folder or os.getcwd()  # 設定輸出資料夾，預設為當前目錄
        
    def _build_session(self) -> requests.Session:
        """建立一支支持重試的 Session"""
        session = requests.Session()
        retries = Retry(
            total=5,                   # 最多重試 5 次 (包含下面各項)
            connect=5,                 # 連線錯誤時最多再重試 5 次
            read=5,                    # 讀取逾時時最多再重試 5 次
            backoff_factor=1,          # 重試間隔：1s, 2s, 4s, 8s, …
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # 針對這些方法啟用重試
            raise_on_status=False      # 不因為狀態碼而拋出異常
        )
           
        adapter = HTTPAdapter(max_retries=retries)  # 建立HTTP適配器
        session.mount('https://', adapter)  # 為HTTPS請求掛載適配器
        session.mount('http://', adapter)  # 為HTTP請求掛載適配器
        return session  # 返回配置好的Session
    
    def _update_status(self, message: str):
        """
        更新狀態訊息
        
        Args:
            message: 要顯示的狀態訊息
        """
        if self.status_callback:  # 如果有設定狀態回調函式
            self.status_callback(message)  # 呼叫回調函式更新狀態
    
    def _update_progress(self, current: int, total: int):
        """
        更新進度
        
        Args:
            current: 當前進度
            total: 總進度
        """
        if self.progress_callback:  # 如果有設定進度回調函式
            self.progress_callback(current, total)  # 呼叫回調函式更新進度
    
    def stop_scraping(self):
        """停止爬取"""
        self.should_stop = True  # 設定停止標誌為True
    
    def create_city_folder(self, city_name: str, city_count: Optional[str] = None):
        """
        建立城市資料夾
        
        Args:
            city_name: 城市名稱
            city_count: 城市資料總筆數（可選）
            
        Returns:
            城市資料夾的Path物件
        """
        # 如果有提供筆數，將筆數加到資料夾名稱中
        # 建立基礎資料夾名稱
        if city_count:
            city_data_name = f"{city_name}({city_count}筆資料)"
        else:
            city_data_name = city_name
        
        # 使用今天的日期
        today_str = datetime.now().strftime("%Y_%m_%d")
        today_folder_name = f"{city_data_name}_{today_str}"
        
        # 確定工作目錄
        base_dir = Path(self.output_folder)
        base_dir.mkdir(parents=True, exist_ok=True)
        
        today_folder_path = base_dir / today_folder_name
        
        # 建立正規表達式模式
        escaped_city_name = re.escape(city_data_name)
        pattern = re.compile(rf"^{escaped_city_name}_(\d{{4}}_\d{{2}}_\d{{2}})$")
        
        # 尋找並分析舊資料夾
        old_folders = []
        try:
            for entry in base_dir.iterdir():
                if entry.is_dir() and pattern.match(entry.name):
                    if entry.name != today_folder_name:
                        date_match = pattern.match(entry.name)
                        if date_match:
                            date_str = date_match.group(1)
                            try:
                                # 轉換為日期物件以便比較
                                folder_date = datetime.strptime(date_str, "%Y_%m_%d")
                                old_folders.append((entry, date_str, folder_date))
                            except ValueError:
                                self._update_status(f"⚠️ 無法解析日期: {date_str}")
        except (OSError, PermissionError) as e:
            self._update_status(f"⚠️ 讀取目錄時發生錯誤: {e}")
        
        # 按日期排序（最新的在前）
        old_folders.sort(key=lambda x: x[2], reverse=True)
        
        # 處理今天的資料夾
        if today_folder_path.exists():
            self._update_status(f"📂 今天的資料夾 {today_folder_name} 已存在，繼續使用")
        else:
            if old_folders:
                # 將最新的舊資料夾改名為今天的
                old_folder_path, old_date_str, old_date = old_folders[0]
                try:
                    old_folder_path.rename(today_folder_path)
                    self._update_status(f"📁 已將資料夾 {old_folder_path.name} 改名為 {today_folder_name}")
                except (OSError, PermissionError) as e:
                    self._update_status(f"❌ 改名資料夾失敗: {e}")
                    today_folder_path.mkdir(parents=True, exist_ok=True)
                    self._update_status(f"✅ 已建立新資料夾: {today_folder_name}")
            else:
                # 沒有舊資料夾，建立新的
                try:
                    today_folder_path.mkdir(parents=True, exist_ok=True)
                    self._update_status(f"✅ 已建立資料夾: {today_folder_name}")
                except (OSError, PermissionError) as e:
                    self._update_status(f"❌ 建立資料夾失敗: {e}")
                    return base_dir
        
        return today_folder_path
 
    
    def separate_name(self, text: str) -> Tuple[str, str]:
        """
        分離名稱和數量
        例如：將 "台北市(1000)" 分離為 "台北市" 和 "1000"
        
        Args:
            text: 包含名稱和數量的文字
            
        Returns:
            (名稱, 數量) 的元組
        """
        name_part, sep, num_part = text.partition('(')  # 以'('為分隔符分割字串
        name = name_part.strip()  # 去除名稱前後空白
        count = num_part.rstrip(')').strip()  # 去除數量部分的')'和空白
        return name, count  # 返回名稱和數量
    
    def get_city_data(self) -> List[Dict]:
        """
        獲取所有城市資料
        
        Returns:
            城市資料列表，每個元素包含城市名稱、數量、區域列表等資訊
        """
        try:
            self._update_status("正在獲取城市列表...")  # 更新狀態
            response = self.session.get(self.base_url, headers=self.headers, timeout=10)  # 發送GET請求
            response.raise_for_status()  # 如果請求失敗則拋出異常
            soup = BeautifulSoup(response.text, "html.parser")  # 解析HTML
            city_tree = soup.find_all('li', {'class': 'treeview'})  # 找到所有城市節點
            
            cities = []  # 初始化城市列表
            for tree in city_tree:  # 遍歷每個城市節點
                span = tree.find('span')  # 找到城市名稱的span標籤
                if not span:  # 如果沒有找到span標籤
                    continue  # 跳過這個節點
                
                city_text = span.get_text(strip=True)  # 獲取城市文字並去除空白
                city_name, city_count = self.separate_name(city_text)  # 分離城市名稱和數量
                
                # 獲取該城市的區域列表
                districts = []  # 初始化區域列表
                for city in tree.find_all('ul', {'class': 'treeview-menu'}):  # 找到區域選單
                    for dis in city.find_all('li'):  # 遍歷每個區域
                        a_tag = dis.find('a')  # 找到連結標籤
                        if not a_tag:  # 如果沒有找到連結
                            continue  # 跳過這個區域
                        a_text = a_tag.get_text(strip=True)  # 獲取連結文字
                        if a_text.startswith('全部'):  # 如果是"全部"選項
                            continue  # 跳過，不加入區域列表
                        district_name, district_count = self.separate_name(a_text)  # 分離區域名稱和數量
                        districts.append({  # 將區域資訊加入列表
                            'name': district_name,
                            'count': district_count,
                            'url': urljoin(self.base_url, unquote(a_tag['href']))  # 合併完整URL
                        })
                
                # 獲取城市全部資料的URL
                city_all_url = None  # 初始化城市全部資料URL
                for city in tree.find_all('ul', {'class': 'treeview-menu'}):  # 找到選單
                    a_tag = city.find('a')  # 找到第一個連結（通常是"全部"選項）
                    if a_tag:  # 如果找到連結
                        city_all_url = urljoin(self.base_url, unquote(a_tag['href']))  # 合併完整URL
                        break  # 找到第一個就結束
                
                cities.append({  # 將城市資訊加入列表
                    'name': city_name,
                    'count': city_count,
                    'districts': districts,
                    'all_url': city_all_url
                })
            
            self._update_status(f"成功獲取 {len(cities)} 個城市資料")  # 更新狀態
            return cities  # 返回城市列表
            
        except Exception as e:  # 捕捉任何異常
            self._update_status(f"獲取城市資料失敗: {str(e)}")  # 更新錯誤狀態
            return []  # 返回空列表

    def parse_existing_communities(self, file_path: Path) -> Dict[str, Dict[str, str]]:
        """
        解析現有檔案中的社區資料
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            字典，key為社區名稱，value為包含電話和地址的字典
        """
        communities = {}
        
        if not file_path.exists():
            return communities
        
        try:
            with file_path.open('r', encoding='utf-8') as f:
                content = f.read()
            
            # 以空行分割每個社區的資料
            blocks = re.split(r'\n\s*\n', content.strip())
            
            for block in blocks:
                if not block.strip():
                    continue
                
                lines = [line.strip() for line in block.split('\n') if line.strip()]
                if not lines:
                    continue
                
                community_name = lines[0]
                phone = ''
                address = ''
                
                # 解析電話和地址
                for line in lines[1:]:
                    if ':' in line or '：' in line:
                        separator = ':' if ':' in line else '：'
                        parts = line.split(separator, 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            
                            if key == '電話':
                                phone = value
                            elif key == '地址':
                                address = value
                
                if community_name:
                    communities[community_name] = {
                        'phone': phone,
                        'address': address
                    }
        
        except Exception as e:
            self._update_status(f"解析現有檔案時發生錯誤: {str(e)}")
        
        return communities

    def scrape_new_communities_from_web(self, url: str) -> List[Dict[str, str]]:
        """
        從網站爬取所有社區資料
        
        Args:
            url: 要爬取的URL
            
        Returns:
            社區資料列表，每個元素包含 name, phone, address
        """
        all_communities = []
        
        try:
            page = 1
            
            while not self.should_stop:
                self._update_status(f"正在爬取第 {page} 頁...")
                
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                div_tags = soup.find_all('div', {'class': 'product-info'})
                if not div_tags:
                    break
                    
                for div_tag in div_tags:
                    if self.should_stop:
                        break
                        
                    a_title = div_tag.find('a')
                    if not a_title:
                        continue
                        
                    title = a_title.text.strip().replace('\xa0', '')
                    if title:
                        phone = address = ""
                        spans = div_tag.find('span')
                        if spans:
                            for label in spans.find_all('label'):
                                label_name = label.get_text(strip=True).replace('\xa0', '')
                                label_text = label.next_sibling
                                if not label_text:
                                    continue
                                value = label_text.strip().replace('\xa0', '')
                                if label_name == "電話":
                                    phone = value
                                elif label_name == "地址":
                                    address = value
                        
                        all_communities.append({
                            'name': title,
                            'phone': phone,
                            'address': address
                        })
                
                # 尋找下一頁連結
                a_tag = soup.find('a', class_='btn btn-primary', string=re.compile(r'下一頁'))
                href = a_tag and a_tag.get('href')
                if not href:
                    break
                
                url = urljoin(self.base_url, unquote(href))
                page += 1
                time.sleep(2)  # 等待2秒，避免請求過於頻繁
        
        except Exception as e:
            self._update_status(f"爬取網站資料時發生錯誤: {str(e)}")
        
        return all_communities
    
    def compare_and_log_updates(self, old_file_path: Path, new_file_path: Path) -> List[Dict[str, str]]:
        """
        比對舊檔案和新檔案的差異，返回新增的完整社區資訊
        
        Args:
            old_file_path: 舊檔案路徑
            new_file_path: 新檔案路徑
            
        Returns:
            新增社區資訊的列表，每個元素包含 {'name': '', 'phone': '', 'address': ''}
        """
        try:
            # 解析舊檔案中的社區資訊
            old_communities = []
            if old_file_path.exists():
                with old_file_path.open('r', encoding='utf-8') as f:
                    old_content = f.read()
                
                # 以空行分割每個社區的資料
                old_blocks = re.split(r'\n\s*\n', old_content.strip())
                
                for block in old_blocks:
                    if not block.strip():
                        continue
                    
                    lines = [line.strip() for line in block.split('\n') if line.strip()]
                    if not lines:
                        continue
                    
                    community = {
                        'name': lines[0] if lines else '',
                        'phone': '',
                        'address': ''
                    }
                    
                    # 解析電話和地址
                    for line in lines[1:]:
                        if ':' in line or '：' in line:
                            separator = ':' if ':' in line else '：'
                            parts = line.split(separator, 1)
                            if len(parts) == 2:
                                key = parts[0].strip()
                                value = parts[1].strip()
                                
                                if key == '電話':
                                    community['phone'] = value
                                elif key == '地址':
                                    community['address'] = value
                    
                    if community['name']:
                        old_communities.append(community)
            
            # 解析新檔案中的社區資訊
            new_communities = []
            with new_file_path.open('r', encoding='utf-8') as f:
                new_content = f.read()
            
            # 以空行分割每個社區的資料
            new_blocks = re.split(r'\n\s*\n', new_content.strip())
            
            for block in new_blocks:
                if not block.strip():
                    continue
                
                lines = [line.strip() for line in block.split('\n') if line.strip()]
                if not lines:
                    continue
                
                community = {
                    'name': lines[0] if lines else '',
                    'phone': '',
                    'address': ''
                }
                
                # 解析電話和地址
                for line in lines[1:]:
                    if ':' in line or '：' in line:
                        separator = ':' if ':' in line else '：'
                        parts = line.split(separator, 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            
                            if key == '電話':
                                community['phone'] = value
                            elif key == '地址':
                                community['address'] = value
                
                if community['name']:
                    new_communities.append(community)
            
            # 創建舊社區名稱的集合，用於快速查找
            old_community_names = {community['name'] for community in old_communities}
            
            # 找出新增的社區
            new_items = []
            for community in new_communities:
                if community['name'] not in old_community_names:
                    new_items.append(community)
            
            return new_items
            
        except Exception as e:
            self._update_status(f"比對檔案差異時發生錯誤: {str(e)}")
            return []
    
    def create_update_log(self, updates: Dict[str, List[Dict[str, str]]]):
        """
        建立增強版更新日誌 - 包含完整的社區資訊
        
        Args:
            updates: 更新項目字典，key為檔案名稱，value為新增社區資訊列表
        """
        try:
            if not any(updates.values()):
                self._update_status("沒有新增項目，不建立更新日誌")
                return
            
            # 建立更新日誌資料夾
            log_folder = Path(self.output_folder) / "資料更新日誌"
            log_folder.mkdir(parents=True, exist_ok=True)
            
            # 建立更新日誌檔案 (使用日期命名)
            date_str = datetime.now().strftime("%Y-%m-%d")
            log_file_path = log_folder / f"{date_str}資料更新日誌.txt"
            
            with log_file_path.open('a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"資料更新日誌 - {timestamp}\n")
                f.write("=" * 60 + "\n\n")
                
                total_new_items = 0
                for file_name, new_communities in updates.items():
                    if new_communities:
                        f.write(f"檔案: {file_name}\n")
                        f.write(f"新增項目數量: {len(new_communities)}\n")
                        f.write("-" * 40 + "\n")
                        
                        for community in new_communities:
                            # 社區名稱
                            f.write(f"+ {community['name']}\n")
                            
                            # 電話資訊
                            phone = community.get('phone', '') or '未提供'
                            f.write(f"  📞 電話: {phone}\n")
                            
                            # 地址資訊
                            address = community.get('address', '') or '未提供'
                            f.write(f"  📍 地址: {address}\n")
                            
                            f.write("\n")  # 每個社區後添加空行
                        
                        f.write("\n")
                        total_new_items += len(new_communities)
                
                f.write(f"總計新增項目: {total_new_items} 筆\n")
                f.write("=" * 60 + "\n")
            
            self._update_status(f"已建立更新日誌: {log_file_path}")
            
        except Exception as e:
            self._update_status(f"建立更新日誌時發生錯誤: {str(e)}") 

    
    def find_data(self, url: str, city_name: str, district_name: Optional[str], 
                  count: str, do_dis: str, city_count: Optional[str] = None) -> bool:
        """
        爬取社區資料 - 修改為增量更新模式，在檔案內直接顯示更新日誌
        
        Args:
            url: 要爬取的URL
            city_name: 城市名稱
            district_name: 區域名稱（可選）
            count: 資料數量
            do_dis: 是否分區（"是"或"否"）
            city_count: 城市總筆數（可選）

        Returns:
            True表示成功，False表示失敗
        """
        try:
            city_folder = self.create_city_folder(city_name, city_count)
            
            today_str = datetime.now().strftime("%Y_%m_%d")
            # 根據是否分區設定檔案名稱
            if do_dis == "否":
                file_name = f"{city_name}全部社區資料(共有{count}筆)_{today_str}.txt"
            elif do_dis == "是":
                file_name = f"{city_name}{district_name}社區資料(共有{count}筆)_{today_str}.txt"
            
            file_path = city_folder / file_name
            
            self._update_status(f"正在爬取: {file_name}")
            self._update_status(f"輸出路徑: {file_path}")
            
            # 1. 解析現有檔案中的所有社區資料（包含舊資料和之前新增的）
            existing_communities = {}
            if file_path.exists():
                with file_path.open('r', encoding='utf-8') as f:
                    content = f.read()
                existing_communities = self.parse_existing_communities_from_content(content)
                self._update_status(f"現有檔案中已有 {len(existing_communities)} 筆社區資料")
            
            # 2. 從網站爬取所有社區資料
            self._update_status("開始從網站爬取最新資料...")
            all_web_communities = self.scrape_new_communities_from_web(url)
            
            if self.should_stop:
                return False
            
            self._update_status(f"從網站爬取到 {len(all_web_communities)} 筆社區資料")
            
            # 3. 找出新增的社區
            new_communities = []
            for community in all_web_communities:
                if community['name'] not in existing_communities:
                    new_communities.append(community)
            
            self._update_status(f"發現 {len(new_communities)} 筆新增社區資料")
            
            # 4. 重新組織所有資料：將所有現有資料（包括之前新增的）整合為標準格式
            with file_path.open(mode="w", encoding="utf-8") as file:
                # 寫入所有現有社區（標準格式）
                all_existing_from_web = []
                for community in all_web_communities:
                    if community['name'] in existing_communities:
                        all_existing_from_web.append(community)
                
                # 寫入現有社區資料（標準格式）
                for community in all_existing_from_web:
                    file.write(f"{community['name']}\n")
                    file.write(f"電話: {community['phone']}\n")
                    file.write(f"地址: {community['address']}\n")
                    file.write("\n")
                
                # 如果有新增資料，添加更新日誌格式
                if new_communities:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write("============================================================\n")
                    file.write(f"資料更新日誌 - {timestamp}\n")
                    file.write("============================================================\n")
                    file.write(f"檔案: {file_name}\n")
                    file.write(f"新增項目數量: {len(new_communities)}\n")
                    file.write("----------------------------------------\n")
                    
                    for community in new_communities:
                        file.write(f"+ {community['name']}\n")
                        phone = community.get('phone', '') or '未提供'
                        file.write(f"  📞 電話: {phone}\n")
                        address = community.get('address', '') or '未提供'
                        file.write(f"  📍 地址: {address}\n")
                        file.write("\n")
                    
                    file.write(f"總計新增項目: {len(new_communities)} 筆\n")
                    
                    self._update_status(f"✅ 已將 {len(new_communities)} 筆新增資料加入檔案")
                else:
                    self._update_status("📋 沒有發現新增資料")
            
            # 記錄更新資訊用於外部日誌（如果需要的話）
            if hasattr(self, '_update_log_data'):
                self._update_log_data[file_name] = new_communities
            else:
                self._update_log_data = {file_name: new_communities}
            
            if not self.should_stop:
                self._update_status(f"完成處理: {file_name}")
                return True
            else:
                self._update_status("處理已停止")
                return False
                
        except Exception as e:
            self._update_status(f"處理失敗: {str(e)}")
            return False

    def parse_existing_communities_from_content(self, content: str) -> Dict[str, Dict[str, str]]:
        """
        從內容字串解析現有的社區資料（包含舊資料和之前新增的資料）
        
        Args:
            content: 檔案內容字串
            
        Returns:
            字典，key為社區名稱，value為包含電話和地址的字典
        """
        communities = {}
        
        if not content.strip():
            return communities
        
        try:
            # 先處理舊資料部分（分隔線之前的內容）
            separator_pattern = r'={60,}'
            parts = re.split(separator_pattern, content)
            
            if parts:
                # 解析分隔線之前的舊資料
                old_data_content = parts[0].strip()
                if old_data_content:
                    old_communities = self._parse_community_blocks(old_data_content)
                    communities.update(old_communities)
                
                # 如果有更新日誌部分，解析其中的新增資料
                if len(parts) > 1:
                    log_content = ''.join(parts[1:])  # 合併所有更新日誌部分
                    new_communities = self._parse_update_log_communities(log_content)
                    communities.update(new_communities)
            else:
                # 沒有分隔線，整個內容都是舊資料
                all_communities = self._parse_community_blocks(content)
                communities.update(all_communities)
        
        except Exception as e:
            self._update_status(f"解析現有內容時發生錯誤: {str(e)}")
        
        return communities

    def _parse_community_blocks(self, content: str) -> Dict[str, Dict[str, str]]:
        """
        解析標準格式的社區資料區塊
        
        Args:
            content: 要解析的內容
            
        Returns:
            解析出的社區資料字典
        """
        communities = {}
        
        # 以空行分割每個社區的資料
        blocks = re.split(r'\n\s*\n', content.strip())
        
        for block in blocks:
            if not block.strip():
                continue
            
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if not lines:
                continue
            
            community_name = lines[0]
            phone = ''
            address = ''
            
            # 解析電話和地址
            for line in lines[1:]:
                if ':' in line or '：' in line:
                    separator = ':' if ':' in line else '：'
                    parts = line.split(separator, 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        
                        if key == '電話':
                            phone = value
                        elif key == '地址':
                            address = value
            
            if community_name:
                communities[community_name] = {
                    'phone': phone,
                    'address': address
                }
        
        return communities

    def _parse_update_log_communities(self, log_content: str) -> Dict[str, Dict[str, str]]:
        """
        解析更新日誌中的社區資料
        
        Args:
            log_content: 更新日誌內容
            
        Returns:
            解析出的社區資料字典
        """
        communities = {}
        
        try:
            # 尋找所有以 "+ " 開頭的社區名稱行
            lines = log_content.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # 找到社區名稱行（以 "+ " 開頭）
                if line.startswith('+ '):
                    community_name = line[2:].strip()  # 去除 "+ " 前綴
                    phone = ''
                    address = ''
                    
                    # 查看接下來的幾行，尋找電話和地址
                    j = i + 1
                    while j < len(lines) and j < i + 5:  # 最多檢查後面5行
                        next_line = lines[j].strip()
                        
                        # 如果遇到下一個社區或其他分隔內容，停止
                        if (next_line.startswith('+ ') or 
                            next_line.startswith('總計新增項目') or
                            next_line.startswith('============')):
                            break
                        
                        # 解析電話和地址
                        if '📞 電話:' in next_line:
                            phone = next_line.split('📞 電話:', 1)[1].strip()
                        elif '📍 地址:' in next_line:
                            address = next_line.split('📍 地址:', 1)[1].strip()
                        
                        j += 1
                    
                    if community_name:
                        communities[community_name] = {
                            'phone': phone,
                            'address': address
                        }
                    
                    i = j  # 跳到處理完的位置
                else:
                    i += 1
        
        except Exception as e:
            self._update_status(f"解析更新日誌時發生錯誤: {str(e)}")
        
        return communities
    
    def scrape_all_cities_with_districts(self, cities_data: List[Dict]) -> bool:
        """
        爬取全部城市分區資料
        
        Args:
            cities_data: 城市資料列表
            
        Returns:
            True表示成功，False表示失敗
        """
        try:
            # 初始化更新日誌資料
            self._update_log_data = {}
            
            # 計算所有城市的總區域數量
            total_districts = sum(len(city['districts']) for city in cities_data)
            current_district = 0  # 當前處理的區域數量
            
            for city in cities_data:  # 遍歷每個城市
                if self.should_stop:  # 如果需要停止
                    break  # 結束迴圈
                    
                self.create_city_folder(city['name'], city['count'])  # 建立城市資料夾
                
                for district in city['districts']:  # 遍歷城市的每個區域
                    if self.should_stop:  # 如果需要停止
                        break  # 結束迴圈
                        
                    current_district += 1  # 區域計數加1
                    self._update_progress(current_district, total_districts)  # 更新進度
                    
                    success = self.find_data(  # 爬取區域資料
                        district['url'], 
                        city['name'], 
                        district['name'], 
                        district['count'], 
                        "是",
                        city['count']
                    )
                    if not success:  # 如果爬取失敗
                        return False  # 返回失敗
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return not self.should_stop  # 如果沒有停止則返回成功
            
        except Exception as e:  # 捕捉異常
            self._update_status(f"爬取全部城市分區資料失敗: {str(e)}")  # 更新錯誤狀態
            return False  # 返回失敗

    def scrape_single_city_with_districts(self, city_data: Dict) -> bool:
        """
        爬取單一城市分區資料
        
        Args:
            city_data: 城市資料字典
            
        Returns:
            True表示成功，False表示失敗
        """
        try:
            # 初始化更新日誌資料
            self._update_log_data = {}
            
            self.create_city_folder(city_data['name'], city_data['count'])  # 建立城市資料夾
            total_districts = len(city_data['districts'])  # 總區域數量
            
            for i, district in enumerate(city_data['districts']):  # 遍歷每個區域
                if self.should_stop:  # 如果需要停止
                    break  # 結束迴圈
                    
                self._update_progress(i + 1, total_districts)  # 更新進度
                
                success = self.find_data(  # 爬取區域資料
                    district['url'], 
                    city_data['name'], 
                    district['name'], 
                    district['count'], 
                    "是",
                    city_data['count']
                )
                if not success:  # 如果爬取失敗
                    return False  # 返回失敗
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return not self.should_stop  # 如果沒有停止則返回成功
            
        except Exception as e:  # 捕捉異常
            self._update_status(f"爬取單一城市分區資料失敗: {str(e)}")  # 更新錯誤狀態
            return False  # 返回失敗
    
    def scrape_single_district(self, city_data: Dict, district_name: str) -> bool:
        """
        爬取單一區域資料
        
        Args:
            city_data: 城市資料字典
            district_name: 區域名稱
            
        Returns:
            True表示成功，False表示失敗
        """
        try:
            # 初始化更新日誌資料
            self._update_log_data = {}
            
            self.create_city_folder(city_data['name'], city_data['count'])  # 建立城市資料夾
            
            # 尋找指定的區域
            target_district = None  # 初始化目標區域
            for district in city_data['districts']:  # 遍歷所有區域
                if district['name'] == district_name:  # 如果找到指定區域
                    target_district = district  # 設定目標區域
                    break  # 結束搜尋
            
            if not target_district:  # 如果沒有找到指定區域
                self._update_status(f"找不到區域: {district_name}")  # 更新錯誤狀態
                return False  # 返回失敗
            
            self._update_progress(1, 1)  # 設定進度為100%
            
            success = self.find_data(  # 爬取區域資料
                target_district['url'], 
                city_data['name'], 
                target_district['name'], 
                target_district['count'], 
                "是",
                city_data['count']
            )
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return success  # 返回爬取結果
            
        except Exception as e:  # 捕捉異常
            self._update_status(f"爬取單一區域資料失敗: {str(e)}")  # 更新錯誤狀態
            return False  # 返回失敗