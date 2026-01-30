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