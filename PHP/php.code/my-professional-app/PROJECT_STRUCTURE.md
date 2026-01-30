# 📋 專案結構說明文件

## 專案概述

**專案名稱**: My Professional App
**框架版本**: Laravel 12.0
**PHP 版本**: 8.2+
**開發環境**: Laravel Sail (Docker)
**專案類型**: 遊戲英雄攻略系統

這是一個使用 Laravel 框架開發的遊戲英雄資料庫與攻略系統，結合物件導向設計模式，提供英雄資料管理和攻略文章功能。

---

## 📁 目錄結構總覽

```
my-professional-app/
├── app/                      # 應用程式核心代碼
│   ├── Game/                 # 🎮 遊戲相關類別（自訂）
│   ├── Http/                 # HTTP 層（控制器、中間件）
│   ├── Models/               # Eloquent 資料模型
│   ├── Providers/            # 服務提供者
│   └── Console/              # Artisan 命令
├── bootstrap/                # 框架啟動檔案
├── config/                   # 設定檔
├── database/                 # 資料庫相關
│   ├── migrations/           # 資料庫遷移檔
│   ├── seeders/              # 資料填充
│   └── factories/            # 模型工廠
├── public/                   # 公開訪問目錄（網站根目錄）
├── resources/                # 前端資源
│   └── views/                # Blade 模板
├── routes/                   # 路由定義
├── storage/                  # 檔案存儲
├── tests/                    # 測試檔案
├── vendor/                   # Composer 依賴套件
├── .env                      # 環境變數設定
├── compose.yaml              # Docker Compose 配置
└── composer.json             # PHP 依賴管理

```

---

## 🎯 核心功能模組

### 1. 遊戲系統模組 (`app/Game/`)

這是**自訂的遊戲邏輯模組**，實現了物件導向的英雄系統。

#### 檔案說明：

**[Hero.php](app/Game/Hero.php)** - 英雄類別
```php
class Hero
{
    public $name;      // 英雄名稱
    public $stats;     // 數值物件 (Stats)
    public $skills;    // 技能陣列 (Skill[])
    public $article;   // 攻略文章
}
```
- **作用**: 定義英雄物件的資料結構
- **設計模式**: 值物件（Value Object）

**[Stats.php](app/Game/Stats.php)** - 數值類別
```php
class Stats
{
    private $hp;   // 生命值
    private $mp;   // 魔力值
    private $atk;  // 攻擊力
    private $def;  // 防禦力
}
```
- **作用**: 封裝英雄的屬性數值
- **特點**: 使用 getter 方法提供數據訪問

**[Skill.php](app/Game/Skill.php)** - 技能類別
```php
class Skill
{
    public $name;         // 技能名稱
    public $description;  // 技能說明
}
```
- **作用**: 定義技能的資料結構

**[HeroFactory.php](app/Game/HeroFactory.php)** - 英雄工廠
```php
class HeroFactory
{
    public static function createKrixi(): Hero
    public static function createVane(): Hero
    public static function create(string $heroName): ?Hero
    public static function getAllHeroes(): array
}
```
- **作用**: 集中管理英雄物件的建立
- **設計模式**: 工廠模式（Factory Pattern）
- **支援英雄**: 克里希 (Krixi)、凡恩 (Vane)
- **特色**: 支援中英文名稱查詢

---

### 2. HTTP 控制器層 (`app/Http/Controllers/`)

**[GameController.php](app/Http/Controllers/GameController.php)** - 遊戲控制器

提供三個主要 API 端點：

| 方法 | 路由 | 功能 |
|------|------|------|
| `testDebug()` | GET `/test-debug` | 測試除錯端點，展示克里希資料 |
| `index()` | GET `/heroes` | 顯示所有英雄列表 |
| `show($heroName)` | GET `/heroes/{heroName}` | 顯示特定英雄詳細資訊 |

**特色功能**:
- ✅ 支援中英文英雄名稱查詢
- ✅ JSON 格式回應
- ✅ 包含除錯示範代碼
- ✅ 錯誤處理與提示

---

### 3. 資料模型層 (`app/Models/`)

**[Guide.php](app/Models/Guide.php)** - 攻略模型

```php
class Guide extends Model
{
    protected $fillable = [
        'title',       // 攻略標題
        'hero_name',   // 英雄名稱
        'content',     // 攻略內容
        'author',      // 作者
        'views',       // 瀏覽次數
    ];
}
```

