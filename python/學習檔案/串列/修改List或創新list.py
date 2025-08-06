# 直接修改 list 本身（原地改動，會變動）
numbers = [1, 2, 3]
for i, val in enumerate(numbers):
    numbers[i] = val * 10

print(numbers)  # [10, 20, 30]

#建立新的 list（保留原本 list）
numbers = [1, 2, 3]
new_numbers = [val * 10 for val in numbers]

print(numbers)       # [1, 2, 3]
print(new_numbers)   # [10, 20, 30]

