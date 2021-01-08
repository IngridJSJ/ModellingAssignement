# unit commitment
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

Nuclearcolor = "#ffff00"
Renewablescolor = "#009900"
Gascolor = "#ffcc00"
Nuclearcolor = "#ffff00"
Lignitecolor = "#cc9900"
Coalcolor = "#000000"
Othercolor = "#6600ff"
# Installed capacity MW
Prices2019 = pd.read_excel("Ewi/installed-capacity-2019.xlsx", sheet_name="prices", usecols="A:J", engine='openpyxl', index_col="Prices")
Plants = pd.read_excel("Ewi/installed-capacity-2019.xlsx", sheet_name="Plants", usecols="O,X:AA", engine='openpyxl')
DayAheadprices = pd.read_excel("smard/Day-ahead_prices_201901010000_201912312359.xlsx", sheet_name="Day-ahead prices", usecols="C:D", engine='openpyxl', nrows=8761, parse_dates=["Datetime"])
DayAheadprices.set_index(['Datetime'], drop=False)
DayAheadprices.index = pd.to_datetime(DayAheadprices.Datetime, infer_datetime_format=True)
#print(DayAheadprices.info())
# Generation MWh
generation= pd.read_excel("smard/Actual_generation_201901010000_201912312359.xlsx", sheet_name="clean", engine='openpyxl',   parse_dates=['Datetime'])
generation.set_index(['Datetime'], drop=False)
generation.index = pd.to_datetime(generation.Datetime, infer_datetime_format=True)
hourly_consumption = generation.Consumption
#print(generation.info())

AllREGeneration = generation.Biomass + generation.Hydropower + generation.WindOffshore + generation.WindOnshore +  generation.Photovoltaics + generation.OtherRE
AllConventional = generation.Nuclear + generation.BrownCoal + generation.HardCoal + generation.Gas + generation.OtherConventional 
TotalGeneration = AllREGeneration + AllConventional + generation.HydroPumpedStorage
NetExports = generation.exports + generation.imports 
#Electrcicity prices Euro*MWh * MWh = EUR 
ElectrcityMarginalCosts = generation.Nuclear*Prices2019.Nuclear.totalCosts + \
                            generation.Gas*Prices2019.Gas.totalCosts + \
                            generation.BrownCoal*Prices2019.Lignite.totalCosts+ \
                            generation.HardCoal*Prices2019.HardCoal.totalCosts + \
                            generation.OtherConventional*Prices2019.Oil.totalCosts

# ElectricityPrices 
ElectrcityPricesbyGeneration = ElectrcityMarginalCosts/AllConventional
#Emissions
# MWh * tonCO2/ MWh = ton CO2
Emissions2019 = generation.Gas*Prices2019.Gas.emissions/Prices2019.Gas.efficiency \
                + generation.BrownCoal*Prices2019.Lignite.emissions/Prices2019.Lignite.efficiency\
                + generation.HardCoal*Prices2019.HardCoal.emissions /Prices2019.HardCoal.efficiency \
                + generation.OtherConventional*Prices2019.Special.emissions/Prices2019.HardCoal.efficiency
#CO2 emission factor ('ton CO2/MWh') 
CO2emissionfactor = Emissions2019/TotalGeneration

# residual load
residual_load = hourly_consumption - AllREGeneration 
residual_load_Exports = hourly_consumption + NetExports - AllREGeneration + NetExports
residual_load_nonuclear = residual_load + generation.Nuclear
residual_load3RE = hourly_consumption - AllREGeneration*3

Residualload = residual_load.values
ResidualloadExports = residual_load_Exports.values
loadcurve = hourly_consumption.sort_values()[::-1]
loadcurve_noNuclear = residual_load_nonuclear.sort_values()[::-1]

residualcurve = residual_load.sort_values()[::-1]
residualcurve_Exports = residual_load_Exports.sort_values()[::-1]
residualcurve3RE = residual_load3RE.sort_values()[::-1]

# Supply curve
#installedCapacity =  Capacity.loc["Capacity"].sum()

#Residualload = [x for x in Residualload if str(x) != 'nan']
Marginalcost =[]
Marginaltechnology =[]
# DISPATCH Algorithm
for num, load_H in enumerate(Residualload, start=1):  
    result_index =  (load_H - Plants.CumulativeCapacity).lt(0).idxmax()
    Marginalcost.append(Plants.Grenzkosten[result_index])
# exports
MarginalcostExports =[]
for num, load_H in enumerate(ResidualloadExports, start=1):  
    result_index =  (load_H - Plants.CumulativeCapacity).lt(0).idxmax()
    MarginalcostExports.append(Plants.Grenzkosten[result_index])

