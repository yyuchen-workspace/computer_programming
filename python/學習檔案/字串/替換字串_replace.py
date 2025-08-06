#使用「str.replace(x, y, n)」可以將字串中的 x 替換為 y，n 為要替換的數量，可不填 ( 表示全部替換 )

a = 'hello world, lol'
b = a.replace('l','XXX')
c = a.replace('l','XXX',2)
print(b)  # heXXXXXXo worXXXd, XXXoXXX ( 所有的 l 都被換成 XXX )
print(c)  # heXXXXXXo world, lol ( 前兩個 l 被換成 XXX )