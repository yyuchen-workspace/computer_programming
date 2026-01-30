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