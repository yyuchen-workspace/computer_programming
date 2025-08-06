# Happy Birthday 專案

## 專案概述
這是一個 Python 生日快樂專案。

## 開發環境
Flutter 前端 + Python 後端
- **Flutter**：處理 UI 和用戶體驗
- **Python**：提供 API 後端服務
- **部署**：Flutter 編譯成各平台原生應用 + Web，Python 作為服務端

## 專案結構
happy_birthday/
├── backend/                 # Python 後端
│   ├── app/
│   │   ├── main.py         # FastAPI 主程式
│   │   ├── models/         # 資料模型
│   │   ├── routers/        # API 路由
│   │   └── database.py     # 資料庫設定
│   ├── requirements.txt
│   └── .env
├── frontend/               # Flutter 前端
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/        # 頁面
│   │   ├── services/       # API 服務
│   │   └── models/         # 資料模型
│   └── pubspec.yaml
└── README.md

## 功能需求

### 🎯 網站核心功能

**主頁面功能：**
1. 可自訂網站背景圖片（用戶可上傳更換）
2. 顯示「請點擊此連結」字樣的按鈕
3. 點擊按鈕跳轉到第二個頁面

**第二頁面功能：**
4. 可自訂頁面標題
5. 可自訂背景圖片
6. 動態互動人物系統：
   - 展示人物圖片
   - 點擊人物可切換成不同圖片
   - 點擊顯示不同的對話框內容
   - 人物狀態和表情管理

**管理功能：**
7. 後台管理系統（上傳圖片、編輯內容）
8. 預覽功能
9. 響應式設計（手機、平板、電腦適配）


## 支援平台

- ✅ **Windows**：Flutter Desktop + Python 後端
- ✅ **Android**：Flutter Android + Python 後端
- ✅ **Linux**：Flutter Desktop + Python 後端  
- ✅ **Web**：Flutter Web + Python 後端



## 開發偏好
- 程式碼風格：
- 測試方式：
- 文件語言：繁體中文
