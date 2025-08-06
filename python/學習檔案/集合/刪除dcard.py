#不希望在移除項目時發生執行錯誤的狀況，可以使用「集合.discard(項目)」，將指定項目移除
a = {0,1,2,3,'x','y','z'}
a.discard('x')
a.discard('a')   # 不會發生錯誤
print(a)         # {0, 1, 2, 3, 'y', 'z'}discard()