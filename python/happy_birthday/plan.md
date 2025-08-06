# Python + Flutter 跨平台開發計劃

## 架構選擇

### 選項 1: Flutter 前端 + Python 後端（推薦）
- **Flutter**：處理 UI 和用戶體驗
- **Python**：提供 API 後端服務
- **部署**：Flutter 編譯成各平台原生應用 + Web，Python 作為服務端

### 選項 2: Flutter Web 應用
- 純 Flutter Web 應用（類似網站）
- Python 提供後端 API 服務

## 需要的環境和工具

### 1. 開發環境設置

**Flutter 環境：**
```bash
# Flutter SDK
# Android Studio (Android 開發)
# Xcode (iOS 開發，需 macOS)
# Visual Studio (Windows 桌面應用)
```

**Python 環境：**
```bash
# Python 3.8+
# 虛擬環境管理工具
```

### 2. 必要套件

**Python 後端套件：**
```python
# Web 框架
fastapi          # 現代 API 框架（推薦）
# 或 flask       # 輕量級框架
# 或 django      # 全功能框架

# 資料庫
sqlalchemy      # ORM
alembic         # 資料庫遷移
# 或 django ORM

# 其他常用
pydantic        # 資料驗證
uvicorn         # ASGI 伺服器
requests        # HTTP 請求
python-jose     # JWT 處理
passlib         # 密碼加密
```

**Flutter 套件：**
```yaml
dependencies:
  http: ^0.13.5           # HTTP 請求
  dio: ^5.3.2            # 更強大的 HTTP 客戶端
  provider: ^6.0.5        # 狀態管理
  shared_preferences: ^2.2.2  # 本地儲存
  sqflite: ^2.3.0        # SQLite 資料庫
  flutter_secure_storage: ^9.0.0  # 安全儲存
```

## 詳細實現流程

### Phase 1: 環境準備
1. **安裝 Flutter SDK**
2. **設置各平台開發環境**
3. **創建 Python 虛擬環境**
4. **設置資料庫（PostgreSQL/MySQL/SQLite）**

### Phase 2: 後端開發 (Python)
```python
# 使用 FastAPI 範例
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允許跨域請求（供 Flutter 調用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from Python backend!"}
```

### Phase 3: 前端開發 (Flutter)
```dart
// HTTP 請求處理
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  static Future<Map<String, dynamic>> fetchData() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/hello'),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }
}
```

### Phase 4: 跨平台部署

**各平台編譯：**
```bash
# Android
flutter build apk --release

# iOS (需要 macOS)
flutter build ios --release

# Windows
flutter build windows --release

# macOS (需要 macOS)
flutter build macos --release

# Linux
flutter build linux --release

# Web
flutter build web --release
```

## 專案結構建議

```
your_project/
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
```

## 開發建議

1. **先從簡單功能開始**：實現基本的資料傳輸
2. **使用狀態管理**：Provider 或 Riverpod
3. **API 設計**：RESTful API 設計原則
4. **測試**：單元測試和整合測試
5. **部署**：考慮使用 Docker 容器化

## 支援平台

- ✅ **Windows**：Flutter Desktop + Python 後端
- ✅ **Android**：Flutter Android + Python 後端
- ✅ **Linux**：Flutter Desktop + Python 後端  
- ✅ **iOS**：Flutter iOS + Python 後端（需 macOS 開發）
- ✅ **macOS**：Flutter Desktop + Python 後端（需 macOS 開發）
- ✅ **Web**：Flutter Web + Python 後端

## 開發階段規劃

### 第一階段：基礎設置
- [ ] 安裝並配置 Flutter 開發環境
- [ ] 設置 Python 開發環境
- [ ] 創建基本專案結構

### 第二階段：後端開發
- [ ] 創建 FastAPI 基礎應用
- [ ] 設計並實現基本 API 端點
- [ ] 設置資料庫和模型

### 第三階段：前端開發
- [ ] 創建 Flutter 應用基礎架構
- [ ] 實現與後端的 API 通信
- [ ] 設計用戶界面

### 第四階段：跨平台測試
- [ ] 在各目標平台測試應用
- [ ] 修復平台特定問題
- [ ] 優化性能

### 第五階段：部署和發布
- [ ] 準備各平台的發布版本
- [ ] 設置後端服務器部署
- [ ] 發布到各平台應用商店

## 階段式開發策略（先 Windows + Android，後 macOS + iOS）

