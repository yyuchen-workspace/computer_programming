
num = int(input("Please enter a number"))
sum = 0
while num / 10 != 0:
    sum += num % 10
    num = num // 10

print(sum + num)
