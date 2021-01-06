import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# list of 3 smaller than 5

a = [1,2,3,4,5,6,7,8,9,1,2,12,14,1,2,3,8,8,8,8]
b = []
for i in a:
    print(a[i:(i+3)])
    newlist = a[i:(i+3)]
    for j in newlist:
        if j > 5:
            print(j)
            break
        else:
            print("added",j)
            b.append(j)
            j+=2
            i+=2




print(b)    