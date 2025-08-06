#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社區資料爬蟲 - 主程式啟動器（簡化版）
"""

import sys
from datetime import datetime
from pathlib import Path
import flet as ft

def setup_logging():
    """設定日誌系統並顯示位置"""
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)
    log_file = log_folder / "startup.log"
    
    print("=" * 50)
    print("🚀 社區資料爬蟲啟動")
    print("=" * 50)
    print(f"📁 日誌檔案: {log_file.absolute()}")
    print(f"💡 提示: 執行記錄將保存在上述位置")
    print("=" * 50)
    
    return log_file

def log_message(message: str, log_file: Path):
    """記錄日誌訊息"""
    try:
        with log_file.open('a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
        print(f"[LOG] {message}")
    except Exception as e:
        print(f"❌ 日誌記錄失敗: {e}")

def main_gui(page: ft.Page):
    """GUI 模式主函式"""
    log_file = setup_logging()
    log_message("啟動 GUI 模式", log_file)
    
    page.title = "社區資料爬蟲 v1.0"
    
    try:
        from flet_gui import CommunityScraperApp
        app = CommunityScraperApp()
        app.build_ui(page)
        log_message("GUI 介面建立成功", log_file)
        
    except Exception as e:
        error_msg = f"GUI 啟動失敗: {str(e)}"
        log_message(error_msg, log_file)
        print(f"❌ {error_msg}")
        
        page.add(
            ft.Column([
                ft.Text(f"❌ 啟動失敗: {e}", color=ft.Colors.RED),
                ft.Text(f"📋 日誌位置: {log_file.absolute()}", size=12, color=ft.Colors.BLUE),
            ])
        )

def main_background():
    """背景模式主函式"""
    log_file = setup_logging()
    log_message("啟動背景模式", log_file)
    
    try:
        from flet_gui import run_background_scraper
        print("⏳ 執行背景爬取中...")
        log_message("開始執行背景爬取", log_file)
        run_background_scraper()
        log_message("背景爬取完成", log_file)
        print("✅ 背景爬取完成")
        
    except Exception as e:
        error_msg = f"背景執行失敗: {str(e)}"
        log_message(error_msg, log_file)
        print(f"❌ {error_msg}")
    
    print(f"\n📋 完整執行記錄請查看: {log_file.absolute()}")

def main():
    """主程式入口"""
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--background":
            main_background()
        else:
            print("💡 提示: 關閉視窗可退出程式")
            ft.app(target=main_gui, assets_dir="assets")
    
    except KeyboardInterrupt:
        print("\n⚠️  程式被用戶中斷")
    except Exception as e:
        print(f"❌ 程式執行錯誤: {e}")
    
    # ✅ 簡單的結束訊息，不重複
    print("👋 程式已結束")

if __name__ == "__main__":
    main()