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

#start決定起始索引值
names = ["黃","煜","宸"]
scores = [70, 80 ,90]
for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{i}. {name} 得分：{score}") 
'''
1. 黃 得分：70
2. 煜 得分：80
3. 宸 得分：90
'''