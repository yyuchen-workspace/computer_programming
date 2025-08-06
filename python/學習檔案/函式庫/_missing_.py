'''
__missing__(self, key) 是什麼？
這是 dict 的特別方法，當你使用 obj[key] 查不到鍵時，會自動呼叫 __missing__(key)，讓你決定該怎麼處理「缺失鍵」。

用在你自己定義的 dict 子類中：
python
'''
class MyDict(dict):
    def __missing__(self, key):
        return 0   # 沒有這個 key，就回傳 0

d = MyDict()
print(d['x'])  # ➜ 0
'''
但要注意：
d.get('x')  # ➜ None，不會觸發 __missing__()
'''