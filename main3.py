a = [1,2,3,4,5,6,7,8,9,1,2,12,14,1,2,3,1,2,8,8,9,10,3,4]
a = [3,3,3,3,3,0,0,0,0,0,0,0,0,0,5,5,5,5,5]
['five', 'five', 'five', 'five', 'eight', 'eight', 'eight', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 0, 0, 0, 0, 'five', 'five', 'five', 'five']
# 5 consecutive values lower  that 4


# 3 consecutive values lower  than 6   
# Steinkohle
b = []
for i, value in enumerate(a):
    print(a[i:(i+3)])
    newlist = a[i:(i+3)]
    for t in newlist:
        if t > 5:
            b.append('five')
            continue
        elif t > 8:   
            print(i, "to eight")
            b.append("eight")
        else:
            b.append(0)
print(b)    
    