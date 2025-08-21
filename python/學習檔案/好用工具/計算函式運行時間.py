# 裝飾器寫法
import time

def timer_decorator(f):
    def wrapper(*args, **kwargs):
        
        start_time = time.time()

        result = f(*args, **kwargs)

        end_time = time.time()
        print(f"函式{f.__name__}總共執行了{end_time - start_time:.4f}秒")
        return result
    
    return wrapper


@timer_decorator
def time_sleeper(): # 此函式可隨意更改
    time.sleep(2)
    print(f"time_sleeper 正在執行")


time_sleeper()

