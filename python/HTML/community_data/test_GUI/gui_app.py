#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Community Data Scraper GUI Application
增強版社區資料爬蟲 GUI 應用程式 - 使用統一錯誤處理模組
"""

# ============================================================================
# 匯入必要的函式庫
# ============================================================================
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
from scraper import CommunityDataScraper
from typing import Dict, List, Optional
import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# 匯入自定義錯誤處理模組
from error_handler import (
    ErrorHandler, ErrorContext, handle_errors, 
    log_error, log_info, log_warning, log_success,
    setup_global_error_handler
)


class SimpleScraperGUI:
    """
    增強版社區爬蟲GUI應用程式類別
    
    主要功能：
    1. 提供友善的圖形介面操作爬蟲
    2. 支援手動爬取和自動排程
    3. 可選擇不同的爬取範圍（全部城市/單一城市/單一區域）
    4. 整合Windows工作排程器進行背景執行
    5. Lock檔案狀態檢查和顯示
    6. 統一的錯誤處理和日誌記錄
    """
    
    def __init__(self, root):
        """
        初始化GUI應用程式
        
        Args:
            root: tkinter主視窗物件
        """
        # ====================================================================
        # 設定錯誤處理器
        # ====================================================================
        self.error_handler = setup_global_error_handler(
            app_name="CommunityScraperGUI",
            enable_console=True,
            enable_file=True,
            enable_gui=True
        )
        
        # ====================================================================
        # 主視窗設定
        # ====================================================================
        self.root = root
        self.root.title("🏘️ 社區資料爬蟲")
        self.root.geometry("800x750")
        self.root.resizable(True, True)
        
        # ====================================================================
        # 核心變數初始化
        # ====================================================================
        self.scraper = None
        self.cities_data = []
        self.selected_city_data = None
        self.scraping_thread = None
        
        # ====================================================================
        # Lock 檔案相關設定
        # ====================================================================
        self.lock_file_path = self.get_lock_file_path()
        
        # ====================================================================
        # 初始化GUI控制變數
        # ====================================================================
        self.output_folder = tk.StringVar(value=os.getcwd())
        
        # 排程相關設定變數
        self.schedule_enabled = tk.BooleanVar(value=False)
        self.schedule_day = tk.StringVar(value="星期一")
        self.schedule_time = tk.StringVar(value="02:00")
        self.schedule_output_folder = tk.StringVar(
            value=os.path.join(os.getcwd(), "爬蟲資料")
        )
        self.schedule_scrape_mode = tk.StringVar(value="all_cities")
        
        # ====================================================================
        # 初始化程序（使用錯誤處理）
        # ====================================================================
        with ErrorContext(self.error_handler, "初始化GUI應用程式"):
            self.create_widgets()
            self.load_config()
            self.load_cities_data()
            self.start_lock_status_checker()
        
        log_info("GUI應用程式初始化完成")

    def get_lock_file_path(self):
        """取得 Lock 檔案的路徑"""
        try:
            if getattr(sys, 'frozen', False):
                program_dir = os.path.dirname(sys.executable)
            else:
                program_dir = os.path.dirname(__file__)
                
            return os.path.join(program_dir, "scraper_running.lock")
        except Exception as e:
            log_error(e, "取得Lock檔案路徑")
            return "scraper_running.lock"  # 回退到預設值

    @handle_errors("檢查Lock檔案狀態", show_gui=False)
    def check_lock_file_status(self):
        """檢查 Lock 檔案狀態"""
        if os.path.exists(self.lock_file_path):
            mtime = os.path.getmtime(self.lock_file_path)
            create_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            try:
                with open(self.lock_file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
            except Exception as e:
                log_warning(f"無法讀取Lock檔案內容: {e}", "檢查Lock檔案狀態")
                content = "無法讀取檔案內容"
            
            return True, create_time, content
        else:
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
            log_error(e, "更新Lock狀態顯示")
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
            log_error(e, "檢查Lock檔案", user_message="檢查Lock檔案時發生錯誤，將繼續執行")
            return True
    
    def create_widgets(self):
        """建立主要的GUI元件結構"""
        # ====================================================================
        # 主框架設定
        # ====================================================================
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ====================================================================
        # 分頁容器建立
        # ====================================================================
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # ====================================================================
        # 建立各個分頁
        # ====================================================================
        # 爬取設定分頁
        scrape_frame = ttk.Frame(notebook, padding="10")
        notebook.add(scrape_frame, text="爬取設定")
        self.create_scrape_tab(scrape_frame)
        
        # 自動排程分頁
        schedule_frame = ttk.Frame(notebook, padding="10")
        notebook.add(schedule_frame, text="自動排程")
        
        # 上下滾動設定
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
        """建立爬取設定分頁的所有元件"""
        # ====================================================================
        # 輸出資料夾設定區域
        # ====================================================================
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
        
        # ====================================================================
        # 城市選擇區域
        # ====================================================================
        ttk.Label(parent, text="選擇城市：").pack(anchor=tk.W, pady=(15, 5))
        self.city_combo = ttk.Combobox(parent, state="readonly")
        self.city_combo.pack(fill=tk.X, pady=5)
        self.city_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        # ====================================================================
        # 區域選擇區域
        # ====================================================================
        ttk.Label(parent, text="選擇區域：").pack(anchor=tk.W, pady=(15, 5))
        self.district_combo = ttk.Combobox(parent, state="readonly")
        self.district_combo.pack(fill=tk.X, pady=5)
        
        # ====================================================================
        # 爬取選項設定
        # ====================================================================
        options_frame = ttk.LabelFrame(parent, text="手動爬取選項", padding="10")
        options_frame.pack(fill=tk.X, pady=15)
        
        self.scrape_option = tk.StringVar(value="all_cities")
        
        ttk.Radiobutton(
            options_frame, 
            text="爬取全部城市(資料分區)", 
            variable=self.scrape_option, 
            value="all_cities"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            options_frame, 
            text="爬取單一城市(資料分區)", 
            variable=self.scrape_option, 
            value="single_city"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            options_frame, 
            text="爬取單一區域", 
            variable=self.scrape_option, 
            value="single_district"
        ).pack(anchor=tk.W, pady=2)

        # ====================================================================
        # 底部控制按鈕區域
        # ====================================================================
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.TOP, pady=(10,0))
        
        # 開始爬取按鈕
        self.start_button = ttk.Button(
            button_frame, 
            text="開始爬取", 
            command=self.start_scraping
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # 停止爬取按鈕
        self.stop_button = ttk.Button(
            button_frame, 
            text="停止爬取", 
            command=self.stop_scraping, 
            state="disabled"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存設定按鈕
        self.save_button = ttk.Button(
            button_frame, 
            text="儲存設定", 
            command=self.save_config
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # 進度顯示區域
        # ====================================================================
        ttk.Label(parent, text="進度：").pack(anchor=tk.W, pady=5)
        self.progress = ttk.Progressbar(parent, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # ====================================================================
        # 狀態顯示區域
        # ====================================================================
        ttk.Label(parent, text="狀態：").pack(anchor=tk.W, pady=5)
        self.status_text = scrolledtext.ScrolledText(parent, height=10)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def create_schedule_tab(self, parent):
        """建立自動排程分頁的所有元件"""
        # ====================================================================
        # Lock 檔案狀態顯示區域
        # ====================================================================
        lock_frame = ttk.LabelFrame(parent, text="爬蟲狀態檢查", padding="10")
        lock_frame.pack(fill=tk.X, pady=10)
        
        self.lock_status_label = ttk.Label(
            lock_frame, 
            text="正在檢查...", 
            font=("Arial", 9),
            wraplength=600
        )
        self.lock_status_label.pack(anchor=tk.W, pady=5)

        # ====================================================================
        # 功能說明區域
        # ====================================================================
        info_text = """
