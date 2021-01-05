import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


# now = datetime.now()
# print("now =", now)
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)	


generation= pd.read_csv("smard/Actual_generation_201601010000_201612312359.csv", sep=';')

print(generation.dtypes)


labels = ["Biomass", "Hydropower", "Wind offshore", "Wind onshore", "Photovoltaics" , "OtherRE"]
#generation.plot.area()
biomass = generation.Biomass
hydropower = generation.Hydropower
print(type(hydropower))
plt.scatter(biomass, hydropower)
plt.show()
ax = generation.plot.area()
# generation.WindOffshore
# generation.WindOnshore
# generation.Photovoltaics 
# generation.OtherRE,
#plt.stackplot(generation.Datetime , biomass ,  hydropower, labels=labels)


