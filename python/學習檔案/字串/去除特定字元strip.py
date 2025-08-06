##使用「str.strip()」可以去除字串開頭或結尾的某些字元。

a = '  hello!!'
b = a.strip()
c = a.strip('!')
d = a.lstrip()
e = a.rstrip()
print(b) # hello!!
print(c) #   hello
print(d) # hello!!    使用 lstrip() 函式可以只去除左邊
print(e) #   hello!!  使用 rstrip() 函式可以只去除右邊

##下面的例子，會去除開頭與結尾指定的字元

s = '@!$##$#ABCDE%#$#%#$'
a = s.strip('!@#$%^&*(')
print(a)  # ABCDE