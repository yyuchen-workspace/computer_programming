import sys
import locale
import os


def set_output_encoding():
    """
    自動偵測系統編碼並設定 PYTHONIOENCODING 環境變數。
    """
    # 取得系統首選編碼
    preferred_encoding = locale.getpreferredencoding(False)
    
    # 檢查是否已經是 UTF-8，或是系統已經支援該編碼
    if preferred_encoding and preferred_encoding.lower() != 'utf-8':
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        # 重新載入 sys.stdout 以應用新的編碼
        # 這是確保立即生效的關鍵步驟
        try:
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
            print(f"偵測到系統編碼為 {preferred_encoding}，將其設定為 UTF-8。")
        except OSError:
            # 如果 stdout 不是 tty (例如被導向檔案)，可能會失敗，
            # 這是正常的，但環境變數仍會生效。
            pass



# 在程式碼最前面呼叫這個函數
set_output_encoding()