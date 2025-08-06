##str.split(x) 
a = 'hello world, I am oxxo, how are you?'
b = a.split(',') # 以逗號「,」進行拆分
c = a.split(' ') # 以空白字元「 」進行拆分
d = a.split()    # 如果不指定分隔符號，自動以空白字元進行拆分
print(b[-1])         # ['hello world', ' I am oxxo', ' how are you?']