#no nuclear
PlantsNoNuclearindex  = Plants['Fuel'] != "Kernenergie"
PlantsNoNuclear  = Plants[PlantsNoNuclearindex]
MarginalcostNONUCLEAR =[]
for num, load_H in enumerate(Residualload, start=1):  
    result_index =  (load_H - PlantsNoNuclear.CumulativeCapacity).lt(0).idxmax()
    MarginalcostNONUCLEAR.append(PlantsNoNuclear.Grenzkosten[result_index])   
#no coal
PlantsNoCoalindex = Plants['Fuel'] != "Steinkohle"
PlantsNoCoalNoLigniteindex = Plants['Fuel'] != "Braunkohle"
PlantsNoCoalNoLigniteNonuclear = Plants[PlantsNoNuclearindex & PlantsNoCoalNoLigniteindex & PlantsNoCoalindex] 

MCNoCoalNoLigniteNonuclear =[]
for num, load_H in enumerate(Residualload, start=1):  
    result_index =  (load_H - PlantsNoCoalNoLigniteNonuclear.CumulativeCapacity).lt(0).idxmax()
    MCNoCoalNoLigniteNonuclear.append(PlantsNoCoalNoLigniteNonuclear.Grenzkosten[result_index])    



# plt.plot(DayAheadprices.index.values, Marginalcost)
# plt.plot(DayAheadprices.index.values, MarginalcostExports)
# plt.plot(DayAheadprices.index.values, DayAheadprices.Prices)
# plt.legend(["Marginal costs","MC Exports", "Day ahead prices"])
# plt.ylabel('Eur/MWh') 
# plt.show()   

# plt.plot(Marginalcost)
# plt.plot(MarginalcostNONUCLEAR)
# plt.plot(MCNoCoalNoLigniteNonuclear)
# plt.legend(['MC', "MC no Nuclear", "MC no lignite"])
# plt.title("FUTURE SCENARIOS")
# plt.ylabel('Eur/MWh') 
# plt.show()   
#-----------------------------------------------SORTED
Dayahead = DayAheadprices.Prices.values
Dayahead.sort()
Marginalcost.sort()
MarginalcostExports.sort()
MarginalcostNONUCLEAR.sort()
MCNoCoalNoLigniteNonuclear.sort()

plt.plot(Marginalcost)
plt.plot(MarginalcostExports)
plt.plot(Dayahead)
plt.legend(["Marginal costs","MC Exports", "Day ahead prices"])
plt.ylabel('Eur/MWh') 
plt.title("SORTED MARGINAL COST")
plt.show()

plt.plot(Marginalcost)
plt.plot(MarginalcostNONUCLEAR)
plt.plot(MCNoCoalNoLigniteNonuclear)
plt.legend(["Marginal costs","No nuclear", "No nuclear, no coal"])
plt.ylabel('Eur/MWh') 
plt.title("SORTED FUTURE SCENARIOS")
plt.show()




#-----------------------------------------------------------------------------------------------------------------------------
# GRAPHS

# plt.plot( generation.index.values, hourly_consumption  , color="pink", label="consumption")
# labels = [ "Renewables" ,  "Nuclear"   ,  "Gas"  , "Lignite" , "Coal" ,"Other" ]
# pal = (Renewablescolor ,  Nuclearcolor ,  Gascolor , Lignitecolor, Coalcolor,Othercolor)
# plt.stackplot(generation.index.values , AllREGeneration, generation.Nuclear  , generation.Gas , generation.BrownCoal , generation.HardCoal , generation.OtherConventional , colors=pal, labels=labels)
# #plt.stackplot(generation.index.values , generation.Biomass  , generation.Hydropower , generation.WindOffshore , generation.WindOnshore , generation.Photovoltaics , generation.OtherRE )
# plt.legend()
# plt.show()
# fig, ax1 = plt.subplots()




# plt.plot(CO2emissionfactor)
# plt.title('CO2 emission factor') 
# plt.ylabel('ton CO2/MWh') 
# plt.show()


# Renewable energy generation'
# labels = [ "Biomass", "Hydropower", "Wind offshore", "Wind onshore", "Photovoltaics" , "OtherRE" ]
# pal = [ "#009933", "#66ccff",  "#000099", "#0000ff", "#ffcc00", "#9900ff" ]
# fig, (ax1, ax2) = plt.subplots(2, sharex=True)
# ax1.plot( generation.index.values, hourly_consumption/1000  , color="pink", label="consumption")
# ax1.stackplot(generation.index.values , generation.Biomass/1000 , generation.Hydropower/1000, generation.WindOffshore/1000, generation.WindOnshore/1000, generation.Photovoltaics/1000, generation.OtherRE/1000 ,   
# labels=labels, colors =pal)
# ax1.legend()
# #ax1.legend( bbox_to_anchor=(1.05, 1))
# ax1.set_title('Renewable energy generation')
# ax1.set_ylabel('GW') 
# ax2.plot(generation.index.values, residual_load/1000,  label="Residual Load")
# ax2.set_title('Residual Load')
# ax2.legend()
# #ax2.legend( bbox_to_anchor=(1.05, 1))
# ax2.set_xlabel('Month')  
# ax2.set_ylabel('GW') 
# plt.show()

