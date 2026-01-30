# Xdebug 調試環境設定說明

## 📅 設定日期
2026-01-28

## 🎯 目標
在 Laravel Sail (Docker) 環境中配置 Xdebug，以便在 VSCode 中進行 PHP 調試。

---

## 🔧 已完成的修改

### 1. **清理本機 PHP 環境**

**檔案**: `/opt/homebrew/etc/php/8.5/php.ini`

**操作**: 移除了錯誤的 Xdebug 配置

**原因**:
- 本機 PHP 不需要 Xdebug（使用 Docker 環境）
- 避免本機環境污染
- 消除 PHP 警告訊息

**結果**: 本機 PHP 保持乾淨，無 Xdebug 警告

---

### 2. **Laravel Sail 環境變數配置**

**檔案**: `.env`

**已存在的配置**（第 72-73 行）:
```env
SAIL_XDEBUG_MODE=develop,debug
SAIL_XDEBUG_CONFIG="client_host=host.docker.internal"
```

**說明**:
- `SAIL_XDEBUG_MODE=develop,debug`: 啟用開發和調試模式
- `SAIL_XDEBUG_CONFIG`: 設定 Xdebug 連接到 Docker host

---

### 3. **VSCode 調試配置**

**檔案**: `.vscode/launch.json`

**已存在的配置**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for Xdebug (Sail)",
      "type": "php",
      "request": "launch",
      "port": 9003,
      "pathMappings": {
        "/var/www/html": "${workspaceFolder}"
      }
    }
  ]
}
```

**說明**:
- `port: 9003`: Xdebug v3 預設端口
- `pathMappings`: 將容器內路徑對應到本地專案路徑

---

### 4. **Docker 容器內 Xdebug 配置**

**檔案**: `/etc/php/8.5/cli/conf.d/20-xdebug.ini` (容器內)

**修改內容**:
```ini
zend_extension=xdebug.so
xdebug.mode=develop,debug
xdebug.client_host=host.docker.internal
xdebug.client_port=9003
xdebug.start_with_request=yes
```

**執行命令**:
```bash
./vendor/bin/sail exec laravel.test bash -c 'echo -e "zend_extension=xdebug.so\nxdebug.mode=develop,debug\nxdebug.client_host=host.docker.internal\nxdebug.client_port=9003\nxdebug.start_with_request=yes" > /etc/php/8.5/cli/conf.d/20-xdebug.ini'
```

**說明**:
- `xdebug.mode=develop,debug`: 啟用開發和調試功能
- `xdebug.client_host=host.docker.internal`: Docker 連接到主機
- `xdebug.client_port=9003`: 監聽端口
- `xdebug.start_with_request=yes`: 每次請求自動啟動 Xdebug

---

## ✅ 驗證結果

### 檢查 Xdebug 版本
```bash
./vendor/bin/sail php -v
```

輸出:
```
PHP 8.5.2 (cli) (built: Jan 18 2026 14:12:15) (NTS)
Copyright (c) The PHP Group
Built by Debian
Zend Engine v4.5.2, Copyright (c) Zend Technologies
    with Xdebug v3.5.0, Copyright (c) 2002-2025, by Derick Rethans
    with Zend OPcache v8.5.2, Copyright (c), by Zend Technologies
```

### 檢查 Xdebug 設定
```bash
./vendor/bin/sail php -i | grep "xdebug.mode\|xdebug.client_host\|xdebug.start_with_request"
```

輸出:
```
xdebug.client_host => host.docker.internal => host.docker.internal
xdebug.mode => develop,debug => develop,debug
xdebug.start_with_request => yes => yes
```

✅ **所有設定正確！**

---

## 🚀 使用方法

### 1. 啟動 Sail 容器
```bash
./vendor/bin/sail up -d
```

### 2. 在 VSCode 中開啟調試
- 按 `F5` 或點擊調試面板的播放按鈕
- 選擇配置: **"Listen for Xdebug (Sail)"**
- 狀態列會顯示橙色，表示正在監聽

### 3. 設置中斷點
在想要調試的程式碼行號左側點擊，出現紅點

### 4. 執行程式
- **網頁應用**: 瀏覽器開啟 `http://localhost`
- **CLI 指令**: `./vendor/bin/sail artisan your-command`
- **測試**: `./vendor/bin/sail test`

