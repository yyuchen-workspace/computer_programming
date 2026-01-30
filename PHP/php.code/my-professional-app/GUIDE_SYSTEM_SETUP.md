# 📚 Laravel 攻略網系統建立教學

本文件提供完整的操作流程，讓您建立一個功能完整的遊戲攻略網站。

## 🎯 系統功能

- ✅ 顯示所有攻略列表
- ✅ 新增攻略（標題、英雄名稱、作者、內容）
- ✅ 查看攻略詳細內容
- ✅ 編輯現有攻略
- ✅ 刪除攻略
- ✅ 自動記錄瀏覽次數
- ✅ 資料驗證
- ✅ 響應式網頁設計

---

## 📋 操作步驟

### 步驟 1：建立資料表 Migration

執行以下指令創建 migration 檔案：

```bash
php artisan make:migration create_guides_table
```

找到生成的檔案 `database/migrations/xxxx_xx_xx_xxxxxx_create_guides_table.php`，將內容替換為：

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('guides', function (Blueprint $table) {
            $table->id();
            $table->string('title');                // 攻略標題
            $table->string('hero_name');            // 英雄名稱
            $table->text('content');                // 攻略內容
            $table->string('author')->nullable();   // 作者名稱
            $table->integer('views')->default(0);   // 瀏覽次數
            $table->timestamps();                   // created_at, updated_at
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('guides');
    }
};
```

---

### 步驟 2：建立 Guide Model

執行指令：

```bash
php artisan make:model Guide
```

編輯 `app/Models/Guide.php`：

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Guide extends Model
{
    protected $fillable = [
        'title',
        'hero_name',
        'content',
        'author',
        'views',
    ];

    protected $casts = [
        'views' => 'integer',
    ];
}
```

---

### 步驟 3：建立 GuideController

執行指令：

```bash
php artisan make:controller GuideController --resource
```

編輯 `app/Http/Controllers/GuideController.php`：

```php
<?php

namespace App\Http\Controllers;

use App\Models\Guide;
use Illuminate\Http\Request;

class GuideController extends Controller
{
    // 顯示所有攻略
    public function index()
    {
        $guides = Guide::orderBy('created_at', 'desc')->get();
        return view('guides.index', compact('guides'));
    }

    // 顯示新增攻略表單
    public function create()
    {
        return view('guides.create');
    }

    // 儲存新攻略
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'hero_name' => 'required|max:255',
            'content' => 'required',
            'author' => 'nullable|max:255',
        ]);

        Guide::create($validated);

        return redirect()->route('guides.index')
            ->with('success', '攻略新增成功！');
    }

    // 顯示單一攻略
    public function show(Guide $guide)
    {
        // 增加瀏覽次數
        $guide->increment('views');

        return view('guides.show', compact('guide'));
    }

    // 顯示編輯表單
    public function edit(Guide $guide)
    {
        return view('guides.edit', compact('guide'));
    }

    // 更新攻略
    public function update(Request $request, Guide $guide)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'hero_name' => 'required|max:255',
            'content' => 'required',
            'author' => 'nullable|max:255',
        ]);

        $guide->update($validated);

        return redirect()->route('guides.show', $guide)
            ->with('success', '攻略更新成功！');
    }

    // 刪除攻略
    public function destroy(Guide $guide)
    {
        $guide->delete();

        return redirect()->route('guides.index')
            ->with('success', '攻略已刪除！');
    }
}
```

---

### 步驟 4：設定路由

編輯 `routes/web.php`，在檔案中加入：

```php
use App\Http\Controllers\GuideController;

// 攻略網路由（加在檔案最後）
Route::resource('guides', GuideController::class);
```

**完整參考（如果您的檔案是空的）：**

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\GameController;
use App\Http\Controllers\GuideController;

Route::get('/', function () {
    return view('welcome');
});

// 遊戲相關路由
Route::get('/heroes', [GameController::class, 'index']);
Route::get('/heroes/{heroName}', [GameController::class, 'show']);

