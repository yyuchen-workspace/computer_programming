#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社區資料爬蟲 GUI 應用程式
使用 Flet 框架建立的桌面應用程式，提供直觀的界面來管理社區資料爬取任務
"""

# 匯入 Flet 框架，用於建立桌面 GUI 應用程式
import flet as ft
# 匯入作業系統相關功能
import os
# 匯入多執行緒模組，用於背景執行爬取作業
import threading
# 匯入時間相關功能
import time
# 匯入 JSON 處理模組，用於設定檔讀寫
import json
# 匯入子程序控制模組，用於執行系統命令
import subprocess
# 匯入系統相關功能
import sys
# 匯入日期時間處理模組
from datetime import datetime, timedelta
# 匯入路徑處理模組
from pathlib import Path
# 匯入型別提示
from typing import Optional, Dict, List
# 匯入日誌記錄模組
import logging

# 匯入您的爬蟲模組
from scraper import CommunityDataScraper
from file_manager import SmartFileManager

class CommunityScraperApp:
    """
    社區資料爬蟲 GUI 應用程式主類別
    功能：
    - 提供圖形化介面管理爬蟲作業
    - 支援多種爬取模式（全部城市、單一城市、單一區域）
    - 自動排程功能
    - 即時狀態監控和日誌顯示
    - 設定檔案管理
    """
    
    def __init__(self):
        """
        初始化應用程式
        功能：設定基本參數、載入設定檔、初始化 UI 元件
        """
        # 基本設定
        self.page: Optional[ft.Page] = None  # Flet 頁面物件，初始為空
        self.scraper: Optional[CommunityDataScraper] = None  # 爬蟲實例，初始為空
        self.file_manager: Optional[SmartFileManager] = None  # 檔案管理器，初始為空
        self.cities_data: List[Dict] = []  # 儲存城市資料的清單
        self.current_scraping_thread: Optional[threading.Thread] = None  # 當前爬取執行緒
        self.is_scraping = False  # 爬取狀態標記
        
        # 設定檔路徑
        self.config_file = Path("config.json")  # 應用程式設定檔路徑
        self.lock_file = Path("scraper.lock")  # 程序鎖定檔案路徑，防止重複執行
        
        # 預設設定
        self.default_config = {  # 預設設定字典
            "output_folder": str(Path.cwd() / "爬蟲資料"),  # 預設輸出資料夾
            "auto_schedule": False,  # 預設關閉自動排程
            "schedule_day": "星期一",  # 預設排程日期
            "schedule_time": "02:00",  # 預設排程時間
            "scrape_mode": "all_cities",  # 預設爬取模式
            "selected_city": "",  # 預設選擇的城市
            "selected_district": "",  # 預設選擇的區域
            "theme_mode": "system"  # 預設主題模式
        }
        
        # 載入設定
        self.config = self.load_config()  # 從檔案載入設定或使用預設值
        
        # 設定日誌
        self.setup_logging()  # 初始化日誌系統
        
        # 初始化 UI 元件
        self.init_ui_components()  # 建立所有使用者介面元件
        
    def setup_logging(self):
        """
        設定日誌系統
        功能：建立日誌資料夾、設定日誌格式和輸出目標
        """
        log_folder = Path("logs")  # 建立日誌資料夾路徑
        log_folder.mkdir(exist_ok=True)  # 建立資料夾，如果已存在則不報錯
        
        # 主程式日誌
        logging.basicConfig(  # 設定基本日誌配置
            level=logging.INFO,  # 設定日誌等級為 INFO
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日誌格式
            handlers=[  # 日誌處理器清單
                logging.FileHandler(log_folder / "app.log", encoding='utf-8'),  # 檔案處理器
                logging.StreamHandler()  # 控制台處理器
            ]
        )
        self.logger = logging.getLogger(__name__)  # 取得當前模組的日誌記錄器
        
    def init_ui_components(self):
        """
        初始化 UI 元件
        功能：建立所有使用者介面元件並設定其屬性
        """
        # 進度相關
        self.progress_bar = ft.ProgressBar(  # 建立進度條元件
            width=None,  # 自動寬度
            color=ft.Colors.BLUE,  # 進度條顏色
            bgcolor=ft.Colors.BLUE_100,  # 背景顏色
            visible=False  # 初始狀態為隱藏
        )
        self.progress_text = ft.Text("", size=14, color=ft.Colors.BLUE_700)  # 進度文字顯示
        
        # 狀態顯示
        self.status_text = ft.Text(  # 建立狀態文字元件
            "準備就緒",  # 初始文字
            size=14,  # 字體大小
            color=ft.Colors.GREEN_700,  # 字體顏色
            weight=ft.FontWeight.BOLD  # 字體粗細
        )

        #加入執行狀態顯示
        self.execution_status_text = ft.Text(  # 建立執行狀態文字元件
            "🟢 無執行程序",  # 初始狀態文字
            size=12,  # 字體大小
            weight=ft.FontWeight.BOLD,  # 字體粗細
            color=ft.Colors.GREEN_700  # 字體顏色
        )

        # 輸出資料夾選擇
        self.output_folder_text = ft.TextField(  # 建立輸出資料夾文字輸入框
            label="輸出資料夾路徑",  # 標籤文字
            value=self.config["output_folder"],  # 從設定檔載入初始值
            width=None,  # 自動寬度，讓它填滿可用空間
            read_only=True  # 設為唯讀
        )
        
        # 城市選擇下拉選單
        self.city_dropdown = ft.Dropdown(  # 建立城市選擇下拉選單
            label="選擇城市",  # 標籤文字
            #width=200,  # 自動寬度
            expand=True,  # 擴展填滿可用空間
            on_change=self.on_city_changed  # 設定變更事件處理函式
        )
        
        # 區域選擇下拉選單
        self.district_dropdown = ft.Dropdown(  # 建立區域選擇下拉選單
            label="選擇區域",  # 標籤文字
            #width=200,  # 自動寬度
            expand=True,  # 擴展填滿可用空間
            disabled=True  # 初始時禁用，直到選擇城市
        )
        
        # 爬取模式選擇
        self.scrape_mode_radio = ft.RadioGroup(  # 建立單選按鈕群組
            content=ft.Column(  # 建立欄位佈局
                [
                    ft.Row([  # 第一行選項
                        ft.Container(  # 容器包裝第一個選項
                            content=ft.Radio(value="all_cities", label="爬取全部城市(資料分區)"),  # 全部城市選項
                            margin=ft.margin.only(right=10, bottom=0.5),  # 設定邊距
                        ),
                        ft.Container(  # 容器包裝第二個選項
                            content=ft.Radio(value="single_city", label="爬取單一城市(資料分區)"),  # 單一城市選項
                            margin=ft.margin.only(bottom=0.5),  # 設定邊距
                        )
                    ]),
                    ft.Row([  # 第二行選項
                        ft.Container(  # 容器包裝第三個選項
                            content=ft.Radio(value="single_district", label="爬取單一區域"),  # 單一區域選項
                            margin=ft.margin.only(bottom=0),  # 設定邊距
                        )
                    ])
                ]
            ),
            value=self.config["scrape_mode"],  # 從設定檔載入初始選項
            on_change=self.on_scrape_mode_changed  # 設定變更事件處理函式
        )
        # 控制按鈕
        self.start_button = ft.ElevatedButton(  # 建立開始按鈕
            text="開始爬取",  # 按鈕文字
            icon=ft.Icons.PLAY_ARROW,  # 按鈕圖示
            on_click=self.start_scraping, # 正式版的點擊事件處理函式
            #on_click=self.test_dialog, #測試對話框執行與否用
            #on_click=self.test_real_dialog,  # #測試對話框執行與否用
            #on_click=self.test_both_dialogs, #測試簡易版+自製版用
            style=ft.ButtonStyle(  # 按鈕樣式
                color=ft.Colors.WHITE,  # 文字顏色
                bgcolor=ft.Colors.GREEN_600  # 背景顏色
            )
        )
        
        self.stop_button = ft.ElevatedButton(  # 建立停止按鈕
            text="停止爬取",  # 按鈕文字
            icon=ft.Icons.STOP,  # 按鈕圖示
            on_click=self.stop_scraping,  # 點擊事件處理函式
            disabled=True,  # 初始狀態為禁用
            style=ft.ButtonStyle(  # 按鈕樣式
                color=ft.Colors.WHITE,  # 文字顏色
                bgcolor=ft.Colors.RED_600  # 背景顏色
            )
        )
        
        
        self.schedule_day_dropdown = ft.Dropdown(  # 建立排程日期下拉選單
            label="執行日期",  # 標籤文字
            width=150,  # 固定寬度
            value=self.config["schedule_day"],  # 從設定檔載入初始值
            options=[  # 選項清單
                ft.dropdown.Option("星期一"),  # 星期一選項
                ft.dropdown.Option("星期二"),  # 星期二選項
                ft.dropdown.Option("星期三"),  # 星期三選項
                ft.dropdown.Option("星期四"),  # 星期四選項
                ft.dropdown.Option("星期五"),  # 星期五選項
                ft.dropdown.Option("星期六"),  # 星期六選項
                ft.dropdown.Option("星期日"),  # 星期日選項
            ]
        )
        
        self.schedule_time_field = ft.TextField(  # 建立排程時間輸入框
            label="執行時間 (HH:MM)",  # 標籤文字
            value=self.config["schedule_time"],  # 從設定檔載入初始值
            width=150,  # 固定寬度
            hint_text="例: 02:00"  # 提示文字
        )
        
        # 排程控制按鈕
        self.set_schedule_button = ft.ElevatedButton(  # 建立設定排程按鈕
            text="設定排程",  # 按鈕文字
            icon=ft.Icons.SCHEDULE,  # 按鈕圖示
            on_click=self.set_schedule,  # 點擊事件處理函式
            style=ft.ButtonStyle(  # 按鈕樣式
                color=ft.Colors.WHITE,  # 文字顏色
                bgcolor=ft.Colors.GREEN_600  # 背景顏色

            )
        )
        
        self.remove_schedule_button = ft.ElevatedButton(  # 建立移除排程按鈕
            text="移除排程",  # 按鈕文字
            icon=ft.Icons.DELETE_FOREVER,  # 按鈕圖示
            on_click=self.remove_schedule,  # 點擊事件處理函式
            style=ft.ButtonStyle(  # 按鈕樣式
                color=ft.Colors.WHITE,  # 文字顏色
                bgcolor=ft.Colors.RED_600  # 背景顏色
            )
        )
        
        self.stop_background_button = ft.ElevatedButton(  # 建立停止背景程序按鈕
            text="停止背景程序",  # 按鈕文字
            icon=ft.Icons.STOP_CIRCLE,  # 按鈕圖示
            on_click=self.stop_background_process,  # 點擊事件處理函式
            style=ft.ButtonStyle(  # 按鈕樣式
                color=ft.Colors.WHITE,  # 文字顏色
                bgcolor=ft.Colors.RED_600  # 背景顏色
            )
        )
        
        # 排程狀態顯示
        self.schedule_status_text = ft.Text(  # 建立排程狀態文字元件
            "排程狀態: 未設定",  # 初始狀態文字
            size=12,  # 字體大小
            color=ft.Colors.GREY_700  # 字體顏色
        )
        
        # 日誌顯示區域
        self.log_text = ft.TextField(  # 建立日誌顯示文字框
            #label="執行日誌",
            multiline=True,  # 多行模式
            max_lines=15,  # 最大行數
            width=None,  # 自動寬度
            height=280,  # 固定高度
            read_only=True,  # 設為唯讀
            text_style=ft.TextStyle(  # 文字樣式
                font_family="Consolas",  # 等寬字體
                size=13  # 字體大小
            )
        )
        
        # 統計資訊顯示
        self.stats_text = ft.Text("", size=12, color=ft.Colors.BLUE_700)  # 建立統計資訊文字元件
        
    def load_config(self) -> Dict:
        """
        載入設定檔
        功能：從 config.json 檔案載入設定，如果檔案不存在或載入失敗則使用預設設定
        返回：設定字典
        """
        if self.config_file.exists():  # 檢查設定檔是否存在
            try:
                with self.config_file.open('r', encoding='utf-8') as f:  # 開啟設定檔
                    config = json.load(f)  # 載入 JSON 設定
                # 合併預設設定，確保所有必要的鍵都存在
                for key, value in self.default_config.items():  # 遍歷預設設定
                    if key not in config:  # 如果設定中缺少某個鍵
                        config[key] = value  # 使用預設值
                return config  # 返回完整設定
            except Exception as e:  # 載入失敗時的異常處理
                self.logger.error(f"載入設定檔失敗: {e}")  # 記錄錯誤
                return self.default_config.copy()  # 返回預設設定的副本
        return self.default_config.copy()  # 檔案不存在時返回預設設定的副本
    
    def save_config(self):
        """
        儲存設定檔
        功能：將當前設定儲存到 config.json 檔案
        """
        try:
            self.config["output_folder"] = self.output_folder_text.value  # 更新輸出資料夾設定
            self.config["scrape_mode"] = self.scrape_mode_radio.value  # 更新爬取模式設定
            self.config["auto_schedule"] = self.schedule_checkbox.value  # 更新自動排程設定
            self.config["schedule_day"] = self.schedule_day_dropdown.value  # 更新排程日期設定
            self.config["schedule_time"] = self.schedule_time_field.value  # 更新排程時間設定
            if self.city_dropdown.value:  # 如果有選擇城市
                self.config["selected_city"] = self.city_dropdown.value  # 更新選擇的城市
            if self.district_dropdown.value:  # 如果有選擇區域
                self.config["selected_district"] = self.district_dropdown.value  # 更新選擇的區域
            
            with self.config_file.open('w', encoding='utf-8') as f:  # 開啟設定檔進行寫入
                json.dump(self.config, f, ensure_ascii=False, indent=2)  # 儲存 JSON 設定
            self.logger.info("設定已儲存")  # 記錄成功訊息
        except Exception as e:  # 儲存失敗時的異常處理
            self.logger.error(f"儲存設定檔失敗: {e}")  # 記錄錯誤
            self.show_error(f"儲存設定失敗: {e}")  # 顯示錯誤訊息
    
    def show_error(self, message: str):
        """
        顯示錯誤訊息
        功能：在頁面上顯示紅色的錯誤提示訊息
        參數：message - 錯誤訊息文字
        """
        if self.page:  # 檢查頁面物件是否存在
            self.page.snack_bar = ft.SnackBar(  # 建立提示訊息框
                content=ft.Text(message),  # 設定訊息內容
                bgcolor=ft.Colors.RED_400  # 設定紅色背景
            )
            self.page.snack_bar.open = True  # 開啟提示訊息框
            self.page.update()  # 更新頁面顯示
    
    def show_success(self, message: str):
        """
        顯示成功訊息
        功能：在頁面上顯示綠色的成功提示訊息
        參數：message - 成功訊息文字
        """
        if self.page:  # 檢查頁面物件是否存在
            self.page.snack_bar = ft.SnackBar(  # 建立提示訊息框
                content=ft.Text(message),  # 設定訊息內容
                bgcolor=ft.Colors.GREEN_400  # 設定綠色背景
            )
            self.page.snack_bar.open = True  # 開啟提示訊息框
            self.page.update()  # 更新頁面顯示
    
    def log_message(self, message: str):
        """
        新增日誌訊息
        功能：在 UI 日誌區域和檔案中記錄訊息
        參數：message - 日誌訊息文字
        """
        timestamp = datetime.now().strftime("%H:%M:%S")  # 取得當前時間戳記
        formatted_message = f"[{timestamp}] {message}"  # 格式化訊息，加上時間戳記
        
        # 更新 UI 日誌
        if self.log_text.value:  # 如果日誌區域已有內容
            self.log_text.value += "\n" + formatted_message  # 添加新訊息到末尾
        else:
            self.log_text.value = formatted_message  # 設定為第一條訊息
        
        # 自動捲動到底部
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
        
        # 記錄到檔案
        self.logger.info(message)  # 將訊息寫入日誌檔案
    
    def update_status(self, message: str):
        """
        更新狀態訊息
        功能：更新狀態文字並記錄到日誌
        參數：message - 狀態訊息文字
        """
        self.status_text.value = message  # 更新狀態文字
        self.log_message(message)  # 記錄到日誌
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
    
    def update_progress(self, current: int, total: int):
        """
        更新進度條
        功能：根據當前進度和總數更新進度條顯示
        參數：current - 當前完成數量，total - 總數量
        """
        if total > 0:  # 如果總數大於 0
            progress = current / total  # 計算進度百分比
            self.progress_bar.value = progress  # 設定進度條值
            self.progress_text.value = f"進度: {current}/{total} ({progress*100:.1f}%)"  # 更新進度文字
        else:
            self.progress_bar.value = 0  # 設定進度條為 0
            self.progress_text.value = "進度: 0/0 (0%)"  # 設定進度文字為 0
        
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
    
    def choose_output_folder(self, e):
        """
        選擇輸出資料夾
        功能：開啟檔案選擇對話框，讓使用者選擇輸出資料夾
        參數：e - 事件物件
        """
        def on_folder_selected(selected_folder):  # 資料夾選擇完成後的回調函式
            """處理選擇的資料夾"""
            if selected_folder:  # 如果有選擇資料夾
                self.output_folder_text.value = selected_folder  # 更新輸出資料夾文字框
                self.page.update()  # 更新頁面顯示
                self.save_config()  # 儲存設定
        
        # 使用 Flet 的檔案選擇對話框
        folder_picker = ft.FilePicker(  # 建立檔案選擇器
            on_result=lambda e: on_folder_selected(e.path)  # 設定結果回調函式
        )
        self.page.overlay.append(folder_picker)  # 將選擇器添加到頁面覆蓋層
        self.page.update()  # 更新頁面顯示
        folder_picker.get_directory_path()  # 開啟資料夾選擇對話框
    
    def on_city_changed(self, e):
        """
        城市選擇變更事件
        功能：當使用者選擇城市時，更新區域下拉選單的選項
        參數：e - 事件物件
        """
        selected_city = e.control.value  # 取得選擇的城市
        if selected_city and self.cities_data and self.scrape_mode_radio.value == "single_district":  # 如果有選擇城市且為單一區域模式
            # 尋找對應的城市資料
            city_data = None  # 初始化城市資料變數
            for city in self.cities_data:  # 遍歷城市資料
                if city['name'] == selected_city:  # 如果找到對應城市
                    city_data = city  # 設定城市資料
                    break  # 跳出迴圈
            
            if city_data:  # 如果找到城市資料
                # 更新區域下拉選單
                self.district_dropdown.options.clear()  # 清空現有選項
                for district in city_data['districts']:  # 遍歷城市的區域
                    self.district_dropdown.options.append(  # 添加區域選項
                        ft.dropdown.Option(district['name'])  # 建立下拉選項
                    )
                # 區域選擇的啟用狀態由爬取模式決定，不在這裡改變
                self.district_dropdown.value = None  # 清空區域選擇
            else:
                self.district_dropdown.options.clear()  # 清空區域選項
        else:
            # 非 single_district 模式下清空區域選項
            self.district_dropdown.options.clear()  # 清空區域選項
            self.district_dropdown.value = None  # 清空區域選擇
        
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
        self.save_config()  # 儲存設定
    
    def on_scrape_mode_changed(self, e):
        """
        爬取模式變更事件
        功能：當使用者變更爬取模式時，啟用或禁用相關控制項
        參數：e - 事件物件
        """
        mode = e.control.value  # 取得選擇的爬取模式
        
        # 根據模式啟用/停用相關控制項
        if mode == "all_cities":  # 如果選擇全部城市模式
            self.city_dropdown.disabled = True  # 禁用城市選擇
            self.district_dropdown.disabled = True  # 禁用區域選擇
            # 清空選擇值
            self.city_dropdown.value = None  # 清空城市選擇
            self.district_dropdown.value = None  # 清空區域選擇
            # 清空區域選項
            self.district_dropdown.options.clear()  # 清空區域選項
        elif mode == "single_city":  # 如果選擇單一城市模式
            self.city_dropdown.disabled = False  # 啟用城市選擇
            self.district_dropdown.disabled = True # single_city 模式下區域選擇保持禁用
            # 清空區域選擇
            self.district_dropdown.value = None  # 清空區域選擇
            self.district_dropdown.options.clear()  # 清空區域選項
        elif mode == "single_district":  # 如果選擇單一區域模式
            self.city_dropdown.disabled = False  # 啟用城市選擇
            self.district_dropdown.disabled = False # 只有這個模式下才啟用區域選擇
            # 如果已有城市選擇，重新載入區域資料
            if self.city_dropdown.value:  # 如果已選擇城市
                self.on_city_changed(type('obj', (object,), {'control': type('obj', (object,), {'value': self.city_dropdown.value})()})())  # 觸發城市變更事件
        
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
        self.save_config()  # 儲存設定
    
    def on_schedule_toggle(self, e):
        """
        自動排程切換事件
        功能：當使用者切換自動排程開關時儲存設定
        參數：e - 事件物件
        """
        self.save_config()  # 儲存設定
    
    def check_lock_file(self) -> bool:
        """
        檢查是否有其他實例正在運行
        功能：檢查鎖定檔案是否存在，防止重複執行
        返回：True 如果有其他實例運行，False 則無
        """
        return self.lock_file.exists()  # 返回鎖定檔案是否存在
    
    def create_lock_file(self):
        """
        建立鎖定檔案
        功能：建立鎖定檔案，記錄當前程序 ID
        """
        try:
            with self.lock_file.open('w') as f:  # 開啟鎖定檔案進行寫入
                f.write(str(os.getpid()))  # 寫入當前程序 ID
        except Exception as e:  # 建立失敗時的異常處理
            self.logger.error(f"建立鎖定檔案失敗: {e}")  # 記錄錯誤
    
    def remove_lock_file(self):
        """
        移除鎖定檔案
        功能：刪除鎖定檔案，釋放程序鎖定
        """
        try:
            if self.lock_file.exists():  # 如果鎖定檔案存在
                self.lock_file.unlink()  # 刪除檔案
        except Exception as e:  # 刪除失敗時的異常處理
            self.logger.error(f"移除鎖定檔案失敗: {e}")  # 記錄錯誤
    
    def load_cities_data(self):
        """
        載入城市資料
        功能：初始化爬蟲並從網站載入城市和區域資料
        """
        try:
            self.update_status("正在載入城市資料...")  # 更新狀態訊息
            
            # 初始化爬蟲
            self.scraper = CommunityDataScraper(  # 建立爬蟲實例
                progress_callback=self.update_progress,  # 設定進度回調函式
                status_callback=self.update_status,  # 設定狀態回調函式
                output_folder=self.output_folder_text.value  # 設定輸出資料夾
            )
            
            # 獲取城市資料
            self.cities_data = self.scraper.get_city_data()  # 取得城市資料
            
            if self.cities_data:  # 如果成功載入城市資料
                # 更新城市下拉選單
                self.city_dropdown.options.clear()  # 清空現有選項
                for city in self.cities_data:  # 遍歷城市資料
                    self.city_dropdown.options.append(  # 添加城市選項
                        ft.dropdown.Option(city['name'])  # 建立下拉選項
                    )
                '''
                # 恢復之前選擇的城市
                if self.config.get("selected_city"):
                    self.city_dropdown.value = self.config["selected_city"]
                    self.on_city_changed(type('obj', (object,), {'control': type('obj', (object,), {'value': self.config["selected_city"]})()})())
                '''
                self.update_status(f"成功載入 {len(self.cities_data)} 個城市資料")  # 更新成功狀態
                self.show_success(f"載入了 {len(self.cities_data)} 個城市的資料")  # 顯示成功訊息
            else:
                self.update_status("載入城市資料失敗")  # 更新失敗狀態
                self.show_error("無法載入城市資料，請檢查網路連線")  # 顯示錯誤訊息
                
        except Exception as e:  # 載入過程中的異常處理
            self.update_status(f"載入城市資料時發生錯誤: {e}")  # 更新錯誤狀態
            self.show_error(f"載入城市資料失敗: {e}")  # 顯示錯誤訊息
    
    def start_scraping(self, e):
        """
        開始爬取
        功能：檢查狀態、驗證設定，然後開始爬取作業
        參數：e - 事件物件
        """
        # 1. 檢查是否已在進行中
        if self.is_scraping:  # 如果正在爬取中
            self.show_dialog("錯誤", "爬取程序已在進行中", is_error=True)  # 顯示錯誤對話框
            return  # 結束函式執行
        
        # 2. 檢查lock_file狀態
        lock_info = self.get_lock_file_info()  # 取得鎖定檔案資訊
        if lock_info["exists"]:  # 如果鎖定檔案存在
            lock_type = lock_info.get("type", "unknown")  # 取得鎖定類型
            if lock_type == "background":  # 如果是背景程序
                self.show_dialog("錯誤", "背景程序爬取中!", is_error=True)  # 顯示背景程序錯誤
            else:
                self.show_dialog("錯誤", "偵測到其他爬取程序正在執行，請稍後再試", is_error=True)  # 顯示其他程序錯誤
            return  # 結束函式執行
        
        # 3. 驗證設定
        is_valid, error_message = self.validate_scrape_settings()  # 驗證爬取設定
        if not is_valid:  # 如果設定無效
            self.show_dialog("錯誤", error_message, is_error=True)  # 顯示設定錯誤
            return  # 結束函式執行
        
        # 4. 一切正常，顯示開始提示並執行
        self.show_dialog("提示", "開始爬取作業...")  # 顯示開始提示
        
        # 更新 UI 狀態
        self.is_scraping = True  # 設定爬取狀態為真
        self.start_button.disabled = True  # 禁用開始按鈕
        self.stop_button.disabled = False  # 啟用停止按鈕
        self.progress_bar.visible = True  # 顯示進度條
        self.progress_bar.value = 0  # 重置進度條值
        self.progress_text.value = "準備開始..."  # 設定進度文字
        
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
        
        # 建立手動爬取的鎖定檔案
        self.create_lock_file("manual")  # 建立手動類型的鎖定檔案
        
        # 更新狀態顯示 ← 加入這行
        self.update_execution_status()  # 更新執行狀態顯示

        # 儲存設定
        self.save_config()  # 儲存當前設定
        
        # 在背景執行緒中進行爬取
        self.current_scraping_thread = threading.Thread(  # 建立新執行緒
            target=self._scraping_worker,  # 設定執行緒目標函式
            daemon=True  # 設為守護執行緒
        )
        self.current_scraping_thread.start()  # 啟動執行緒
    
    def _scraping_worker(self):
        """
        爬取工作執行緒
        功能：在背景執行緒中執行實際的爬取工作
        """
        try:
            
            # 重新初始化爬蟲（確保使用最新設定）
            self.scraper = CommunityDataScraper(  # 建立新的爬蟲實例
                progress_callback=self.update_progress,  # 設定進度回調函式
                status_callback=self.update_status,  # 設定狀態回調函式
                output_folder=self.output_folder_text.value,  # 設定輸出資料夾
                auto_cleanup=True,  # 啟用自動清理
                enable_backup=True  # 啟用備份功能
            )
            
            mode = self.scrape_mode_radio.value  # 取得爬取模式
            success = False  # 初始化成功標記
            
            if mode == "all_cities":  # 如果是全部城市模式
                success = self.scraper.scrape_all_cities_with_districts(self.cities_data)  # 爬取全部城市
            elif mode == "single_city":  # 如果是單一城市模式
                city_name = self.city_dropdown.value  # 取得選擇的城市名稱
                city_data = None  # 初始化城市資料變數
                for city in self.cities_data:  # 遍歷城市資料
                    if city['name'] == city_name:  # 如果找到對應城市
                        city_data = city  # 設定城市資料
                        break  # 跳出迴圈
                if city_data:  # 如果找到城市資料
                    success = self.scraper.scrape_single_city_with_districts(city_data)  # 爬取單一城市
            elif mode == "single_district":  # 如果是單一區域模式
                city_name = self.city_dropdown.value  # 取得選擇的城市名稱
                district_name = self.district_dropdown.value  # 取得選擇的區域名稱
                city_data = None  # 初始化城市資料變數
                for city in self.cities_data:  # 遍歷城市資料
                    if city['name'] == city_name:  # 如果找到對應城市
                        city_data = city  # 設定城市資料
                        break  # 跳出迴圈
                if city_data:  # 如果找到城市資料
                    success = self.scraper.scrape_single_district(city_data, district_name)  # 爬取單一區域
            
            if success:  # 如果爬取成功
                # 顯示統計資訊
                stats = self.scraper.get_scrape_statistics()  # 取得爬取統計資訊
                stats_message = (  # 建立統計訊息
                    f"爬取完成！統計資訊:\n"
                    f"- 處理檔案數: {stats.get('processed_files', 0)}\n"
                    f"- 總社區數: {stats.get('total_communities', 0)}\n"
                    f"- 新增社區數: {stats.get('new_communities', 0)}\n"
                    f"- 處理時間: {stats.get('duration_formatted', '未知')}"
                )
                self.stats_text.value = stats_message  # 設定統計文字
                self.update_status("✅ 爬取作業完成")  # 更新狀態為完成
                self.show_success("爬取作業順利完成！")  # 顯示成功訊息
            else:
                self.update_status("❌ 爬取作業失敗或被中斷")  # 更新狀態為失敗
                
        except Exception as e:  # 爬取過程中的異常處理
            self.update_status(f"❌ 爬取過程發生錯誤: {e}")  # 更新錯誤狀態
            self.logger.error(f"爬取錯誤: {e}", exc_info=True)  # 記錄詳細錯誤
        finally:
            # 清理和重置狀態
            self._reset_scraping_state()  # 重置爬取狀態
    

    def stop_scraping(self, e):
        """
        停止爬取
        功能：停止正在進行的爬取作業
        參數：e - 事件物件
        """
        # 1. 檢查lock_file狀態
        lock_info = self.get_lock_file_info()  # 取得鎖定檔案資訊
        
        if not lock_info["exists"]:  # 如果鎖定檔案不存在
            self.show_dialog("錯誤", "當前未有爬取進行", is_error=True)  # 顯示沒有爬取進行錯誤
            return  # 結束函式執行
        
        lock_type = lock_info.get("type", "unknown")  # 取得鎖定類型
        
        if lock_type == "background":  # 如果是背景程序
            self.show_dialog("錯誤", "背景程序爬取中!", is_error=True)  # 顯示背景程序錯誤
            return  # 結束函式執行
        
        # 2. 執行停止操作
        if self.scraper:  # 如果爬蟲實例存在
            self.scraper.stop_scraping()  # 停止爬蟲作業
        
        self.update_status("正在停止爬取...")  # 更新狀態為停止中
        self.show_dialog("提示", "爬取已停止")  # 顯示停止提示

    def _reset_scraping_state(self):
        """
        重置爬取狀態
        功能：重置所有爬取相關的狀態和 UI 元件
        """
        self.is_scraping = False  # 設定爬取狀態為假
        self.start_button.disabled = False  # 啟用開始按鈕
        self.stop_button.disabled = True  # 禁用停止按鈕
        self.progress_bar.visible = False  # 隱藏進度條
        
        # 移除鎖定檔案
        self.remove_lock_file()  # 移除鎖定檔案
        
        # 更新狀態顯示 
        self.update_execution_status()  # 更新執行狀態顯示

        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示
    
    def set_schedule(self, e):
        """
        設定自動排程
        功能：建立 Windows 工作排程，在指定時間自動執行爬取
        參數：e - 事件物件
        """
        try:
            if not self.schedule_checkbox.value:  # 如果未啟用自動排程
                self.show_error("請先啟用自動排程")  # 顯示錯誤訊息
                return  # 結束函式執行
            
            # 驗證時間格式
            time_str = self.schedule_time_field.value  # 取得時間字串
            try:
                datetime.strptime(time_str, "%H:%M")  # 驗證時間格式
            except ValueError:  # 時間格式錯誤
                self.show_error("時間格式錯誤，請使用 HH:MM 格式（例: 02:00）")  # 顯示格式錯誤
                return  # 結束函式執行
            
            # 建立批次檔
            batch_content = self._create_batch_file()  # 建立批次檔案
            
            # 設定 Windows 工作排程器
            self._create_windows_schedule()  # 建立 Windows 排程
            
            self.schedule_status_text.value = f"排程狀態: 已設定 - {self.schedule_day_dropdown.value} {time_str}"  # 更新排程狀態文字
            self.update_status("✅ 自動排程設定成功")  # 更新狀態為成功
            self.show_success("自動排程已成功設定到系統")  # 顯示成功訊息
            
            self.save_config()  # 儲存設定
            
        except Exception as e:  # 設定過程中的異常處理
            self.update_status(f"❌ 設定排程失敗: {e}")  # 更新錯誤狀態
            self.show_error(f"設定排程失敗: {e}")  # 顯示錯誤訊息
    
    def _create_batch_file(self) -> str:
        """
        建立批次檔案
        功能：建立用於背景執行的批次檔案
        返回：批次檔案的完整路徑
        """
        batch_file = Path("scraper_background.bat")  # 設定批次檔案路徑
        python_exe = sys.executable  # 取得 Python 執行檔路徑
        script_path = Path(__file__).resolve()  # 取得當前腳本路徑
        
        # 建立背景執行的批次檔內容
        batch_content = f'''
@echo off
REM 社區爬蟲背景執行批次檔 - 修正版
chcp 65001 > nul
cd /d "%~dp0"

echo [%date% %time%] 開始背景爬取程序
echo =====================================

REM 優先使用exe版本，否則使用Python版本
if exist "community_scraper.exe" (
    echo [%date% %time%] 找到 community_scraper.exe，使用編譯版本
    "community_scraper.exe" --background
    set "exit_code=%errorlevel%"
) 
else (
    echo [%date% %time%] 錯誤：找不到執行檔案
    echo 請確認 community_scraper.exe 或 main.py 存在於當前目錄
    set "exit_code=1"
    goto error_exit
)

REM 檢查執行結果
if %exit_code% equ 0 (
    echo [%date% %time%] 背景爬取程序執行完成
) else (
    echo [%date% %time%] 背景爬取程序執行失敗，退出代碼：%exit_code%
)

goto end

:error_exit
echo [%date% %time%] 程序執行失敗
pause

:end
echo [%date% %time%] 批次檔執行結束
REM 取消註解下面這行可以看到執行結果
REM pause
'''
        
        with batch_file.open('w', encoding='utf-8') as f:  # 開啟批次檔案進行寫入
            f.write(batch_content)  # 寫入批次檔內容
        
        return str(batch_file.resolve())  # 返回批次檔案的完整路徑
    
    def _create_windows_schedule(self):
        """
        建立 Windows 工作排程
        功能：使用 schtasks 命令建立系統排程任務
        """
        task_name = "CommunityScraperTask"  # 設定任務名稱
        batch_file = Path("scraper_background.bat").resolve()  # 取得批次檔案完整路徑
        
        # 轉換星期
        day_map = {  # 星期對應字典
            "星期一": "MON", "星期二": "TUE", "星期三": "WED", "星期四": "THU",
            "星期五": "FRI", "星期六": "SAT", "星期日": "SUN"
        }
        
        day_en = day_map.get(self.schedule_day_dropdown.value, "MON")  # 取得對應的英文星期
        time_str = self.schedule_time_field.value  # 取得時間字串
        
        # 建立排程命令
        schtasks_cmd = [  # 排程命令清單
            "schtasks", "/create",  # 建立排程命令
            "/tn", task_name,  # 任務名稱
            "/tr", f'"{batch_file}"',  # 要執行的檔案
            "/sc", "weekly",  # 排程類型：每週
            "/d", day_en,  # 執行日期
            "/st", time_str,  # 執行時間
            "/f"  # 強制覆蓋現有排程
        ]
        
        result = subprocess.run(schtasks_cmd, capture_output=True, text=True)  # 執行排程命令
        if result.returncode != 0:  # 如果命令執行失敗
            raise Exception(f"建立排程失敗: {result.stderr}")  # 拋出異常
    
    def remove_schedule(self, e):
        """
        移除自動排程
        功能：從系統中移除已建立的排程任務
        參數：e - 事件物件
        """
        try:
            task_name = "CommunityScraperTask"  # 設定任務名稱
            
            # 移除 Windows 工作排程
            schtasks_cmd = ["schtasks", "/delete", "/tn", task_name, "/f"]  # 刪除排程命令
            result = subprocess.run(schtasks_cmd, capture_output=True, text=True)  # 執行刪除命令
            
            if result.returncode == 0 or "找不到系統中的指定工作" in result.stderr:  # 如果成功或任務不存在
                self.schedule_status_text.value = "排程狀態: 未設定"  # 更新排程狀態文字
                self.update_status("✅ 自動排程已移除")  # 更新狀態為成功
                self.show_success("自動排程已成功移除")  # 顯示成功訊息
            else:
                raise Exception(f"移除排程失敗: {result.stderr}")  # 拋出異常
                
        except Exception as e:  # 移除過程中的異常處理
            self.update_status(f"❌ 移除排程失敗: {e}")  # 更新錯誤狀態
            self.show_error(f"移除排程失敗: {e}")  # 顯示錯誤訊息
    

    def stop_background_process(self, e):
        """
        停止背景程序
        功能：強制終止正在執行的背景爬取程序
        參數：e - 事件物件
        """
        # 1. 檢查lock_file狀態
        lock_info = self.get_lock_file_info()  # 取得鎖定檔案資訊
        
        if not lock_info["exists"]:  # 如果鎖定檔案不存在
            self.show_dialog("錯誤", "當前未有爬取進行", is_error=True)  # 顯示沒有爬取進行錯誤
            return  # 結束函式執行
        
        lock_type = lock_info.get("type", "unknown")  # 取得鎖定類型
        
        if lock_type == "manual":  # 如果是手動爬取
            self.show_dialog("錯誤", "手動爬取進行中!", is_error=True)  # 顯示手動爬取錯誤
            return  # 結束函式執行
        
        # 2. 執行停止背景程序
        try:
            pid = lock_info.get("pid")  # 取得程序 ID
            if pid:  # 如果有程序 ID
                # 在 Windows 上終止程序
                subprocess.run(["taskkill", "/f", "/pid", str(pid)],  # 強制終止程序命令
                            capture_output=True)  # 捕獲輸出
            
            # 移除鎖定檔案
            self.remove_lock_file()  # 移除鎖定檔案
            
            # 更新狀態顯示 
            self.update_execution_status()  # 更新執行狀態顯示

            self.update_status("✅ 背景程序已停止")  # 更新狀態為成功
            self.show_dialog("提示", "背景程序已停止")  # 顯示停止提示
            
        except Exception as e:  # 停止過程中的異常處理
            self.update_status(f"❌ 停止背景程序失敗: {e}")  # 更新錯誤狀態
            self.show_dialog("錯誤", f"停止背景程序失敗: {e}", is_error=True)  # 顯示錯誤對話框


    def show_dialog(self, title: str, message: str, is_error: bool = False):
        """
        Flet 0.28.3 版本的正確對話框實現
        功能：顯示對話框給使用者查看重要訊息
        參數：title - 對話框標題，message - 對話框內容，is_error - 是否為錯誤訊息
        """
        if not self.page:  # 如果頁面物件不存在
            print("Page 是 None!")  # 輸出錯誤訊息
            return  # 結束函式執行
        
        def close_dlg(e):
            """關閉對話框"""
            try:
                dlg_modal.open = False  # 設定對話框為關閉狀態
                self.page.update()  # 更新頁面顯示
                print("對話框已關閉")  # 輸出關閉訊息
            except Exception as ex:  # 關閉過程中的異常處理
                print(f"關閉對話框錯誤: {ex}")  # 輸出錯誤訊息
        
        try:
            # 創建 AlertDialog（注意不要添加到 overlay）
            dlg_modal = ft.AlertDialog(  # 建立警告對話框
                modal=True,  # 設為模態對話框
                title=ft.Text(title, weight=ft.FontWeight.BOLD),  # 設定標題
                content=ft.Text(message, selectable=True),  # 設定內容，可選取文字
                actions=[  # 設定按鈕
                    ft.TextButton("確定", on_click=close_dlg)  # 確定按鈕
                ],
                actions_alignment=ft.MainAxisAlignment.END,  # 按鈕對齊方式
            )
            
            # 在 Flet 0.28.3 中，需要先添加到 page.overlay，然後設置 open=True
            self.page.overlay.append(dlg_modal)  # 添加到頁面覆蓋層
            dlg_modal.open = True  # 開啟對話框
            self.page.update()  # 更新頁面顯示
            
            print(f"AlertDialog 已顯示: {title}")  # 輸出顯示訊息
            
        except Exception as e:  # 顯示過程中的異常處理
            print(f"顯示 AlertDialog 錯誤: {e}")  # 輸出錯誤訊息
            import traceback  # 匯入追蹤模組
            traceback.print_exc()  # 輸出詳細錯誤追蹤
            
            # 使用備用的自製對話框
            self.show_custom_dialog(title, message, is_error)  # 呼叫備用對話框

    # 自製對話框（100% 可靠）
    '''
    def show_custom_dialog(self, title: str, message: str, is_error: bool = False):
        """自製對話框容器 - 100% 在 0.28.3 可用"""
        if not self.page:
            return
        
        def close_custom_dlg(e):
            """關閉自製對話框"""
            try:
                # 清除 overlay 中的對話框
                self.page.overlay.clear()
                self.page.update()
                print("自製對話框已關閉")
            except Exception as ex:
                print(f"關閉自製對話框錯誤: {ex}")
        
        try:
            # 清除現有 overlay
            self.page.overlay.clear()
            
            # 創建對話框內容
            dialog_content = ft.Container(
                content=ft.Column([
                    # 標題
                    ft.Text(
                        title, 
                        size=18, 
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.RED_700 if is_error else ft.Colors.BLUE_700
                    ),
                    ft.Container(height=15),
                    
                    # 內容
                    ft.Text(
                        message, 
                        size=14,
                        selectable=True,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Container(height=25),
                    
                    # 按鈕區域
                    ft.Row([
                        ft.ElevatedButton(
                            "確定", 
                            on_click=close_custom_dlg,
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.RED_600 if is_error else ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE,
                                elevation=2
                            ),
                            width=80,
                            height=35
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ], 
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(25),
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=15,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(0, 4)
                ),
                width=420,
                # 根據內容自動調整高度，但設定最小值
                height=max(180, len(message) // 25 * 20 + 150)
            )
            
            # 半透明背景容器
            backdrop = ft.Container(
                content=dialog_content,
                bgcolor=ft.Colors.BLACK54,  # 半透明黑色背景
                alignment=ft.alignment.center,
                expand=True,
                # 點擊背景也能關閉（可選）
                on_click=close_custom_dlg
            )
            
            # 添加到 overlay 並顯示
            self.page.overlay.append(backdrop)
            self.page.update()
            
            print(f"自製對話框已顯示: {title}")
            
        except Exception as e:
            print(f"自製對話框錯誤: {e}")
            import traceback
            traceback.print_exc()
            
            # 最終備用方案：SnackBar
            try:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"{title}: {message}"),
                    bgcolor=ft.Colors.RED_400 if is_error else ft.Colors.GREEN_400,
                    duration=5000
                )
                self.page.snack_bar.open = True
                self.page.update()
                print("使用 SnackBar 作為最終備用方案")
            except Exception as e2:
                print(f"連 SnackBar 都失敗: {e2}")
    '''

    # 測試自製對話框和簡易對話框
    '''
    def test_both_dialogs(self, e):
        """測試兩種對話框方法"""
        print("=== 測試 Flet 0.28.3 對話框 ===")
        
        # 先試 AlertDialog
        print("嘗試 AlertDialog...")
        try:
            self.show_dialog("AlertDialog 測試", "這是使用 ft.AlertDialog 的測試")
        except Exception as ex:
            print(f"AlertDialog 失敗: {ex}")
            
            # 改用自製對話框
            print("改用自製對話框...")
            self.show_custom_dialog("自製對話框測試", "AlertDialog 不行，這是自製的對話框")
    '''


    # 在任何按鈕的 on_click 中測試
    #測試onclick是否可執行對話框
    '''
    def test_dialog(self, e):
        """測試對話框 - 簡化版本"""
        print("test_dialog 被調用了!")
        
        try:
            if not self.page:
                print("self.page 是 None!")
                return
                
            print("開始建立對話框...")
            
            # 最簡單的對話框
            dlg = ft.AlertDialog(
                title=ft.Text("測試"),
                content=ft.Text("這是測試對話框")
            )
            
            print("對話框建立完成，開始顯示...")
            
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()
            
            print("對話框設定完成!")
            
        except Exception as ex:
            print(f"測試對話框發生錯誤: {ex}")
            import traceback
            traceback.print_exc() 
    '''

    
    # 在任何按鈕的 on_click 中測試
    #測試onclick是否可執行對話框
    '''
    def test_real_dialog(self, e):
        """測試對話框"""
        print("測試對話框被調用!")
        print(f"Flet 版本檢查...")
        print(f"Page 有 dialog 屬性: {hasattr(self.page, 'dialog')}")
        print(f"Page 有 overlay 屬性: {hasattr(self.page, 'overlay')}")
        
        self.show_dialog("測試標題", "這是用容器實現的對話框，應該可以正常顯示")
    '''


    def create_lock_file(self, execution_type: str = "manual"):
        """
        建立鎖定檔案，記錄執行類型
        功能：建立包含程序資訊的鎖定檔案
        參數：execution_type - 執行類型（"manual" 或 "background"）
        """
        try:
            lock_data = {  # 鎖定檔案資料字典
                "pid": os.getpid(),  # 當前程序 ID
                "type": execution_type,  # "manual" 或 "background"
                "start_time": datetime.now().isoformat()  # 開始時間
            }
            with self.lock_file.open('w', encoding='utf-8') as f:  # 開啟鎖定檔案進行寫入
                json.dump(lock_data, f, ensure_ascii=False, indent=2)  # 寫入 JSON 資料
        except Exception as e:  # 建立失敗時的異常處理
            self.logger.error(f"建立鎖定檔案失敗: {e}")  # 記錄錯誤

    def get_lock_file_info(self) -> dict:
        """
        取得鎖定檔案資訊
        功能：讀取並解析鎖定檔案內容
        返回：包含鎖定檔案資訊的字典
        """
        if not self.lock_file.exists():  # 如果鎖定檔案不存在
            return {"exists": False}  # 返回不存在標記
        
        try:
            with self.lock_file.open('r', encoding='utf-8') as f:  # 開啟鎖定檔案進行讀取
                lock_data = json.load(f)  # 載入 JSON 資料
            return {  # 返回鎖定檔案資訊
                "exists": True,  # 存在標記
                "type": lock_data.get("type", "unknown"),  # 執行類型
                "pid": lock_data.get("pid"),  # 程序 ID
                "start_time": lock_data.get("start_time")  # 開始時間
            }
        except Exception as e:  # 讀取失敗時的異常處理
            self.logger.error(f"讀取鎖定檔案失敗: {e}")  # 記錄錯誤
            # 如果是舊格式（只有PID），嘗試讀取
            try:
                with self.lock_file.open('r') as f:  # 開啟鎖定檔案（舊格式）
                    pid = int(f.read().strip())  # 讀取程序 ID
                return {  # 返回舊格式資訊
                    "exists": True,  # 存在標記
                    "type": "unknown",  # 未知類型
                    "pid": pid,  # 程序 ID
                    "start_time": None  # 無開始時間
                }
            except:  # 舊格式讀取也失敗
                return {"exists": False}  # 返回不存在標記

    def validate_scrape_settings(self) -> tuple[bool, str]:
        """
        驗證爬取設定，返回 (是否有效, 錯誤訊息)
        功能：檢查當前爬取設定是否完整有效
        返回：(是否有效的布林值, 錯誤訊息字串)
        """
        mode = self.scrape_mode_radio.value  # 取得爬取模式
        
        if mode == "single_city":  # 如果是單一城市模式
            if not self.city_dropdown.value:  # 如果未選擇城市
                return False, "未選擇城市!"  # 返回錯誤
        elif mode == "single_district":  # 如果是單一區域模式
            if not self.city_dropdown.value:  # 如果未選擇城市
                return False, "未選擇城市!"  # 返回錯誤
            if not self.district_dropdown.value:  # 如果未選擇區域
                return False, "未選擇區域!"  # 返回錯誤
        
        return True, ""  # 返回設定有效

    
    def update_execution_status(self):
        """
        更新執行狀態顯示
        功能：根據鎖定檔案狀態更新執行狀態文字和顏色
        """
        lock_info = self.get_lock_file_info()  # 取得鎖定檔案資訊
        
        if not lock_info["exists"]:  # 如果鎖定檔案不存在
            self.execution_status_text.value = "🟢 無執行程序"  # 設定狀態文字
            self.execution_status_text.color = ft.Colors.GREEN_700  # 設定綠色
        else:
            lock_type = lock_info.get("type", "unknown")  # 取得執行類型
            if lock_type == "manual":  # 如果是手動執行
                self.execution_status_text.value = "🔵 手動爬取中"  # 設定狀態文字
                self.execution_status_text.color = ft.Colors.BLUE_700  # 設定藍色
            elif lock_type == "background":  # 如果是背景執行
                self.execution_status_text.value = "🟡 背景爬取中"  # 設定狀態文字
                self.execution_status_text.color = ft.Colors.ORANGE_700  # 設定橘色
            else:
                self.execution_status_text.value = "🔴 未知程序執行中"  # 設定狀態文字
                self.execution_status_text.color = ft.Colors.RED_700  # 設定紅色
        # 在UI中顯示狀態


    def build_ui(self, page: ft.Page):
        """
        建立使用者介面
        功能：建立完整的使用者介面佈局和元件
        參數：page - Flet 頁面物件
        """
        self.page = page  # 設定頁面物件
        
        # 設定頁面屬性
        page.title = "社區資料爬蟲"  # 設定視窗標題
        page.theme_mode = ft.ThemeMode.SYSTEM  # 設定主題模式為系統預設
        page.window.width = 550   # 調整為更合適的寬度
        page.window.height = 700  # 調整高度
        page.window.resizable = True  # 允許調整視窗大小
        page.window.min_width = 300  # 設定最小寬度
        page.window.min_height = 650  # 設定最小高度
        
        # 設定主題
        page.theme = ft.Theme(  # 建立主題物件
            color_scheme_seed=ft.Colors.BLUE,  # 設定主色調為藍色
            use_material3=True  # 使用 Material 3 設計
        )
        
        # 建立分頁介面
        tabs = ft.Tabs(  # 建立分頁容器
            selected_index=0,  # 預設選擇第一個分頁
            animation_duration=300,  # 切換動畫時間
            tab_alignment=ft.TabAlignment.CENTER,  # 分頁置中
            tabs=[  # 分頁清單
                ft.Tab(  # 爬取設定分頁
                    text="爬取設定",  # 分頁文字
                    icon=ft.Icons.SETTINGS,  # 分頁圖示
                    content=self._build_scraping_tab()  # 分頁內容
                ),
                ft.Tab(  # 自動排程分頁
                    text="自動排程",  # 分頁文字
                    icon=ft.Icons.SCHEDULE,  # 分頁圖示
                    content=self._build_schedule_tab()  # 分頁內容
                ),
                ft.Tab(  # 執行狀態分頁
                    text="執行狀態",  # 分頁文字
                    icon=ft.Icons.MONITOR,  # 分頁圖示
                    content=self._build_status_tab()  # 分頁內容
                ),
                ft.Tab(  # 資料結構分頁
                    text="資料結構",  # 分頁文字
                    icon=ft.Icons.FOLDER,  # 分頁圖示
                    content=self._build_data_structure_tab()  # 分頁內容
                ),
                ft.Tab(  # 新增的操作說明分頁
                    text="操作說明",  # 分頁文字
                    icon=ft.Icons.HELP,  # 分頁圖示
                    content=self._build_help_tab()  # 分頁內容
                )
            ]
        )
        
        # 主佈局 - 置中設計
        main_container = ft.Container(  # 建立主容器
            content=ft.Column([  # 建立垂直佈局
                # 標題區域
                ft.Container(  # 標題容器
                    content=ft.Column([  # 標題垂直佈局
                        # 主標題
                        ft.Row([  # 標題水平佈局
                            ft.Icon(ft.Icons.BUSINESS, size=35, color=ft.Colors.BLUE),  # 圖示
                            ft.Container(width=8),  # 間距
                            ft.Text(  # 標題文字
                                "社區資料爬蟲管理系統",  # 標題內容
                                size=22,  # 字體大小
                                weight=ft.FontWeight.BOLD,  # 字體粗細
                                color=ft.Colors.BLUE_800  # 字體顏色
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER),  # 置中對齊
                        
                        # 執行狀態顯示
                        ft.Container(height=4),  # 間距
                        ft.Container(  # 狀態容器
                            content=self.execution_status_text,  # 執行狀態文字
                            alignment=ft.alignment.center  # 置中對齊
                        )
                    ]),
                    margin=ft.margin.only(bottom=20),  # 底部邊距
                    padding=ft.padding.symmetric(vertical=8)  # 垂直內距
                ),
                
                # 分頁內容 - 置中容器
                ft.Container(  # 分頁容器
                    content=tabs,  # 分頁內容
                    expand=True,  # 擴展填滿可用空間
                    alignment=ft.alignment.center,  # 置中對齊
                    width=None  # 自動寬度
                )
            ]), 
            padding=ft.padding.symmetric(horizontal=30, vertical=20),  # 左右較大邊距
            expand=True,  # 擴展填滿可用空間
            alignment=ft.alignment.center  # 整體置中
        )
        
        page.add(main_container)  # 將主容器添加到頁面
        
        # 初始化完成後載入城市資料
        threading.Thread(target=self.load_cities_data, daemon=True).start()  # 在背景執行緒載入城市資料
        
        # 根據當前模式設定 dropdown 狀態
        self.update_dropdown_states()  # 更新下拉選單狀態

        # 初始化狀態顯示
        self.update_execution_status()  # 更新執行狀態顯示
    

    def update_dropdown_states(self):
        """
        根據當前爬取模式更新 dropdown 狀態
        功能：根據選擇的爬取模式啟用或禁用相關的下拉選單
        """
        mode = self.scrape_mode_radio.value  # 取得當前爬取模式
        
        if mode == "all_cities":  # 如果是全部城市模式
            self.city_dropdown.disabled = True  # 禁用城市選擇
            self.district_dropdown.disabled = True  # 禁用區域選擇
            self.city_dropdown.value = None  # 清空城市選擇
            self.district_dropdown.value = None  # 清空區域選擇
            self.district_dropdown.options.clear()  # 清空區域選項
            
        elif mode == "single_city":  # 如果是單一城市模式
            self.city_dropdown.disabled = False  # 啟用城市選擇
            self.district_dropdown.disabled = True  # 禁用區域選擇
            self.district_dropdown.value = None  # 清空區域選擇
            self.district_dropdown.options.clear()  # 清空區域選項
            
        elif mode == "single_district":  # 如果是單一區域模式
            self.city_dropdown.disabled = False  # 啟用城市選擇
            self.district_dropdown.disabled = False  # 啟用區域選擇
            
        if self.page:  # 檢查頁面物件是否存在
            self.page.update()  # 更新頁面顯示


    def _build_scraping_tab(self) -> ft.Container:
        """
        建立爬取設定分頁
        功能：建立包含爬取設定的分頁內容
        返回：包含爬取設定的容器
        """
        return ft.Container(  # 返回分頁容器
            content=ft.Column([  # 建立垂直佈局
                # 輸出資料夾設定
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            #ft.Text("輸出設定", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(height=8),  # 間距
                            ft.Row([  # 輸出資料夾水平佈局
                                ft.Container(  # 文字框容器
                                    height=50,          # 在 Container 設定高度
                                    width=200,          # 設定寬度
                                    content=self.output_folder_text,  # 輸出資料夾文字框
                                    expand=True  # 擴展填滿空間
                                ),
                                ft.Container(width=8),  # 間距
                                ft.ElevatedButton(  # 瀏覽按鈕
                                    "瀏覽",  # 按鈕文字
                                    icon=ft.Icons.FOLDER_OPEN,  # 按鈕圖示
                                    on_click=self.choose_output_folder  # 點擊事件
                                )
                            ])
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 爬取模式設定
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            #ft.Text("爬取模式", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(height=1),  # 間距
                            # 選項排列更緊湊
                            ft.Container(  # 單選按鈕容器
                                content=self.scrape_mode_radio,  # 爬取模式單選按鈕
                                padding=ft.padding.only(left=8)  # 左側內距
                            ),
                            ft.Container(height=1),  # 間距
                            # 城市和區域選擇
                            # 改為置中版本：
                            ft.Row([  # 下拉選單水平佈局
                                ft.Container(  # 城市選擇容器
                                    height=50,          # 在 Container 設定高度
                                    width=200,          # 設定寬度
                                    content=self.city_dropdown,  # 城市下拉選單
                                    expand=True,  # 擴展填滿空間
                                    alignment=ft.alignment.center  # 加入這行置中對齊
                                ),
                                ft.Container(width=12),  # 間距
                                ft.Container(  # 區域選擇容器
                                    height=50,          # 在 Container 設定高度
                                    width=200,          # 設定寬度
                                    content=self.district_dropdown,  # 區域下拉選單
                                    expand=True,  # 擴展填滿空間
                                    alignment=ft.alignment.center  # 加入這行置中對齊
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER)  # 整個 Row 也置中
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 控制按鈕
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            #ft.Text("操作控制", size=16, weight=ft.FontWeight.BOLD),
                            ft.Container(height=8),  # 間距
                            ft.Row([  # 按鈕水平佈局
                                self.start_button,  # 開始按鈕
                                ft.Container(width=8),  # 間距
                                self.stop_button,  # 停止按鈕
                                ft.Container(width=8),  # 間距
                                ft.ElevatedButton(  # 儲存設定按鈕
                                    "儲存設定",  # 按鈕文字
                                    icon=ft.Icons.SAVE,  # 按鈕圖示
                                    on_click=lambda e: self.save_config()  # 點擊事件
                                )
                            ], alignment=ft.MainAxisAlignment.CENTER),  # 置中對齊
                            ft.Container(height=12),  # 間距
                            # 進度顯示
                            ft.Column([  # 進度顯示垂直佈局
                                ft.Container(  # 進度條容器
                                    content=self.progress_bar,  # 進度條
                                    alignment=ft.alignment.center  # 置中對齊
                                ),
                                ft.Container(height=4),  # 間距
                                ft.Container(  # 進度文字容器
                                    content=self.progress_text,  # 進度文字
                                    alignment=ft.alignment.center  # 置中對齊
                                )
                            ], visible=False)  # 初始隱藏
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 底部空間
                ft.Container(height=16)  # 底部間距
            ], 
            scroll=ft.ScrollMode.AUTO,  # 啟用捲動
            spacing=0,  # 元件間距
            alignment=ft.MainAxisAlignment.START,  # 垂直對齊方式
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平置中
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),  # 容器內距
            expand=True,  # 擴展填滿空間
            alignment=ft.alignment.top_center  # 內容靠上置中
        )
    
    def _build_schedule_tab(self) -> ft.Container:
        """
        建立自動排程分頁
        功能：建立包含自動排程設定的分頁內容
        返回：包含自動排程設定的容器
        """
        return ft.Container(  # 返回分頁容器
            content=ft.Column([  # 建立垂直佈局
                # 輸出資料夾設定 - 新增的區域
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Text("輸出設定", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                            ft.Container(height=8),  # 間距
                            ft.Row([  # 輸出資料夾水平佈局
                                ft.Container(  # 文字框容器
                                    height=50,  # 高度設定
                                    content=self.output_folder_text,  # 輸出資料夾文字框
                                    expand=True  # 擴展填滿空間
                                ),
                                ft.Container(width=8),  # 間距
                                ft.ElevatedButton(  # 瀏覽按鈕
                                    "瀏覽",  # 按鈕文字
                                    icon=ft.Icons.FOLDER_OPEN,  # 按鈕圖示
                                    on_click=self.choose_output_folder  # 點擊事件
                                )
                            ])
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),  

                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            # 標題和狀態在同一行 - 左右分佈
                            ft.Row([  # 標題列水平佈局
                                ft.Text("自動排程設定", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                               
                                # 排程狀態
                                ft.Container(  # 狀態容器
                                    content=self.schedule_status_text,  # 排程狀態文字
                                    padding=ft.padding.all(8),  # 內距
                                    bgcolor=ft.Colors.GREEN_50,  # 背景顏色
                                    border_radius=6,  # 圓角
                                    alignment=ft.alignment.center  # 置中對齊
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),  # 左右分佈對齊
            
                            ft.Container(height=8),  # 間距
                            
                            ft.Row([  # 排程設定水平佈局
                                #ft.Container(width=8),
                                ft.Container(  # 排程日期容器
                                    content=self.schedule_day_dropdown,  # 排程日期下拉選單
                                    expand=1  # 按比例擴展
                                ),
                                ft.Container(width=12),  # 間距
                                ft.Container(  # 排程時間容器

                                    content=self.schedule_time_field,  # 排程時間輸入框
                                    expand=1  # 按比例擴展
                                )
                            ]),
                            
                            
                            # 控制按鈕
                            ft.Text("排程控制", size=14, weight=ft.FontWeight.BOLD),  # 控制按鈕標題
                            ft.Container(height=8),  # 間距
                            ft.Row([  # 控制按鈕水平佈局
                                self.set_schedule_button,  # 設定排程按鈕
                                ft.Container(width=8),  # 間距
                                self.remove_schedule_button,  # 移除排程按鈕
                                ft.Container(width=8),  # 間距
                                self.stop_background_button  # 停止背景程序按鈕
                            ], alignment=ft.MainAxisAlignment.CENTER)  # 置中對齊
                            
                            
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                 
                
                # 底部空間
                ft.Container(height=16)  # 底部間距
            ], 
            scroll=ft.ScrollMode.AUTO,  # 啟用捲動
            spacing=0,  # 元件間距
            alignment=ft.MainAxisAlignment.START,  # 垂直對齊方式
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平置中
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),  # 容器內距
            expand=True,  # 擴展填滿空間
            alignment=ft.alignment.top_center  # 內容靠上置中
        )
    
    def _build_status_tab(self) -> ft.Container:
        """
        建立執行狀態分頁
        功能：建立包含執行狀態和日誌顯示的分頁內容
        返回：包含執行狀態的容器
        """
        return ft.Container(  # 返回分頁容器
            content=ft.Column([  # 建立垂直佈局
                # 狀態顯示
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            
                            #ft.Text("執行狀態", size=16, weight=ft.FontWeight.BOLD),
                            #ft.Container(height=8),
                
                            # 當前狀態
                            ft.Container(  # 狀態容器
                                content=ft.Column([  # 狀態垂直佈局
                                    #ft.Text("目前狀態", size=13, weight=ft.FontWeight.BOLD),
                                    ft.Container(height=2),  # 間距
                                    self.status_text  # 狀態文字
                                ]),
                                padding=ft.padding.all(8),  # 內距
                                bgcolor=ft.Colors.GREEN_50,  # 背景顏色
                                border_radius=6,  # 圓角
                                margin=ft.margin.only(bottom=8)  # 底部邊距
                            ),
                            
                            # 統計資訊
                            ft.Container(  # 統計資訊容器
                                content=ft.Column([  # 統計資訊垂直佈局
                                    ft.Text("統計資訊", size=13, weight=ft.FontWeight.BOLD),  # 統計資訊標題
                                    ft.Container(height=4),  # 間距
                                    self.stats_text  # 統計資訊文字
                                ]),
                                padding=ft.padding.all(8),  # 內距
                                bgcolor=ft.Colors.BLUE_50,  # 背景顏色
                                border_radius=6  # 圓角
                            )
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 日誌顯示
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Row([  # 日誌標題列水平佈局
                                ft.Text("執行日誌", size=13, weight=ft.FontWeight.BOLD),  # 日誌標題
                                ft.ElevatedButton(  # 清除日誌按鈕
                                    "清除日誌",  # 按鈕文字
                                    icon=ft.Icons.CLEAR,  # 按鈕圖示
                                    on_click=lambda e: setattr(self.log_text, 'value', '') or self.page.update()  # 清除日誌的點擊事件
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),  # 左右分佈對齊
                            
                            ft.Container(height=8),  # 間距
                            
                            # 日誌內容區域
                            ft.Container(  # 日誌內容容器
                                content=self.log_text,  # 日誌文字框
                                height=280,  # 調整為適中的高度
                                border_radius=6,  # 圓角
                                bgcolor=ft.Colors.GREY_50,  # 背景顏色
                                padding=ft.padding.all(4)  # 內距
                            )
                        ]),
                        padding=16  # 內距
                    ),

                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 底部空間
                ft.Container(height=16)  # 底部間距
            ], 
            scroll=ft.ScrollMode.AUTO,  # 啟用捲動
            spacing=0,  # 元件間距
            alignment=ft.MainAxisAlignment.START,  # 垂直對齊方式
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平置中
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),  # 容器內距
            expand=True,  # 擴展填滿空間
            alignment=ft.alignment.top_center  # 內容靠上置中
        )


    def _build_help_tab(self) -> ft.Container:
        """
        建立操作提示分頁
        功能：建立包含操作說明和使用指南的分頁內容
        返回：包含操作說明的容器
        """
        return ft.Container(  # 返回分頁容器
            content=ft.Column([  # 建立垂直佈局
                # 基本操作說明
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Text("基本操作說明", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                            ft.Container(height=12),  # 間距
                            
                            ft.Text("🚀 爬取操作", size=14, weight=ft.FontWeight.BOLD),  # 爬取操作標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 爬取操作說明文字
                                "• 選擇爬取模式：全部城市、單一城市或單一區域\n"
                                "• 設定輸出資料夾路徑\n"
                                "• 點擊「開始爬取」按鈕執行\n"
                                "• 可隨時點擊「停止爬取」中斷程序",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),
                            
                            ft.Container(height=12),  # 間距
                            ft.Text("📅 自動排程", size=14, weight=ft.FontWeight.BOLD),  # 自動排程標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 自動排程說明文字
                                "• 設定執行的星期和時間\n"
                                "• 點擊設定排程，排程會在指定時間自動執行全部城市爬取\n"
                                "• 排程執行時在背景進行，不顯示GUI界面\n"
                                "• 執行結果記錄在 logs/background.log 檔案\n"
                                "• 可透過「停止背景程序」中止執行中的排程",                               
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),
                            
                            ft.Container(height=12),  # 間距
                            ft.Text("📊 執行狀態", size=14, weight=ft.FontWeight.BOLD),  # 執行狀態標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 執行狀態說明文字
                                "• 執行日誌會即時顯示爬取進度和狀態\n"
                                "• 統計資訊會在爬取完成後顯示詳細結果\n"
                                "• 可使用「清除日誌」按鈕清空日誌內容\n"
                                "• 所有執行記錄同時儲存到 logs/app.log 檔案",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            )
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 檔案說明
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Text("檔案與資料說明", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                            ft.Container(height=12),  # 間距
                            
                            ft.Text("📁 輸出檔案", size=14, weight=ft.FontWeight.BOLD),  # 輸出檔案標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 輸出檔案說明文字
                                "• 社區資料檔案：包含社區名稱、電話、地址\n"
                                "• 更新日誌：記錄每次新增的資料變化\n"
                                "• 備份檔案：自動備份舊版本資料\n"
                                "• 檔案命名包含日期和筆數統計",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),
                            
                            ft.Container(height=12),  # 間距
                            ft.Text("🔧 系統檔案", size=14, weight=ft.FontWeight.BOLD),  # 系統檔案標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 系統檔案說明文字
                                "• config.json：應用程式設定檔\n"
                                "• scraper.lock：防止重複執行的鎖定檔\n"
                                "• logs/：存放所有執行日誌\n"
                                "• scraper_background.bat：背景執行批次檔",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),
                                                        
                            ft.Container(height=12),  # 間距
                            ft.Text("📊 檔案命名規則", size=14, weight=ft.FontWeight.BOLD),  # 檔案命名規則標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 檔案命名規則說明文字
                                "• 城市資料夾：城市名(筆數)_年_月_日\n"
                                "• 社區檔案：城市區域社區資料(筆數)_年_月_日.txt\n"
                                "• 更新日誌：年-月-日資料更新日誌.txt",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),        
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 常見問題
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Text("常見問題與解決方案", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                            ft.Container(height=12),  # 間距
                            
                            ft.Text("❓ 常見問題", size=14, weight=ft.FontWeight.BOLD),  # 常見問題標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 常見問題說明文字
                                "• 無法開始爬取：檢查網路連線和城市資料是否載入\n"
                                "• 爬取中斷：查看日誌了解具體錯誤原因\n"
                                "• 排程無法設定：確認系統權限和時間格式\n"
                                "• 程序卡住：使用「停止背景程序」強制結束",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            ),
                            
                            ft.Container(height=12),  # 間距
                            ft.Text("💡 使用技巧", size=14, weight=ft.FontWeight.BOLD),  # 使用技巧標題
                            ft.Container(height=6),  # 間距
                            ft.Text(  # 使用技巧說明文字
                                "• 建議在網路穩定時進行爬取\n"
                                "• 大量資料爬取建議在非工作時間執行\n"
                                "• 定期備份重要的爬取結果\n"
                                "• 關注日誌訊息以了解執行狀況",
                                size=12,  # 字體大小
                                color=ft.Colors.GREY_700  # 字體顏色
                            )
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 底部空間
                ft.Container(height=16)  # 底部間距
            ], 
            scroll=ft.ScrollMode.AUTO,  # 啟用捲動
            spacing=0,  # 元件間距
            alignment=ft.MainAxisAlignment.START,  # 垂直對齊方式
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平置中
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),  # 容器內距
            expand=True,  # 擴展填滿空間
            alignment=ft.alignment.top_center  # 內容靠上置中
        )


    def _build_data_structure_tab(self) -> ft.Container:
        """
        建立資料結構分頁
        功能：建立包含檔案結構說明的分頁內容
        返回：包含資料結構說明的容器
        """
        structure_text = """