### 5. 調試功能
程式在中斷點暫停時，可以：
- 📊 查看變數值（滑鼠懸停或查看調試面板）
- ⏭️ 單步執行（F10: Step Over, F11: Step Into）
- 📍 查看呼叫堆疊
- 🔍 在 Debug Console 執行 PHP 表達式
- ⏯️ 繼續執行（F5）

---

## 🔍 快捷鍵

| 功能 | macOS 快捷鍵 |
|------|-------------|
| 開始調試 | `F5` |
| 單步跳過 (Step Over) | `F10` |
| 單步進入 (Step Into) | `F11` |
| 單步跳出 (Step Out) | `Shift + F11` |
| 繼續執行 | `F5` |
| 停止調試 | `Shift + F5` |
| 切換中斷點 | `F9` |

---

## ⚠️ 注意事項

### 容器重啟後的處理
如果執行 `./vendor/bin/sail down` 或重建容器，容器內的 Xdebug 配置會遺失。

**解決方案**:
重新執行配置命令：
```bash
./vendor/bin/sail exec laravel.test bash -c 'echo -e "zend_extension=xdebug.so\nxdebug.mode=develop,debug\nxdebug.client_host=host.docker.internal\nxdebug.client_port=9003\nxdebug.start_with_request=yes" > /etc/php/8.5/cli/conf.d/20-xdebug.ini'
```

### 性能影響
Xdebug 會降低 PHP 執行速度。如果不需要調試，可以暫時停用：

**停用 Xdebug**:
```bash
# 修改 .env
SAIL_XDEBUG_MODE=off

# 重啟容器
./vendor/bin/sail down && ./vendor/bin/sail up -d
```

**重新啟用**:
```bash
# 修改 .env
SAIL_XDEBUG_MODE=develop,debug

# 重啟容器
./vendor/bin/sail down && ./vendor/bin/sail up -d
```

---

## 🐛 故障排除

### 問題 1: VSCode 無法連接到 Xdebug

**檢查清單**:
1. ✅ Sail 容器是否運行: `./vendor/bin/sail ps`
2. ✅ VSCode 調試監聽是否啟動（狀態列橙色）
3. ✅ 檢查端口是否被佔用: `lsof -i :9003`
4. ✅ 防火牆是否阻擋端口 9003

### 問題 2: 中斷點無法暫停

**檢查清單**:
1. ✅ 確認 `pathMappings` 路徑正確
2. ✅ 確認中斷點設在會執行的程式碼上
3. ✅ 檢查 Xdebug 日誌: `./vendor/bin/sail logs -f laravel.test`

### 問題 3: 容器內看不到 Xdebug

**解決方案**:
```bash
# 檢查 Xdebug 是否安裝
./vendor/bin/sail php -v

# 如果沒有 Xdebug，重新執行配置命令
./vendor/bin/sail exec laravel.test bash -c 'echo -e "zend_extension=xdebug.so\nxdebug.mode=develop,debug\nxdebug.client_host=host.docker.internal\nxdebug.client_port=9003\nxdebug.start_with_request=yes" > /etc/php/8.5/cli/conf.d/20-xdebug.ini'
```

---

## 📚 參考資源

- [Xdebug 官方文件](https://xdebug.org/docs/)
- [VSCode PHP Debug 擴展](https://marketplace.visualstudio.com/items?itemName=xdebug.php-debug)
- [Laravel Sail 文件](https://laravel.com/docs/sail)
- [Xdebug 3.x 設定指南](https://xdebug.org/docs/upgrade_guide)

---

## 📝 版本資訊

- **PHP**: 8.5.2
- **Xdebug**: 3.5.0
- **Laravel Sail**: Docker 環境
- **容器系統**: OrbStack
- **VSCode 擴展**: PHP Debug by Xdebug

---

## 🎉 完成！

現在你的 Laravel Sail 專案已經完全配置好 Xdebug 調試環境了！

如有任何問題，請參考故障排除章節或查看官方文件。
