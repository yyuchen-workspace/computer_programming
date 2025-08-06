#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一錯誤處理模組
提供統一的錯誤處理、日誌記錄和使用者通知功能
"""

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Any
from tkinter import messagebox
import logging


class ErrorHandler:
    """
    統一錯誤處理類別
    
    功能：
    1. 統一的錯誤記錄格式
    2. 多種輸出方式（檔案、控制台、GUI）
    3. 自動建立錯誤日誌目錄
    4. 統一的使用者錯誤通知
    """
    
    def __init__(self, 
                 log_directory: str = None,
                 app_name: str = "CommunityDataScraper",
                 enable_console: bool = True,
                 enable_file: bool = True,
                 enable_gui: bool = True):
        """
        初始化錯誤處理器
        
        Args:
            log_directory: 日誌檔案目錄，None時使用程式目錄
            app_name: 應用程式名稱，用於日誌檔案命名
            enable_console: 是否啟用控制台輸出
            enable_file: 是否啟用檔案記錄
            enable_gui: 是否啟用GUI錯誤提示
        """
        self.app_name = app_name
        self.enable_console = enable_console
        self.enable_file = enable_file
        self.enable_gui = enable_gui
        
        # 設定日誌目錄
        if log_directory is None:
            # 自動偵測程式目錄
            if getattr(sys, 'frozen', False):
                self.log_directory = os.path.dirname(sys.executable)
            else:
                self.log_directory = os.path.dirname(__file__)
        else:
            self.log_directory = log_directory
        
        # 建立日誌目錄
        self.logs_folder = os.path.join(self.log_directory, "logs")
        os.makedirs(self.logs_folder, exist_ok=True)
        
        # 設定檔案路徑
        today = datetime.now().strftime('%Y-%m-%d')
        self.error_log_file = os.path.join(self.logs_folder, f"{app_name}_error_{today}.log")
        self.general_log_file = os.path.join(self.logs_folder, f"{app_name}_general_{today}.log")
        
        # 設定Python的logging
        self._setup_logging()
    
    def _setup_logging(self):
        """設定Python的logging系統"""
        # 建立logger
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重複添加handler
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 設定格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 檔案handler
        if self.enable_file:
            file_handler = logging.FileHandler(self.general_log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # 控制台handler
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def log_error(self, 
                  error: Exception, 
                  context: str = "",
                  show_gui: bool = None,
                  user_message: str = None) -> str:
        """
        記錄錯誤並提供適當的使用者通知
        
        Args:
            error: 錯誤物件
            context: 錯誤發生的上下文說明
            show_gui: 是否顯示GUI錯誤對話框，None時使用預設設定
            user_message: 自定義的使用者友善錯誤訊息
        
        Returns:
            str: 格式化的錯誤訊息
        """
        # 建立錯誤訊息
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # 包含毫秒的唯一ID
        
        # 基本錯誤資訊
        error_message = {
            'timestamp': timestamp,
            'error_id': error_id,
            'context': context,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc()
        }
        
        # 格式化錯誤文字
        formatted_error = self._format_error_message(error_message)
        
        # 記錄到檔案
        if self.enable_file:
            self._write_to_error_file(formatted_error)
        
        # 記錄到一般日誌
        self.logger.error(f"{context} - {error}")
        
        # 控制台輸出
        if self.enable_console:
            print(f"❌ 錯誤 [{error_id}]: {error}")
            if context:
                print(f"📍 上下文: {context}")
        
        # GUI通知
        if (show_gui if show_gui is not None else self.enable_gui):
            self._show_gui_error(error, context, error_id, user_message)
        
        return formatted_error
    
    def log_info(self, message: str, context: str = ""):
        """
        記錄一般資訊
        
        Args:
            message: 資訊內容
            context: 上下文說明
        """
        full_message = f"{context} - {message}" if context else message
        self.logger.info(full_message)
        
        if self.enable_console:
            print(f"ℹ️ {full_message}")
    
    def log_warning(self, message: str, context: str = "", show_gui: bool = False):
        """
        記錄警告訊息
        
        Args:
            message: 警告內容
            context: 上下文說明
            show_gui: 是否顯示GUI警告對話框
        """
        full_message = f"{context} - {message}" if context else message
        self.logger.warning(full_message)
        
        if self.enable_console:
            print(f"⚠️ {full_message}")
        
        if show_gui and self.enable_gui:
            messagebox.showwarning("警告", message)
    
    def log_success(self, message: str, context: str = ""):
        """
        記錄成功訊息
        
        Args:
            message: 成功訊息內容
            context: 上下文說明
        """
        full_message = f"{context} - {message}" if context else message
        self.logger.info(f"SUCCESS: {full_message}")
        
        if self.enable_console:
            print(f"✅ {full_message}")
    
    def _format_error_message(self, error_info: dict) -> str:
        """格式化錯誤訊息"""
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
        """寫入錯誤檔案"""
        try:
            with open(self.error_log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_error)
                f.flush()
        except Exception as e:
            # 避免記錄錯誤本身造成錯誤
            print(f"❌ 無法寫入錯誤日誌檔案: {e}")
    
    def _show_gui_error(self, error: Exception, context: str, error_id: str, user_message: str = None):
        """顯示GUI錯誤對話框"""
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
            # 避免GUI錯誤顯示本身造成錯誤
            print(f"❌ 無法顯示GUI錯誤訊息: {e}")


class ErrorContext:
    """
    錯誤上下文管理器，用於統一處理特定區塊的錯誤
    
    使用方式：
    with ErrorContext(error_handler, "爬取數據"):
        # 可能發生錯誤的程式碼
        pass
    """
    
    def __init__(self, 
                 error_handler: ErrorHandler, 
                 context: str,
                 show_gui_on_error: bool = True,
                 user_message: str = None,
                 reraise: bool = False):
        """
        初始化錯誤上下文
        
        Args:
            error_handler: 錯誤處理器實例
            context: 上下文說明
            show_gui_on_error: 發生錯誤時是否顯示GUI
            user_message: 自定義使用者錯誤訊息
            reraise: 是否重新拋出錯誤
        """
        self.error_handler = error_handler
        self.context = context
        self.show_gui_on_error = show_gui_on_error
        self.user_message = user_message
        self.reraise = reraise
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 記錄錯誤
            self.error_handler.log_error(
                exc_val, 
                self.context, 
                show_gui=self.show_gui_on_error,
                user_message=self.user_message
            )
            
            # 決定是否重新拋出錯誤
            return not self.reraise  # True = 抑制錯誤，False = 重新拋出


# ============================================================================
# 便利函數
# ============================================================================

# 全域錯誤處理器實例
_global_error_handler = None

def get_error_handler() -> ErrorHandler:
    """取得全域錯誤處理器實例"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler

