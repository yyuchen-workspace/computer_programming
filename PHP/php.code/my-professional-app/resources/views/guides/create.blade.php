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