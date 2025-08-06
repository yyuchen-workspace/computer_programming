#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合版社區資料爬蟲
包含所有功能模組的完整版本
"""

import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import requests
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import time
import re
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
import subprocess
import shutil
import logging
import traceback
from typing import Callable, Optional, Dict, List, Tuple, Any
import glob


# ============================================================================
# 錯誤處理模組
# ============================================================================
class ErrorHandler:
    """統一錯誤處理類別"""
    
    def __init__(self, 
                 log_directory: str = None,
                 app_name: str = "CommunityDataScraper",
                 enable_console: bool = True,
                 enable_file: bool = True,
                 enable_gui: bool = True):
        self.app_name = app_name
        self.enable_console = enable_console
        self.enable_file = enable_file
        self.enable_gui = enable_gui
        
        if log_directory is None:
            if getattr(sys, 'frozen', False):
                self.log_directory = os.path.dirname(sys.executable)
            else:
                self.log_directory = os.path.dirname(__file__)
        else:
            self.log_directory = log_directory
        
        self.logs_folder = os.path.join(self.log_directory, "logs")
        os.makedirs(self.logs_folder, exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        self.error_log_file = os.path.join(self.logs_folder, f"{app_name}_error_{today}.log")
        self.general_log_file = os.path.join(self.logs_folder, f"{app_name}_general_{today}.log")
        
        self._setup_logging()
    
    def _setup_logging(self):
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        if self.enable_file:
            file_handler = logging.FileHandler(self.general_log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def log_error(self, error: Exception, context: str = "", show_gui: bool = None, user_message: str = None) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        
        error_message = {
            'timestamp': timestamp,
            'error_id': error_id,
            'context': context,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc()
        }
        
        formatted_error = self._format_error_message(error_message)
        
        if self.enable_file:
            self._write_to_error_file(formatted_error)
        
        self.logger.error(f"{context} - {error}")
        
        if self.enable_console:
            print(f"❌ 錯誤 [{error_id}]: {error}")
            if context:
                print(f"📍 上下文: {context}")
        
        if (show_gui if show_gui is not None else self.enable_gui):
            self._show_gui_error(error, context, error_id, user_message)
        
        return formatted_error
    
    def log_info(self, message: str, context: str = ""):
        full_message = f"{context} - {message}" if context else message
        self.logger.info(full_message)
        if self.enable_console:
            print(f"ℹ️ {full_message}")
    
    def log_warning(self, message: str, context: str = "", show_gui: bool = False):
        full_message = f"{context} - {message}" if context else message
        self.logger.warning(full_message)
        if self.enable_console:
            print(f"⚠️ {full_message}")
        if show_gui and self.enable_gui:
            messagebox.showwarning("警告", message)
    
    def log_success(self, message: str, context: str = ""):
        full_message = f"{context} - {message}" if context else message
        self.logger.info(f"SUCCESS: {full_message}")
        if self.enable_console:
            print(f"✅ {full_message}")
    
    def _format_error_message(self, error_info: dict) -> str:
        return f"""
{'='*80}
錯誤報告 - {error_info['error_id']}
{'='*80}
時間: {error_info['timestamp']}
上下文: {error_info['context']}
錯誤類型: {error_info['error_type']}
錯誤訊息: {error_info['error_message']}

詳細追蹤:
{error_info['traceback']}
{'='*80}

