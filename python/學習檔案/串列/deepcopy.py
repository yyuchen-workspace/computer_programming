import copy
a = [0,1,2,3,4,[100,200]]
b = a[:]
c = a.copy()
d = list(a)
e = copy.deepcopy(a)
a[-1][0]=999
print(a)   # [0, 1, 2, 3, 4, [999, 200]]
print(b)   # [0, 1, 2, 3, 4, [999, 200]]
print(c)   # [0, 1, 2, 3, 4, [999, 200]]
print(d)   # [0, 1, 2, 3, 4, [999, 200]]
print(e)   # [0, 1, 2, 3, 4, [100, 200]]  使用 deepcopy 的沒有被改變