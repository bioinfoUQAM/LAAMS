"""
HEADER 
CMS_data_analysis_HERDS.py 
    File created to load the cms data and perform a few basic analyses on it. 
 
Created on Thur Apr  2 16:07:40 2020
@author: Amanda Boatswain Jacques
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import time

# Create a list of all the files we will work with
input_path = "./input/cms_Extracts_07Apr2020/"
file_path = "cms_Herds.cpickle"
date_columns = ["exported_date", "export_start_date", "export_end_date", "crtn_date"]

# Load the Herds dataset in the folder and save to a pandas dataframe (df) 
herds = pickle.load(open(input_path + file_path, "rb"))

""" Do a bit of cleaning up """
# Convert the time data to datetimes that can be understood by pandas
herds[date_columns].apply(pd.to_datetime)

# Drop the columns that aren't needed 
herds = herds.drop(["last_modfd_by", "last_modfd_date", "cms_software_code", 
                    "cms_software_version", "installation_code", "interface_code", "manufacturer_code"], axis = 1)

# Sort the values by hrd_id > hrd_prv_id > id > export_date
herds = herds.sort_values(by=["hrd_id", "hrd_prv_cd", "id", "exported_date"])

# Rearrange the column values and drop the index column
herds = herds.reindex(columns =["id","hrd_id", "herd_prv_cd", "exported_date", "export_start_date", "export_end_date","crtn_date"])

# Print an overview of the dataset in the terminal 
print("Loaded Herds Dataset: ")
print(herds.head())

""" Create plots of the time series data """
# Calculate the duration between the start date and end date 
herds["duration (end-start)"] = herds["export_end_date"]-herds["export_start_date"]

print(herds.describe())



"""
# create a stem plot for a single cow
dates = herds["exported_date"]
dates_cow1 = list(herds[date_columns].iloc[0])
print(dates_cow1)


# Choose some nice levels
levels = np.tile([ 7, 5, 3, 1],
                 int(np.ceil(len(dates_cow1)/6)))[:len(dates_cow1)]


# Create figure and plot a stem plot with the date
fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
ax.set(title="Observed Milking pattern Dates")

markerline, stemline, baseline = ax.stem(dates_cow1, levels,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)

plt.show() 
"""


"""
plt.setp(markerline, mec="k", mfc="w", zorder=3)

# Shift the markers to the baseline by replacing the y-data by zeros.
markerline.set_ydata(np.zeros(len(dates_cow1)))


# annotate lines
vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
for d, l, r, va in zip(dates_cow1, levels, date_columns, vert):
    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
              textcoords="offset points", va=va, ha="right")

# format xaxis with 4 month intervals
ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")


# remove y axis and spines
ax.get_yaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)

ax.margins(y=0.1)
plt.show()
"""

"""
# Find the region in the df corresponding to the first cow & make sure that 
# the data is properly sorted by date
animal1 = cms_Milkings.copy()[cms_Milkings["cca_id"] == 6688]
animal1["milkng_date"] = pd.to_datetime(animal1["milkng_date"])

# Print the first few values of the new df
print("Data retrieved for the first animal: ")
print(animal1.head())

# set the index of the dataframe to the date time
animal1.set_index("milkng_date")
# drop some of the irrelevant columns
animal1 = animal1.drop(["id", "cca_id", "milkng_code", "lr_scc", "lf_scc", "rf_scc", 
              "rr_scc", "lactose", "urea", "crtn_date", "last_modfd_by", "last_modfd_date"], axis =1)

# Print some of the main statistics of this set to screen 
print("Stats: ", animal1.describe())
print("Correlations: ", animal1.corr())

# Create a simple plot of the correlations between the different variables
fig = plt.figure(figsize = (12, 12))
ax = fig.add_subplot(111)

# Add labels to the ticks and do a bit of cleaning up
ax.set_yticklabels(list(animal1.columns))
ax.set_xticklabels(list(animal1.columns))
# Format the colorbar and show the final plot 
cax = ax.matshow(animal1.corr(), cmap='RdBu', vmin=-1, vmax=1)
fig.colorbar(cax)

"""
    
    