### ✅ 可行性分析
這個策略**完全可行**且**推薦**，原因如下：

1. **Flutter 核心代碼 99% 共用**：大部分業務邏輯、UI 組件、狀態管理都可以直接復用
2. **Python 後端完全通用**：後端 API 對所有平台都是相同的
3. **降低初期復雜度**：先專注在兩個平台，減少環境配置負擔
4. **漸進式開發**：可以先驗證核心功能，再擴展到其他平台

### 🔄 後續擴展流程

**第一階段：Windows + Android 開發**
```bash
# 只需要安裝這些
- Flutter SDK
- Android Studio + Android SDK
- Visual Studio 2019+ (Windows desktop)
- Python 環境
```

**第二階段：添加 macOS + iOS（需要 Mac 電腦）**
```bash
# 在 Mac 上額外安裝
- Xcode (iOS 開發)
- CocoaPods (iOS 依賴管理)
# 然後直接運行
flutter build ios
flutter build macos
```

### 📋 需要注意的事項

#### 1. 程式碼結構建議
```dart
// 平台特定代碼隔離
lib/
├── main.dart
├── core/              # 共用核心邏輯
├── screens/           # 共用 UI 畫面
├── services/          # 共用服務
└── platform/          # 平台特定代碼
    ├── android/
    ├── ios/
    ├── windows/
    └── macos/
```

#### 2. 可能需要平台特定處理的功能
- **文件路徑**：Windows 使用 `\`，其他使用 `/`
- **網絡權限**：Android 需要網絡權限聲明
- **本地存儲位置**：各平台的文件系統結構不同
- **推送通知**：iOS 和 Android 有不同的實現方式

#### 3. 避免後期問題的建議

**A. 使用跨平台套件：**
```yaml
dependencies:
  path_provider: ^2.1.1    # 跨平台路徑處理
  connectivity_plus: ^4.0.2 # 跨平台網絡檢測
  device_info_plus: ^9.1.0  # 跨平台設備資訊
```

**B. 條件編譯處理：**
```dart
import 'dart:io' show Platform;

if (Platform.isIOS) {
  // iOS 特定邏輯
} else if (Platform.isAndroid) {
  // Android 特定邏輯
} else if (Platform.isWindows) {
  // Windows 特定邏輯
}
```

**C. 抽象化平台差異：**
```dart
abstract class PlatformService {
  Future<String> getDeviceId();
  Future<void> showNotification(String message);
}

class AndroidPlatformService implements PlatformService { ... }
class IOSPlatformService implements PlatformService { ... }
```

### 🎯 推薦的開發順序

1. **第一階段：核心功能 (Windows + Android)**
   - [ ] 建立基本專案架構
   - [ ] 實現核心業務邏輯
   - [ ] 完成主要 UI 界面
   - [ ] Python 後端 API 開發
   - [ ] Windows 和 Android 測試

2. **第二階段：擴展到 Apple 生態系 (需要 Mac)**
   - [ ] 在 Mac 環境下 clone 專案
   - [ ] 運行 `flutter build ios` 和 `flutter build macos`
   - [ ] 處理平台特定問題（通常很少）
   - [ ] iOS 和 macOS 測試

### 💡 額外建議

1. **版本控制**：使用 Git，這樣在不同環境下開發很方便
2. **CI/CD**：可以設置 GitHub Actions 自動化構建各平台
3. **測試策略**：先在 Android 和 Windows 充分測試，再移植到其他平台
4. **依賴選擇**：優先選擇支持所有平台的套件

這種策略很多成功的 Flutter 專案都在使用，你完全可以放心採用！

## 🌐 免費部署方案

### 🎯 推薦方案組合

**方案一：Vercel + Railway（推薦）**
```
Flutter Web (前端) → Vercel (免費)
Python API (後端) → Railway (免費額度)
資料庫 → PostgreSQL on Railway (免費)
```

**方案二：Netlify + Render**
```
Flutter Web (前端) → Netlify (免費)
Python API (後端) → Render (免費額度)
資料庫 → PostgreSQL on Render (免費)
```

**方案三：GitHub Pages + PythonAnywhere**
```
Flutter Web (前端) → GitHub Pages (免費)
Python API (後端) → PythonAnywhere (免費額度)
資料庫 → SQLite 或 PythonAnywhere MySQL (免費)
```

### 📋 各服務詳細比較

#### 前端部署（Flutter Web）

**1. Vercel（推薦）**
- ✅ **完全免費**
- ✅ 自動 HTTPS
- ✅ 全球 CDN
- ✅ 自動部署（Git 整合）
- ✅ 自定義域名支援
- 限制：100GB 頻寬/月

**2. Netlify**
- ✅ 完全免費
- ✅ 自動 HTTPS
- ✅ 全球 CDN
- ✅ 自動部署（Git 整合）
- 限制：100GB 頻寬/月

**3. GitHub Pages**
- ✅ 完全免費
- ✅ 自動 HTTPS（github.io 域名）
- ✅ Git 整合
- ❌ 僅靜態網站
- 限制：1GB 儲存空間

#### 後端部署（Python API）

**1. Railway（推薦）**
- ✅ 免費：$5/月 額度
- ✅ 支援 FastAPI/Flask/Django
- ✅ PostgreSQL 資料庫內建
- ✅ 自動部署
- ✅ HTTPS 自動配置
- 限制：每月 $5 額度用完後暫停

**2. Render**
- ✅ 免費方案
- ✅ 支援 Python
- ✅ PostgreSQL 資料庫
- ✅ 自動部署
- ❌ 免費版會休眠（15分鐘不活動）

**3. PythonAnywhere**
- ✅ 免費方案
- ✅ Python 專門平台
- ✅ MySQL 資料庫（100MB）
- ❌ 免費版有限制（CPU秒數）

**4. Heroku替代方案（已不免費）**
- ❌ Heroku 2022年底停止免費方案
- 建議轉用上述替代方案

### 🚀 部署步驟

#### Step 1: Flutter Web 部署到 Vercel

```bash
# 1. 建置 Flutter Web
flutter build web

