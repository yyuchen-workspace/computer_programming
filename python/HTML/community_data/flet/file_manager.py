#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧檔案管理器模組
Smart File Manager Module - 支援自動備份、清理和統計功能
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import glob
import logging


class SmartFileManager:
    """
    智慧檔案管理器
    
    功能：
    1. 自動備份舊檔案
    2. 清理過期檔案
    3. 檔案統計和健康檢查
    4. 安全的檔案操作
    """
    
    def __init__(self, base_folder: str, enable_backup: bool = True, 
                 backup_days: int = 7, max_backup_size_mb: int = 1000):
        """
        初始化檔案管理器
        
        Args:
            base_folder: 基礎資料夾路徑
            enable_backup: 是否啟用備份功能
            backup_days: 備份保留天數
            max_backup_size_mb: 備份資料夾最大大小（MB）
        """
        self.base_folder = Path(base_folder)
        self.backup_folder = self.base_folder / "備份檔案"
        self.enable_backup = enable_backup
        self.backup_days = backup_days
        self.max_backup_size_mb = max_backup_size_mb
        
        # 建立必要資料夾
        self.base_folder.mkdir(parents=True, exist_ok=True)
        if self.enable_backup:
            self.backup_folder.mkdir(parents=True, exist_ok=True)
        
        # 設定日誌
        self.logger = logging.getLogger(__name__)
        
    def backup_file(self, file_path: Path, preserve_structure: bool = True) -> bool:
        """
        備份單個檔案
        
        Args:
            file_path: 要備份的檔案路徑
            preserve_structure: 是否保持目錄結構
            
        Returns:
            備份是否成功
        """
        if not self.enable_backup or not file_path.exists():
            return False
        
        try:
            if preserve_structure:
                # 保持相對路徑結構
                relative_path = file_path.relative_to(self.base_folder)
                backup_path = self.backup_folder / relative_path
            else:
                # 直接放在備份根目錄
                backup_path = self.backup_folder / file_path.name
            
            # 建立備份目錄
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 如果備份檔案已存在，添加時間戳
            if backup_path.exists():
                timestamp = datetime.now().strftime("%H%M%S")
                backup_path = backup_path.with_name(
                    f"{backup_path.stem}_{timestamp}{backup_path.suffix}"
                )
            
            # 複製檔案
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"檔案已備份: {file_path.name} -> {backup_path.relative_to(self.backup_folder)}")
            return True
            
        except Exception as e:
            self.logger.error(f"備份檔案失敗 {file_path}: {e}")
            return False
    
    def backup_folder(self, folder_path: Path, exclude_patterns: List[str] = None) -> bool:
        """
        備份整個資料夾
        
        Args:
            folder_path: 要備份的資料夾路徑
            exclude_patterns: 要排除的檔案模式列表
            
        Returns:
            備份是否成功
        """
        if not self.enable_backup or not folder_path.exists():
            return False
        
        exclude_patterns = exclude_patterns or []
        
        try:
            # 計算相對路徑
            relative_path = folder_path.relative_to(self.base_folder)
            backup_path = self.backup_folder / relative_path
            
            # 如果備份資料夾已存在，添加時間戳
            if backup_path.exists():
                timestamp = datetime.now().strftime("%H%M%S")
                backup_path = backup_path.with_name(f"{backup_path.name}_{timestamp}")
            
            # 複製整個資料夾
            def ignore_patterns(dir_name, filenames):
                ignored = []
                for pattern in exclude_patterns:
                    ignored.extend(glob.fnmatch.filter(filenames, pattern))
                return set(ignored)
            
            shutil.copytree(folder_path, backup_path, ignore=ignore_patterns)
            self.logger.info(f"資料夾已備份: {folder_path.name} -> {backup_path.relative_to(self.backup_folder)}")
            return True
            
        except Exception as e:
            self.logger.error(f"備份資料夾失敗 {folder_path}: {e}")
            return False
    
    def clean_old_files(self, pattern: str, keep_latest: int = 3, 
                       older_than_days: int = None) -> List[Path]:
        """
        清理舊檔案
        
        Args:
            pattern: 檔案模式（支援萬用字元）
            keep_latest: 保留最新的檔案數量
            older_than_days: 只清理超過指定天數的檔案
            
        Returns:
            已清理的檔案列表
        """
        cleaned_files = []
        
        try:
            # 尋找符合模式的檔案
            matched_files = list(self.base_folder.rglob(pattern))
            
            # 按修改時間排序（最新的在前）
            matched_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # 決定要清理的檔案
            files_to_clean = []
            
            if older_than_days is not None:
                cutoff_time = time.time() - (older_than_days * 24 * 3600)
                files_to_clean = [
                    f for f in matched_files[keep_latest:]
                    if f.stat().st_mtime < cutoff_time
                ]
            else:
                files_to_clean = matched_files[keep_latest:]
            
            # 執行清理
            for file_path in files_to_clean:
                try:
                    # 先備份（如果啟用）
                    if self.enable_backup:
                        self.backup_file(file_path)
                    
                    # 刪除檔案
                    if file_path.is_file():
                        file_path.unlink()
                        cleaned_files.append(file_path)
                        self.logger.info(f"已清理檔案: {file_path.name}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        cleaned_files.append(file_path)
                        self.logger.info(f"已清理資料夾: {file_path.name}")
                        
                except Exception as e:
                    self.logger.error(f"清理檔案失敗 {file_path}: {e}")
            
            if cleaned_files:
                self.logger.info(f"清理完成，共處理 {len(cleaned_files)} 個項目")
            
        except Exception as e:
            self.logger.error(f"清理舊檔案時發生錯誤: {e}")
        
        return cleaned_files
    
    def clean_old_backups(self) -> List[Path]:
        """
        清理過期的備份檔案
        
        Returns:
            已清理的備份檔案列表
        """
        if not self.enable_backup or not self.backup_folder.exists():
            return []
        
        cleaned_files = []
        cutoff_time = time.time() - (self.backup_days * 24 * 3600)
        
        try:
            for item in self.backup_folder.rglob("*"):
                if item.stat().st_mtime < cutoff_time:
                    try:
                        if item.is_file():
                            item.unlink()
                            cleaned_files.append(item)
                        elif item.is_dir() and not any(item.iterdir()):
                            # 只刪除空資料夾
                            item.rmdir()
                            cleaned_files.append(item)
                    except Exception as e:
                        self.logger.error(f"清理備份項目失敗 {item}: {e}")
            
            # 檢查備份資料夾大小
            self._check_backup_size()
            
        except Exception as e:
            self.logger.error(f"清理備份檔案時發生錯誤: {e}")
        
        return cleaned_files
    
    def _check_backup_size(self):
        """檢查並控制備份資料夾大小"""
        try:
            total_size = self.get_folder_size(self.backup_folder)
            size_mb = total_size / (1024 * 1024)
            
            if size_mb > self.max_backup_size_mb:
                self.logger.warning(f"備份資料夾大小超過限制: {size_mb:.1f}MB > {self.max_backup_size_mb}MB")
                
                # 刪除最舊的備份檔案直到大小合適
                all_files = []
                for item in self.backup_folder.rglob("*"):
                    if item.is_file():
                        all_files.append((item, item.stat().st_mtime))
                
                # 按時間排序（最舊的在前）
                all_files.sort(key=lambda x: x[1])
                
                for file_path, _ in all_files:
                    try:
                        file_path.unlink()
                        total_size = self.get_folder_size(self.backup_folder)
                        size_mb = total_size / (1024 * 1024)
                        
                        if size_mb <= self.max_backup_size_mb * 0.8:  # 保留20%緩衝
                            break
                    except Exception as e:
                        self.logger.error(f"刪除備份檔案失敗 {file_path}: {e}")
                
        except Exception as e:
            self.logger.error(f"檢查備份大小時發生錯誤: {e}")
    
    def get_folder_size(self, folder_path: Path) -> int:
        """
        計算資料夾大小
        
        Args:
            folder_path: 資料夾路徑
            
        Returns:
            大小（位元組）
        """
        total_size = 0
        try:
            for item in folder_path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
        except Exception as e:
            self.logger.error(f"計算資料夾大小失敗 {folder_path}: {e}")
        
        return total_size
    
    def get_file_statistics(self, pattern: str = "*") -> Dict:
        """
        取得檔案統計資訊
        
        Args:
            pattern: 檔案模式
            
        Returns:
            統計資訊字典
        """
        stats = {
            "total_files": 0,
            "total_size": 0,
            "file_types": {},
            "oldest_file": None,
            "newest_file": None,
            "largest_file": None
        }
        
        try:
            matched_files = list(self.base_folder.rglob(pattern))
            stats["total_files"] = len(matched_files)
            
            if not matched_files:
                return stats
            
            oldest_time = float('inf')
            newest_time = 0
            largest_size = 0
            
            for file_path in matched_files:
                if not file_path.is_file():
                    continue
                
                file_stat = file_path.stat()
                file_size = file_stat.st_size
                file_time = file_stat.st_mtime
                file_ext = file_path.suffix.lower()
                
                # 累加大小
                stats["total_size"] += file_size
                
                # 檔案類型統計
                if file_ext not in stats["file_types"]:
                    stats["file_types"][file_ext] = {"count": 0, "size": 0}
                stats["file_types"][file_ext]["count"] += 1
                stats["file_types"][file_ext]["size"] += file_size
                
                # 最舊檔案
                if file_time < oldest_time:
                    oldest_time = file_time
                    stats["oldest_file"] = {
                        "path": str(file_path.relative_to(self.base_folder)),
                        "time": datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                # 最新檔案
                if file_time > newest_time:
                    newest_time = file_time
                    stats["newest_file"] = {
                        "path": str(file_path.relative_to(self.base_folder)),
                        "time": datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                # 最大檔案
                if file_size > largest_size:
                    largest_size = file_size
                    stats["largest_file"] = {
                        "path": str(file_path.relative_to(self.base_folder)),
                        "size": self._format_size(file_size)
                    }
            
        except Exception as e:
            self.logger.error(f"取得檔案統計時發生錯誤: {e}")
        
        return stats
    
    def get_comprehensive_statistics(self) -> Dict:
        """
        取得全面的統計資訊
        
        Returns:
            詳細統計資訊
        """
        stats = {
            "summary": {
                "total_files": 0,
                "total_size_mb": 0,
                "backup_files": 0,
                "backup_size_mb": 0,
                "storage_health": "良好"
            },
            "main_folder": {},
            "backup_folder": {},
            "file_types": {},
            "recent_activity": []
        }
        
        try:
            # 主資料夾統計
            main_stats = self.get_file_statistics()
            stats["main_folder"] = main_stats
            stats["summary"]["total_files"] = main_stats["total_files"]
            stats["summary"]["total_size_mb"] = round(main_stats["total_size"] / (1024 * 1024), 2)
            
            # 備份資料夾統計
            if self.enable_backup and self.backup_folder.exists():
                backup_size = self.get_folder_size(self.backup_folder)
                backup_files = len(list(self.backup_folder.rglob("*.*")))
                stats["backup_folder"] = {
                    "total_files": backup_files,
                    "total_size": backup_size
                }
                stats["summary"]["backup_files"] = backup_files
                stats["summary"]["backup_size_mb"] = round(backup_size / (1024 * 1024), 2)
            
            # 檔案類型統計
            stats["file_types"] = main_stats.get("file_types", {})
            
            # 近期活動（最近7天修改的檔案）
            recent_cutoff = time.time() - (7 * 24 * 3600)
            recent_files = []
            
            for file_path in self.base_folder.rglob("*.*"):
                if file_path.is_file() and file_path.stat().st_mtime > recent_cutoff:
                    recent_files.append({
                        "path": str(file_path.relative_to(self.base_folder)),
                        "time": datetime.fromtimestamp(file_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                        "size": self._format_size(file_path.stat().st_size)
                    })
            
            # 按時間排序（最新的在前）
            recent_files.sort(key=lambda x: x["time"], reverse=True)
            stats["recent_activity"] = recent_files[:10]  # 只顯示最近10個
            
            # 儲存健康評估
            total_size_mb = stats["summary"]["total_size_mb"]
            if total_size_mb > 1000:
                stats["summary"]["storage_health"] = "需要清理"
            elif total_size_mb > 500:
                stats["summary"]["storage_health"] = "注意"
            else:
                stats["summary"]["storage_health"] = "良好"
            
        except Exception as e:
            self.logger.error(f"取得全面統計時發生錯誤: {e}")
        
        return stats
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化檔案大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def optimize_storage(self) -> Dict:
        """
        優化儲存空間
        
        Returns:
            優化結果報告
        """
        report = {
            "actions_taken": [],
            "space_freed_mb": 0,
            "files_cleaned": 0,
            "recommendations": []
        }
        
        try:
            initial_size = self.get_folder_size(self.base_folder)
            
            # 1. 清理過期備份
            if self.enable_backup:
                cleaned_backups = self.clean_old_backups()
                if cleaned_backups:
                    report["actions_taken"].append(f"清理了 {len(cleaned_backups)} 個過期備份檔案")
                    report["files_cleaned"] += len(cleaned_backups)
            
            # 2. 清理重複的日誌檔案（保留最新3個）
            cleaned_logs = self.clean_old_files("*.log", keep_latest=3, older_than_days=30)
            if cleaned_logs:
                report["actions_taken"].append(f"清理了 {len(cleaned_logs)} 個舊日誌檔案")
                report["files_cleaned"] += len(cleaned_logs)
            
            # 3. 清理臨時檔案
            temp_patterns = ["*.tmp", "*.temp", "*~"]
            for pattern in temp_patterns:
                cleaned_temp = self.clean_old_files(pattern, keep_latest=0)
                if cleaned_temp:
                    report["actions_taken"].append(f"清理了 {len(cleaned_temp)} 個臨時檔案 ({pattern})")
                    report["files_cleaned"] += len(cleaned_temp)
            
            # 計算釋放的空間
            final_size = self.get_folder_size(self.base_folder)
            space_freed = max(0, initial_size - final_size)
            report["space_freed_mb"] = round(space_freed / (1024 * 1024), 2)
            
            # 提供建議
            stats = self.get_comprehensive_statistics()
            if stats["summary"]["total_size_mb"] > 500:
                report["recommendations"].append("考慮清理較舊的資料檔案")
            
            if stats["summary"]["backup_size_mb"] > 200:
                report["recommendations"].append("考慮調整備份保留策略")
            
            large_files = []
            for file_path in self.base_folder.rglob("*.*"):
                if file_path.is_file() and file_path.stat().st_size > 50 * 1024 * 1024:  # 50MB
                    large_files.append(file_path.name)
            
            if large_files:
                report["recommendations"].append(f"檢查大型檔案: {', '.join(large_files[:3])}")
            
        except Exception as e:
            self.logger.error(f"優化儲存時發生錯誤: {e}")
            report["actions_taken"].append(f"優化過程中發生錯誤: {e}")
        
        return report


# 使用範例
def demo_file_manager():
    """演示檔案管理器的使用"""
    print("🗂️ 智慧檔案管理器演示")
    
    # 建立檔案管理器
    manager = SmartFileManager(
        base_folder="./test_data",
        enable_backup=True,
        backup_days=7,
        max_backup_size_mb=100
    )
    
    # 取得統計資訊
    stats = manager.get_comprehensive_statistics()
    print(f"\n📊 統計資訊:")
    print(f"總檔案數: {stats['summary']['total_files']}")
    print(f"總大小: {stats['summary']['total_size_mb']} MB")
    print(f"儲存健康: {stats['summary']['storage_health']}")
    
    # 執行儲存優化
    optimization_report = manager.optimize_storage()
    print(f"\n🔧 優化結果:")
    print(f"執行的動作: {optimization_report['actions_taken']}")
    print(f"釋放空間: {optimization_report['space_freed_mb']} MB")
    print(f"清理檔案數: {optimization_report['files_cleaned']}")
    
    if optimization_report['recommendations']:
        print(f"建議: {optimization_report['recommendations']}")


if __name__ == "__main__":
    demo_file_manager()