#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Community Data Scraper Module
增強版社區資料爬蟲模組 - 支援智慧檔案管理
Contains all the web scraping logic with integrated file management
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

# 匯入檔案管理器
from file_manager import SmartFileManager


class CommunityDataScraper:
    """
    增強版社區資料爬蟲類別
    
    新增功能：
    1. 整合智慧檔案管理器
    2. 支援自動檔案清理和備份
    3. 增強的錯誤處理和狀態回報
    4. 更靈活的輸出管理
    """
    
    def __init__(self, progress_callback: Optional[Callable] = None, 
                 status_callback: Optional[Callable] = None, 
                 output_folder: Optional[str] = None,
                 file_manager: Optional[SmartFileManager] = None,
                 auto_cleanup: bool = True,
                 enable_backup: bool = True):
        """
        初始化增強版爬蟲
        
        Args:
            progress_callback: 進度更新回調函數
            status_callback: 狀態更新回調函數
            output_folder: 輸出資料夾路徑
            file_manager: 檔案管理器實例
            auto_cleanup: 是否自動清理舊檔案
            enable_backup: 是否啟用備份功能
        """
        self.base_url = "https://group.lifego.tw/"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        self.session = self._build_session()
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.should_stop = False
        self.output_folder = output_folder or os.getcwd()
        
        # 檔案管理設定 ⭐ 新增
        self.auto_cleanup = auto_cleanup
        self.enable_backup = enable_backup
        
        # 初始化檔案管理器
        if file_manager:
            self.file_manager = file_manager
        else:
            self.file_manager = SmartFileManager(
                self.output_folder, 
                enable_backup=enable_backup
            )
        
        # 統計資訊
        self.scrape_stats = {
            'start_time': None,
            'end_time': None,
            'total_communities': 0,
            'new_communities': 0,
            'processed_files': 0,
            'cleaned_files': 0
        }
        
    def _build_session(self) -> requests.Session:
        """建立支援重試的 Session"""
        session = requests.Session()
        retries = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            raise_on_status=False
        )
           
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session
    
    def _update_status(self, message: str):
        """更新狀態訊息"""
        if self.status_callback:
            self.status_callback(message)
    
    def _update_progress(self, current: int, total: int):
        """更新進度"""
        if self.progress_callback:
            self.progress_callback(current, total)
    
    def stop_scraping(self):
        """停止爬取"""
        self.should_stop = True
        self._update_status("⏹️ 用戶請求停止爬取")
    
    def get_scrape_statistics(self) -> Dict:
        """取得爬取統計資訊"""
        stats = self.scrape_stats.copy()
        if stats['start_time'] and stats['end_time']:
            duration = stats['end_time'] - stats['start_time']
            stats['duration_seconds'] = duration.total_seconds()
            stats['duration_formatted'] = self._format_duration(duration.total_seconds())
        return stats
    
    def _format_duration(self, seconds: float) -> str:
        """格式化持續時間"""
        if seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分鐘"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}小時"
    
    def create_city_folder(self, city_name: str, city_count: Optional[str] = None) -> Path:
        """
        建立城市資料夾 - 增強版
        
        Args:
            city_name: 城市名稱
            city_count: 城市資料總筆數
            
        Returns:
            城市資料夾的Path物件
        """
        if city_count:
            city_data_name = f"{city_name}({city_count}筆資料)"
        else:
            city_data_name = city_name
        
        today_str = datetime.now().strftime("%Y_%m_%d")
        today_folder_name = f"{city_data_name}_{today_str}"
        
        base_dir = Path(self.output_folder)
        base_dir.mkdir(parents=True, exist_ok=True)
        
        today_folder_path = base_dir / today_folder_name
        
        # 檢查是否需要重命名舊資料夾
        escaped_city_name = re.escape(city_data_name)
        pattern = re.compile(rf"^{escaped_city_name}_(\d{{4}}_\d{{2}}_\d{{2}})$")
        
        old_folders = []
        try:
            for entry in base_dir.iterdir():
                if entry.is_dir() and pattern.match(entry.name):
                    if entry.name != today_folder_name:
                        date_match = pattern.match(entry.name)
                        if date_match:
                            date_str = date_match.group(1)
                            try:
                                folder_date = datetime.strptime(date_str, "%Y_%m_%d")
                                old_folders.append((entry, date_str, folder_date))
                            except ValueError:
                                self._update_status(f"⚠️ 無法解析資料夾日期: {date_str}")
        except (OSError, PermissionError) as e:
            self._update_status(f"⚠️ 讀取目錄時發生錯誤: {e}")
        
        old_folders.sort(key=lambda x: x[2], reverse=True)
        
        if today_folder_path.exists():
            self._update_status(f"📂 今天的資料夾 {today_folder_name} 已存在，繼續使用")
        else:
            if old_folders and self.auto_cleanup:
                # 使用檔案管理器處理舊資料夾
                old_folder_path, old_date_str, old_date = old_folders[0]
                try:
                    if self.enable_backup:
                        # 備份舊資料夾
                        backup_folder = self.file_manager.backup_folder / old_folder_path.name
                        if backup_folder.exists():
                            timestamp = datetime.now().strftime('%H%M%S')
                            backup_folder = backup_folder.with_name(f"{backup_folder.name}_{timestamp}")
                        
                        backup_folder.parent.mkdir(parents=True, exist_ok=True)
                        old_folder_path.rename(backup_folder)
                        self._update_status(f"📦 已備份舊資料夾: {old_folder_path.name} -> 備份檔案/{backup_folder.name}")
                    
                    # 建立新資料夾
                    today_folder_path.mkdir(parents=True, exist_ok=True)
                    self._update_status(f"✅ 已建立新資料夾: {today_folder_name}")
                    
                except (OSError, PermissionError) as e:
                    self._update_status(f"❌ 處理舊資料夾失敗: {e}")
                    today_folder_path.mkdir(parents=True, exist_ok=True)
                    self._update_status(f"✅ 已建立新資料夾: {today_folder_name}")
            else:
                try:
                    today_folder_path.mkdir(parents=True, exist_ok=True)
                    self._update_status(f"✅ 已建立資料夾: {today_folder_name}")
                except (OSError, PermissionError) as e:
                    self._update_status(f"❌ 建立資料夾失敗: {e}")
                    return base_dir
        
        return today_folder_path
 
    def separate_name(self, text: str) -> Tuple[str, str]:
        """分離名稱和數量"""
        name_part, sep, num_part = text.partition('(')
        name = name_part.strip()
        count = num_part.rstrip(')').strip()
        return name, count
    
    def get_city_data(self) -> List[Dict]:
        """獲取所有城市資料"""
        try:
            self._update_status("🌐 正在連接目標網站...")
            response = self.session.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            self._update_status("📝 正在解析城市列表...")
            soup = BeautifulSoup(response.text, "html.parser")
            city_tree = soup.find_all('li', {'class': 'treeview'})
            
            cities = []
            total_districts = 0
            
            for tree in city_tree:
                span = tree.find('span')
                if not span:
                    continue
                
                city_text = span.get_text(strip=True)
                city_name, city_count = self.separate_name(city_text)
                
                # 獲取該城市的區域列表
                districts = []
                for city in tree.find_all('ul', {'class': 'treeview-menu'}):
                    for dis in city.find_all('li'):
                        a_tag = dis.find('a')
                        if not a_tag:
                            continue
                        a_text = a_tag.get_text(strip=True)
                        if a_text.startswith('全部'):
                            continue
                        district_name, district_count = self.separate_name(a_text)
                        districts.append({
                            'name': district_name,
                            'count': district_count,
                            'url': urljoin(self.base_url, unquote(a_tag['href']))
                        })
                
                # 獲取城市全部資料的URL
                city_all_url = None
                for city in tree.find_all('ul', {'class': 'treeview-menu'}):
                    a_tag = city.find('a')
                    if a_tag:
                        city_all_url = urljoin(self.base_url, unquote(a_tag['href']))
                        break
                
                cities.append({
                    'name': city_name,
                    'count': city_count,
                    'districts': districts,
                    'all_url': city_all_url
                })
                
                total_districts += len(districts)
            
            self._update_status(f"✅ 成功載入 {len(cities)} 個城市，共 {total_districts} 個區域")
            return cities
            
        except Exception as e:
            self._update_status(f"❌ 獲取城市資料失敗: {str(e)}")
            return []

    def scrape_new_communities_from_web(self, url: str) -> List[Dict[str, str]]:
        """從網站爬取所有社區資料"""
        all_communities = []
        
        try:
            page = 1
            
            while not self.should_stop:
                self._update_status(f"📄 正在爬取第 {page} 頁...")
                
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                div_tags = soup.find_all('div', {'class': 'product-info'})
                if not div_tags:
                    self._update_status(f"📋 第 {page} 頁沒有更多資料，爬取完成")
                    break
                    
                page_communities = 0
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
                        page_communities += 1
                
                self._update_status(f"📊 第 {page} 頁找到 {page_communities} 筆社區資料")
                
                # 尋找下一頁連結
                a_tag = soup.find('a', class_='btn btn-primary', string=re.compile(r'下一頁'))
                href = a_tag and a_tag.get('href')
                if not href:
                    break
                
                url = urljoin(self.base_url, unquote(href))
                page += 1
                time.sleep(2)  # 避免請求過於頻繁
            
            if not self.should_stop:
                self._update_status(f"🎯 網站爬取完成，共取得 {len(all_communities)} 筆社區資料")
        
        except Exception as e:
            self._update_status(f"❌ 爬取網站資料時發生錯誤: {str(e)}")
        
        return all_communities
    
    def parse_existing_communities_from_content(self, content: str) -> Dict[str, Dict[str, str]]:
        """從內容字串解析現有的社區資料"""
        communities = {}
        
        if not content.strip():
            return communities
        
        try:
            # 分離標準資料和更新日誌
            separator_pattern = r'={60,}'
            parts = re.split(separator_pattern, content)
            
            if parts:
                # 解析標準資料部分
                old_data_content = parts[0].strip()
                if old_data_content:
                    old_communities = self._parse_community_blocks(old_data_content)
                    communities.update(old_communities)
                
                # 解析更新日誌部分
                if len(parts) > 1:
                    log_content = ''.join(parts[1:])
                    new_communities = self._parse_update_log_communities(log_content)
                    communities.update(new_communities)
            else:
                # 整個內容都是標準資料
                all_communities = self._parse_community_blocks(content)
                communities.update(all_communities)
        
        except Exception as e:
            self._update_status(f"❌ 解析現有內容時發生錯誤: {str(e)}")
        
        return communities

    def _parse_community_blocks(self, content: str) -> Dict[str, Dict[str, str]]:
        """解析標準格式的社區資料區塊"""
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
        """解析更新日誌中的社區資料"""
        communities = {}
        
        try:
            lines = log_content.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # 找到社區名稱行（以 "+ " 開頭）
                if line.startswith('+ '):
                    community_name = line[2:].strip()
                    phone = ''
                    address = ''
                    
                    # 查看接下來的行，尋找電話和地址
                    j = i + 1
                    while j < len(lines) and j < i + 5:
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
                    
                    i = j
                else:
                    i += 1
        
        except Exception as e:
            self._update_status(f"❌ 解析更新日誌時發生錯誤: {str(e)}")
        
        return communities
    
    def find_data(self, url: str, city_name: str, district_name: Optional[str], 
                  count: str, do_dis: str, city_count: Optional[str] = None) -> bool:
        """
        爬取社區資料 - 增強版增量更新模式
        
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
            # 建立城市資料夾
            city_folder = self.create_city_folder(city_name, city_count)
            
            # 生成檔案名稱
            today_str = datetime.now().strftime("%Y_%m_%d")
            if do_dis == "否":
                file_name = f"{city_name}全部社區資料(共有{count}筆)_{today_str}.txt"
            elif do_dis == "是":
                file_name = f"{city_name}{district_name}社區資料(共有{count}筆)_{today_str}.txt"
            
            file_path = city_folder / file_name
            
            self._update_status(f"🎯 正在處理: {file_name}")
            self._update_status(f"📁 輸出路徑: {file_path}")
            
            # 解析現有檔案中的社區資料
            existing_communities = {}
            if file_path.exists():
                with file_path.open('r', encoding='utf-8') as f:
                    content = f.read()
                existing_communities = self.parse_existing_communities_from_content(content)
                self._update_status(f"📋 現有檔案中已有 {len(existing_communities)} 筆社區資料")
            
            # 從網站爬取最新資料
            self._update_status("🕷️ 開始從網站爬取最新資料...")
            all_web_communities = self.scrape_new_communities_from_web(url)
            
            if self.should_stop:
                return False
            
            self._update_status(f"📊 從網站爬取到 {len(all_web_communities)} 筆社區資料")
            
            # 找出新增的社區
            new_communities = []
            for community in all_web_communities:
                if community['name'] not in existing_communities:
                    new_communities.append(community)
            
            self._update_status(f"🆕 發現 {len(new_communities)} 筆新增社區資料")
            
            # 寫入檔案
            success = self._write_community_data_file(
                file_path, all_web_communities, existing_communities, 
                new_communities, file_name
            )
            
            # 更新統計資訊
            if success:
                self.scrape_stats['total_communities'] += len(all_web_communities)
                self.scrape_stats['new_communities'] += len(new_communities)
                self.scrape_stats['processed_files'] += 1
                
                # 記錄更新日誌
                if hasattr(self, '_update_log_data'):
                    self._update_log_data[file_name] = new_communities
                else:
                    self._update_log_data = {file_name: new_communities}
            
            if not self.should_stop and success:
                self._update_status(f"✅ 完成處理: {file_name}")
                return True
            else:
                self._update_status("⏹️ 處理已停止或失敗")
                return False
                
        except Exception as e:
            self._update_status(f"❌ 處理失敗: {str(e)}")
            return False

    def _write_community_data_file(self, file_path: Path, all_web_communities: List[Dict], 
                                  existing_communities: Dict, new_communities: List[Dict], 
                                  file_name: str) -> bool:
        """
        寫入社區資料檔案
        
        Args:
            file_path: 檔案路徑
            all_web_communities: 所有網站社區資料
            existing_communities: 現有社區資料
            new_communities: 新增社區資料
            file_name: 檔案名稱
            
        Returns:
            True表示成功，False表示失敗
        """
        try:
            with file_path.open(mode="w", encoding="utf-8") as file:
                # 寫入現有社區資料（標準格式）
                existing_from_web = []
                for community in all_web_communities:
                    if community['name'] in existing_communities:
                        existing_from_web.append(community)
                
                # 寫入現有資料
                for community in existing_from_web:
                    file.write(f"{community['name']}\n")
                    file.write(f"電話: {community['phone']}\n")
                    file.write(f"地址: {community['address']}\n")
                    file.write("\n")
                
                # 如果有新增資料，添加更新日誌
                if new_communities:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    file.write("============================================================\n")
                    file.write(f"📊 資料更新日誌 - {timestamp}\n")
                    file.write("============================================================\n")
                    file.write(f"📁 檔案: {file_name}\n")
                    file.write(f"🆕 新增項目數量: {len(new_communities)}\n")
                    file.write("----------------------------------------\n")
                    
                    for community in new_communities:
                        file.write(f"+ {community['name']}\n")
                        phone = community.get('phone', '') or '未提供'
                        file.write(f"  📞 電話: {phone}\n")
                        address = community.get('address', '') or '未提供'
                        file.write(f"  📍 地址: {address}\n")
                        file.write("\n")
                    
                    file.write(f"📈 總計新增項目: {len(new_communities)} 筆\n")
                    file.write("============================================================\n")
                    
                    self._update_status(f"✅ 已將 {len(new_communities)} 筆新增資料加入檔案")
                else:
                    self._update_status("📋 沒有發現新增資料，檔案已更新")
            
            return True
            
        except Exception as e:
            self._update_status(f"❌ 寫入檔案失敗: {str(e)}")
            return False

    def create_update_log(self, updates: Dict[str, List[Dict[str, str]]]):
        """建立增強版更新日誌"""
        try:
            if not any(updates.values()):
                self._update_status("📋 沒有新增項目，不建立更新日誌")
                return
            
            # 建立更新日誌資料夾
            log_folder = Path(self.output_folder) / "資料更新日誌"
            log_folder.mkdir(parents=True, exist_ok=True)
            
            # 建立更新日誌檔案
            date_str = datetime.now().strftime("%Y-%m-%d")
            log_file_path = log_folder / f"{date_str}資料更新日誌.txt"
            
            with log_file_path.open('a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write("=" * 80 + "\n")
                f.write(f"📊 社區資料爬蟲 - 更新日誌\n")
                f.write(f"🕐 更新時間: {timestamp}\n")
                f.write("=" * 80 + "\n\n")
                
                total_new_items = 0
                for file_name, new_communities in updates.items():
                    if new_communities:
                        f.write(f"📁 檔案: {file_name}\n")
                        f.write(f"🆕 新增項目數量: {len(new_communities)}\n")
                        f.write("-" * 60 + "\n")
                        
                        for i, community in enumerate(new_communities, 1):
                            f.write(f"{i:3d}. {community['name']}\n")
                            phone = community.get('phone', '') or '未提供'
                            f.write(f"     📞 電話: {phone}\n")
                            address = community.get('address', '') or '未提供'
                            f.write(f"     📍 地址: {address}\n")
                            f.write("\n")
                        
                        f.write(f"小計: {len(new_communities)} 筆\n")
                        f.write("\n")
                        total_new_items += len(new_communities)
                
                f.write("=" * 80 + "\n")
                f.write(f"📈 本次更新總計: {total_new_items} 筆新增資料\n")
                
                # 添加統計摘要
                stats = self.get_scrape_statistics()
                if stats.get('duration_formatted'):
                    f.write(f"⏱️ 處理時間: {stats['duration_formatted']}\n")
                f.write(f"📄 處理檔案數: {stats.get('processed_files', 0)}\n")
                
                f.write("=" * 80 + "\n\n")
            
            self._update_status(f"📋 已建立更新日誌: {log_file_path}")
            
        except Exception as e:
            self._update_status(f"❌ 建立更新日誌時發生錯誤: {str(e)}")
    
    def scrape_all_cities_with_districts(self, cities_data: List[Dict]) -> bool:
        """爬取全部城市分區資料 - 增強版"""
        try:
            self.scrape_stats['start_time'] = datetime.now()
            self._update_log_data = {}
            
            # 計算總區域數量
            total_districts = sum(len(city['districts']) for city in cities_data)
            current_district = 0
            
            self._update_status(f"🚀 開始爬取全部城市分區資料，共 {len(cities_data)} 個城市，{total_districts} 個區域")
            
            for city_index, city in enumerate(cities_data, 1):
                if self.should_stop:
                    break
                    
                self._update_status(f"🏙️ 處理第 {city_index}/{len(cities_data)} 個城市: {city['name']}")
                self.create_city_folder(city['name'], city['count'])
                
                for district_index, district in enumerate(city['districts'], 1):
                    if self.should_stop:
                        break
                        
                    current_district += 1
                    self._update_progress(current_district, total_districts)
                    
                    self._update_status(f"🏘️ 處理 {city['name']} 第 {district_index}/{len(city['districts'])} 個區域: {district['name']}")
                    
                    success = self.find_data(
                        district['url'], 
                        city['name'], 
                        district['name'], 
                        district['count'], 
                        "是",
                        city['count']
                    )
                    if not success:
                        self._update_status(f"❌ 處理 {city['name']}-{district['name']} 失敗")
                        return False
            
            # 自動清理檔案（如果啟用）
            if self.auto_cleanup and not self.should_stop:
                self._perform_auto_cleanup()
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data') and not self.should_stop:
                self.create_update_log(self._update_log_data)
            
            self.scrape_stats['end_time'] = datetime.now()
            
            if not self.should_stop:
                stats = self.get_scrape_statistics()
                self._update_status(f"🎉 全部城市分區爬取完成！")
                self._update_status(f"📊 統計: 處理了 {stats['processed_files']} 個檔案，"
                                  f"總計 {stats['total_communities']} 筆社區資料，"
                                  f"新增 {stats['new_communities']} 筆，"
                                  f"耗時 {stats.get('duration_formatted', '未知')}")
                return True
            else:
                self._update_status("⏹️ 爬取已被用戶停止")
                return False
            
        except Exception as e:
            self.scrape_stats['end_time'] = datetime.now()
            self._update_status(f"❌ 爬取全部城市分區資料失敗: {str(e)}")
            return False

    def _perform_auto_cleanup(self):
        """執行自動檔案清理"""
        try:
            self._update_status("🧹 開始執行自動檔案清理...")
            
            patterns = ["*社區資料*.txt", "*城市*.txt", "*區域*.txt"]
            total_cleaned = 0
            
            for pattern in patterns:
                cleaned_files = self.file_manager.clean_old_files(pattern, keep_latest=1)
                total_cleaned += len(cleaned_files)
            
            if total_cleaned > 0:
                self.scrape_stats['cleaned_files'] = total_cleaned
                self._update_status(f"✅ 自動清理完成，處理了 {total_cleaned} 個舊檔案")
            else:
                self._update_status("📋 沒有需要清理的舊檔案")
                
        except Exception as e:
            self._update_status(f"❌ 自動清理檔案時發生錯誤: {str(e)}")

    def scrape_single_city_with_districts(self, city_data: Dict) -> bool:
        """爬取單一城市分區資料 - 增強版"""
        try:
            self.scrape_stats['start_time'] = datetime.now()
            self._update_log_data = {}
            
            self._update_status(f"🏙️ 開始爬取 {city_data['name']} 的分區資料")
            self.create_city_folder(city_data['name'], city_data['count'])
            total_districts = len(city_data['districts'])
            
            for i, district in enumerate(city_data['districts']):
                if self.should_stop:
                    break
                    
                self._update_progress(i + 1, total_districts)
                self._update_status(f"🏘️ 處理第 {i+1}/{total_districts} 個區域: {district['name']}")
                
                success = self.find_data(
                    district['url'], 
                    city_data['name'], 
                    district['name'], 
                    district['count'], 
                    "是",
                    city_data['count']
                )
                if not success:
                    return False
            
            # 自動清理檔案（如果啟用）
            if self.auto_cleanup and not self.should_stop:
                self._perform_auto_cleanup()
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data') and not self.should_stop:
                self.create_update_log(self._update_log_data)
            
            self.scrape_stats['end_time'] = datetime.now()
            
            if not self.should_stop:
                stats = self.get_scrape_statistics()
                self._update_status(f"🎉 {city_data['name']} 分區爬取完成！")
                self._update_status(f"📊 統計: 處理了 {stats['processed_files']} 個檔案，"
                                  f"總計 {stats['total_communities']} 筆社區資料，"
                                  f"新增 {stats['new_communities']} 筆，"
                                  f"耗時 {stats.get('duration_formatted', '未知')}")
                return True
            else:
                return False
            
        except Exception as e:
            self.scrape_stats['end_time'] = datetime.now()
            self._update_status(f"❌ 爬取單一城市分區資料失敗: {str(e)}")
            return False
    
    def scrape_single_district(self, city_data: Dict, district_name: str) -> bool:
        """爬取單一區域資料 - 增強版"""
        try:
            self.scrape_stats['start_time'] = datetime.now()
            self._update_log_data = {}
            
            self._update_status(f"🏘️ 開始爬取 {city_data['name']}-{district_name} 的資料")
            self.create_city_folder(city_data['name'], city_data['count'])
            
            # 尋找指定的區域
            target_district = None
            for district in city_data['districts']:
                if district['name'] == district_name:
                    target_district = district
                    break
            
            if not target_district:
                self._update_status(f"❌ 找不到區域: {district_name}")
                return False
            
            self._update_progress(1, 1)
            
            success = self.find_data(
                target_district['url'], 
                city_data['name'], 
                target_district['name'], 
                target_district['count'], 
                "是",
                city_data['count']
            )
            
            # 建立更新日誌
            if hasattr(self, '_update_log_data') and success:
                self.create_update_log(self._update_log_data)
            
            self.scrape_stats['end_time'] = datetime.now()
            
            if success and not self.should_stop:
                stats = self.get_scrape_statistics()
                self._update_status(f"🎉 {city_data['name']}-{district_name} 爬取完成！")
                self._update_status(f"📊 統計: 處理了 {stats['processed_files']} 個檔案，"
                                  f"總計 {stats['total_communities']} 筆社區資料，"
                                  f"新增 {stats['new_communities']} 筆，"
                                  f"耗時 {stats.get('duration_formatted', '未知')}")
                return True
            else:
                return False
            
        except Exception as e:
            self.scrape_stats['end_time'] = datetime.now()
            self._update_status(f"❌ 爬取單一區域資料失敗: {str(e)}")
            return False


# ============================================================================
# 使用範例和測試
# ============================================================================

def demo_enhanced_scraper():
    """演示增強版爬蟲的使用方法"""
    print("🧪 演示增強版社區資料爬蟲")
    
    def status_callback(message):
        print(f"📢 {message}")
    
    def progress_callback(current, total):
        percentage = (current / total * 100) if total > 0 else 0
        print(f"📊 進度: {current}/{total} ({percentage:.1f}%)")
    
    # 建立增強版爬蟲
    scraper = CommunityDataScraper(
        status_callback=status_callback,
        progress_callback=progress_callback,
        output_folder="./測試資料",
        auto_cleanup=True,
        enable_backup=True
    )
    
    print("\n🌐 載入城市資料:")
    cities_data = scraper.get_city_data()
    
    if cities_data:
        print(f"✅ 成功載入 {len(cities_data)} 個城市資料")
        
        # 測試爬取單一城市的第一個區域
        if cities_data[0]['districts']:
            city = cities_data[0]
            district = city['districts'][0]
            
            print(f"\n🏘️ 測試爬取: {city['name']}-{district['name']}")
            success = scraper.scrape_single_district(city, district['name'])
            
            if success:
                print("✅ 測試爬取成功")
                
                # 顯示統計資訊
                stats = scraper.get_scrape_statistics()
                print(f"\n📊 統計資訊:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                
                # 顯示檔案管理器統計
                file_stats = scraper.file_manager.get_comprehensive_statistics()
                print(f"\n📁 檔案統計:")
                print(f"  總檔案數: {file_stats['summary']['total_files']}")
                print(f"  總大小: {file_stats['summary']['total_size_mb']} MB")
                print(f"  儲存健康: {file_stats['summary']['storage_health']}")
            else:
                print("❌ 測試爬取失敗")
    else:
        print("❌ 載入城市資料失敗")


if __name__ == "__main__":
    demo_enhanced_scraper()