def setup_global_error_handler(log_directory: str = None, **kwargs) -> ErrorHandler:
    """
    設定全域錯誤處理器
    
    Args:
        log_directory: 日誌目錄
        **kwargs: 其他ErrorHandler參數
    
    Returns:
        ErrorHandler: 設定好的錯誤處理器實例
    """
    global _global_error_handler
    _global_error_handler = ErrorHandler(log_directory=log_directory, **kwargs)
    return _global_error_handler

def log_error(error: Exception, context: str = "", **kwargs) -> str:
    """便利函數：記錄錯誤"""
    return get_error_handler().log_error(error, context, **kwargs)

def log_info(message: str, context: str = ""):
    """便利函數：記錄資訊"""
    get_error_handler().log_info(message, context)

def log_warning(message: str, context: str = "", show_gui: bool = False):
    """便利函數：記錄警告"""
    get_error_handler().log_warning(message, context, show_gui)

def log_success(message: str, context: str = ""):
    """便利函數：記錄成功"""
    get_error_handler().log_success(message, context)


# ============================================================================
# 裝飾器
# ============================================================================

def handle_errors(context: str = "", 
                  show_gui: bool = True, 
                  user_message: str = None,
                  return_on_error: Any = None):
    """
    錯誤處理裝飾器
    
    Args:
        context: 錯誤上下文說明
        show_gui: 是否顯示GUI錯誤訊息
        user_message: 自定義使用者錯誤訊息
        return_on_error: 發生錯誤時的回傳值
    
    使用方式：
    @handle_errors("載入城市資料", user_message="無法載入城市資料，請檢查網路連線")
    def load_cities():
        # 可能發生錯誤的程式碼
        pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_error(
                    e, 
                    context or f"執行函數 {func.__name__}",
                    show_gui=show_gui,
                    user_message=user_message
                )
                return return_on_error
        return wrapper
    return decorator


# ============================================================================
# 測試和範例
# ============================================================================

if __name__ == "__main__":
    # 建立錯誤處理器
    error_handler = ErrorHandler()
    
    print("🧪 測試錯誤處理模組")
    
    # 測試1：基本錯誤記錄
    try:
        1 / 0
    except Exception as e:
        error_handler.log_error(e, "測試除零錯誤")
    
    # 測試2：使用上下文管理器
    with ErrorContext(error_handler, "測試上下文管理器", show_gui_on_error=False):
        raise ValueError("這是一個測試錯誤")
    
    # 測試3：使用裝飾器
    @handle_errors("測試裝飾器", show_gui=False, return_on_error="錯誤回傳值")
    def test_function():
        raise RuntimeError("這是裝飾器測試錯誤")
    
    result = test_function()
    print(f"裝飾器測試結果: {result}")
    
    # 測試4：一般日誌
    error_handler.log_info("這是一個資訊訊息", "測試資訊")
    error_handler.log_warning("這是一個警告訊息", "測試警告")
    error_handler.log_success("這是一個成功訊息", "測試成功")
    
    print(f"✅ 測試完成，請檢查日誌檔案：{error_handler.logs_folder}")