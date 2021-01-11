import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

Prices2019 = pd.read_excel("Ewi/installed-capacity-2019.xlsx", sheet_name="prices", usecols="A:J", engine='openpyxl', index_col="Prices")
Plants = pd.read_excel("Ewi/installed-capacity-2019.xlsx", sheet_name="Plants", usecols="O,X:AA", engine='openpyxl')


DayAheadprices = pd.read_excel("smard/Day-ahead_prices_201901010000_201912312359.xlsx", sheet_name="Day-ahead prices", usecols="C:D", engine='openpyxl', nrows=8761, parse_dates=["Datetime"])
DayAheadprices.set_index(['Datetime'], drop=False)
DayAheadprices.index = pd.to_datetime(DayAheadprices.Datetime, infer_datetime_format=True)
# print(DayAheadprices.index[1:10])
# print(DayAheadprices.index[-10:-1])
# price2 = DayAheadprices.resample('15Min').pad()
# print(price2.info())
# Generation MWh
generation= pd.read_excel("smard/Actual_generation_201901010000_201912312359.xlsx", sheet_name="Actual generation", usecols="C:Q", engine='openpyxl',   parse_dates=['Datetime'])
generation.set_index(['Datetime'], drop=False)

cols = ["WindOnshore", "Consumption"]
generation[cols] = generation[cols].applymap(lambda x: np.nan if isinstance(x, str) else x)
generation.Consumption.fillna(method='ffill')
generation.index = pd.to_datetime(generation.Datetime, infer_datetime_format=True)
hourly_consumption = generation.Consumption
AllREGeneration = generation.Biomass + generation.Hydropower + generation.WindOffshore + generation.WindOnshore +  generation.Photovoltaics + generation.OtherRE
AllConventional = generation.Nuclear + generation.BrownCoal + generation.HardCoal + generation.Gas + generation.OtherConventional 
TotalGeneration = AllREGeneration + AllConventional + generation.HydroPumpedStorage
#NetExports = generation.exports + generation.imports 


#-----------------------------------------------residual load
residual_load = hourly_consumption - AllREGeneration 
#residual_load_Exports = hourly_consumption + NetExports - AllREGeneration + NetExports
residual_load_nonuclear = residual_load + generation.Nuclear
residual_load3RE = hourly_consumption - AllREGeneration*3


residual_load.resample('H').agg(['max'])
Residualload = residual_load.values
#ResidualloadExports = residual_load_Exports.values
loadcurve = hourly_consumption.sort_values()[::-1]
loadcurve_noNuclear = residual_load_nonuclear.sort_values()[::-1]

residualcurve = residual_load.sort_values()[::-1]
#residualcurve_Exports = residual_load_Exports.sort_values()[::-1]
residualcurve3RE = residual_load3RE.sort_values()[::-1]

Marginalcost =[]
Marginaltechnology =[]

for num, load_H in enumerate(Residualload, start=1):  
    result_index =  (load_H - Plants.CumulativeCapacity).lt(0).idxmax()
    Marginalcost.append(Plants.Grenzkosten[result_index])
# exports
# MarginalcostExports =[]
# for num, load_H in enumerate(ResidualloadExports, start=1):  
#     result_index =  (load_H - Plants.CumulativeCapacity).lt(0).idxmax()
#     MarginalcostExports.append(Plants.Grenzkosten[result_index])

plt.plot(DayAheadprices.index.values, DayAheadprices.Prices)
plt.plot(DayAheadprices.index.values, Marginalcost)
#plt.plot(DayAheadprices.index.values, MarginalcostExports)
plt.legend([ "Day ahead prices", "Marginal costs" ])
plt.ylabel('Eur/MWh') 
plt.show()   
#print(generation.info())

# a = [1,2,3,4,5,6,7,8,9,1,2,12,14,1,2,3,1,2,8,8,9,10,3,4]
# a = [3,3,3,3,3,0,0,0,0,0,0,0,0,0,5,5,5,5,5]
# ['five', 'five', 'five', 'five', 'eight', 'eight', 'eight', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 'five', 0, 0, 0, 0, 'five', 'five', 'five', 'five']
# # 5 consecutive values lower  that 4


# # 3 consecutive values lower  than 6   
# # Steinkohle
# b = []
# for i, value in enumerate(a):
#     print(a[i:(i+3)])
#     newlist = a[i:(i+3)]
#     for t in newlist:
#         if t > 5:
#             b.append('five')
#             continue
#         elif t > 8:   
#             print(i, "to eight")
#             b.append("eight")
#         else:
#             b.append(0)
# print(b)    
    