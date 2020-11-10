# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 14:36:41 2020
@author: Amanda
"""

import pickle
import os 
import pandas as pd
pd.options.mode.chained_assignment = None
import datetime
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
from readdata import plot_features
#plt.rcParams.update({'font.size': 22})



""" Load the dataframe into memory """
# Create a list of all the files we will work with
input_path = "./input/anoMilkings.cpickle"
result = pickle.load(open(input_path, "rb"))
# Convert all column names to lower case
result = result.rename(str.lower, axis='columns')

""" Do some cleaning on the dataset """
# Dropping the NA when there is no value on the current columns
print("Before dropping the NA :", result.shape)
result = result.dropna(how="any", subset=["lact_no", "milkng_date"])
print("After dropping the NA :", result.shape)

# Remove Duplicates 
result = result.drop_duplicates(subset=["milkng_date", "milk_wgt", 
                                              "milkng_temp", "milk_flow_avg", 
                                              "milk_flow_max", "fat_pcnt", "prot_pcnt"])

# Print size of the df after dropping duplicates
print("After dropping the duplicates:", result.shape)


""" Add any additional columns we might need """
# Convert all the time columns to datetime objects
#result = pd.to_datetime(["milkng_date"], errors='coerce')
# Create a column for the date of milking (excluding time)
result["milkng_day"] = result["milkng_date"].dt.date
result.set_index("milkng_day")


"""
BIRTH DATE DOES NOT EXIST IN THIS DATAFRAME => CANNOT DO MaB AGE CONVERSION

# Creating custom columns for MaB, MaBint (integer value), seasons
result["MaB"]= (pd.to_datetime(result.milkng_date) - pd.to_datetime(result.birth_date)).astype('timedelta64[D]')/365.25*12
result["MaBint"] = round(result.MaB) 
"""

# Calculate the season by seperating the year into quarters 
result["WINT"]= result.milkng_date.astype(str).str[5:7].astype(int).isin([1,2,3])
result["SPRI"]= result.milkng_date.astype(str).str[5:7].astype(int).isin([4,5,6])
result["SUMM"]= result.milkng_date.astype(str).str[5:7].astype(int).isin([7,8,9])
result["FALL"]= result.milkng_date.astype(str).str[5:7].astype(int).isin([10,11,12])
print(result.head)


""" Plot some of the distributions in this new dataset """

#plot_features(result, ["dim", "lact_no", "milk_wgt", "milkng_temp", "milk_flow_avg", "milk_flow_max", "fat_pcnt", "prot_pcnt"])

""" Group the data by animal, laction #, milking day, week and month """

print("Grouping Data....")
anm_group = result.groupby(["anm_id"])
anm_group_lactation = result.groupby(["anm_id", pd.Grouper(key="lact_no")])
sample1 = pd.DataFrame(dtype=float)

# can use freq = "M", "W" with the key variable to group by month and week 
#anm_group = result.groupby(["anm_ident", pd.Grouper(key="milkng_day")]).milk_wgt.agg(['count','min','max','mean'])
anm_group_day = result.groupby(["anm_id", pd.Grouper(key="milkng_day")])
anm_group_day_summ = result.groupby(["anm_id", pd.Grouper(key="milkng_day")]).agg({"milkng_date":['count'],
                                                                                 "milk_wgt": ['sum','min','max','mean', 'std', 'var', 'sem'], 
                                                                                 "milkng_temp" : ['min','max','mean', 'std', 'var', 'sem'],
                                                                                 "milk_flow_avg": ['min','max','mean', 'std', 'var', 'sem'],
                                                                                 "milk_flow_max": ['min','max','mean', 'std', 'var', 'sem'],
                                                                                 "fat_pcnt": ['min','max','mean', 'std', 'var', 'sem'],
                                                                                 "prot_pcnt": ['min','max','mean', 'std', 'var', 'sem']})


# Create plots of the different traits in the data

"""
#HISTOGRAMS 
fig1 = plt.figure()
(result["prot_pcnt"]/100).plot.hist()
plt.legend(loc="upper right")
plt.title("Milk Protein Percentage Distribution")
plt.ylabel("Count")
plt.xlabel("Percentage (%)")
#plt.xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-10-31'))
#plt.xlim(0, 20 )
#ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.savefig("AnoMilkings_prot_percentage")
plt.show()
plt.close()
"""

"""
#BOXPLOTS 
fig2 = plt.figure()
# percentages = result[["prot_pcnt", "fat_pcnt"]]*(1/100)
percentages = result[["milk_wgt"]]
percentages.boxplot()
plt.legend(loc="upper right")
plt.title("Milk Weight Boxplot")
plt.ylabel("Value (Kg)")
plt.xlabel("Milking Trait")
#plt.xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-10-31'))
#plt.xlim(0, 20 )
#ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.savefig("AnoMilkings_milk_weight_boxplot")
plt.show()
plt.close()
"""


"""
for name, group in anm_group:
    print("Name: ", name)
    ax1 = plt.figure().gca()
    #sample1 = anm_group_lactation.get_group(("anm_92", 2))
    sample1 = anm_group.get_group(name)
    print(sample1.head())
    sample1.loc[:,"milk_time_diff"] = pd.to_timedelta(sample1["milkng_date"].diff())
    sample1.loc[:,"milk_time_diff_flt"] = (sample1["milk_time_diff"].dt.total_seconds()/3600).map('{:,.4f}'.format)
    sample1["milk_time_diff_flt"] = sample1["milk_time_diff_flt"].str.replace(',','').astype(float)
    sample1.loc[:,"rolling_time"]= sample1["milk_time_diff_flt"].rolling(window=13).mean()
    sample1.loc[:,"rolling_yield"] = sample1["milk_wgt"].rolling(window=13).mean()
    sample1.loc[:,"rolling_yield_smoothed"] = sample1["rolling_yield"].rolling(3, win_type='gaussian').mean(std=1)
    sample1.loc[:,"24_hr_yield"] = (sample1["rolling_yield"]/sample1["rolling_time"])*24
    sample1.loc[:,"24_hr_yield_smoothed"] = (sample1["rolling_yield_smoothed"]/sample1["rolling_time"])*24
    
    ax1 = plt.figure(figsize = (20, 12)).gca()
    anm_group_day_summ.loc[name]["milk_wgt"]["sum"].plot()
    sample1.plot(ax=ax1, x="milkng_day", y="24_hr_yield", style = '--')
    #sample1.plot(ax=ax1, x="milkng_day", y="24_hr_yield_smoothed", style = '--')
    ax1.legend(labels = ("Daily sum", "Estimated 24-Hour Daily Yield"), loc="upper right")
    plt.title("Milk yield for " + name.upper())
    plt.ylabel("Milk Weight (Kg)")
    plt.xlabel("Time")
    plt.xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-10-31'))
    plt.ylim(0, 80)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig('milking_weight_kg_24hr_unsmoothed_'+ name)
    #plt.show()
    plt.close()
"""   

#sample1["milk_time_diff"] = sample1["milkng_date"].diff(pd.to_datetime(result.milkng_date))


"""
for name, group in list(anm_group_lactation.groups):
    print(anm_group_lactation.get_group((name, group)))
"""