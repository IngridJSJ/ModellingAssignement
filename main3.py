a = [1,2,3,4,5,6,7,8,9,1,2,12,14,1,2,3,8,8,8,8]
b = []
for i, value in enumerate(a):
    print(a[i:(i+3)])
    newlist = a[i:(i+3)]
    if any(t > 5 for t in newlist):
        b.append(0)
        continue
    else:
        b.append(value)
print(b)    
    