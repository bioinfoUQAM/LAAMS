"""
HEADER 
CMS_data_analysis.py 
    File created to load the cms data and perform a few basic analyses on it. 
 
Created on Thur Apr  2 16:07:40 2020
@author: Amanda Boatswain Jacques
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# Create a list of all the files we will work with
input_path = "./input/"
file_paths = ["cms_Animals.cpickle", "cms_Herds.cpickle", "cms_Milkings.cpickle"]
datasets = []

# Load each dataset in the folder and save to a pandas dataframe (df) 
for i, file in enumerate(file_paths): 
    datasets.append(pickle.load(open(input_path + file, "rb")))
    
    # Print an overview of the dataset in the terminal 
    print("Loaded Dataset: " + file)
    print(datasets[i].head())

# First try looking at the milking data values for a single cow
cms_Milkings = datasets[2]

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

    
    