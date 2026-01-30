# Xdebug 除錯配置修復指南 (OrbStack + Laravel Sail)

## 問題描述

在 OrbStack + Laravel Sail 環境中，Xdebug 無法連接到 VSCode，導致：
- 中斷點無法觸發
- 變數面板為空
- 除錯功能完全無法使用

---

## 根本原因分析

經過診斷，發現了以下問題：

### 1. 網路連接問題
- **問題**: `host.docker.internal` 在 OrbStack 中無法正確解析或被阻擋
- **解決**: 使用主機的實際 IP 地址 (`192.168.5.23`)

### 2. Xdebug 模式配置問題
- **問題**: 即使 `.env` 設定了 `SAIL_XDEBUG_MODE=develop,debug`，但 PHP 只讀取到 `develop`
- **原因**: PHP-FPM 沒有正確繼承環境變數
- **解決**: 直接在 `php.ini` 中配置 Xdebug

### 3. 配置未生效
- **問題**: 環境變數存在，但 Xdebug 實際運行時沒有使用
- **原因**: PHP 的配置優先順序：`php.ini` > 環境變數
- **解決**: 修改容器內的 Xdebug INI 配置檔

---

## 完整修復步驟

### 步驟 1: 獲取主機 IP 地址

```bash
ipconfig getifaddr en0
# 輸出: 192.168.5.23 (你的實際 IP)
```

**說明**: 這個 IP 是你的 Mac 在區域網路中的地址，容器會使用這個 IP 連接到主機的 VSCode。

---

### 步驟 2: 更新 .env 配置

**檔案位置**: `/my-professional-app/.env`

**修改內容**:
```env
SAIL_XDEBUG_MODE=develop,debug
SAIL_XDEBUG_CONFIG="client_host=192.168.5.23"
```

**重要說明**:
- `develop,debug` - 同時啟用開發模式和除錯模式
- `client_host=192.168.5.23` - 使用實際 IP 而非 `host.docker.internal`
- **移除 `coverage` 模式** - 會降低性能且不需要用於一般除錯

---

### 步驟 3: 重啟容器使環境變數生效

```bash
./vendor/bin/sail down
./vendor/bin/sail up -d
```

**驗證環境變數**:
```bash
./vendor/bin/sail exec laravel.test env | grep XDEBUG
```

**預期輸出**:
```
XDEBUG_MODE=develop,debug
XDEBUG_CONFIG=client_host=192.168.5.23
```

---

### 步驟 4: 修改容器內的 Xdebug INI 配置

**關鍵步驟**: 直接在容器內的 `php.ini` 添加 Xdebug 配置

```bash
./vendor/bin/sail exec laravel.test bash -c 'echo "[xdebug]
xdebug.mode=debug,develop
xdebug.client_host=192.168.5.23
xdebug.client_port=9003
xdebug.start_with_request=yes
xdebug.idekey=VSCODE
xdebug.log=/tmp/xdebug.log
xdebug.log_level=7" >> /etc/php/8.5/cli/conf.d/20-xdebug.ini'
```

**配置說明**:
- `xdebug.mode=debug,develop` - 啟用除錯和開發模式
- `xdebug.client_host=192.168.5.23` - Xdebug 連接到這個主機 IP
- `xdebug.client_port=9003` - VSCode 監聽的埠號
- `xdebug.start_with_request=yes` - 每次 HTTP 請求都啟動 Xdebug
- `xdebug.idekey=VSCODE` - IDE 識別碼
- `xdebug.log=/tmp/xdebug.log` - 日誌檔案位置（用於除錯）
- `xdebug.log_level=7` - 詳細日誌等級

---

### 步驟 5: 驗證 Xdebug 配置

```bash
./vendor/bin/sail exec laravel.test php -i | grep "xdebug.mode =>"
```

**預期輸出**:
```
xdebug.mode => debug,develop => debug,develop
```

**完整驗證**:
```bash
./vendor/bin/sail exec laravel.test php -i | grep -E "xdebug\.(mode|client_host|client_port|start_with_request)"
```

**預期輸出**:
```
xdebug.client_host => 192.168.5.23 => 192.168.5.23
xdebug.client_port => 9003 => 9003
xdebug.mode => debug,develop => debug,develop
xdebug.start_with_request => yes => yes
```

---

### 步驟 6: 重啟 Laravel 容器

```bash
./vendor/bin/sail restart laravel.test
```

**說明**: 讓 PHP-FPM 重新載入配置

---

### 步驟 7: 測試網路連接

```bash
./vendor/bin/sail exec laravel.test bash -c 'curl -v telnet://192.168.5.23:9003 --max-time 3 2>&1 | grep -E "Trying|Connected|refused"'
```

**成功的輸出**:
```
*   Trying 192.168.5.23:9003...
* Connected to 192.168.5.23 (192.168.5.23) port 9003
```

**失敗的輸出**:
```
* connect to 192.168.5.23 port 9003 failed: Connection refused
```

如果連接失敗，確保：
1. VSCode 已按 `F5` 啟動除錯監聽
2. macOS 防火牆沒有阻擋連線