📂 檔案結構說明

爬蟲資料/
├── 台北市(4776筆資料)_2025_07_14/
│   ├── 台北市中正區社區資料(共有776筆)_2025_07_14.txt
│   ├── 台北市大安區社區資料(共有850筆)_2025_07_14.txt
│   └── ...
├── 新北市(2000筆資料)_2025_07_14/
│   ├── 新北市板橋區社區資料(共有300筆)_2025_07_14.txt
│   ├── 新北市中和區社區資料(共有250筆)_2025_07_14.txt
│   └── ...
├── 備份檔案/
│   ├── 台北市(4775筆資料)_2025_07_13/
│   ├── 新北市(1999筆資料)_2025_07_13/
│   └── ...
├── 資料更新日誌/
│   ├── 2025-07-13資料更新日誌.txt
│   ├── 2025-07-14資料更新日誌.txt
│   └── ...
└── logs/
    ├── app.log
    └── background.log

📄 檔案內容格式

社區資料檔案內容：
社區名稱1
電話: 02-12345678
地址: 台北市中正區xxx路123號

社區名稱2
電話: 02-87654321
地址: 台北市中正區yyy路456號

============================================================
📊 資料更新日誌 - 2025-07-14 10:30:00
============================================================
📁 檔案: 台北市中正區社區資料(共有776筆)_2025_07_14.txt
🆕 新增項目數量: 2
----------------------------------------
+ 新社區名稱1
  📞 電話: 02-11111111
  📍 地址: 台北市中正區新地址1

