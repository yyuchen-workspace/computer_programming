#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧檔案管理模組
自動管理爬蟲輸出檔案，只保留最新日期的檔案並自動命名
"""

import os
import re
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import shutil


class SmartFileManager:
    """
    智慧檔案管理器
    
    功能：
    1. 自動偵測並清理舊檔案
    2. 智慧命名新檔案
    3. 支援多種檔案格式
    4. 提供檔案版本管理
    """
    
    def __init__(self, base_folder: str, enable_backup: bool = True):
        """
        初始化檔案管理器
        
        Args:
            base_folder: 基礎輸出資料夾
            enable_backup: 是否啟用備份功能
        """
        self.base_folder = Path(base_folder)
        self.enable_backup = enable_backup
        self.backup_folder = self.base_folder / "備份檔案"
        
        # 建立必要的資料夾
        self.base_folder.mkdir(parents=True, exist_ok=True)
        if self.enable_backup:
            self.backup_folder.mkdir(parents=True, exist_ok=True)
    
    def get_latest_file_pattern(self, 
                               file_pattern: str, 
                               date_format: str = r'\d{4}-\d{2}-\d{2}') -> Optional[Path]:
        """
        找到符合模式的最新檔案
        
        Args:
            file_pattern: 檔案名稱模式，如 "*城市*.txt"
            date_format: 日期正則表達式格式
            
        Returns:
            最新檔案的路徑，沒有找到時回傳 None
        """
        # 搜尋符合模式的所有檔案
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if not matching_files:
            return None
        
        # 從檔案名稱中提取日期並排序
        file_dates = []
        for file_path in matching_files:
            # 使用正則表達式提取日期
            date_match = re.search(date_format, file_path.name)
            if date_match:
                try:
                    date_str = date_match.group()
                    # 嘗試解析日期
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    file_dates.append((file_date, file_path))
                except ValueError:
                    continue
        
        if not file_dates:
            return None
        
        # 按日期排序，回傳最新的
        file_dates.sort(key=lambda x: x[0], reverse=True)
        return file_dates[0][1]
    
    def clean_old_files(self, 
                       file_pattern: str, 
                       keep_latest: int = 1,
                       date_format: str = r'\d{4}-\d{2}-\d{2}') -> List[Path]:
        """
        清理舊檔案，只保留最新的幾個
        
        Args:
            file_pattern: 檔案名稱模式
            keep_latest: 保留最新的檔案數量
            date_format: 日期正則表達式格式
            
        Returns:
            被清理的檔案列表
        """
        # 搜尋符合模式的所有檔案
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if len(matching_files) <= keep_latest:
            return []  # 檔案數量不超過保留數量，不需要清理
        
        # 從檔案名稱中提取日期並排序
        file_dates = []
        for file_path in matching_files:
            date_match = re.search(date_format, file_path.name)
            if date_match:
                try:
                    date_str = date_match.group()
                    file_date = datetime.strptime(date_str, '%Y-%m-%d')
                    file_dates.append((file_date, file_path))
                except ValueError:
                    # 如果無法解析日期，使用檔案修改時間
                    file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    file_dates.append((file_date, file_path))
        
        # 按日期排序
        file_dates.sort(key=lambda x: x[0], reverse=True)
        
        # 確定要清理的檔案
        files_to_clean = file_dates[keep_latest:]
        cleaned_files = []
        
        for _, file_path in files_to_clean:
            try:
                if self.enable_backup:
                    # 移動到備份資料夾
                    backup_path = self.backup_folder / file_path.name
                    # 如果備份檔案已存在，加上時間戳記
                    if backup_path.exists():
                        timestamp = datetime.now().strftime('%H%M%S')
                        backup_path = backup_path.with_name(
                            f"{backup_path.stem}_{timestamp}{backup_path.suffix}"
                        )
                    shutil.move(str(file_path), str(backup_path))
                    print(f"📦 已備份舊檔案: {file_path.name} -> {backup_path.name}")
                else:
                    # 直接刪除
                    file_path.unlink()
                    print(f"🗑️ 已刪除舊檔案: {file_path.name}")
                
                cleaned_files.append(file_path)
                
            except Exception as e:
                print(f"❌ 清理檔案失敗 {file_path.name}: {e}")
        
        return cleaned_files
    
    def generate_smart_filename(self, 
                               base_name: str, 
                               extension: str = '.txt',
                               include_time: bool = False) -> str:
        """
        生成智慧檔案名稱
        
        Args:
            base_name: 基礎檔案名稱
            extension: 檔案副檔名
            include_time: 是否包含時間
            
        Returns:
            完整的檔案名稱
        """
        today = datetime.now()
        
        if include_time:
            date_str = today.strftime('%Y-%m-%d_%H%M')
        else:
            date_str = today.strftime('%Y-%m-%d')
        
        # 清理基礎名稱，移除可能的舊日期
        clean_base = re.sub(r'_?\d{4}-\d{2}-\d{2}(_\d{4})?', '', base_name)
        clean_base = clean_base.strip('_')
        
        return f"{clean_base}_{date_str}{extension}"
    
    def prepare_output_file(self, 
                           base_name: str, 
                           extension: str = '.txt',
                           auto_clean: bool = True,
                           include_time: bool = False) -> Path:
        """
        準備輸出檔案，自動清理舊檔案並生成新檔案名稱
        
        Args:
            base_name: 基礎檔案名稱
            extension: 檔案副檔名
            auto_clean: 是否自動清理舊檔案
            include_time: 是否在檔案名稱中包含時間
            
        Returns:
            準備好的檔案路徑
        """
        # 生成新檔案名稱
        new_filename = self.generate_smart_filename(base_name, extension, include_time)
        new_file_path = self.base_folder / new_filename
        
        if auto_clean:
            # 清理同類型的舊檔案
            # 建立搜尋模式：移除日期部分，用萬用字元替代
            clean_base = re.sub(r'_?\d{4}-\d{2}-\d{2}(_\d{4})?', '', base_name).strip('_')
            search_pattern = f"{clean_base}_*{extension}"
            
            cleaned_files = self.clean_old_files(search_pattern, keep_latest=0)
            
            if cleaned_files:
                print(f"🧹 已清理 {len(cleaned_files)} 個舊檔案")
        
        print(f"📝 準備輸出檔案: {new_filename}")
        return new_file_path
    
    def get_file_info(self, file_pattern: str) -> Dict[str, any]:
        """
        取得檔案資訊統計
        
        Args:
            file_pattern: 檔案搜尋模式
            
        Returns:
            檔案資訊字典
        """
        matching_files = list(self.base_folder.glob(file_pattern))
        
        if not matching_files:
            return {
                'total_files': 0,
                'latest_file': None,
                'oldest_file': None,
                'total_size': 0
            }
        
        # 計算檔案資訊
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
        
        # 按修改時間排序
        file_info.sort(key=lambda x: x['modified'])
        
        return {
            'total_files': len(matching_files),
            'latest_file': file_info[-1]['path'] if file_info else None,
            'oldest_file': file_info[0]['path'] if file_info else None,
            'total_size': total_size,
            'size_mb': round(total_size / (1024 * 1024), 2)
        }
    
    def list_all_files_by_date(self) -> Dict[str, List[Path]]:
        """
        按日期列出所有檔案
        
        Returns:
            按日期分組的檔案字典
        """
        all_files = list(self.base_folder.glob('*.txt'))
        files_by_date = {}
        
        for file_path in all_files:
            # 嘗試從檔案名稱提取日期
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', file_path.name)
            if date_match:
                date_str = date_match.group()
            else:
                # 使用檔案修改日期
                file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                date_str = file_date.strftime('%Y-%m-%d')
            
            if date_str not in files_by_date:
                files_by_date[date_str] = []
            files_by_date[date_str].append(file_path)
        
        return files_by_date


class ScraperFileManager(SmartFileManager):
    """
    專為爬蟲設計的檔案管理器
    包含爬蟲特定的檔案處理邏輯
    """
    
    def __init__(self, base_folder: str, enable_backup: bool = True):
        super().__init__(base_folder, enable_backup)
        
        # 爬蟲特定的檔案類型
        self.file_types = {
            'city': '城市',
            'district': '區域',
            'all': '全部城市'
        }
    
    def prepare_city_file(self, city_name: str, auto_clean: bool = True) -> Path:
        """
        準備城市檔案
        
        Args:
            city_name: 城市名稱
            auto_clean: 是否自動清理舊檔案
            
        Returns:
            準備好的城市檔案路徑
        """
        base_name = f"{city_name}_{self.file_types['city']}"
        return self.prepare_output_file(base_name, '.txt', auto_clean)
    
    def prepare_district_file(self, city_name: str, district_name: str, auto_clean: bool = True) -> Path:
        """
        準備區域檔案
        
        Args:
            city_name: 城市名稱
            district_name: 區域名稱
            auto_clean: 是否自動清理舊檔案
            
        Returns:
            準備好的區域檔案路徑
        """
        base_name = f"{city_name}_{district_name}_{self.file_types['district']}"
        return self.prepare_output_file(base_name, '.txt', auto_clean)
    
    def prepare_all_cities_file(self, auto_clean: bool = True) -> Path:
        """
        準備全部城市檔案
        
        Args:
            auto_clean: 是否自動清理舊檔案
            
        Returns:
            準備好的全部城市檔案路徑
        """
        base_name = self.file_types['all']
        return self.prepare_output_file(base_name, '.txt', auto_clean)
    
    def get_scraper_statistics(self) -> Dict[str, any]:
        """
        取得爬蟲檔案統計資訊
        
        Returns:
            爬蟲檔案統計字典
        """
        stats = {}
        
        for file_type, type_name in self.file_types.items():
            if file_type == 'city':
                pattern = f"*_{type_name}_*.txt"
            elif file_type == 'district':
                pattern = f"*_{type_name}_*.txt"
            else:  # all
                pattern = f"{type_name}_*.txt"
            
            stats[file_type] = self.get_file_info(pattern)
        
        return stats
    
    def cleanup_all_old_files(self, keep_latest: int = 1) -> Dict[str, List[Path]]:
        """
        清理所有類型的舊檔案
        
        Args:
            keep_latest: 每種類型保留的最新檔案數量
            
        Returns:
            被清理的檔案統計
        """
        cleanup_results = {}
        
        for file_type, type_name in self.file_types.items():
            if file_type == 'city':
                pattern = f"*_{type_name}_*.txt"
            elif file_type == 'district':
                pattern = f"*_{type_name}_*.txt"
            else:  # all
                pattern = f"{type_name}_*.txt"
            
            cleaned = self.clean_old_files(pattern, keep_latest)
            cleanup_results[file_type] = cleaned
        
        return cleanup_results


# ============================================================================
# 使用範例和測試
# ============================================================================

def demo_file_manager():
    """演示檔案管理器的使用方法"""
    print("🧪 演示智慧檔案管理器")
    
    # 建立檔案管理器
    file_manager = ScraperFileManager("./爬蟲資料", enable_backup=True)
    
    # 1. 準備不同類型的檔案
    print("\n📝 準備輸出檔案:")
    
    # 城市檔案
    city_file = file_manager.prepare_city_file("台北市")
    print(f"城市檔案: {city_file}")
    
    # 區域檔案
    district_file = file_manager.prepare_district_file("台北市", "中正區")
    print(f"區域檔案: {district_file}")
    
    # 全部城市檔案
    all_file = file_manager.prepare_all_cities_file()
    print(f"全部城市檔案: {all_file}")
    
    # 2. 顯示統計資訊
    print("\n📊 檔案統計:")
    stats = file_manager.get_scraper_statistics()
    for file_type, info in stats.items():
        print(f"{file_type}: {info['total_files']} 個檔案, {info['size_mb']} MB")
    
    # 3. 列出按日期分組的檔案
    print("\n📅 按日期分組:")
    files_by_date = file_manager.list_all_files_by_date()
    for date, files in sorted(files_by_date.items()):
        print(f"{date}: {len(files)} 個檔案")
        for file in files:
            print(f"  - {file.name}")


if __name__ == "__main__":
    demo_file_manager()