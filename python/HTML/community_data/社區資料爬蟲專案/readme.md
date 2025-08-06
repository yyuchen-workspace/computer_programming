# 社區資料爬蟲 (增強版)

一個用於爬取台灣社區資料的 Python GUI 應用程式，具備自動排程、資料比對、更新日誌等功能。

## 🆕 新功能

### 1. 城市資料夾顯示筆數
- 城市資料夾名稱現在會包含資料筆數，例如：`新北市(4776筆資料)`
- 更容易識別各城市的資料規模

### 2. 每週自動排程
- 可設定每週固定時間自動執行爬取
- 支援自訂星期幾和時間
- 背景執行，不影響其他操作

### 3. 資料比對與更新日誌
- 每次爬取後自動比對新舊資料
- 將新增項目記錄到時間戳記的更新日誌中
- 例如：`2025-07-02-23:00資料更新日誌.txt`

### 4. 增強的 GUI 介面
- 分頁式介面，功能分類更清楚
- 排程設定分頁
- 更新日誌檢視分頁
- 設定儲存與載入功能

## 📦 安裝

### 1. 克隆或下載專案
```bash
git clone <repository_url>
cd community-scraper
```

### 2. 安裝必要套件
```bash
pip install -r requirements.txt
```

### 3. 執行程式
```bash
# 執行 GUI 版本
python gui_app.py

# 或執行主程式
python main.py

# 執行獨立排程器
python scheduled_scraper.py
```

## 🖥️ GUI 使用說明

### 爬取設定分頁
1. **選擇輸出資料夾**：點擊「瀏覽」選擇資料儲存位置
2. **選擇城市和區域**：從下拉選單選擇要爬取的目標
3. **選擇爬取模式**：
   - 單一區域
   - 單一城市（分區）
   - 全部城市（分區）
4. **啟用資料比對**：勾選後會自動產生更新日誌

### 排程設定分頁
1. **啟用自動排程**：勾選「啟用自動排程」
2. **設定執行時間**：選擇星期幾和時間
3. **選擇排程模式**：選擇要定期執行的爬取模式
4. **檢視排程狀態**：顯示下次執行時間

### 更新日誌分頁
1. **檢視日誌列表**：顯示所有更新日誌資料夾
2. **點擊查看內容**：選擇日誌項目查看詳細內容
3. **重新整理**：更新日誌列表

## 🤖 獨立排程器使用

### 1. 建立設定檔
```bash
python scheduled_scraper.py --create-config
```

### 2. 編輯設定檔 `scraper_config.json`
```json
{
  "schedule": {
    "enabled": true,
    "day_of_week": "monday",
    "time": "02:00",
    "timezone": "Asia/Taipei"
  },
  "scraping": {
    "mode": "all_cities_with_districts",
    "output_folder": "./scraped_data",
    "max_retries": 3,
    "retry_delay": 300
  },
  "logging": {
    "log_file": "scraper_schedule.log",
    "log_level": "INFO"
  },
  "notifications": {
    "enabled": false,
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your_email@gmail.com",
      "password": "your_app_password",
      "to_addresses": ["admin@example.com"]
    }
  }
}
```

### 3. 執行排程器
```bash
# 背景執行排程器
python scheduled_scraper.py

# 立即執行一次後結束
python scheduled_scraper.py --run-once
```

## 📁 檔案結構

```
community-scraper/
├── gui_app.py              # 主要 GUI 應用程式
├── main.py                 # 程式進入點
├── scraper.py              # 爬蟲核心邏輯
├── scheduled_scraper.py    # 獨立排程器
├── requirements.txt        # 必要套件清單
├── README.md              # 使用說明
├── gui_config.json        # GUI 設定檔 (自動生成)
├── scraper_config.json    # 排程器設定檔 (自動生成)
└── scraped_data/          # 預設輸出資料夾
    ├── 新北市(4776筆資料)/
    ├── 台北市(3245筆資料)/
    └── 資料更新日誌/
        ├── 2025-07-02資料更新日誌.txt
        ├── 2025-07-03資料更新日誌.txt
        └── 2025-07-04資料更新日誌.txt
```

## 📝 更新日誌格式

更新日誌檔案包含以下資訊：
- 檔案位置：`scraped_data/資料更新日誌/YYYY-MM-DD資料更新日誌.txt`
- 內容格式：
  ```
  資料更新日誌 - 2025-07-02 14:30:25
  ==================================================
  
  檔案: 新北市板橋區社區資料(共有500筆).txt
  新增項目數量: 3
  ------------------------------
  + 新社區名稱A
  + 新社區名稱B
  + 新社區名稱C
  
  檔案: 台北市大安區社區資料(共有300筆).txt
  新增項目數量: 1
  ------------------------------
  + 新社區名稱D
  
  總計新增項目: 4 筆
  ```

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 啟動 GUI
```bash
python gui_app.py
```

### 3. 基本使用流程
1. 選擇輸出資料夾
2. 等待城市資料載入完成
3. 選擇要爬取的城市和區域
4. 點擊「開始爬取」
5. 查看「更新日誌」分頁檢視新增項目

## 🔧 進階功能

### 自動排程設定
1. 切換到「排程設定」分頁
2. 勾選「啟用自動排程」
3. 設定執行時間（例如：每週一 02:00）
4. 選擇排程爬取模式
5. 點擊「儲存設定」

### 獨立排程器
```bash
# 建立設定檔
python scheduled_scraper.py --create-config

# 編輯 scraper_config.json 後執行
python scheduled_scraper.py

# 立即執行一次
python scheduled_scraper.py --run-once
```

## 💡 使用技巧

### 1. 批次爬取建議
- 使用「爬取全部城市（資料分區）」模式可獲得最完整的資料
- 建議在網路流量較低的時間執行（如凌晨 2-4 點）

### 2. 更新日誌活用
- 定期檢查更新日誌，了解新增的社區資料
- 可結合排程功能，每週自動爬取並比對差異

### 3. 資料夾命名規則
- 城市資料夾：`城市名(筆數筆資料)`
- 區域檔案：`城市名區域名社區資料(共有筆數筆).txt`
- 更新日誌：`YYYY-MM-DD資料更新日誌.txt`

## 🐛 常見問題

### Q: 城市資料載入失敗？
A: 檢查網路連線，確保能正常訪問目標網站。

### Q: 排程沒有執行？
A: 確認排程設定正確，程式需要保持運行狀態。

### Q: 更新日誌顯示空白？
A: 表示沒有新增項目，或是第一次爬取該區域資料。

### Q: 爬取速度很慢？
A: 程式已內建延遲機制避免對伺服器造成負擔，這是正常現象。

## 📞 技術支援

如有問題或建議，請提供以下資訊：
- 作業系統版本
- Python 版本
- 錯誤訊息截圖
- 設定檔內容

## 📄 授權條款

本專案僅供學習研究使用，請遵守相關網站的使用條款。