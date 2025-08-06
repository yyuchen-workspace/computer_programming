#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化測試版本 - 專門用來測試背景執行
"""

import sys
import os
from datetime import datetime

def test_log(message):
    """測試日誌函式"""
    log_file = os.path.join(os.path.dirname(sys.executable), "test.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] {message}\n")

def main():
    """主程式"""
    test_log("程式啟動")
    test_log(f"參數: {sys.argv}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto-background":
        test_log("背景模式啟動")
        
        try:
            test_log("嘗試匯入 gui_app")
            from gui_app import run_background_scraper
            test_log("成功匯入")
            
            test_log("開始執行 run_background_scraper")
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
        import tkinter as tk
        from gui_app import SimpleScraperGUI
        
        root = tk.Tk() #建立父容器
        app = SimpleScraperGUI(root)
        root.mainloop()
        
    except Exception as e:
        test_log(f"GUI 錯誤: {str(e)}")
        print(f"錯誤: {e}")
        input("按 Enter 退出...")

if __name__ == "__main__":
    main()