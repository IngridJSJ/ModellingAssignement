# unit commitment
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

#df = pd.read_excel("national_generation_capacity.xlsx", sheet_name="output", usecols="A,LI", engine='openpyxl')

# #PV profile
PV = pd.read_csv('ninja/ninja_pv_country_DE_merra-2_corrected.csv', delimiter=',')
PV.index = pd.to_datetime(PV.time, infer_datetime_format=True)
indexdatesPV = PV[ (  PV["time"]< "2016-01-01")   ].index 
PV.drop(indexdatesPV , inplace=True)
indexdatesPV = PV[ (  PV["time"]> "2017-01-01")   ].index 
PV.drop(indexdatesPV , inplace=True)
#Wind profile
Wind = pd.read_csv('ninja/ninja_wind_country_DE_near-termfuture-merra-2_corrected.csv', delimiter=',')
Wind.index = pd.to_datetime(Wind.time, infer_datetime_format=True)
indexdatesWind = Wind[ (  Wind["time"]< "2016-01-01")   ].index 
Wind.drop(indexdatesWind , inplace=True)
indexdatesWind = Wind[ (  Wind["time"]> "2017-01-01")   ].index 
Wind.drop(indexdatesWind , inplace=True)

plt.plot(PV.national, color="#FFC300", zorder=1)
plt.plot(Wind.offshore, color="#000099", zorder=2)
plt.plot(Wind.onshore,color="#0000ff", zorder=3)
plt.legend(["PV", "offshore", "onshore"])
plt.show()

# Installed capacity MW
Capacity = pd.read_excel("smard/Installed_generation_capacity_201601010000_201612312359.xlsx", sheet_name="capacity", usecols="A:M", engine='openpyxl', index_col="Names")
#print(Capacity.Gas.EnergyValue)
#POWER PLANTS RENEWABLES 
PowerPlants = pd.read_csv('ninja/renewable_power_plants_DE_2020.csv', usecols=[1,2,3,4,5,16,17], parse_dates=['commissioning_date', 'decommissioning_date'])
PowerPlants['commissioning_date']= pd.to_datetime(PowerPlants['commissioning_date'])
indexdatescomission = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01")  ].index
indexdates = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01") & (PowerPlants["decommissioning_date"]< "2016-01-01") ].index
PowerPlants.drop(indexdates , inplace=True)
uniquetechnology = PowerPlants["energy_source_level_2"].unique() 
print(uniquetechnology)

#POWER PLANTS CONVENTIONALS

# ElectricityDemand 2016-12-31 19:00:00
load = pd.read_excel("smard/Actual_consumption_201601010000_201612312359.xlsx", sheet_name="Actual consumption", engine='openpyxl', parse_dates=['Datetime'])
load.set_index(['Datetime'], drop=False)
load.index = pd.to_datetime(load.Datetime, infer_datetime_format=True)
hourly_consumption = load.Total.resample("H").mean()


# Generation MWh
generation= pd.read_excel("smard/Actual_generation_201601010000_201612312359.xlsx", sheet_name="Actual generation", engine='openpyxl',  usecols="C:O", parse_dates=['Datetime'])
generation.set_index(['Datetime'], drop=False)
generation.index = pd.to_datetime(generation.Datetime, infer_datetime_format=True)
generation = generation.resample("H").mean()
# MWh * tonCO2/ MWh = ton CO2
Emissions2016 = generation.Gas*Capacity.Gas.EmissionsperMWh + generation.BrownCoal*Capacity.BrownCoal.EmissionsperMWh + generation.HardCoal*Capacity.HardCoal.EmissionsperMWh + generation.OtherConventional*Capacity.OtherConventional.EmissionsperMWh

# plt.plot(Emissions2016)
# plt.ylabel('ton CO2') 
# plt.show()

AllREGeneration = generation.Biomass + generation.Hydropower + generation.WindOffshore + generation.WindOnshore +  generation.Photovoltaics + generation.OtherRE
AllConventional = generation.Nuclear + generation.BrownCoal + generation.HardCoal + generation.Gas + generation.OtherConventional 
#TotalGeneration = AllREGeneration + AllConventional + generation.HydroPumpedStorage
TotalGeneration = generation.sum(axis=1)
# Electrcicity prices Euro*MWh * MWh = EUR 
ElectrcityMarginalCosts = generation.Nuclear*Capacity.Nuclear.PricewithCO2 + \
                            generation.Gas*Capacity.Gas.PricewithCO2 + \
                            generation.BrownCoal*Capacity.BrownCoal.PricewithCO2 + \
                            generation.HardCoal*Capacity.HardCoal.PricewithCO2 + \
                            generation.OtherConventional*Capacity.OtherConventional.PricewithCO2
# ElectricityPrices 
ElectrcityPrices = ElectrcityMarginalCosts/TotalGeneration
plt.plot(ElectrcityPrices)
plt.ylabel('Eur/MWh') 
plt.show()

#CO2 emission factor ('ton CO2/MWh') 
CO2emissionfactor = Emissions2016/TotalGeneration
plt.plot(CO2emissionfactor)
plt.ylabel('ton CO2/MWh') 
plt.show()

# residual load
residual_load = hourly_consumption - AllREGeneration 
residual_load3RE = hourly_consumption - AllREGeneration*3
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

ax2.plot(generation.index.values, residual_load,  label="Residual Load")
ax2.set_title('Residual Load')
ax2.legend( bbox_to_anchor=(1.05, 1))
ax2.set_xlabel('Month')  
ax2.set_ylabel('Mwh') 
plt.show()

residualcurve = residual_load.sort_values()[::-1]
plt.plot(residualcurve.values)

residualcurve3RE = residual_load3RE.sort_values()[::-1]
plt.plot(residualcurve3RE.values)
plt.xlabel("hours")
plt.ylabel("Capacity MWh")
plt.title("Residual Load duration curve Germany")
plt.legend(['2006', "3 times RE"])
plt.show()

# Supply curve
print(residualcurve.values.size())

# Marginalcost = []
# for i in residualcurve.values.length:
#     if i < Capacity.Nuclear.Capacity:
#         Marginalcost[i] = Capacity.Nuclear.PricewithCO2 
#     else if i < (Capacity.BrownCoal.Capacity +  Capacity.BrownCoal.Capacity)
#         Marginalcost[i] = Capacity.BrownCoal.PricewithCO2 
#     else if i < (Capacity.BrownCoal.Capacity +  Capacity.BrownCoal.Capacity + Capacity.HardCoal.Capacity)
#         Marginalcost[i] = Capacity.Nuclear.PricewithCO2

#supply curve

installedCapacity =  Capacity.Capacity.sum(axis=1)
print(installedCapacity)
# for i in 10:
#     if i < Capacity.Nuclear.Capacity:
#         Marginalcost[i] = Capacity.Nuclear.PricewithCO2 
#     else if i < (Capacity.BrownCoal.Capacity +  Capacity.BrownCoal.Capacity)
#         Marginalcost[i] = Capacity.BrownCoal.PricewithCO2 
#     else if i < (Capacity.BrownCoal.Capacity +  Capacity.BrownCoal.Capacity + Capacity.HardCoal.Capacity)
#         Marginalcost[i] = Capacity.Nuclear.PricewithCO2
# Capacity.Nuclear.PricewithCO2 