// 攻略網路由
Route::resource('guides', GuideController::class);
```

---

### 步驟 5：建立視圖檔案

首先建立視圖目錄：

```bash
mkdir -p resources/views/guides
```

#### 5.1 建立攻略列表頁面

創建檔案 `resources/views/guides/index.blade.php`：

```blade
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>攻略列表</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft JhengHei', sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; margin-bottom: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .btn { padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; display: inline-block; }
        .btn:hover { background: #45a049; }
        .guide-card { background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .guide-card h3 { color: #333; margin-bottom: 10px; }
        .guide-meta { color: #666; font-size: 14px; margin-bottom: 10px; }
        .guide-meta span { margin-right: 15px; }
        .guide-content { color: #555; margin-bottom: 15px; }
        .alert { padding: 15px; background: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 遊戲攻略網</h1>
            <a href="{{ route('guides.create') }}" class="btn">+ 新增攻略</a>
        </div>

        @if(session('success'))
            <div class="alert">{{ session('success') }}</div>
        @endif

        @forelse($guides as $guide)
            <div class="guide-card">
                <h3>{{ $guide->title }}</h3>
                <div class="guide-meta">
                    <span>🦸 英雄：{{ $guide->hero_name }}</span>
                    <span>👤 作者：{{ $guide->author ?? '匿名' }}</span>
                    <span>👁️ 瀏覽：{{ $guide->views }}</span>
                    <span>📅 {{ $guide->created_at->format('Y-m-d') }}</span>
                </div>
                <div class="guide-content">
                    {{ Str::limit($guide->content, 150) }}
                </div>
                <a href="{{ route('guides.show', $guide) }}" class="btn">查看完整攻略 →</a>
            </div>
        @empty
            <div class="guide-card">
                <p style="text-align: center; color: #999;">目前還沒有攻略，快來新增第一篇吧！</p>
            </div>
        @endforelse
    </div>
</body>
</html>
```

#### 5.2 建立新增攻略表單

創建檔案 `resources/views/guides/create.blade.php`：

```blade
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新增攻略</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft JhengHei', sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
        input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
        textarea { min-height: 200px; resize: vertical; font-family: inherit; }
        .btn { padding: 12px 30px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #45a049; }
        .btn-secondary { background: #999; margin-left: 10px; }
        .btn-secondary:hover { background: #888; }
        .error { color: #d32f2f; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✍️ 新增攻略</h1>

        <form action="{{ route('guides.store') }}" method="POST">
            @csrf

            <div class="form-group">
                <label for="title">攻略標題 *</label>
                <input type="text" id="title" name="title" value="{{ old('title') }}" required>
                @error('title')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="hero_name">英雄名稱 *</label>
                <input type="text" id="hero_name" name="hero_name" value="{{ old('hero_name') }}" required>
                @error('hero_name')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="author">作者名稱</label>
                <input type="text" id="author" name="author" value="{{ old('author') }}">
                @error('author')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="content">攻略內容 *</label>
                <textarea id="content" name="content" required>{{ old('content') }}</textarea>
                @error('content')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div>
                <button type="submit" class="btn">發布攻略</button>
                <a href="{{ route('guides.index') }}" class="btn btn-secondary">取消</a>
            </div>
        </form>
    </div>
</body>
</html>
```

#### 5.3 建立攻略詳細頁面

創建檔案 `resources/views/guides/show.blade.php`：

```blade
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $guide->title }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft JhengHei', sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 20px; }
        .meta { color: #666; font-size: 14px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #eee; }
        .meta span { margin-right: 20px; }
        .content { line-height: 1.8; color: #333; white-space: pre-wrap; margin-bottom: 30px; }
        .btn { padding: 10px 20px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; display: inline-block; margin-right: 10px; }
        .btn:hover { background: #45a049; }
        .btn-danger { background: #f44336; }
        .btn-danger:hover { background: #da190b; }
        .alert { padding: 15px; background: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        @if(session('success'))
            <div class="alert">{{ session('success') }}</div>
        @endif

        <h1>{{ $guide->title }}</h1>

        <div class="meta">
            <span>🦸 英雄：{{ $guide->hero_name }}</span>
            <span>👤 作者：{{ $guide->author ?? '匿名' }}</span>
            <span>👁️ 瀏覽：{{ $guide->views }}</span>
            <span>📅 發布時間：{{ $guide->created_at->format('Y-m-d H:i') }}</span>
        </div>

        <div class="content">{{ $guide->content }}</div>

        <div>
            <a href="{{ route('guides.index') }}" class="btn">← 返回列表</a>
            <a href="{{ route('guides.edit', $guide) }}" class="btn">編輯</a>
            <form action="{{ route('guides.destroy', $guide) }}" method="POST" style="display: inline;" onsubmit="return confirm('確定要刪除這篇攻略嗎？');">
                @csrf
                @method('DELETE')
                <button type="submit" class="btn btn-danger">刪除</button>
            </form>
        </div>
    </div>
</body>
</html>
```

#### 5.4 建立編輯攻略頁面

創建檔案 `resources/views/guides/edit.blade.php`：

```blade
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>編輯攻略</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Microsoft JhengHei', sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #333; font-weight: bold; }
        input[type="text"], textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
        textarea { min-height: 200px; resize: vertical; font-family: inherit; }
        .btn { padding: 12px 30px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #45a049; }
        .btn-secondary { background: #999; margin-left: 10px; }
        .btn-secondary:hover { background: #888; }
        .error { color: #d32f2f; font-size: 14px; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>✏️ 編輯攻略</h1>

        <form action="{{ route('guides.update', $guide) }}" method="POST">
            @csrf
            @method('PUT')

            <div class="form-group">
                <label for="title">攻略標題 *</label>
                <input type="text" id="title" name="title" value="{{ old('title', $guide->title) }}" required>
                @error('title')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="hero_name">英雄名稱 *</label>
                <input type="text" id="hero_name" name="hero_name" value="{{ old('hero_name', $guide->hero_name) }}" required>
                @error('hero_name')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="author">作者名稱</label>
                <input type="text" id="author" name="author" value="{{ old('author', $guide->author) }}">
                @error('author')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div class="form-group">
                <label for="content">攻略內容 *</label>
                <textarea id="content" name="content" required>{{ old('content', $guide->content) }}</textarea>
                @error('content')
                    <div class="error">{{ $message }}</div>
                @enderror
            </div>

            <div>
                <button type="submit" class="btn">更新攻略</button>
                <a href="{{ route('guides.show', $guide) }}" class="btn btn-secondary">取消</a>
            </div>
        </form>
    </div>
</body>
</html>
```

---

### 步驟 6：執行資料庫遷移

執行以下指令來建立資料表：

```bash
php artisan migrate
```

如果遇到錯誤，請確保：
1. 資料庫已啟動（如果使用 Docker Sail：`./vendor/bin/sail up -d`）
2. `.env` 檔案中的資料庫設定正確

---

### 步驟 7：啟動開發伺服器

```bash
# 如果使用內建伺服器
php artisan serve

# 或使用 Laravel Sail (Docker)
./vendor/bin/sail up
```

---

## 🌐 訪問網站

開啟瀏覽器，訪問以下網址：

- **攻略列表**: http://localhost:8000/guides
- **新增攻略**: http://localhost:8000/guides/create
- **首頁**: http://localhost:8000

---

## 📊 資料庫結構

`guides` 資料表結構：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| id | BIGINT | 主鍵（自動遞增） |
| title | VARCHAR(255) | 攻略標題 |
| hero_name | VARCHAR(255) | 英雄名稱 |
| content | TEXT | 攻略內容 |
| author | VARCHAR(255) | 作者名稱（可為空） |
| views | INTEGER | 瀏覽次數（預設0） |
| created_at | TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | 更新時間 |

---

## 🎯 功能測試清單

完成設定後，請測試以下功能：

- [ ] 訪問攻略列表頁面
- [ ] 新增一篇攻略
- [ ] 查看攻略詳細內容（檢查瀏覽次數是否增加）
- [ ] 編輯現有攻略
- [ ] 刪除攻略
- [ ] 測試表單驗證（嘗試提交空白表單）

---

## 🔧 常見問題

### Q1: 執行 migrate 時出現 "Access denied" 錯誤

**解決方法**：
1. 檢查 `.env` 檔案中的資料庫設定
2. 確保資料庫服務已啟動
3. 如使用 Sail：`./vendor/bin/sail artisan migrate`

### Q2: 頁面顯示 404 錯誤

**解決方法**：
1. 執行 `php artisan route:list` 檢查路由是否正確註冊
2. 清除路由快取：`php artisan route:clear`

### Q3: 樣式沒有正確顯示

**解決方法**：
確認瀏覽器已正確載入 HTML，可以按 F12 檢查開發者工具的 Console 是否有錯誤。

---

## 📝 後續擴充建議

完成基本功能後，您可以考慮加入：

1. **使用者認證系統** - 限制只有登入使用者才能新增/編輯攻略
2. **圖片上傳功能** - 讓攻略可以包含圖片
3. **評分系統** - 讓使用者可以為攻略評分
4. **留言功能** - 在攻略下方加入留言區
5. **搜尋功能** - 根據英雄名稱或標題搜尋攻略
6. **分頁功能** - 當攻略數量很多時使用分頁
7. **Markdown 支援** - 支援 Markdown 格式編寫攻略

---

## 🎓 相關文件

- [Laravel 官方文檔](https://laravel.com/docs)
- [Eloquent ORM](https://laravel.com/docs/eloquent)
- [Blade 模板引擎](https://laravel.com/docs/blade)
- [表單驗證](https://laravel.com/docs/validation)

---

**建立日期**: 2026-01-30
**適用版本**: Laravel 12.x