# 2. 在專案根目錄創建 vercel.json
{
  "buildCommand": "flutter build web",
  "outputDirectory": "build/web",
  "installCommand": "wget -O- https://raw.githubusercontent.com/flutter/flutter/master/bin/install_flutter.sh | bash"
}

# 3. 推送到 GitHub
# 4. 在 Vercel 連接 GitHub repo
# 5. 自動部署完成
```

#### Step 2: Python API 部署到 Railway

```bash
# 1. 創建 requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23

# 2. 創建 main.py (FastAPI 應用)
# 3. 創建 railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"

# 4. 推送到 GitHub
# 5. 在 Railway 連接 GitHub repo
# 6. 自動部署完成
```

### 💡 成本分析

**完全免費方案（小型專案）：**
- Vercel: 免費
- Railway: $5/月 免費額度（通常夠用）
- **總成本：$0/月**

**付費升級（高流量時）：**
- Vercel Pro: $20/月
- Railway: 用多少付多少
- **總成本：約 $25-50/月**

### 🔧 技術建議

**1. API 網址配置：**
```dart
// Flutter 中設定不同環境的 API 網址
class ApiConfig {
  static const String baseUrl = 
    kDebugMode 
      ? 'http://localhost:8000'  // 開發環境
      : 'https://your-api.railway.app';  // 生產環境
}
```

**2. 環境變數管理：**
```python
# Python 後端設定
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

**3. CORS 設定：**
```python
# 允許 Flutter Web 跨域請求
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-flutter-app.vercel.app",
        "http://localhost:3000"  # 開發時使用
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🐳 Docker 容器化方案

### 🎯 為什麼要使用 Docker？

**主要優勢：**
1. **環境一致性**：開發、測試、生產環境完全相同
2. **簡化部署**：一鍵部署到任何支援 Docker 的平台
3. **易於擴展**：水平擴展和負載均衡更簡單
4. **隔離性**：避免環境衝突和依賴問題
5. **版本控制**：Docker 映像版本管理
6. **微服務架構**：前端、後端、資料庫可獨立部署

### 📦 Docker 架構設計

```
專案結構（Docker 版本）
├── docker-compose.yml      # 服務編排
├── .env                   # 環境變數
├── backend/
│   ├── Dockerfile         # Python API 容器
│   ├── requirements.txt
│   └── app/
├── frontend/
│   ├── Dockerfile         # Flutter Web 容器
│   └── lib/
├── nginx/
│   ├── Dockerfile         # Nginx 反向代理
│   └── nginx.conf
└── database/
    └── init.sql           # 資料庫初始化
