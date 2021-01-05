# unit commitment
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

#df = pd.read_excel("national_generation_capacity.xlsx", sheet_name="output", usecols="A,LI", engine='openpyxl')

#POWER PLANTS RENEWABLES 
# PowerPlants = pd.read_csv('renewable_power_plants_DE_2020.csv', usecols=[1,2,3,4,5,16,17], parse_dates=['commissioning_date', 'decommissioning_date'])

# PowerPlants['commissioning_date']= pd.to_datetime(PowerPlants['commissioning_date'])

# indexdatescomission = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01")  ].index
# indexdates = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01") & (PowerPlants["decommissioning_date"]< "2016-01-01") ].index
# PowerPlants.drop(indexdates , inplace=True)


# uniquetechnology = PowerPlants["energy_source_level_2"].unique() 
# print(uniquetechnology)
#POWER PLANTS CONVENTIONALS

# ElectricityDemand 2016-12-31 19:00:00
load = pd.read_excel("smard/Actual_consumption_201601010000_201612312359.xlsx", sheet_name="Actual consumption", engine='openpyxl', parse_dates=['Datetime'])
load.set_index(['Datetime'], drop=False)
load.index = pd.to_datetime(load.Datetime, infer_datetime_format=True)
hourly_consumption = load.Total.resample("H").mean()

#######################################################################################################################################
# RE generation

generation= pd.read_excel("smard/Actual_generation_201601010000_201612312359.xlsx", sheet_name="Actual generation", engine='openpyxl', parse_dates=['Datetime'])
generation.set_index(['Datetime'], drop=False)
#print(generation.dtypes)
generation.index = pd.to_datetime(generation.Datetime, infer_datetime_format=True)
generation = generation.resample("H").mean()

# residual load

AllREGeneration = generation.Biomass + generation.Hydropower + generation.WindOffshore + generation.WindOnshore +  generation.Photovoltaics + generation.OtherRE
residual_load = hourly_consumption - AllREGeneration

# marginal costs


#graphs
labels = [ "Biomass", "Hydropower", "Wind offshore", "Wind onshore", "Photovoltaics" , "OtherRE" ]
pal = [ "#009933", "#66ccff",  "#000099", "#0000ff", "#ffcc00", "#9900ff" ]

fig, (ax1, ax2) = plt.subplots(2, sharex=True)

ax1.plot( generation.index.values, hourly_consumption  , color="pink", label="consumption")
ax1.stackplot(generation.index.values , generation.Biomass , generation.Hydropower, generation.WindOffshore, generation.WindOnshore, generation.Photovoltaics, generation.OtherRE ,   
labels=labels, colors =pal)
ax1.legend( bbox_to_anchor=(1.05, 1))

ax1.set_title('Renewable energy generation')
ax1.set_ylabel('Mwh') 

ax2.plot(generation.index.values, residual_load, label="Residual Load")
ax2.set_title('Residual Load')
ax2.legend( bbox_to_anchor=(1.05, 1))
ax2.set_xlabel('Month')  
ax2.set_ylabel('Mwh') 
plt.show()

#newtime = load[['Date','Time of day']].apply(pd.to_datetime,  )
#mydatetime = datetime.combine(load['Date'], load['Time of day'])
# date_dt1 = pd.to_datetime(load['Date'][1], '%A, %B %d, %Y')




