key_values = [('even',2),('odd',1),('even',8),('odd',3),('float',2.4),('odd',7)]

multi_dict = {}
for key,value in key_values:
    if key not in multi_dict:
        multi_dict[key] = [value]
    else:
        multi_dict[key].append(value)