- **資料表**: `guides`
- **作用**: 管理遊戲英雄攻略文章
- **特性**:
  - 可批量賦值（Mass Assignment）
  - 自動時間戳記（created_at, updated_at）
  - 整數類型轉換（views 欄位）

**[User.php](app/Models/User.php)** - 使用者模型
- Laravel 預設的使用者認證模型
- 支援密碼加密、記住我功能

---

### 4. 資料庫遷移 (`database/migrations/`)

**現有遷移檔案**:

1. **[0001_01_01_000000_create_users_table.php](database/migrations/0001_01_01_000000_create_users_table.php)**
   - 建立 `users` 表（使用者系統）

2. **[0001_01_01_000001_create_cache_table.php](database/migrations/0001_01_01_000001_create_cache_table.php)**
   - 建立快取相關資料表

3. **[0001_01_01_000002_create_jobs_table.php](database/migrations/0001_01_01_000002_create_jobs_table.php)**
   - 建立佇列任務資料表

4. **[2026_01_30_065602_create_guides_table.php](database/migrations/2026_01_30_065602_create_guides_table.php)**
   - 建立 `guides` 攻略資料表
   ```sql
   - id (主鍵)
   - title (標題)
   - hero_name (英雄名稱)
   - content (內容)
   - author (作者，可為空)
   - views (瀏覽次數，預設0)
   - created_at, updated_at (時間戳)
   ```

---

### 5. 路由定義 (`routes/`)

**[web.php](routes/web.php)** - 網頁路由

```php
// 首頁
GET /                    → welcome 視圖

// 問候頁面
GET /hello              → greeting 視圖

// 遊戲相關路由
GET /test-debug         → GameController@testDebug
GET /heroes             → GameController@index
GET /heroes/{heroName}  → GameController@show
```

**路由特色**:
- 支援 RESTful API 設計
- 中英文參數支援（如: `/heroes/krixi` 或 `/heroes/克里希`）

---

## 🐳 Docker 環境配置

### Sail 服務容器 ([compose.yaml](compose.yaml))

| 服務名稱 | 映像 | 端口 | 用途 |
|---------|------|------|------|
| **laravel.test** | sail-8.5/app | 80, 5173 | PHP 應用主容器 |
| **mysql** | mysql:8.4 | 3306 | MySQL 資料庫 |
| **redis** | redis:alpine | 6379 | 快取與 Session |
| **meilisearch** | getmeili/meilisearch | 7700 | 全文搜尋引擎 |
| **mailpit** | axllent/mailpit | 1025, 8025 | 郵件測試工具 |
| **selenium** | selenium/standalone-chromium | - | 瀏覽器測試 |

### 環境變數重點 ([.env](.env))

```env
# 應用設定
APP_NAME=Laravel
APP_ENV=local
APP_DEBUG=true

# 資料庫（使用 Docker 容器名稱）
DB_CONNECTION=mysql
DB_HOST=mysql           # ← Docker 服務名稱
DB_DATABASE=laravel
DB_USERNAME=sail
DB_PASSWORD=password

# Redis（使用 Docker 容器名稱）
REDIS_HOST=redis        # ← Docker 服務名稱

# Xdebug 除錯設定
SAIL_XDEBUG_MODE=develop,debug
SAIL_XDEBUG_CONFIG="client_host=192.168.5.23"

# 郵件測試
MAIL_HOST=mailpit
MAIL_PORT=1025

# 搜尋引擎
MEILISEARCH_HOST=http://meilisearch:7700
```

---

## 🛠️ 開發工具與設定

### VSCode 設定 ([.vscode/launch.json](.vscode/launch.json))

已配置 Xdebug 除錯功能，可以直接在 VSCode 中設置斷點進行除錯。

詳細設定請參考：
- [XDEBUG_SETUP.md](XDEBUG_SETUP.md) - Xdebug 初始設定指南
- [XDEBUG_FIX_GUIDE.md](XDEBUG_FIX_GUIDE.md) - Xdebug 問題排解
- [GUIDE_SYSTEM_SETUP.md](GUIDE_SYSTEM_SETUP.md) - 攻略系統設定說明

### Composer 腳本

```bash
# 完整專案設置
composer setup

# 開發模式（同時啟動多個服務）
composer dev

# 執行測試
composer test
```

---

## 📦 依賴套件

