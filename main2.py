
# Renewable Energy generation tests
import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

#Wind profile
Wind = pd.read_csv('ninja/ninja_wind_country_DE_near-termfuture-merra-2_corrected.csv', delimiter=',', header=2)
Wind.index = pd.to_datetime(Wind.time, infer_datetime_format=True)
Wind = Wind.loc["2019"]

# #PV profile
PV = pd.read_csv('ninja/ninja_pv_country_DE_merra-2_corrected.csv', delimiter=',', header=2)
PV.index = pd.to_datetime(PV.time, infer_datetime_format=True)
PV = PV.loc["2019"]

# Generation MWh
generation= pd.read_excel("smard/Actual_generation_201901010000_201912312359.xlsx", sheet_name="clean", engine='openpyxl',   parse_dates=['Datetime'])
generation.set_index(['Datetime'], drop=False)
generation.index = pd.to_datetime(generation.Datetime, infer_datetime_format=True)

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