```

### 🔧 Docker 配置檔案

#### 1. docker-compose.yml（主要編排檔案）
```yaml
version: '3.8'

services:
  # PostgreSQL 資料庫
  database:
    image: postgres:15
    container_name: happy_birthday_db
    environment:
      POSTGRES_DB: happy_birthday
      POSTGRES_USER: ${DB_USER:-admin}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - app-network

  # Python 後端 API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: happy_birthday_api
    environment:
      DATABASE_URL: postgresql://${DB_USER:-admin}:${DB_PASSWORD:-password}@database:5432/happy_birthday
      DEBUG: ${DEBUG:-false}
    depends_on:
      - database
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    networks:
      - app-network

  # Flutter Web 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: happy_birthday_web
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - app-network

  # Nginx 反向代理
  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    container_name: happy_birthday_nginx
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - frontend
      - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

#### 2. backend/Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 暴露端口
EXPOSE 8000

# 啟動命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### 3. frontend/Dockerfile
```dockerfile
# 階段 1: 建置 Flutter Web
FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app

# 複製 pubspec 檔案並安裝依賴
COPY pubspec.* ./
RUN flutter pub get

# 複製源代碼並建置
COPY . .
RUN flutter build web --release

# 階段 2: Nginx 服務
FROM nginx:alpine

# 複製建置結果到 nginx
COPY --from=build /app/build/web /usr/share/nginx/html

# 複製 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### 4. nginx/nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # 前端靜態檔案
        location / {
            proxy_pass http://frontend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # API 請求轉發到後端
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # 健康檢查
        location /health {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
```

### 🚀 Docker 開發流程

#### 開發環境啟動：
```bash
# 1. 啟動所有服務
docker-compose up -d

# 2. 查看運行狀態
docker-compose ps

# 3. 查看日誌
docker-compose logs -f backend

# 4. 停止服務
docker-compose down
```

#### 生產環境部署：
```bash
# 1. 建置生產映像
docker-compose -f docker-compose.prod.yml build

# 2. 啟動生產服務
docker-compose -f docker-compose.prod.yml up -d

# 3. 擴展服務（如需要）
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### 🌐 容器化部署方案

#### 方案一：Docker + 雲端平台
```
前端容器 → Vercel (支援 Docker)
後端容器 → Railway/Render (Docker 部署)
資料庫 → 託管 PostgreSQL
```

#### 方案二：完整容器化部署
```
整個應用 → DigitalOcean App Platform (Docker)
整個應用 → Google Cloud Run (Docker)
整個應用 → AWS ECS (Docker)
```

#### 方案三：自託管 VPS
```
整個 Docker Compose → VPS (Ubuntu/CentOS)
使用 Traefik 作為反向代理和 SSL 終端
```

### 💡 Docker 最佳實踐

**1. 多階段建置：**
- 減少映像大小
- 分離建置和運行環境

**2. 環境變數管理：**
```bash
# .env 檔案
DB_USER=admin
DB_PASSWORD=your_secure_password
DEBUG=false
API_BASE_URL=https://your-api.com
```

**3. 健康檢查：**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

**4. 日誌管理：**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 📊 Docker vs 傳統部署比較

| 功能 | 傳統部署 | Docker 部署 |
|------|----------|-------------|
| 環境一致性 | ❌ 困難 | ✅ 完美 |
| 部署速度 | ⚠️ 中等 | ✅ 很快 |
| 擴展性 | ❌ 複雜 | ✅ 簡單 |
| 回滾 | ⚠️ 手動 | ✅ 一鍵 |
| 資源隔離 | ❌ 無 | ✅ 完整 |
| 學習成本 | ✅ 低 | ⚠️ 中等 |

### 🎯 建議採用策略

**階段一：先傳統部署**
- 快速驗證功能
- 降低初期複雜度

**階段二：引入 Docker**
- 功能穩定後容器化
- 提升部署和維護效率

**階段三：微服務化**
- 業務複雜後拆分服務
- 獨立擴展不同組件

1. **iOS 開發需要 macOS**：如果要開發 iOS 應用，必須在 macOS 環境下進行
2. **跨平台考量**：某些功能可能在不同平台有差異，需要針對性處理
3. **網絡請求**：需要處理不同平台的網絡權限和安全策略
4. **資料存儲**：考慮離線功能和本地資料同步
5. **階段式開發**：建議先完成 Windows + Android，再擴展到 macOS + iOS