---

## VSCode 配置

### launch.json 配置

**檔案位置**: `.vscode/launch.json`

**內容**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for Xdebug (Sail)",
      "type": "php",
      "request": "launch",
      "port": 9003,
      "hostname": "0.0.0.0",
      "pathMappings": {
        "/var/www/html": "${workspaceFolder}"
      },
      "log": true,
      "xdebugSettings": {
        "max_data": 65535,
        "show_hidden": 1,
        "max_children": 100,
        "max_depth": 5
      }
    }
  ]
}
```

**重要參數**:
- `port: 9003` - Xdebug 3 的標準埠號
- `hostname: "0.0.0.0"` - 監聽所有網路介面
- `pathMappings` - 容器路徑映射到本機路徑
- `log: true` - 啟用除錯日誌（可以查看連接問題）

---

## 使用除錯功能

### 1. 啟動除錯監聽

1. 在 VSCode 中按 `Cmd+Shift+D` 打開除錯面板
2. 選擇「Listen for Xdebug (Sail)」
3. 按 `F5` 或點擊綠色播放按鈕 ▶️
4. 狀態列會變成**橘色**

### 2. 設置中斷點

在 `app/Http/Controllers/GameController.php` 第 23 行：
```php
$heroName = $krixi->name;  // ← 點擊行號左側設置紅色中斷點
```

### 3. 觸發除錯

在瀏覽器訪問:
```
http://localhost/test-debug
```

### 4. 檢查變數

當程式暫停在中斷點時：
- **變數面板** - 查看所有當前變數
- **監看面板** - 添加要追蹤的表達式
- **除錯主控台** - 輸入 PHP 表達式：
  ```php
  $krixi->name
  $krixi->stats->getHp()
  $krixi->skills[0]->name
  ```

### 5. 除錯控制

快捷鍵：
- `F5` - 繼續執行
- `F10` - 跨越（執行當前行，不進入函數）
- `F11` - 進入（進入函數內部）
- `Shift+F11` - 跳出（跳出當前函數）
- `Shift+F5` - 停止除錯

---

## 疑難排解

### 問題 1: 中斷點變成灰色（未驗證）

**原因**: 路徑映射不正確

**檢查**:
```bash
./vendor/bin/sail exec laravel.test pwd
# 應該輸出: /var/www/html
```

**解決**: 確保 `launch.json` 中的 `pathMappings` 正確：
```json
"/var/www/html": "${workspaceFolder}"
```

---

### 問題 2: 變數面板為空

**原因**: Xdebug 沒有連接到 VSCode

**診斷步驟**:

1. **檢查 VSCode 是否監聽**:
```bash
lsof -i :9003 -P -n
```
如果沒有輸出，表示 VSCode 沒有啟動除錯監聽。

2. **檢查容器是否能連接**:
```bash
./vendor/bin/sail exec laravel.test bash -c 'curl -v telnet://192.168.5.23:9003 --max-time 3'
```

3. **檢查 Xdebug 日誌**:
```bash
./vendor/bin/sail exec laravel.test tail -50 /tmp/xdebug.log
```

---

### 問題 3: 容器重啟後配置消失

**OrbStack 特性**:
- OrbStack 的容器**會保留**檔案系統變更
- 如果使用 `./vendor/bin/sail down` 完全停止，配置會保留
- 如果重建容器（`sail build`），配置會消失

**永久解決方案**:

創建啟動腳本自動配置 Xdebug：

**檔案**: `docker/xdebug-setup.sh`
```bash
#!/bin/bash

echo "[xdebug]
xdebug.mode=debug,develop
xdebug.client_host=192.168.5.23
xdebug.client_port=9003
xdebug.start_with_request=yes
xdebug.idekey=VSCODE
xdebug.log=/tmp/xdebug.log
xdebug.log_level=7" >> /etc/php/8.5/cli/conf.d/20-xdebug.ini

echo "Xdebug configured successfully"
```

在容器啟動後執行：
```bash
./vendor/bin/sail exec laravel.test bash /var/www/html/docker/xdebug-setup.sh
```

---

### 問題 4: IP 地址變更

**情況**: 當你的 Mac 連接到不同的 Wi-Fi 時，IP 地址會改變

**快速修復腳本**:

創建 `update-xdebug-ip.sh`:
```bash
#!/bin/bash

# 獲取當前 IP
NEW_IP=$(ipconfig getifaddr en0 || ipconfig getifaddr en1)

echo "當前 IP: $NEW_IP"

# 更新 .env
sed -i '' "s/SAIL_XDEBUG_CONFIG=.*/SAIL_XDEBUG_CONFIG=\"client_host=$NEW_IP\"/" .env

# 更新容器內配置
./vendor/bin/sail exec laravel.test bash -c "sed -i 's/xdebug.client_host=.*/xdebug.client_host=$NEW_IP/' /etc/php/8.5/cli/conf.d/20-xdebug.ini"

# 重啟容器
./vendor/bin/sail restart laravel.test