🤖 自動排程功能：

此功能會在 Windows 工作排程器中建立一個任務，讓程式在指定時間自動在背景執行爬取工作。
⚠️ 需要管理員權限才能建立系統排程
⚠️ 請勿更改本執行檔檔名
✅ 自動排程會完全在背景執行，不會跳出視窗
        """
        
        info_label = ttk.Label(parent, text=info_text, font=("Arial", 9))
        info_label.pack(pady=10)
        
        # ====================================================================
        # 排程啟用開關
        # ====================================================================
        ttk.Checkbutton(
            parent, 
            text="啟用自動排程", 
            variable=self.schedule_enabled
        ).pack(anchor=tk.W, pady=10)
        
        # ====================================================================
        # 自動排程資料夾設定
        # ====================================================================
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
        
        # ====================================================================
        # 爬取模式設定
        # ====================================================================
        mode_frame = ttk.LabelFrame(parent, text="自動排程爬取模式", padding="10")
        mode_frame.pack(fill=tk.X, pady=10)
        
        ttk.Radiobutton(
            mode_frame, 
            text="爬取全部城市（資料分區）", 
            variable=self.schedule_scrape_mode, 
            value="all_cities"
        ).pack(anchor=tk.W, pady=2)
        
        # ====================================================================
        # 排程時間設定
        # ====================================================================
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
        
        # ====================================================================
        # 排程管理按鈕區域
        # ====================================================================
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
        
        # ====================================================================
        # 排程狀態顯示
        # ====================================================================
        status_frame = ttk.LabelFrame(parent, text="排程狀態", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.schedule_status_label = ttk.Label(status_frame, text="尚未設定自動排程")
        self.schedule_status_label.pack(anchor=tk.W)

    @handle_errors("選擇手動爬取資料夾", user_message="選擇資料夾時發生錯誤")
    def browse_folder(self):
        """開啟資料夾選擇對話框，讓使用者選擇手動爬取的輸出資料夾"""
        folder = filedialog.askdirectory(
            title="選擇手動爬取輸出資料夾", 
            initialdir=self.output_folder.get()
        )
        if folder:
            self.output_folder.set(folder)
            log_info(f"已選擇手動爬取資料夾: {folder}")

    @handle_errors("選擇自動排程資料夾", user_message="選擇資料夾時發生錯誤")
    def browse_schedule_folder(self):
        """開啟資料夾選擇對話框，讓使用者選擇自動排程的輸出資料夾"""
        folder = filedialog.askdirectory(
            title="選擇自動排程輸出資料夾", 
            initialdir=self.schedule_output_folder.get()
        )
        if folder:
            self.schedule_output_folder.set(folder)
            self.update_status(f"已選擇自動排程資料夾: {folder}")
            log_info(f"已選擇自動排程資料夾: {folder}")

    def load_cities_data(self):
        """在背景線程中載入城市資料，避免阻塞GUI"""
        def load_in_background():
            with ErrorContext(self.error_handler, "載入城市資料", show_gui_on_error=False):
                self.update_status("正在載入城市資料...")
                
                scraper = CommunityDataScraper(status_callback=self.update_status)
                cities_data = scraper.get_city_data()

                if cities_data:
                    self.cities_data = cities_data
                    city_names = [f"{city['name']} ({city['count']}筆)" for city in cities_data]
                    self.root.after(0, lambda: self.city_combo.configure(values=city_names))
                    self.update_status(f"成功載入 {len(cities_data)} 個城市資料")
                    log_success(f"成功載入 {len(cities_data)} 個城市資料")
                else:
                    self.update_status("載入城市資料失敗")
                    log_warning("載入城市資料失敗")
        
        threading.Thread(target=load_in_background, daemon=True).start()
    
    @handle_errors("選擇城市", show_gui=False)
    def on_city_selected(self, event):
        """當使用者選擇城市時的事件處理函數"""
        selection = self.city_combo.current()
        
        if selection >= 0 and selection < len(self.cities_data):
            self.selected_city_data = self.cities_data[selection]
            districts = self.selected_city_data['districts']
            
            district_names = [f"{district['name']} ({district['count']}筆)" for district in districts]
            
            self.district_combo.configure(values=district_names)
            
            if district_names:
                self.district_combo.current(0)
    
    @handle_errors("取得執行檔路徑", show_gui=False)
    def get_executable_path(self):
        """取得程式的執行檔路徑，用於設定Windows排程器"""
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
    
    @handle_errors("設定Windows排程器", user_message="設定自動排程時發生錯誤，請檢查是否有管理員權限")
    def setup_windows_scheduler(self):
        """設定Windows工作排程器，建立自動執行任務"""
        if not self.schedule_enabled.get():
            log_warning("請先勾選「啟用自動排程」", show_gui=True)
            return
        
        if not self.schedule_output_folder.get():
            log_warning("請選擇自動排程的輸出資料夾", show_gui=True)
            return
        
        task_name = "CommunityScraperAutoTask"
        
        day_mapping = {
            "星期一": "MON", "星期二": "TUE", "星期三": "WED",
            "星期四": "THU", "星期五": "FRI", "星期六": "SAT", "星期日": "SUN"
        }
        schtasks_day = day_mapping.get(self.schedule_day.get(), "MON")
        
        self.save_config()
        
        # 先刪除可能存在的同名任務
        subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], 
                     capture_output=True, text=True)
        
        # 建立背景執行批次檔
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))

        batch_file = os.path.join(script_dir, "background_runner.bat")
        
        batch_content = '''@echo off
REM 背景執行批次檔 - 修復編碼問題
chcp 65001 > nul
cd /d "%~dp0"

REM 使用英文文件名或通配符避免編碼問題
REM 檢查是否存在任何.exe文件（排除自己）
if exist "community_scraper.exe" (
    echo [%date% %time%] 執行community_scraper.exe
    "community_scraper.exe" --auto-background
)

REM 如果找不到exe，使用Python執行
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
            log_success("自動排程設定成功")
        else:
            raise RuntimeError(f"設定失敗：{result.stderr}")

    @handle_errors("移除Windows排程器", user_message="移除自動排程時發生錯誤")
    def remove_windows_scheduler(self):
        """移除Windows工作排程器中的自動執行任務"""
        task_name = "CommunityScraperAutoTask"
        
        result = subprocess.run(["schtasks", "/delete", "/tn", task_name, "/f"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            self.schedule_status_label.config(text="尚未設定自動排程")
            messagebox.showinfo("成功", "✅ 自動排程已移除")
            self.update_status("自動排程已移除")
            log_success("自動排程已移除")
        else:
            log_warning("沒有找到要移除的排程任務", show_gui=True)

    @handle_errors("測試排程執行", user_message="測試排程執行時發生錯誤")
    def test_scheduler(self):
        """立即執行排程任務進行測試"""
        task_name = "CommunityScraperAutoTask"
        
        result = subprocess.run(["schtasks", "/run", "/tn", task_name], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            messagebox.showinfo("成功", "✅ 排程任務已開始在背景執行\n\n您可以檢查輸出資料夾來確認執行結果")
            self.update_status("排程任務測試執行中...")
            log_info("排程任務測試執行")
        else:
            raise RuntimeError("執行失敗，請先設定自動排程")

    def start_scraping(self):
        """開始手動爬取作業"""
        try:
            if not self.check_lock_before_start():
                return
            
            if not self.cities_data:
                log_warning("城市資料尚未載入完成", show_gui=True)
                return
            
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            self.scraping_thread = threading.Thread(target=self.scrape_data, daemon=True)
            self.scraping_thread.start()
            
            log_info("開始手動爬取作業")
            
        except Exception as e:
            log_error(e, "開始爬取", user_message="開始爬取時發生錯誤")

    def stop_scraping(self):
        """停止進行中的爬取作業"""
        try:
            if self.scraper:
                self.scraper.stop_scraping()
            self.update_status("正在停止爬取...")
            log_info("使用者請求停止爬取")
        except Exception as e:
            log_error(e, "停止爬取")

    def scrape_data(self):
        """實際執行爬取作業的函數（在背景線程中運行）"""
        try:
            with ErrorContext(self.error_handler, "執行爬取作業"):
                self.scraper = CommunityDataScraper(
                    progress_callback=self.update_progress,
                    status_callback=self.update_status,
                    output_folder=self.output_folder.get()
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
                
                if success:
                    self.update_status("🎉 手動爬取完成！")
                    log_success("手動爬取完成")
                else:
                    self.update_status("❌ 手動爬取失敗或被中止")
                    log_warning("手動爬取失敗或被中止")
                    
        except Exception as e:
            log_error(e, "執行爬取作業")
            self.update_status(f"❌ 手動爬取錯誤: {str(e)}")
        
        finally:
            self.root.after(0, lambda: [
                self.start_button.configure(state="normal"),
                self.stop_button.configure(state="disabled")
            ])

    def update_status(self, message: str):
        """更新狀態顯示區域的訊息"""
        def update():
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.status_text.see(tk.END)
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, update)
        else:
            update()

    def update_progress(self, current: int, total: int):
        """更新進度條顯示"""
        def update():
            if total > 0:
                self.progress['value'] = (current / total) * 100
        
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, update)
        else:
            update()

    @handle_errors("強制停止背景程序", user_message="停止背景程序時發生錯誤")
    def force_stop_background_scraper(self):
        """強制停止背景執行的自動排程爬取"""
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
            log_success("已強制停止背景程序")
            self.update_lock_status_display()
        else:
            log_warning("Lock檔案已經不存在，背景程序可能已經停止", show_gui=True)

    @handle_errors("清理爬蟲鎖定", user_message="清理鎖定檔案時發生錯誤")
    def clear_scraper_lock(self):
        """清理爬蟲鎖定檔案"""
        if os.path.exists(self.lock_file_path):
            os.remove(self.lock_file_path)
            messagebox.showinfo("成功", "✅ 已清理鎖定檔案，現在可以正常執行自動排程了")
            self.update_status("已清理爬蟲鎖定檔案")
            log_success("已清理爬蟲鎖定檔案")
            self.update_lock_status_display()
        else:
            messagebox.showinfo("提示", "沒有找到鎖定檔案，無需清理")
            self.update_status("沒有找到鎖定檔案")

    @handle_errors("儲存設定", user_message="儲存設定時發生錯誤")
    def save_config(self):
        """儲存所有GUI設定到JSON檔案"""
        config = {
            "output_folder": self.output_folder.get(),
            "scrape_option": self.scrape_option.get(),
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
        log_success("設定已儲存")

    @handle_errors("載入設定", show_gui=False)
    def load_config(self):
        """從JSON檔案載入GUI設定"""
        if os.path.exists("gui_config.json"):
            with open("gui_config.json", 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.output_folder.set(config.get("output_folder", os.getcwd()))
            self.scrape_option.set(config.get("scrape_option", "all_cities"))
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
            
            log_info("設定檔載入完成")


# ============================================================================
# 背景自動爬取功能（供Windows排程器呼叫）
# ============================================================================
def run_background_scraper():
    """
    背景自動爬取功能，由Windows工作排程器呼叫
    包含完整的Lock檔案管理機制和錯誤處理
    """
    import sys
    
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
        with ErrorContext(bg_error_handler, "背景自動爬取"):
            # ================================================================
            # 初始化和環境準備
            # ================================================================
            bg_error_handler.log_info("開始背景自動爬取...")
            print("🤖 開始背景自動爬取...")
            
            bg_error_handler.log_info(f"程式目錄: {program_dir}")
            
            # ================================================================
            # 載入設定檔
            # ================================================================
            config_path = os.path.join(program_dir, "gui_config.json")
            bg_error_handler.log_info(f"尋找設定檔: {config_path}")
            
            if not os.path.exists(config_path):
                bg_error_handler.log_warning("找不到設定檔，使用預設設定")
                output_folder = os.path.join(program_dir, "爬蟲資料")
                scrape_mode = "all_cities"
            else:
                bg_error_handler.log_success("找到設定檔，載入設定")
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                output_folder = config.get("schedule_output_folder", os.path.join(program_dir, "爬蟲資料"))
                scrape_mode = config.get("schedule_scrape_mode", "all_cities")
               
                bg_error_handler.log_info(f"載入設定 - 輸出資料夾: {output_folder}")
                bg_error_handler.log_info(f"載入設定 - 爬取模式: {scrape_mode}")
            
            # ================================================================
            # 準備輸出環境
            # ================================================================
            bg_error_handler.log_info(f"確保輸出資料夾存在: {output_folder}")
            os.makedirs(output_folder, exist_ok=True)
            
            # ================================================================
            # 建立爬蟲並設定回調函數
            # ================================================================
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
                output_folder=output_folder
            )
            
            # ================================================================
            # 載入城市資料
            # ================================================================
            bg_error_handler.log_info("開始載入城市資料...")
            cities_data = scraper.get_city_data()
            
            if not cities_data:
                raise RuntimeError("無法載入城市資料")
            
            bg_error_handler.log_success(f"成功載入 {len(cities_data)} 個城市資料")
            print(f"📊 載入了 {len(cities_data)} 個城市資料")
            
            # ================================================================
            # 執行爬取作業
            # ================================================================
            bg_error_handler.log_info(f"開始執行爬取，模式: {scrape_mode}")
            success = False
            
            if scrape_mode == "all_cities":
                bg_error_handler.log_info("執行：爬取全部城市（分區）")
                success = scraper.scrape_all_cities_with_districts(cities_data)
            else:
                bg_error_handler.log_warning(f"未知的爬取模式: {scrape_mode}")
            
            # ================================================================
            # 處理執行結果
            # ================================================================
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
        # ================================================================
        # 錯誤處理和記錄
        # ================================================================
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
        # ================================================================
        # 清理Lock檔案
        # ================================================================
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                bg_error_handler.log_success("已清理Lock檔案")
        except Exception as e:
            bg_error_handler.log_error(e, "清理Lock檔案")
        
        bg_error_handler.log_info("背景自動爬取函式結束")


# ============================================================================
# 主程式進入點
# ============================================================================
def main():
    """主程式進入點"""
    try:
        # 檢查是否為背景自動執行模式
        if len(sys.argv) > 1 and "--auto-background" in sys.argv:
            run_background_scraper()
        else:
            # 一般GUI模式
            root = tk.Tk()
            app = SimpleScraperGUI(root)
            root.mainloop()
            
    except Exception as e:
        # 最頂層的錯誤處理
        try:
            log_error(e, "主程式執行", user_message="程式啟動時發生嚴重錯誤")
        except:
            # 如果連錯誤處理都失敗，直接輸出到控制台
            print(f"❌ 嚴重錯誤: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()