# #Residual Curve
# plt.plot(loadcurve.values)
# plt.plot(residualcurve.values)
# plt.plot(residualcurve3RE.values)
# plt.plot(residualcurve_Exports.values)
# plt.xlabel("hours")
# plt.ylabel("Capacity MW")
# plt.title("Residual Load duration curve Germany")
# plt.legend(["2019 Load", '2019 residual load', "3 times RE generation", " plus exports"])
# plt.show()



#-------------------------------------------------------------------------------------------------------------------------------------------------
#df = pd.read_excel("national_generation_capacity.xlsx", sheet_name="output", usecols="A,LI", engine='openpyxl')

# # #PV profile
# PV = pd.read_csv('ninja/ninja_pv_country_DE_merra-2_corrected.csv', delimiter=',')
# PV.index = pd.to_datetime(PV.time, infer_datetime_format=True)
# indexdatesPV = PV[ (  PV["time"]< "2016-01-01")   ].index 
# PV.drop(indexdatesPV , inplace=True)
# indexdatesPV = PV[ (  PV["time"]> "2017-01-01")   ].index 
# PV.drop(indexdatesPV , inplace=True)
# #Wind profile
# Wind = pd.read_csv('ninja/ninja_wind_country_DE_near-termfuture-merra-2_corrected.csv', delimiter=',')
# Wind.index = pd.to_datetime(Wind.time, infer_datetime_format=True)
# indexdatesWind = Wind[ (  Wind["time"]< "2016-01-01")   ].index 
# Wind.drop(indexdatesWind , inplace=True)
# indexdatesWind = Wind[ (  Wind["time"]> "2017-01-01")   ].index 
# Wind.drop(indexdatesWind , inplace=True)

# plt.plot(PV.national, color="#FFC300", zorder=1)
# plt.plot(Wind.offshore, color="#000099", zorder=2)
# plt.plot(Wind.onshore,color="#0000ff", zorder=3)
# plt.legend(["PV", "offshore", "onshore"])
# plt.show()

# #POWER PLANTS RENEWABLES 
# PowerPlants = pd.read_csv('openpower/renewable_power_plants_DE_2020.csv', usecols=[1,2,3,4,5,16,17], parse_dates=['commissioning_date', 'decommissioning_date'])
# PowerPlants['commissioning_date']= pd.to_datetime(PowerPlants['commissioning_date'])
# indexdatescomission = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01")  ].index
# indexdates = PowerPlants[ (PowerPlants["commissioning_date"]< "2017-01-01") & (PowerPlants["decommissioning_date"]< "2016-01-01") ].index
# PowerPlants.drop(indexdates , inplace=True)
# uniquetechnology = PowerPlants["energy_source_level_2"].unique() 
# print(uniquetechnology)



# OLD CAPACITY PRICES
#Capacity = pd.read_excel("smard/Installed_generation_capacity_201601010000_201612312359.xlsx", sheet_name="capacity", usecols="A:M", engine='openpyxl', index_col="Names")
# Electrcicity prices Euro*MWh * MWh = EUR 
# ElectrcityMarginalCosts = generation.Nuclear*Capacity.Nuclear.PricewithCO2 + \
#                             generation.Gas*Capacity.Gas.PricewithCO2 + \
#                             generation.BrownCoal*Capacity.BrownCoal.PricewithCO2 + \
#                             generation.HardCoal*Capacity.HardCoal.PricewithCO2 + \
#                             generation.OtherConventional*Capacity.OtherConventional.PricewithCO2

# ElectricityDemand 
# load = pd.read_excel("smard/Actual_consumption_201901010000_201912312359.xlsx", sheet_name="clean", engine='openpyxl',   parse_dates=['Datetime'])
# load.index = pd.to_datetime(load.Datetime, infer_datetime_format=True)
# load.set_index(['Datetime'], drop=False)
# hourly_consumption = load.Total

#Emissions2016 = generation.Gas*Capacity.Gas.EmissionsperMWh + generation.BrownCoal*Capacity.BrownCoal.EmissionsperMWh + generation.HardCoal*Capacity.HardCoal.EmissionsperMWh + generation.OtherConventional*Capacity.OtherConventional.EmissionsperMWh
#CO2 emission factor ('ton CO2/MWh') 
#CO2emissionfactor = Emissions2016/TotalGeneration

# ax1.plot(DayAheadprices.Prices)
# ax1.plot(DayAheadprices.index.values, ElectrcityPricesbyGeneration)
# plt.title('Electricity prices') 
# plt.legend(["day ahead", "by generation"])
# plt.ylabel('Eur/MWh') 
# ax2 = ax1.twinx() 
# color = 'tab:red'
# ax2.plot(DayAheadprices.index.values,residual_load, color=color)
# fig.tight_layout()
# plt.show()