### 核心套件 (require)
- `laravel/framework: ^12.0` - Laravel 框架核心
- `laravel/tinker: ^2.10.1` - 互動式命令列工具

### 開發套件 (require-dev)
- `laravel/sail: ^1.41` - Docker 開發環境
- `laravel/pint: ^1.24` - 程式碼風格檢查
- `laravel/pail: ^1.2.2` - 即時日誌查看
- `phpunit/phpunit: ^11.5.3` - 單元測試框架
- `fakerphp/faker: ^1.23` - 假資料生成器

---

## 🚀 快速開始指令

```bash
# 1. 啟動 Docker 環境
./vendor/bin/sail up -d

# 2. 執行資料庫遷移
./vendor/bin/sail artisan migrate

# 3. 訪問應用
# 瀏覽器開啟: http://localhost

# 4. 測試 API 端點
curl http://localhost/heroes
curl http://localhost/heroes/krixi
curl http://localhost/test-debug

# 5. 查看 Mailpit (郵件測試介面)
# 瀏覽器開啟: http://localhost:8025

# 6. 停止環境
./vendor/bin/sail down
```

---

## 🎮 API 測試範例

### 取得所有英雄列表
```bash
GET http://localhost/heroes

# 回應範例
{
  "heroes": [
    {
      "name": "克里希",
      "hp": 3200,
      "atk": 180,
      "skills": ["蝶影穿花", "落葉歸根", "月落星沉"]
    },
    {
      "name": "凡恩",
      "hp": 100,
      "atk": 40,
      "skills": ["獵手", "血腥獵殺", "送葬詛咒", "水銀彈幕"]
    }
  ]
}
```

### 取得特定英雄資訊
```bash
GET http://localhost/heroes/克里希
# 或
GET http://localhost/heroes/krixi

# 回應範例
{
  "name": "克里希",
  "article": "克里希是一名強大的遠程消耗型法師。",
  "stats": {
    "hp": 3200,
    "mp": 500,
    "atk": 180,
    "def": 120
  },
  "skills": [...]
}
```

---

## 📝 專案特色

### ✨ 設計模式應用
- **工廠模式**: `HeroFactory` 集中管理物件建立
- **值物件**: `Hero`, `Stats`, `Skill` 封裝資料結構
- **MVC 架構**: 清晰的職責分離

### 🔧 開發體驗
- ✅ 完整的 Docker 開發環境
- ✅ Xdebug 除錯支援
- ✅ 熱重載（Vite）
- ✅ 郵件測試工具（Mailpit）
- ✅ 中英文雙語支援

### 📚 文檔完善
- 詳細的設定指南
- 程式碼註解完整
- API 使用範例

---

## 🔗 相關文件索引

- [README.md](README.md) - 專案說明
- [GUIDE_SYSTEM_SETUP.md](GUIDE_SYSTEM_SETUP.md) - 攻略系統設置指南
- [XDEBUG_SETUP.md](XDEBUG_SETUP.md) - Xdebug 設定教學
- [XDEBUG_FIX_GUIDE.md](XDEBUG_FIX_GUIDE.md) - Xdebug 疑難排解
- [compose.yaml](compose.yaml) - Docker 服務配置

---

## 📞 常用命令速查

```bash
# Sail 命令（前綴 ./vendor/bin/sail）
sail up -d              # 啟動環境
sail down               # 停止環境
sail artisan            # 執行 Artisan 命令
sail composer           # 執行 Composer
sail mysql              # 進入 MySQL CLI
sail redis              # 進入 Redis CLI
sail shell              # 進入容器 Shell

# Artisan 命令
sail artisan migrate              # 執行遷移
sail artisan migrate:fresh        # 重置並執行遷移
sail artisan make:model Guide     # 建立模型
sail artisan make:controller XXX  # 建立控制器
sail artisan route:list           # 查看所有路由
sail artisan tinker               # 進入互動式模式

# 測試命令
sail test                         # 執行測試
sail artisan test                 # 執行測試（替代）
```

---

## 📌 注意事項

1. **資料庫主機名稱**: 在 Docker 環境中使用 `mysql` 而非 `localhost`
2. **端口衝突**: 確保本機的 80、3306、6379 端口未被佔用
3. **Xdebug 設定**: 需要配置正確的 `client_host` IP 位址
4. **權限問題**: 如遇權限錯誤，檢查 `storage/` 目錄權限

---

**最後更新**: 2026-01-30
**維護者**: Professional App Team
