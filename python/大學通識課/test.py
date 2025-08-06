import sys
x = 2
a = 0
for line in sys.stdin:
   
    line = line.strip()
    
    if not line:
        continue

    if line == 'EOF':
        break
    for i in range(1, int(line)):
        a+= 2*i
    print(a+x)
    a = 0
  