"""
    
    def _write_to_error_file(self, formatted_error: str):
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_error)
                f.flush()
        except Exception as e:
            print(f"❌ 無法寫入錯誤日誌檔案: {e}")
    
    def _show_gui_error(self, error: Exception, context: str, error_id: str, user_message: str = None):
        try:
            if user_message:
                display_message = user_message
            else:
                display_message = f"操作過程中發生錯誤：\n\n{str(error)}"
            
            if context:
                display_message += f"\n\n發生位置：{context}"
            
            display_message += f"\n\n錯誤編號：{error_id}"
            display_message += f"\n詳細錯誤記錄已保存至：\n{self.error_log_file}"
            
            messagebox.showerror("錯誤", display_message)
        except Exception as e:
            print(f"❌ 無法顯示GUI錯誤訊息: {e}")


# ============================================================================
# 智慧檔案管理模組
# ============================================================================
class SmartFileManager:
    """智慧檔案管理器"""
    
    def __init__(self, base_folder: str, enable_backup: bool = True):
        self.base_folder = Path(base_folder)
        self.enable_backup = enable_backup
        self.backup_folder = self.base_folder / "備份檔案"
        
        self.base_folder.mkdir(parents=True, exist_ok=True)
        if self.enable_backup:
            self.backup_folder.mkdir(parents=True, exist_ok=True)
    
    def get_latest_file_pattern(self, file_pattern: str, date_format: str = r'\d{4}_\d{2}_\d{2}') -> Optional[Path]:
        """找到符合模式的最新檔案"""
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if not matching_files:
            return None
        
        file_dates = []
        for file_path in matching_files:
            date_match = re.search(date_format, file_path.name)
            if date_match:
                try:
                    date_str = date_match.group().replace('_', '-')
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    file_dates.append((file_date, file_path))
                except ValueError:
                    continue
        
        if not file_dates:
            return None
        
        file_dates.sort(key=lambda x: x[0], reverse=True)
        return file_dates[0][1]
    
    def clean_old_files(self, file_pattern: str, keep_latest: int = 1, date_format: str = r'\d{4}_\d{2}_\d{2}') -> List[Path]:
        """清理舊檔案，只保留最新的幾個"""
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if len(matching_files) <= keep_latest:
            return []
        
        file_dates = []
        for file_path in matching_files:
            date_match = re.search(date_format, file_path.name)
            if date_match:
                try:
                    date_str = date_match.group().replace('_', '-')
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    file_dates.append((file_date, file_path))
                except ValueError:
                    file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    file_dates.append((file_date, file_path))
        
        file_dates.sort(key=lambda x: x[0], reverse=True)
        
        files_to_clean = file_dates[keep_latest:]
        cleaned_files = []
        
        for _, file_path in files_to_clean:
            try:
                if self.enable_backup:
                    backup_path = self.backup_folder / file_path.name
                    if backup_path.exists():
                        timestamp = datetime.now().strftime('%H%M%S')
                        backup_path = backup_path.with_name(
                            f"{backup_path.stem}_{timestamp}{backup_path.suffix}"
                        )
                    shutil.move(str(file_path), str(backup_path))
                    print(f"📦 已備份舊檔案: {file_path.name} -> {backup_path.name}")
                else:
                    file_path.unlink()
                    print(f"🗑️ 已刪除舊檔案: {file_path.name}")
                
                cleaned_files.append(file_path)
                
            except Exception as e:
                print(f"❌ 清理檔案失敗 {file_path.name}: {e}")
        
        return cleaned_files
    
    def generate_smart_filename(self, base_name: str, extension: str = '.txt', include_time: bool = False) -> str:
        """生成智慧檔案名稱"""
        today = datetime.now()
        
        if include_time:
            date_str = today.strftime('%Y_%m_%d_%H%M')
        else:
            date_str = today.strftime('%Y_%m_%d')
        
        clean_base = re.sub(r'_?\d{4}_\d{2}_\d{2}(_\d{4})?', '', base_name)
        clean_base = clean_base.strip('_')
        
        return f"{clean_base}_{date_str}{extension}"
    
    def get_file_info(self, file_pattern: str) -> Dict[str, any]:
        """取得檔案資訊統計"""
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if not matching_files:
            return {
                'total_files': 0,
                'latest_file': None,
                'oldest_file': None,
                'total_size': 0,
                'size_mb': 0
            }
        
        file_info = []
        total_size = 0
        
        for file_path in matching_files:
            stat = file_path.stat()
            file_info.append({
                'path': file_path,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
            total_size += stat.st_size
        
        file_info.sort(key=lambda x: x['modified'])
        
        return {
            'total_files': len(matching_files),
            'latest_file': file_info[-1]['path'] if file_info else None,
            'oldest_file': file_info[0]['path'] if file_info else None,
            'total_size': total_size,
            'size_mb': round(total_size / (1024 * 1024), 2)
        }


# ============================================================================
# 爬蟲核心模組
# ============================================================================
class CommunityDataScraper:
    """社區資料爬蟲類別"""
    
    def __init__(self, progress_callback: Optional[Callable] = None, 
                 status_callback: Optional[Callable] = None, 
                 output_folder: Optional[str] = None,
                 file_manager: Optional[SmartFileManager] = None):
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
        self.file_manager = file_manager or SmartFileManager(self.output_folder)
        
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
    
    def create_city_folder(self, city_name: str, city_count: Optional[str] = None):
        """建立城市資料夾"""
        if city_count:
            city_data_name = f"{city_name}({city_count}筆資料)"
        else:
            city_data_name = city_name
        
        today_str = datetime.now().strftime("%Y_%m_%d")
        today_folder_name = f"{city_data_name}_{today_str}"
        
        base_dir = Path(self.output_folder)
        base_dir.mkdir(parents=True, exist_ok=True)
        
        today_folder_path = base_dir / today_folder_name
        
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
                                self._update_status(f"⚠️ 無法解析日期: {date_str}")
        except (OSError, PermissionError) as e:
            self._update_status(f"⚠️ 讀取目錄時發生錯誤: {e}")
        
        old_folders.sort(key=lambda x: x[2], reverse=True)
        
        if today_folder_path.exists():
            self._update_status(f"📂 今天的資料夾 {today_folder_name} 已存在，繼續使用")
        else:
            if old_folders:
                old_folder_path, old_date_str, old_date = old_folders[0]
                try:
                    old_folder_path.rename(today_folder_path)
                    self._update_status(f"📁 已將資料夾 {old_folder_path.name} 改名為 {today_folder_name}")
                except (OSError, PermissionError) as e:
                    self._update_status(f"❌ 改名資料夾失敗: {e}")
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
            self._update_status("正在獲取城市列表...")
            response = self.session.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            city_tree = soup.find_all('li', {'class': 'treeview'})
            
            cities = []
            for tree in city_tree:
                span = tree.find('span')
                if not span:
                    continue
                
                city_text = span.get_text(strip=True)
                city_name, city_count = self.separate_name(city_text)
                
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
            
            self._update_status(f"成功獲取 {len(cities)} 個城市資料")
            return cities
            
        except Exception as e:
            self._update_status(f"獲取城市資料失敗: {str(e)}")
            return []

    def scrape_new_communities_from_web(self, url: str) -> List[Dict[str, str]]:
        """從網站爬取所有社區資料"""
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
                
                a_tag = soup.find('a', class_='btn btn-primary', string=re.compile(r'下一頁'))
                href = a_tag and a_tag.get('href')
                if not href:
                    break
                
                url = urljoin(self.base_url, unquote(href))
                page += 1
                time.sleep(2)
        
        except Exception as e:
            self._update_status(f"爬取網站資料時發生錯誤: {str(e)}")
        
        return all_communities
    
    def parse_existing_communities_from_content(self, content: str) -> Dict[str, Dict[str, str]]:
        """從內容字串解析現有的社區資料"""
        communities = {}
        
        if not content.strip():
            return communities
        
        try:
            separator_pattern = r'={60,}'
            parts = re.split(separator_pattern, content)
            
            if parts:
                old_data_content = parts[0].strip()
                if old_data_content:
                    old_communities = self._parse_community_blocks(old_data_content)
                    communities.update(old_communities)
                
                if len(parts) > 1:
                    log_content = ''.join(parts[1:])
                    new_communities = self._parse_update_log_communities(log_content)
                    communities.update(new_communities)
            else:
                all_communities = self._parse_community_blocks(content)
                communities.update(all_communities)
        
        except Exception as e:
            self._update_status(f"解析現有內容時發生錯誤: {str(e)}")
        
        return communities

    def _parse_community_blocks(self, content: str) -> Dict[str, Dict[str, str]]:
        """解析標準格式的社區資料區塊"""
        communities = {}
        
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
                
                if line.startswith('+ '):
                    community_name = line[2:].strip()
                    phone = ''
                    address = ''
                    
                    j = i + 1
                    while j < len(lines) and j < i + 5:
                        next_line = lines[j].strip()
                        
                        if (next_line.startswith('+ ') or 
                            next_line.startswith('總計新增項目') or
                            next_line.startswith('============')):
                            break
                        
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
            self._update_status(f"解析更新日誌時發生錯誤: {str(e)}")
        
        return communities
    
    def find_data(self, url: str, city_name: str, district_name: Optional[str], 
                  count: str, do_dis: str, city_count: Optional[str] = None) -> bool:
        """爬取社區資料 - 增量更新模式"""
        try:
            city_folder = self.create_city_folder(city_name, city_count)
            
            today_str = datetime.now().strftime("%Y_%m_%d")
            if do_dis == "否":
                file_name = f"{city_name}全部社區資料(共有{count}筆)_{today_str}.txt"
            elif do_dis == "是":
                file_name = f"{city_name}{district_name}社區資料(共有{count}筆)_{today_str}.txt"
            
            file_path = city_folder / file_name
            
            self._update_status(f"正在爬取: {file_name}")
            self._update_status(f"輸出路徑: {file_path}")
            
            existing_communities = {}
            if file_path.exists():
                with file_path.open('r', encoding='utf-8') as f:
                    content = f.read()
                existing_communities = self.parse_existing_communities_from_content(content)
                self._update_status(f"現有檔案中已有 {len(existing_communities)} 筆社區資料")
            
            self._update_status("開始從網站爬取最新資料...")
            all_web_communities = self.scrape_new_communities_from_web(url)
            
            if self.should_stop:
                return False
            
            self._update_status(f"從網站爬取到 {len(all_web_communities)} 筆社區資料")
            
            new_communities = []
            for community in all_web_communities:
                if community['name'] not in existing_communities:
                    new_communities.append(community)
            
            self._update_status(f"發現 {len(new_communities)} 筆新增社區資料")
            
            with file_path.open(mode="w", encoding="utf-8") as file:
                all_existing_from_web = []
                for community in all_web_communities:
                    if community['name'] in existing_communities:
                        all_existing_from_web.append(community)
                
                for community in all_existing_from_web:
                    file.write(f"{community['name']}\n")
                    file.write(f"電話: {community['phone']}\n")
                    file.write(f"地址: {community['address']}\n")
                    file.write("\n")
                
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

    def create_update_log(self, updates: Dict[str, List[Dict[str, str]]]):
        """建立增強版更新日誌"""
        try:
            if not any(updates.values()):
                self._update_status("沒有新增項目，不建立更新日誌")
                return
            
            log_folder = Path(self.output_folder) / "資料更新日誌"
            log_folder.mkdir(parents=True, exist_ok=True)
            
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
                            f.write(f"+ {community['name']}\n")
                            phone = community.get('phone', '') or '未提供'
                            f.write(f"  📞 電話: {phone}\n")
                            address = community.get('address', '') or '未提供'
                            f.write(f"  📍 地址: {address}\n")
                            f.write("\n")
                        
                        f.write("\n")
                        total_new_items += len(new_communities)
                
                f.write(f"總計新增項目: {total_new_items} 筆\n")
                f.write("=" * 60 + "\n")
            
            self._update_status(f"已建立更新日誌: {log_file_path}")
            
        except Exception as e:
            self._update_status(f"建立更新日誌時發生錯誤: {str(e)}")
    
    def scrape_all_cities_with_districts(self, cities_data: List[Dict]) -> bool:
        """爬取全部城市分區資料"""
        try:
            self._update_log_data = {}
            
            total_districts = sum(len(city['districts']) for city in cities_data)
            current_district = 0
            
            for city in cities_data:
                if self.should_stop:
                    break
                    
                self.create_city_folder(city['name'], city['count'])
                
                for district in city['districts']:
                    if self.should_stop:
                        break
                        
                    current_district += 1
                    self._update_progress(current_district, total_districts)
                    
                    success = self.find_data(
                        district['url'], 
                        city['name'], 
                        district['name'], 
                        district['count'], 
                        "是",
                        city['count']
                    )
                    if not success:
                        return False
            
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return not self.should_stop
            
        except Exception as e:
            self._update_status(f"爬取全部城市分區資料失敗: {str(e)}")
            return False

    def scrape_single_city_with_districts(self, city_data: Dict) -> bool:
        """爬取單一城市分區資料"""
        try:
            self._update_log_data = {}
            
            self.create_city_folder(city_data['name'], city_data['count'])
            total_districts = len(city_data['districts'])
            
            for i, district in enumerate(city_data['districts']):
                if self.should_stop:
                    break
                    
                self._update_progress(i + 1, total_districts)
                
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
            
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return not self.should_stop
            
        except Exception as e:
            self._update_status(f"爬取單一城市分區資料失敗: {str(e)}")
            return False
    
    def scrape_single_district(self, city_data: Dict, district_name: str) -> bool:
        """爬取單一區域資料"""
        try:
            self._update_log_data = {}
            
            self.create_city_folder(city_data['name'], city_data['count'])
            
            target_district = None
            for district in city_data['districts']:
                if district['name'] == district_name:
                    target_district = district
                    break
            
            if not target_district:
                self._update_status(f"找不到區域: {district_name}")
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
            
            if hasattr(self, '_update_log_data'):
                self.create_update_log(self._update_log_data)
            
            return success
            
        except Exception as e:
            self._update_status(f"爬取單一區域資料失敗: {str(e)}")
            return False


# ============================================================================
# GUI 應用程式
# ============================================================================
class EnhancedScraperGUI:
    """增強版社區爬蟲GUI應用程式"""
    
    def __init__(self, root):
        self.error_handler = ErrorHandler(
            app_name="CommunityScraperGUI",
            enable_console=True,
            enable_file=True,
            enable_gui=True
        )
        
        self.root = root
        self.root.title("🏘️ 社區資料爬蟲 (增強版)")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        self.scraper = None
        self.cities_data = []
        self.selected_city_data = None
        self.scraping_thread = None
        
        self.lock_file_path = self.get_lock_file_path()
        
        # GUI 變數
        self.output_folder = tk.StringVar(value=os.getcwd())
        self.auto_cleanup = tk.BooleanVar(value=True)
        self.enable_backup = tk.BooleanVar(value=True)
        
        # 排程變數
        self.schedule_enabled = tk.BooleanVar(value=False)
        self.schedule_day = tk.StringVar(value="星期一")
        self.schedule_time = tk.StringVar(value="02:00")
        self.schedule_output_folder = tk.StringVar(
            value=os.path.join(os.getcwd(), "爬蟲資料")
        )
        self.schedule_scrape_mode = tk.StringVar(value="all_cities")
        
        try:
            self.create_widgets()
            self.load_config()
            self.load_cities_data()
            self.start_lock_status_checker()
            self.error_handler.log_info("GUI應用程式初始化完成")
        except Exception as e:
            self.error_handler.log_error(e, "初始化GUI應用程式")

    def get_lock_file_path(self):
        """取得 Lock 檔案的路徑"""
        try:
            if getattr(sys, 'frozen', False):
                program_dir = os.path.dirname(sys.executable)
            else:
                program_dir = os.path.dirname(__file__)
                
            return os.path.join(program_dir, "scraper_running.lock")
        except Exception as e:
            self.error_handler.log_error(e, "取得Lock檔案路徑")
            return "scraper_running.lock"

    def check_lock_file_status(self):
        """檢查 Lock 檔案狀態"""
        try:
            if os.path.exists(self.lock_file_path):
                mtime = os.path.getmtime(self.lock_file_path)
                create_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                try:
                    with open(self.lock_file_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                except Exception as e:
                    self.error_handler.log_warning(f"無法讀取Lock檔案內容: {e}", "檢查Lock檔案狀態")
                    content = "無法讀取檔案內容"
                
                return True, create_time, content
            else:
                return False, None, None
        except Exception as e:
            self.error_handler.log_error(e, "檢查Lock檔案狀態", show_gui=False)
            return False, None, None

    def update_lock_status_display(self):
        """更新 Lock 檔案狀態顯示"""
        try:
            exists, create_time, content = self.check_lock_file_status()
            
            if exists:
                status_text = f"🔒 Lock檔案存在\n創建時間: {create_time}\n內容: {content}"
                self.lock_status_label.config(text=status_text, foreground="red")
            else:
                status_text = "✅ 沒有Lock檔案，可以正常執行"
                self.lock_status_label.config(text=status_text, foreground="green")
                
        except Exception as e:
            self.error_handler.log_error(e, "更新Lock狀態顯示", show_gui=False)
            self.lock_status_label.config(text=f"❌ 檢查Lock狀態時發生錯誤", foreground="red")

    def start_lock_status_checker(self):
        """開始定期檢查 Lock 檔案狀態"""
        def check_periodically():
            self.update_lock_status_display()
            self.root.after(3000, check_periodically)
        
        self.update_lock_status_display()
        self.root.after(3000, check_periodically)

    def check_lock_before_start(self):
        """在開始爬取前檢查 Lock 檔案"""
        try:
            exists, create_time, content = self.check_lock_file_status()
            
            if exists:
                result = messagebox.askyesno(
                    "⚠️ 檢測到Lock檔案", 
                    f"檢測到爬蟲程序可能正在執行：\n\n"
                    f"Lock檔案創建時間: {create_time}\n"
                    f"檔案內容: {content}\n\n"
                    f"這可能表示：\n"
                    f"• 有其他爬蟲程序正在執行\n"
                    f"• 之前的程序異常結束未清理Lock檔案\n\n"
                    f"是否要強制繼續執行？\n"
                    f"（建議先點選「清理鎖定」按鈕）",
                    icon='warning'
                )
                return result
            
            return True
        except Exception as e:
            self.error_handler.log_error(e, "檢查Lock檔案", user_message="檢查Lock檔案時發生錯誤，將繼續執行")
            return True
    
    def create_widgets(self):
        """建立主要的GUI元件結構"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 爬取設定分頁
        scrape_frame = ttk.Frame(notebook, padding="10")
        notebook.add(scrape_frame, text="爬取設定")
        self.create_scrape_tab(scrape_frame)
        
        # 檔案管理分頁
        file_frame = ttk.Frame(notebook, padding="10")
        notebook.add(file_frame, text="檔案管理")
        self.create_file_management_tab(file_frame)
        
        # 自動排程分頁
        schedule_frame = ttk.Frame(notebook, padding="10")
        notebook.add(schedule_frame, text="自動排程")
        
        canvas = tk.Canvas(schedule_frame)
        vbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content = ttk.Frame(canvas)
        canvas.create_window((0,0), window=content, anchor="nw")
        
        def on_content_config(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        content.bind("<Configure>", on_content_config)

        def on_mousewheel(ev):
            canvas.yview_scroll(int(-1*(ev.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.create_schedule_tab(content)

    def create_scrape_tab(self, parent):
        """建立爬取設定分頁"""
        # 輸出資料夾設定
        ttk.Label(parent, text="手動爬取輸出資料夾：").pack(anchor=tk.W, pady=5)
        
        folder_frame = ttk.Frame(parent)
        folder_frame.pack(fill=tk.X, pady=5)
        
        folder_entry = ttk.Entry(
            folder_frame, 
            textvariable=self.output_folder,
            state="readonly"
        )
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            folder_frame, 
            text="瀏覽", 
            command=self.browse_folder
        ).pack(side=tk.RIGHT)
        
        # 檔案管理選項
        options_frame = ttk.LabelFrame(parent, text="檔案管理選項", padding="10")
        options_frame.pack(fill=tk.X, pady=15)
        
        ttk.Checkbutton(
            options_frame, 
            text="自動清理舊檔案（保留最新版本）", 
            variable=self.auto_cleanup
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Checkbutton(
            options_frame, 
            text="將舊檔案備份到備份資料夾", 
            variable=self.enable_backup
        ).pack(anchor=tk.W, pady=2)
        
        # 城市選擇
        ttk.Label(parent, text="選擇城市：").pack(anchor=tk.W, pady=(15, 5))
        self.city_combo = ttk.Combobox(parent, state="readonly")
        self.city_combo.pack(fill=tk.X, pady=5)
        self.city_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        # 區域選擇
        ttk.Label(parent, text="選擇區域：").pack(anchor=tk.W, pady=(15, 5))
        self.district_combo = ttk.Combobox(parent, state="readonly")
        self.district_combo.pack(fill=tk.X, pady=5)
        
        # 爬取選項
        scrape_options_frame = ttk.LabelFrame(parent, text="手動爬取選項", padding="10")
        scrape_options_frame.pack(fill=tk.X, pady=15)
        
        self.scrape_option = tk.StringVar(value="all_cities")
        
        ttk.Radiobutton(
            scrape_options_frame, 
            text="爬取全部城市(資料分區)", 
            variable=self.scrape_option, 
            value="all_cities"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            scrape_options_frame, 
            text="爬取單一城市(資料分區)", 
            variable=self.scrape_option, 
            value="single_city"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            scrape_options_frame, 
            text="爬取單一區域", 
            variable=self.scrape_option, 
            value="single_district"
        ).pack(anchor=tk.W, pady=2)

        # 控制按鈕
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.TOP, pady=(10,0))
        
        self.start_button = ttk.Button(
            button_frame, 
            text="開始爬取", 
            command=self.start_scraping
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame, 
            text="停止爬取", 
            command=self.stop_scraping, 
            state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(
            button_frame, 
            text="儲存設定", 
            command=self.save_config
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # 進度顯示
        ttk.Label(parent, text="進度：").pack(anchor=tk.W, pady=5)
        self.progress = ttk.Progressbar(parent, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # 狀態顯示
        ttk.Label(parent, text="狀態：").pack(anchor=tk.W, pady=5)
        self.status_text = scrolledtext.ScrolledText(parent, height=8)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def create_file_management_tab(self, parent):
        """建立檔案管理分頁"""
        # 檔案管理說明
        info_frame = ttk.LabelFrame(parent, text="檔案管理功能說明", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = """
📂 智慧檔案管理功能：

• 自動生成格式：類型_日期.txt (例如：台北市_2024_07_14.txt)
• 自動清理舊檔案：只保留最新日期的檔案
• 備份舊檔案：將舊檔案移至備份資料夾，避免意外遺失
• 檔案統計：查看詳細的檔案使用情況
• 手動清理：可以手動控制檔案清理時機

📁 檔案結構：
爬蟲資料夾/
├── 台北市(4776筆資料)_2025_07_14/
│   ├── 台北市_中正區(776筆資料)_2025_07_14.txt
│   └── ...
├── 備份檔案/
│   ├── 舊檔案自動備份於此
└── 資料更新日誌/
    └── 記錄每次更新的詳細內容
        """
        
        info_label = ttk.Label(info_frame, text=info_text, font=("Arial", 9), justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
        
        # 檔案管理控制
        control_frame = ttk.LabelFrame(parent, text="檔案管理控制", padding="10")
        control_frame.pack(fill=tk.X, pady=10)
        
        # 檔案管理按鈕
        button_row1 = ttk.Frame(control_frame)
        button_row1.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_row1, 
            text="📊 檢視檔案統計", 
            command=self.show_file_statistics
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_row1, 
            text="🧹 手動清理舊檔案", 
            command=self.manual_cleanup_files
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_row1, 
            text="📁 開啟輸出資料夾", 
            command=self.open_output_folder
        ).pack(side=tk.LEFT, padx=5)
        
        button_row2 = ttk.Frame(control_frame)
        button_row2.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_row2, 
            text="📦 檢視備份資料夾", 
            command=self.open_backup_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_row2, 
            text="📋 檢視更新日誌", 
            command=self.open_update_log_folder
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_row2, 
            text="🔄 重新整理統計", 
            command=self.refresh_file_statistics
        ).pack(side=tk.LEFT, padx=5)
        
        # 檔案統計顯示區域
        stats_frame = ttk.LabelFrame(parent, text="檔案統計資訊", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=15)
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # 自動載入統計
        self.refresh_file_statistics()

    def create_schedule_tab(self, parent):
        """建立自動排程分頁"""
        # Lock 檔案狀態顯示
        lock_frame = ttk.LabelFrame(parent, text="爬蟲狀態檢查", padding="10")
        lock_frame.pack(fill=tk.X, pady=10)
        
        self.lock_status_label = ttk.Label(
            lock_frame, 
            text="正在檢查...", 
            font=("Arial", 9),
            wraplength=600
        )
        self.lock_status_label.pack(anchor=tk.W, pady=5)

        # 功能說明
        info_text = """
🤖 自動排程功能：

此功能會在 Windows 工作排程器中建立一個任務，讓程式在指定時間自動在背景執行爬取工作。
⚠️ 需要管理員權限才能建立系統排程
⚠️ 請勿更改本執行檔檔名
✅ 自動排程會完全在背景執行，不會跳出視窗
        """
        
        info_label = ttk.Label(parent, text=info_text, font=("Arial", 9))
        info_label.pack(pady=10)
        
        # 排程啟用開關
        ttk.Checkbutton(
            parent, 
            text="啟用自動排程", 
            variable=self.schedule_enabled
        ).pack(anchor=tk.W, pady=10)
        
        # 自動排程資料夾設定
        folder_frame = ttk.LabelFrame(parent, text="自動排程資料存放位置", padding="10")
        folder_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(folder_frame, text="自動排程輸出資料夾：").pack(anchor=tk.W, pady=(0, 5))
        
        schedule_folder_frame = ttk.Frame(folder_frame)
        schedule_folder_frame.pack(fill=tk.X, pady=5)
        
        schedule_folder_entry = ttk.Entry(
            schedule_folder_frame, 
            textvariable=self.schedule_output_folder, 
            state="readonly"
        )
        schedule_folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            schedule_folder_frame, 
            text="瀏覽", 
            command=self.browse_schedule_folder
        ).pack(side=tk.RIGHT)
        
        # 爬取模式設定
        mode_frame = ttk.LabelFrame(parent, text="自動排程爬取模式", padding="10")
        mode_frame.pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(
            mode_frame, 
            text="爬取全部城市（資料分區）", 
            variable=self.schedule_scrape_mode, 
            value="all_cities"
        ).pack(anchor=tk.W, pady=2)
        
        # 排程時間設定
        schedule_frame = ttk.LabelFrame(parent, text="排程時間設定", padding="10")
        schedule_frame.pack(fill=tk.X, pady=10)
        
        day_frame = ttk.Frame(schedule_frame)
        day_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(day_frame, text="執行日期：").pack(side=tk.LEFT)
        day_combo = ttk.Combobox(
            day_frame, 
            textvariable=self.schedule_day, 
            state="readonly", 
            width=15
        )
        day_combo['values'] = ('星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日')
        day_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        time_frame = ttk.Frame(schedule_frame)
        time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(time_frame, text="執行時間：").pack(side=tk.LEFT)
        ttk.Entry(
            time_frame, 
            textvariable=self.schedule_time, 
            width=10
        ).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(time_frame, text="(24小時制，例如：02:00)").pack(side=tk.LEFT)
        
        # 排程管理按鈕
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="🔧 設定自動排程", 
            command=self.setup_windows_scheduler
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🗑️ 移除排程", 
            command=self.remove_windows_scheduler
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, 
            text="🛑 停止背景程序", 
            command=self.force_stop_background_scraper
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, 
            text="🚀 立即測試", 
            command=self.test_scheduler
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🧹 清理鎖定", 
            command=self.clear_scraper_lock
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="🔄 刷新狀態", 
            command=self.update_lock_status_display
        ).pack(side=tk.LEFT, padx=5)
        
        # 排程狀態顯示
        status_frame = ttk.LabelFrame(parent, text="排程狀態", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.schedule_status_label = ttk.Label(status_frame, text="尚未設定自動排程")
        self.schedule_status_label.pack(anchor=tk.W)

    # ========================================================================
    # 檔案管理相關方法
    # ========================================================================
    
    def show_file_statistics(self):
        """顯示詳細的檔案統計視窗"""
        try:
            stats_window = tk.Toplevel(self.root)
            stats_window.title("📊 檔案統計詳情")
            stats_window.geometry("700x500")
            
            # 建立分頁
            notebook = ttk.Notebook(stats_window)
            notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 總覽分頁
            overview_frame = ttk.Frame(notebook)
            notebook.add(overview_frame, text="總覽")
            
            overview_text = scrolledtext.ScrolledText(overview_frame)
            overview_text.pack(fill=tk.BOTH, expand=True)
            
            # 詳細分頁
            detail_frame = ttk.Frame(notebook)
            notebook.add(detail_frame, text="詳細清單")
            
            detail_text = scrolledtext.ScrolledText(detail_frame)
            detail_text.pack(fill=tk.BOTH, expand=True)
            
            # 取得統計資料
            file_manager = SmartFileManager(self.output_folder.get())
            
            # 總覽資訊
            overview_content = self._generate_overview_statistics(file_manager)
            overview_text.insert(tk.END, overview_content)
            
            # 詳細清單
            detail_content = self._generate_detail_statistics(file_manager)
            detail_text.insert(tk.END, detail_content)
            
        except Exception as e:
            self.error_handler.log_error(e, "顯示檔案統計", user_message="顯示檔案統計時發生錯誤")

    def _generate_overview_statistics(self, file_manager: SmartFileManager) -> str:
        """生成總覽統計內容"""
        content = []
        content.append("📊 檔案統計總覽")
        content.append("=" * 50)
        content.append("")
        
        # 統計不同類型的檔案
        patterns = [
            ("*.txt", "所有文字檔"),
            ("*社區資料*.txt", "社區資料檔"),
            ("*更新日誌*.txt", "更新日誌"),
        ]
        
        total_files = 0
        total_size = 0
        
        for pattern, description in patterns:
            info = file_manager.get_file_info(pattern)
            content.append(f"📁 {description}:")
            content.append(f"   檔案數量: {info['total_files']} 個")
            content.append(f"   總大小: {info['size_mb']} MB")
            
            if info['latest_file']:
                content.append(f"   最新檔案: {info['latest_file'].name}")
            
            content.append("")
            total_files += info['total_files']
            total_size += info['size_mb']
        
        content.append("📈 整體統計:")
        content.append(f"   總檔案數: {total_files} 個")
        content.append(f"   總大小: {total_size:.2f} MB")
        content.append("")
        
        # 檢查備份資料夾
        backup_folder = Path(self.output_folder.get()) / "備份檔案"
        if backup_folder.exists():
            backup_files = list(backup_folder.glob("*.txt"))
            backup_size = sum(f.stat().st_size for f in backup_files) / (1024 * 1024)
            content.append("📦 備份資料夾:")
            content.append(f"   備份檔案數: {len(backup_files)} 個")
            content.append(f"   備份大小: {backup_size:.2f} MB")
        else:
            content.append("📦 備份資料夾: 不存在")
        
        content.append("")
        content.append("🕐 統計時間: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return "\n".join(content)

    def _generate_detail_statistics(self, file_manager: SmartFileManager) -> str:
        """生成詳細統計內容"""
        content = []
        content.append("📋 詳細檔案清單")
        content.append("=" * 80)
        content.append("")
        
        base_folder = Path(self.output_folder.get())
        
        # 按日期分組顯示檔案
        files_by_date = {}
        
        # 收集所有檔案
        for file_path in base_folder.rglob("*.txt"):
            try:
                # 嘗試從檔案名稱提取日期
                date_match = re.search(r'(\d{4}_\d{2}_\d{2})', file_path.name)
                if date_match:
                    date_str = date_match.group(1).replace('_', '-')
                else:
                    # 使用檔案修改日期
                    file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    date_str = file_date.strftime('%Y-%m-%d')
                
                if date_str not in files_by_date:
                    files_by_date[date_str] = []
                
                file_size = file_path.stat().st_size / 1024  # KB
                files_by_date[date_str].append((file_path, file_size))
                
            except Exception as e:
                content.append(f"❌ 處理檔案 {file_path.name} 時發生錯誤: {e}")
        
        # 按日期排序顯示
        for date_str in sorted(files_by_date.keys(), reverse=True):
            files = files_by_date[date_str]
            total_size = sum(size for _, size in files)
            
            content.append(f"📅 {date_str} ({len(files)} 個檔案, {total_size:.1f} KB)")
            content.append("-" * 40)
            
            for file_path, file_size in sorted(files, key=lambda x: x[0].name):
                relative_path = file_path.relative_to(base_folder)
                content.append(f"   📄 {relative_path} ({file_size:.1f} KB)")
            
            content.append("")
        
        return "\n".join(content)

    def manual_cleanup_files(self):
        """手動清理舊檔案"""
        try:
            result = messagebox.askyesno(
                "確認清理", 
                "確定要清理舊檔案嗎？\n\n"
                "這個操作會：\n"
                f"• {'備份舊檔案到備份資料夾' if self.enable_backup.get() else '直接刪除舊檔案'}\n"
                "• 只保留最新日期的檔案\n"
                "• 無法復原（除非有備份）",
                icon='warning'
            )
            
            if not result:
                return
            
            file_manager = SmartFileManager(
                self.output_folder.get(), 
                enable_backup=self.enable_backup.get()
            )
            
            # 清理不同類型的檔案
            patterns = ["*社區資料*.txt", "*城市*.txt", "*區域*.txt"]
            total_cleaned = 0
            
            for pattern in patterns:
                cleaned_files = file_manager.clean_old_files(pattern, keep_latest=1)
                total_cleaned += len(cleaned_files)
            
            messagebox.showinfo(
                "清理完成", 
                f"✅ 清理完成！\n\n"
                f"共清理了 {total_cleaned} 個舊檔案\n"
                f"{'檔案已備份到備份資料夾' if self.enable_backup.get() else '檔案已刪除'}"
            )
            
            self.update_status(f"手動清理完成，處理了 {total_cleaned} 個檔案")
            self.refresh_file_statistics()
            
        except Exception as e:
            self.error_handler.log_error(e, "手動清理檔案", user_message="清理檔案時發生錯誤")

    def open_output_folder(self):
        """開啟輸出資料夾"""
        try:
            folder_path = self.output_folder.get()
            if os.path.exists(folder_path):
                if sys.platform == "win32":
                    os.startfile(folder_path)
                else:
                    subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", folder_path])
                self.update_status(f"已開啟資料夾: {folder_path}")
            else:
                messagebox.showwarning("警告", f"資料夾不存在: {folder_path}")
        except Exception as e:
            self.error_handler.log_error(e, "開啟輸出資料夾", user_message="開啟資料夾時發生錯誤")

    def open_backup_folder(self):
        """開啟備份資料夾"""
        try:
            backup_folder = os.path.join(self.output_folder.get(), "備份檔案")
            if os.path.exists(backup_folder):
                if sys.platform == "win32":
                    os.startfile(backup_folder)
                else:
                    subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", backup_folder])
                self.update_status(f"已開啟備份資料夾: {backup_folder}")
            else:
                messagebox.showinfo("提示", "備份資料夾不存在，可能還沒有建立備份檔案")
        except Exception as e:
            self.error_handler.log_error(e, "開啟備份資料夾", user_message="開啟備份資料夾時發生錯誤")

    def open_update_log_folder(self):
        """開啟更新日誌資料夾"""
        try:
            log_folder = os.path.join(self.output_folder.get(), "資料更新日誌")
            if os.path.exists(log_folder):
                if sys.platform == "win32":
                    os.startfile(log_folder)
                else:
                    subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", log_folder])
                self.update_status(f"已開啟更新日誌資料夾: {log_folder}")
            else:
                messagebox.showinfo("提示", "更新日誌資料夾不存在，可能還沒有進行過更新")
        except Exception as e:
            self.error_handler.log_error(e, "開啟更新日誌資料夾", user_message="開啟更新日誌資料夾時發生錯誤")

    def refresh_file_statistics(self):
        """重新整理檔案統計資訊"""
        try:
            file_manager = SmartFileManager(self.output_folder.get())
            stats_content = self._generate_overview_statistics(file_manager)
            
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, stats_content)
            
            self.update_status("檔案統計已更新")
            
        except Exception as e:
            self.error_handler.log_error(e, "更新檔案統計", show_gui=False)

    # ========================================================================
    # 其他GUI方法
    # ========================================================================

    def browse_folder(self):
        """選擇手動爬取資料夾"""
        try:
            folder = filedialog.askdirectory(
                title="選擇手動爬取輸出資料夾", 
                initialdir=self.output_folder.get()
            )
            if folder:
                self.output_folder.set(folder)
                self.refresh_file_statistics()  # 更新檔案統計
                self.error_handler.log_info(f"已選擇手動爬取資料夾: {folder}")
        except Exception as e:
            self.error_handler.log_error(e, "選擇手動爬取資料夾", user_message="選擇資料夾時發生錯誤")

    def browse_schedule_folder(self):
        """選擇自動排程資料夾"""
        try:
            folder = filedialog.askdirectory(
                title="選擇自動排程輸出資料夾", 
                initialdir=self.schedule_output_folder.get()
            )
            if folder:
                self.schedule_output_folder.set(folder)
                self.update_status(f"已選擇自動排程資料夾: {folder}")
                self.error_handler.log_info(f"已選擇自動排程資料夾: {folder}")
        except Exception as e:
            self.error_handler.log_error(e, "選擇自動排程資料夾", user_message="選擇資料夾時發生錯誤")

    def load_cities_data(self):
        """載入城市資料"""
        def load_in_background():
            try:
                self.update_status("正在載入城市資料...")
                
                scraper = CommunityDataScraper(status_callback=self.update_status)
                cities_data = scraper.get_city_data()

                if cities_data:
                    self.cities_data = cities_data
                    city_names = [f"{city['name']} ({city['count']}筆)" for city in cities_data]
                    self.root.after(0, lambda: self.city_combo.configure(values=city_names))
                    self.update_status(f"成功載入 {len(cities_data)} 個城市資料")
                    self.error_handler.log_success(f"成功載入 {len(cities_data)} 個城市資料")
                else:
                    self.update_status("載入城市資料失敗")
                    self.error_handler.log_warning("載入城市資料失敗")
            except Exception as e:
                self.error_handler.log_error(e, "載入城市資料")
        
        threading.Thread(target=load_in_background, daemon=True).start()
    
    def on_city_selected(self, event):
        """選擇城市事件處理"""
        try:
            selection = self.city_combo.current()
            
            if selection >= 0 and selection < len(self.cities_data):
                self.selected_city_data = self.cities_data[selection]
                districts = self.selected_city_data['districts']
                
                district_names = [f"{district['name']} ({district['count']}筆)" for district in districts]
                
                self.district_combo.configure(values=district_names)
                
                if district_names:
                    self.district_combo.current(0)
        except Exception as e:
            self.error_handler.log_error(e, "選擇城市", show_gui=False)
    
    def get_executable_path(self):
        """取得執行檔路徑"""
        try:
            if getattr(sys, 'frozen', False):
                return sys.executable
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                
                possible_exe_names = [
                    "社區資料爬蟲.exe",
                    "community_scraper.exe", 
                    "main.exe",
                    "gui_app.exe"
                ]
                
                for exe_name in possible_exe_names:
                    exe_path = os.path.join(script_dir, exe_name)
                    if os.path.exists(exe_path):
                        return exe_path
                
                return f'"{sys.executable}" "{os.path.join(script_dir, "main.py")}"'
        except Exception as e:
            self.error_handler.log_error(e, "取得執行檔路徑", show_gui=False)
            return sys.executable
    
    def setup_windows_scheduler(self):
        """設定Windows排程器"""
        try:
            if not self.schedule_enabled.get():
                self.error_handler.log_warning("請先勾選「啟用自動排程」", show_gui=True)
                return
            
            if not self.schedule_output_folder.get():
                self.error_handler.log_warning("請選擇自動排程的輸出資料夾", show_gui=True)
                return
            
            task_name = "CommunityScraperAutoTask"
            
            day_mapping = {
                "星期一": "MON", "星期二": "TUE", "星期三": "WED",
                "星期四": "THU", "星期五": "FRI", "星期六": "SAT", "星期日": "SUN"
            }
            schtasks_day = day_mapping.get(self.schedule_day.get(), "MON")
            
            self.save_config()
            
            subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], 
                         capture_output=True, text=True)
            
            if getattr(sys, 'frozen', False):
                script_dir = os.path.dirname(sys.executable)
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))

            batch_file = os.path.join(script_dir, "background_runner.bat")
            
            batch_content = '''@echo off
REM 背景執行批次檔
chcp 65001 > nul
cd /d "%~dp0"

if exist "community_scraper.exe" (
    echo [%date% %time%] 執行community_scraper.exe
    "community_scraper.exe" --auto-background
)

if exist "main.py" (
    echo [%date% %time%] 使用Python執行main.py
    python "main.py" --auto-background
)

:end
'''
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            cmd = [
                "schtasks", "/create",
                "/tn", task_name,
                "/tr", f'cmd /c "{batch_file}"',
                "/sc", "weekly",
                "/d", schtasks_day,
                "/st", self.schedule_time.get(),
                "/rl", "HIGHEST",
                "/ru", "SYSTEM",
                "/f"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.schedule_status_label.config(
                    text=f"✅ 已設定自動排程：每週{schtasks_day} {self.schedule_time.get()}"
                )
                messagebox.showinfo("成功", 
                    f"✅ 自動排程設定成功！\n\n"
                    f"任務名稱：{task_name}\n"
                    f"執行時間：每週{schtasks_day} {self.schedule_time.get()}\n"
                    f"輸出資料夾：{self.schedule_output_folder.get()}\n"
                    f"爬取模式：{self.schedule_scrape_mode.get()}\n"
                    f"執行方式：完全背景執行\n\n"
                    f"程式會在指定時間自動在背景執行，完全不會跳出視窗。\n"
                    f"可在 Windows 工作排程器中管理此任務。")
                self.update_status("自動排程設定成功")
                self.error_handler.log_success("自動排程設定成功")
            else:
                raise RuntimeError(f"設定失敗：{result.stderr}")
        except Exception as e:
            self.error_handler.log_error(e, "設定Windows排程器", user_message="設定自動排程時發生錯誤，請檢查是否有管理員權限")

    def remove_windows_scheduler(self):
        """移除Windows排程器"""
        try:
            task_name = "CommunityScraperAutoTask"
            
            result = subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.schedule_status_label.config(text="尚未設定自動排程")
                messagebox.showinfo("成功", "✅ 自動排程已移除")
                self.update_status("自動排程已移除")
                self.error_handler.log_success("自動排程已移除")
            else:
                self.error_handler.log_warning("沒有找到要移除的排程任務", show_gui=True)
        except Exception as e:
            self.error_handler.log_error(e, "移除Windows排程器", user_message="移除自動排程時發生錯誤")

    def test_scheduler(self):
        """測試排程執行"""
        try:
            task_name = "CommunityScraperAutoTask"
            
            result = subprocess.run(["schtasks", "/run", "/tn", task_name], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("成功", "✅ 排程任務已開始在背景執行\n\n您可以檢查輸出資料夾來確認執行結果")
                self.update_status("排程任務測試執行中...")
                self.error_handler.log_info("排程任務測試執行")
            else:
                raise RuntimeError("執行失敗，請先設定自動排程")
        except Exception as e:
            self.error_handler.log_error(e, "測試排程執行", user_message="測試排程執行時發生錯誤")

    def start_scraping(self):
        """開始手動爬取"""
        try:
            if not self.check_lock_before_start():
                return
            
            if not self.cities_data:
                self.error_handler.log_warning("城市資料尚未載入完成", show_gui=True)
                return
            
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            self.scraping_thread = threading.Thread(target=self.scrape_data, daemon=True)
            self.scraping_thread.start()
            
            self.error_handler.log_info("開始手動爬取作業")
            
        except Exception as e:
            self.error_handler.log_error(e, "開始爬取", user_message="開始爬取時發生錯誤")

    def stop_scraping(self):
        """停止爬取"""
        try:
            if self.scraper:
                self.scraper.stop_scraping()
            self.update_status("正在停止爬取...")
            self.error_handler.log_info("使用者請求停止爬取")
        except Exception as e:
            self.error_handler.log_error(e, "停止爬取")

    def scrape_data(self):
        """執行爬取作業"""
        try:
            # 建立檔案管理器
            file_manager = SmartFileManager(
                self.output_folder.get(), 
                enable_backup=self.enable_backup.get()
            )
            
            self.scraper = CommunityDataScraper(
                progress_callback=self.update_progress,
                status_callback=self.update_status,
                output_folder=self.output_folder.get(),
                file_manager=file_manager
            )
            
            option = self.scrape_option.get()
            success = False
            
            if option == "all_cities":
                success = self.scraper.scrape_all_cities_with_districts(self.cities_data)
                
            elif option == "single_city" and self.selected_city_data:
                success = self.scraper.scrape_single_city_with_districts(self.selected_city_data)
                
            elif option == "single_district" and self.selected_city_data:
                district_index = self.district_combo.current()
                if district_index >= 0:
                    district_name = self.selected_city_data['districts'][district_index]['name']
                    success = self.scraper.scrape_single_district(self.selected_city_data, district_name)
            
            # 自動清理檔案（如果啟用）
            if success and self.auto_cleanup.get():
                self.update_status("正在執行自動檔案清理...")
                patterns = ["*社區資料*.txt", "*城市*.txt", "*區域*.txt"]
                total_cleaned = 0
                
                for pattern in patterns:
                    cleaned_files = file_manager.clean_old_files(pattern, keep_latest=1)
                    total_cleaned += len(cleaned_files)
                
                if total_cleaned > 0:
                    self.update_status(f"自動清理完成，處理了 {total_cleaned} 個舊檔案")
                
            if success:
                self.update_status("🎉 手動爬取完成！")
                self.error_handler.log_success("手動爬取完成")
            else:
                self.update_status("❌ 手動爬取失敗或被中止")
                self.error_handler.log_warning("手動爬取失敗或被中止")
            
            # 更新檔案統計
            self.refresh_file_statistics()
                
        except Exception as e:
            self.error_handler.log_error(e, "執行爬取作業")
            self.update_status(f"❌ 手動爬取錯誤: {str(e)}")
        
        finally:
            self.root.after(0, lambda: [
                self.start_button.configure(state="normal"),
                self.stop_button.configure(state="disabled")
            ])

    def update_status(self, message: str):
        """更新狀態顯示"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.status_text.see(tk.END)
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, update)
        else:
            update()

    def update_progress(self, current: int, total: int):
        """更新進度條"""
        def update():
            if total > 0:
                self.progress['value'] = (current / total) * 100
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, update)
        else:
            update()

    def force_stop_background_scraper(self):
        """強制停止背景執行的自動排程爬取"""
        try:
            exists, create_time, content = self.check_lock_file_status()
            
            if not exists:
                messagebox.showinfo("提示", "目前沒有背景程序在執行")
                self.update_status("沒有發現正在執行的背景程序")
                return
            
            result = messagebox.askyesno(
                "⚠️ 確認停止背景程序", 
                f"檢測到背景程序正在執行：\n\n"
                f"Lock檔案創建時間: {create_time}\n"
                f"檔案內容: {content}\n\n"
                f"確定要強制停止背景程序嗎？\n"
                f"（這會刪除Lock檔案，正在執行的爬取可能會不完整）",
                icon='warning'
            )
            
            if not result:
                return
            
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
                messagebox.showinfo("成功", "✅ 已強制停止背景程序\n\n背景爬取程序將會在下次檢查時停止執行")
                self.update_status("已強制停止背景自動排程程序")
                self.error_handler.log_success("已強制停止背景程序")
                self.update_lock_status_display()
            else:
                self.error_handler.log_warning("Lock檔案已經不存在，背景程序可能已經停止", show_gui=True)
        except Exception as e:
            self.error_handler.log_error(e, "強制停止背景程序", user_message="停止背景程序時發生錯誤")

    def clear_scraper_lock(self):
        """清理爬蟲鎖定檔案"""
        try:
            if os.path.exists(self.lock_file_path):
                os.remove(self.lock_file_path)
                messagebox.showinfo("成功", "✅ 已清理鎖定檔案，現在可以正常執行自動排程了")
                self.update_status("已清理爬蟲鎖定檔案")
                self.error_handler.log_success("已清理爬蟲鎖定檔案")
                self.update_lock_status_display()
            else:
                messagebox.showinfo("提示", "沒有找到鎖定檔案，無需清理")
                self.update_status("沒有找到鎖定檔案")
        except Exception as e:
            self.error_handler.log_error(e, "清理爬蟲鎖定", user_message="清理鎖定檔案時發生錯誤")

    def save_config(self):
        """儲存設定"""
        try:
            config = {
                "output_folder": self.output_folder.get(),
                "scrape_option": self.scrape_option.get(),
                "auto_cleanup": self.auto_cleanup.get(),
                "enable_backup": self.enable_backup.get(),
                "schedule_enabled": self.schedule_enabled.get(),
                "schedule_day": self.schedule_day.get(),
                "schedule_time": self.schedule_time.get(),
                "schedule_output_folder": self.schedule_output_folder.get(),
                "schedule_scrape_mode": self.schedule_scrape_mode.get(),
                "last_updated": datetime.now().isoformat()
            }
            
            with open("gui_config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("成功", "設定已儲存")
            self.update_status("設定已儲存")
            self.error_handler.log_success("設定已儲存")
        except Exception as e:
            self.error_handler.log_error(e, "儲存設定", user_message="儲存設定時發生錯誤")

    def load_config(self):
        """載入設定"""
        try:
            if os.path.exists("gui_config.json"):
                with open("gui_config.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.output_folder.set(config.get("output_folder", os.getcwd()))
                self.scrape_option.set(config.get("scrape_option", "all_cities"))
                self.auto_cleanup.set(config.get("auto_cleanup", True))
                self.enable_backup.set(config.get("enable_backup", True))
                self.schedule_enabled.set(config.get("schedule_enabled", False))
                self.schedule_day.set(config.get("schedule_day", "星期一"))
                self.schedule_time.set(config.get("schedule_time", "02:00"))
                self.schedule_output_folder.set(config.get("schedule_output_folder", 
                                                         os.path.join(os.getcwd(), "爬蟲資料")))
                self.schedule_scrape_mode.set(config.get("schedule_scrape_mode", "all_cities"))
                
                if self.schedule_enabled.get():
                    result = subprocess.run(["schtasks", "/query", "/tn", "CommunityScraperAutoTask"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        day_mapping = {
                            "星期一": "MON", "星期二": "TUE", "星期三": "WED",
                            "星期四": "THU", "星期五": "FRI", "星期六": "SAT", "星期日": "SUN"
                        }
                        schtasks_day = day_mapping.get(self.schedule_day.get(), "MON")
                        self.schedule_status_label.config(
                            text=f"✅ 已設定自動排程：每週{schtasks_day} {self.schedule_time.get()}"
                        )
                
                self.error_handler.log_info("設定檔載入完成")
        except Exception as e:
            self.error_handler.log_error(e, "載入設定", show_gui=False)


# ============================================================================
# 背景自動爬取功能
# ============================================================================
def run_background_scraper():
    """背景自動爬取功能，由Windows工作排程器呼叫"""
    
    # 設定背景專用的錯誤處理器
    bg_error_handler = ErrorHandler(
        app_name="CommunityScraperBackground",
        enable_console=True,
        enable_file=True,
        enable_gui=False  # 背景執行不顯示GUI
    )
    
    # 確定程式目錄和Lock檔案路徑
    if getattr(sys, 'frozen', False):
        program_dir = os.path.dirname(sys.executable)
    else:
        program_dir = os.path.dirname(__file__)
    
    lock_file = os.path.join(program_dir, "scraper_running.lock")
    
    # 檢查Lock檔案是否存在
    if os.path.exists(lock_file):
        bg_error_handler.log_warning("爬蟲程序已在執行中，請稍後再試")
        return

    # 建立Lock檔案
    try:
        with open(lock_file, 'w', encoding='utf-8') as f:
            f.write(f"程序開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"PID: {os.getpid()}\n")
        bg_error_handler.log_success("已建立Lock檔案")
    except Exception as e:
        bg_error_handler.log_error(e, "建立Lock檔案")
        return
        
    try:
        # 初始化和環境準備
        bg_error_handler.log_info("開始背景自動爬取...")
        print("🤖 開始背景自動爬取...")
        
        bg_error_handler.log_info(f"程式目錄: {program_dir}")
        
        # 載入設定檔
        config_path = os.path.join(program_dir, "gui_config.json")
        bg_error_handler.log_info(f"尋找設定檔: {config_path}")
        
        if not os.path.exists(config_path):
            bg_error_handler.log_warning("找不到設定檔，使用預設設定")
            output_folder = os.path.join(program_dir, "爬蟲資料")
            scrape_mode = "all_cities"
            auto_cleanup = True
            enable_backup = True
        else:
            bg_error_handler.log_success("找到設定檔，載入設定")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            output_folder = config.get("schedule_output_folder", os.path.join(program_dir, "爬蟲資料"))
            scrape_mode = config.get("schedule_scrape_mode", "all_cities")
            auto_cleanup = config.get("auto_cleanup", True)
            enable_backup = config.get("enable_backup", True)
           
            bg_error_handler.log_info(f"載入設定 - 輸出資料夾: {output_folder}")
            bg_error_handler.log_info(f"載入設定 - 爬取模式: {scrape_mode}")
            bg_error_handler.log_info(f"載入設定 - 自動清理: {auto_cleanup}")
            bg_error_handler.log_info(f"載入設定 - 啟用備份: {enable_backup}")
        
        # 準備輸出環境
        bg_error_handler.log_info(f"確保輸出資料夾存在: {output_folder}")
        os.makedirs(output_folder, exist_ok=True)
        
        # 建立檔案管理器
        file_manager = SmartFileManager(output_folder, enable_backup=enable_backup)
        
        # 建立爬蟲並設定回調函數
        bg_error_handler.log_info("建立爬蟲物件")
        
        def status_callback(msg):
            """狀態更新回調函數"""
            bg_error_handler.log_info(f"狀態: {msg}")
            print(f"📢 {msg}")
        
        def progress_callback(current, total):
            """進度更新回調函數"""
            bg_error_handler.log_info(f"進度: {current}/{total}")
            print(f"📊 進度: {current}/{total}")
        
        # 建立爬蟲實例
        scraper = CommunityDataScraper(
            status_callback=status_callback,
            progress_callback=progress_callback,
            output_folder=output_folder,
            file_manager=file_manager
        )
        
        # 載入城市資料
        bg_error_handler.log_info("開始載入城市資料...")
        cities_data = scraper.get_city_data()
        
        if not cities_data:
            raise RuntimeError("無法載入城市資料")
        
        bg_error_handler.log_success(f"成功載入 {len(cities_data)} 個城市資料")
        print(f"📊 載入了 {len(cities_data)} 個城市資料")
        
        # 執行爬取作業
        bg_error_handler.log_info(f"開始執行爬取，模式: {scrape_mode}")
        success = False
        
        if scrape_mode == "all_cities":
            bg_error_handler.log_info("執行：爬取全部城市（分區）")
            success = scraper.scrape_all_cities_with_districts(cities_data)
        else:
            bg_error_handler.log_warning(f"未知的爬取模式: {scrape_mode}")
        
        # 自動清理檔案（如果啟用）
        if success and auto_cleanup:
            bg_error_handler.log_info("開始執行自動檔案清理...")
            patterns = ["*社區資料*.txt", "*城市*.txt", "*區域*.txt"]
            total_cleaned = 0
            
            for pattern in patterns:
                cleaned_files = file_manager.clean_old_files(pattern, keep_latest=1)
                total_cleaned += len(cleaned_files)
            
            if total_cleaned > 0:
                bg_error_handler.log_success(f"自動清理完成，處理了 {total_cleaned} 個舊檔案")
        
        # 處理執行結果
        if success:
            bg_error_handler.log_success("背景自動爬取完成")
            print("✅ 背景自動爬取完成")
            
            # 記錄成功執行到結果檔案
            result_log = os.path.join(output_folder, "auto_scrape_log.txt")
            with open(result_log, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 自動爬取成功 (模式: {scrape_mode})\n")
            
            bg_error_handler.log_info(f"記錄執行結果到: {result_log}")
        else:
            bg_error_handler.log_warning("背景自動爬取失敗")
            print("❌ 背景自動爬取失敗")
            
    except Exception as e:
        # 錯誤處理和記錄
        bg_error_handler.log_error(e, "背景自動爬取")
        print(f"❌ 背景自動爬取錯誤: {e}")
        
        # 將錯誤記錄到輸出資料夾
        if 'output_folder' in locals():
            try:
                error_log = os.path.join(output_folder, "auto_scrape_error.log")
                with open(error_log, 'a', encoding='utf-8') as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 自動爬取錯誤: {e}\n")
                    f.write(f"詳細錯誤請查看: {bg_error_handler.error_log_file}\n")
                    f.write("-" * 50 + "\n")
            except Exception as log_error:
                bg_error_handler.log_error(log_error, "寫入錯誤日誌")
    
    finally:
        # 清理Lock檔案
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                bg_error_handler.log_success("已清理Lock檔案")
        except Exception as e:
            bg_error_handler.log_error(e, "清理Lock檔案")
        
        bg_error_handler.log_info("背景自動爬取函式結束")


def test_log(message):
    """測試日誌函式（與main.py兼容）"""
    log_file = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "test.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")


# ============================================================================
# 主程式進入點
# ============================================================================
def main():
    """主程式進入點"""
    test_log("程式啟動")
    test_log(f"參數: {sys.argv}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-background":
        test_log("背景模式啟動")
        
        try:
            test_log("嘗試執行 run_background_scraper")
            run_background_scraper()
            test_log("run_background_scraper 執行完成")
            
        except Exception as e:
            test_log(f"錯誤: {str(e)}")
            import traceback
            test_log(f"詳細錯誤: {traceback.format_exc()}")
        
        test_log("背景模式結束")
        return
    
    # GUI 模式
    test_log("GUI 模式")
    try:
        root = tk.Tk()
        app = EnhancedScraperGUI(root)
        root.mainloop()
        
    except Exception as e:
        test_log(f"GUI 錯誤: {str(e)}")
        print(f"錯誤: {e}")
        input("按 Enter 退出...")


if __name__ == "__main__":
    main()