+ 新社區名稱2
  📞 電話: 02-22222222
  📍 地址: 台北市中正區新地址2

📈 總計新增項目: 2 筆
============================================================

🔧 系統檔案

config.json - 應用程式設定檔
scraper.lock - 程序鎖定檔案（避免重複執行）
scraper_background.bat - 背景執行批次檔
        """  # 資料結構說明文字內容
        
        return ft.Container(  # 返回分頁容器
            content=ft.Column([  # 建立垂直佈局
                # 檔案結構說明
                ft.Card(  # 建立卡片容器
                    content=ft.Container(  # 卡片內容容器
                        content=ft.Column([  # 卡片內容垂直佈局
                            ft.Text("資料結構與檔案說明", size=16, weight=ft.FontWeight.BOLD),  # 標題文字
                            ft.Container(height=10),  # 間距
                            
                            # 文件顯示區域
                            ft.Container(  # 文件顯示容器
                                content=ft.TextField(  # 文件顯示文字框
                                    value=structure_text,  # 設定文字內容
                                    multiline=True,  # 多行模式
                                    max_lines=22,  # 最大行數
                                    read_only=True,  # 設為唯讀
                                    text_style=ft.TextStyle(font_family="Consolas"),  # 等寬字體
                                    width=None,  # 自動寬度
                                    height=320,  # 調整為適中的高度
                                    border_color=ft.Colors.BLUE_200,  # 邊框顏色
                                    focused_border_color=ft.Colors.BLUE_400,  # 焦點時的邊框顏色
                                ),
                                padding=ft.padding.all(6),  # 內距
                                bgcolor=ft.Colors.GREY_50,  # 背景顏色
                                border_radius=6  # 圓角
                            )
                        ]),
                        padding=16  # 內距
                    ),
                    margin=ft.margin.only(bottom=12)  # 底部邊距
                ),
                
                # 底部空間
                ft.Container(height=16)  # 底部間距
            ], 
            scroll=ft.ScrollMode.AUTO,  # 啟用捲動
            spacing=0,  # 元件間距
            alignment=ft.MainAxisAlignment.START,  # 垂直對齊方式
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # 水平置中
            ),
            padding=ft.padding.symmetric(horizontal=16, vertical=8),  # 容器內距
            expand=True,  # 擴展填滿空間
            alignment=ft.alignment.top_center  # 內容靠上置中
        )


def run_background_scraper():
    """
    背景模式執行
    功能：在背景模式下執行爬蟲作業，不顯示 GUI 界面
    """
    print("開始背景爬取作業...")  # 輸出開始訊息
    
    # 檢查鎖定檔案
    lock_file = Path("scraper.lock")  # 建立鎖定檔案路徑
    if lock_file.exists():  # 如果鎖定檔案存在
        print("偵測到其他程序正在執行，退出")  # 輸出衝突訊息
        return  # 結束函式執行
    
    try:
        # 建立背景執行的鎖定檔案
        lock_data = {  # 鎖定檔案資料字典
            "pid": os.getpid(),  # 當前程序 ID
            "type": "background",  # 背景執行類型
            "start_time": datetime.now().isoformat()  # 開始時間
        }
        with lock_file.open('w', encoding='utf-8') as f:  # 開啟鎖定檔案進行寫入
            json.dump(lock_data, f, ensure_ascii=False, indent=2)  # 寫入 JSON 資料

        # 建立鎖定檔案
        with lock_file.open('w') as f:  # 開啟鎖定檔案（簡化版本）
            f.write(str(os.getpid()))  # 寫入程序 ID
        
        # 載入設定
        config_file = Path("config.json")  # 建立設定檔路徑
        if config_file.exists():  # 如果設定檔存在
            with config_file.open('r', encoding='utf-8') as f:  # 開啟設定檔進行讀取
                config = json.load(f)  # 載入 JSON 設定
        else:
            config = {"output_folder": str(Path.cwd() / "爬蟲資料")}  # 使用預設設定
        
        # 設定背景日誌
        log_folder = Path("logs")  # 建立日誌資料夾路徑
        log_folder.mkdir(exist_ok=True)  # 建立資料夾，如果已存在則不報錯
        
        logging.basicConfig(  # 設定背景日誌配置
            level=logging.INFO,  # 設定日誌等級為 INFO
            format='%(asctime)s - %(levelname)s - %(message)s',  # 日誌格式
            handlers=[  # 日誌處理器清單
                logging.FileHandler(log_folder / "background.log", encoding='utf-8'),  # 背景日誌檔案處理器
                logging.StreamHandler()  # 控制台處理器
            ]
        )
        
        logger = logging.getLogger(__name__)  # 取得當前模組的日誌記錄器
        logger.info("開始背景爬取作業")  # 記錄開始訊息
        
        # 建立爬蟲實例
        scraper = CommunityDataScraper(  # 建立爬蟲實例
            status_callback=lambda msg: logger.info(msg),  # 設定狀態回調函式
            output_folder=config["output_folder"],  # 設定輸出資料夾
            auto_cleanup=True,  # 啟用自動清理
            enable_backup=True  # 啟用備份功能
        )
        
        # 載入城市資料
        cities_data = scraper.get_city_data()  # 取得城市資料
        if not cities_data:  # 如果無法載入城市資料
            logger.error("無法載入城市資料")  # 記錄錯誤
            return  # 結束函式執行
        
        # 執行全部城市爬取
        success = scraper.scrape_all_cities_with_districts(cities_data)  # 爬取全部城市
        
        if success:  # 如果爬取成功
            stats = scraper.get_scrape_statistics()  # 取得爬取統計資訊
            logger.info(f"背景爬取完成: 處理 {stats.get('processed_files', 0)} 個檔案，"  # 記錄完成訊息
                       f"新增 {stats.get('new_communities', 0)} 筆資料")
        else:
            logger.error("背景爬取失敗")  # 記錄失敗訊息
            
    except Exception as e:  # 背景執行過程中的異常處理
        logging.error(f"背景執行錯誤: {e}", exc_info=True)  # 記錄詳細錯誤
    finally:
        # 移除鎖定檔案
        if lock_file.exists():  # 如果鎖定檔案存在
            lock_file.unlink()  # 刪除檔案


if __name__ == "__main__":
    def main(page: ft.Page):
        """
        獨立執行時的入口
        功能：當程式被直接執行時的主要入口函式
        參數：page - Flet 頁面物件
        """
        app = CommunityScraperApp()  # 建立應用程式實例
        app.build_ui(page)  # 建立使用者介面
    
    ft.app(target=main, assets_dir="assets")  # 啟動 Flet 應用程式