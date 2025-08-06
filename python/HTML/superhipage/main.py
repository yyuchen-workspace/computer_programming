import subprocess
import os
import sys

def run_cleanly():
    devnull = open(os.devnull, 'w')
    subprocess.run(
        [sys.executable, 'scraper.py'],  # 換成你主程式檔名
        stderr=devnull,                  # 關鍵：攔截所有背景雜訊
        stdin=sys.stdin,
        stdout=sys.stdout
    )

if __name__ == "__main__":
    run_cleanly()