echo "Xdebug IP 已更新為: $NEW_IP"
```

使用：
```bash
chmod +x update-xdebug-ip.sh
./update-xdebug-ip.sh
```

---

## 驗證清單

在開始除錯前，確認以下項目：

- [ ] ✅ 容器正在運行 (`./vendor/bin/sail ps`)
- [ ] ✅ Xdebug 已安裝 (`./vendor/bin/sail exec laravel.test php -m | grep xdebug`)
- [ ] ✅ Xdebug mode 包含 debug (`php -i | grep "xdebug.mode"`)
- [ ] ✅ client_host 設定正確 (`env | grep XDEBUG_CONFIG`)
- [ ] ✅ VSCode 正在監聽 9003 (`lsof -i :9003`)
- [ ] ✅ 容器可以連接主機 (`curl telnet://192.168.5.23:9003`)
- [ ] ✅ 中斷點已設置且為紅色（已驗證）
- [ ] ✅ 除錯配置已選擇並啟動（狀態列為橘色）

---

## 配置檔案總覽

### 1. .env (專案根目錄)

```env
SAIL_XDEBUG_MODE=develop,debug
SAIL_XDEBUG_CONFIG="client_host=192.168.5.23"
```

### 2. .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for Xdebug (Sail)",
      "type": "php",
      "request": "launch",
      "port": 9003,
      "hostname": "0.0.0.0",
      "pathMappings": {
        "/var/www/html": "${workspaceFolder}"
      },
      "log": true,
      "xdebugSettings": {
        "max_data": 65535,
        "show_hidden": 1,
        "max_children": 100,
        "max_depth": 5
      }
    }
  ]
}
```

### 3. 容器內 Xdebug 配置

**位置**: `/etc/php/8.5/cli/conf.d/20-xdebug.ini`

```ini
zend_extension=xdebug.so
[xdebug]
xdebug.mode=debug,develop
xdebug.client_host=192.168.5.23
xdebug.client_port=9003
xdebug.start_with_request=yes
xdebug.idekey=VSCODE
xdebug.log=/tmp/xdebug.log
xdebug.log_level=7
```

---

## 常用命令參考

### 檢查與診斷

```bash
# 檢查容器狀態
./vendor/bin/sail ps

# 檢查 Xdebug 是否安裝
./vendor/bin/sail exec laravel.test php -m | grep xdebug

# 檢查 Xdebug 配置
./vendor/bin/sail exec laravel.test php -i | grep xdebug

# 檢查環境變數
./vendor/bin/sail exec laravel.test env | grep XDEBUG

# 檢查 Xdebug 日誌
./vendor/bin/sail exec laravel.test tail -f /tmp/xdebug.log

# 測試網路連接
./vendor/bin/sail exec laravel.test curl -v telnet://192.168.5.23:9003 --max-time 3
```

### 容器管理

```bash
# 重啟所有容器
./vendor/bin/sail restart

# 重啟 Laravel 容器
./vendor/bin/sail restart laravel.test

# 完全停止並重新啟動
./vendor/bin/sail down
./vendor/bin/sail up -d

# 進入容器 Shell
./vendor/bin/sail shell
```

---

## 效能考量

### Xdebug 對效能的影響

Xdebug 會**顯著降低**應用程式效能：
- 請求處理時間增加 3-10 倍
- 記憶體使用增加

### 建議

1. **只在開發時啟用**
   ```env
   # 開發
   SAIL_XDEBUG_MODE=develop,debug

   # 正式環境
   SAIL_XDEBUG_MODE=off
   ```

2. **使用觸發模式而非自動啟動**
   ```ini
   xdebug.start_with_request=trigger
   ```

   然後使用瀏覽器擴充（Xdebug Helper）來觸發除錯。

3. **除錯完成後關閉**
   - 在 VSCode 按 `Shift+F5` 停止除錯
   - 或在 .env 中暫時關閉：
     ```env
     SAIL_XDEBUG_MODE=off
     ```

---

## 總結

這次修復解決了三個主要問題：

1. **網路連接** - 從 `host.docker.internal` 改為實際 IP `192.168.5.23`
2. **Xdebug 模式** - 確保 `debug` 模式正確啟用
3. **配置生效** - 直接修改 `php.ini` 而不依賴環境變數

現在 Xdebug 應該可以正常工作，你可以：
- ✅ 設置中斷點並暫停程式執行
- ✅ 查看和修改變數
- ✅ 逐步執行程式碼
- ✅ 追蹤函數呼叫堆疊

---

## 參考資源

- [Xdebug 官方文件](https://xdebug.org/docs/)
- [Laravel Sail 文件](https://laravel.com/docs/sail)
- [VSCode PHP Debug 擴充](https://marketplace.visualstudio.com/items?itemName=xdebug.php-debug)
- [OrbStack 文件](https://docs.orbstack.dev/)

---

**文件建立日期**: 2026-01-30
**測試環境**: macOS + OrbStack + Laravel Sail + PHP 8.5.2 + Xdebug 3.x
**主機 IP**: 192.168.5.23 (你的實際 IP)
