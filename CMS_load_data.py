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
import os


# Create a list of all the files we will work with
input_path = "./input/cms_Extracts_07Apr2020/"
file_paths = os.listdir(input_path)
datasets = dict()

# Load each dataset in the folder and save to a pandas dataframe (df) 
for i, file in enumerate(os.listdir(input_path)): 
    if file.endswith(".cpickle"):
        # load the dataframe 
        df = pickle.load(open(input_path + file, "rb"))
        # convert all column names to lower case  
        df = df.rename(str.lower, axis='columns')
        
        # Store all the final dataframes in a dictionary 
        datasets[file.split(".")[0]] = df
        
        # Print an overview of the dataset in the terminal 
        print("Loaded Dataset {}: {}".format(i, file))
        print(datasets[file.split(".")[0]].head())
        print(" ")

# Next, start working on the combined dataset using the included files

# Rename the id column in cms_Animals
datasets["cms_Animals"].rename(columns={'id': 'cca_id'}, inplace=True)  
datasets["cms_Herds"].rename(columns={'id': 'cch_id'}, inplace=True)  
  
# Drop the columns we don't need 
datasets["cms_Animals"].drop(["visible_id_no_6", "last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)    
datasets["cms_Breeding_Dates"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_End_Lactations"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_Start_Lactations"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_Herds"].drop(["last_modfd_by", "last_modfd_date", "cms_software_code", 
                    "cms_software_version", "installation_code", "interface_code", "manufacturer_code"], inplace=True, axis = 1) 
datasets["cms_Milkings"].drop(["milkng_code", "lr_scc", "lf_scc", "rf_scc", 
              "rr_scc", "lactose", "urea", "crtn_date", "last_modfd_by", "last_modfd_date"], inplace=True, axis =1)       

# Merge the datasets to create a final one
result = pd.merge(datasets["cms_Animals"], datasets["cms_Breeding_Dates"][["cca_id", "service_date"]], 
                  on="cca_id", how="right")

result = pd.merge(result, datasets["cms_Start_Lactations"][["cca_id", "lact_no", "start_date"]], 
                  on="cca_id", how="left")

result = pd.merge(result, datasets["cms_Start_Lactations"][["cca_id", "lact_no", "start_date"]], 
                  on="cca_id", how="outer")

result = pd.merge(result, datasets["cms_End_Lactations"][["cca_id", "end_date"]], 
                  on="cca_id", how="outer")

result = pd.merge(result, datasets["cms_Herds"][["cch_id", "hrd_id", "hrd_prv_cd"]], 
                  on="cch_id", how="outer")

result = pd.merge(result, datasets["cms_Milkings"][["cca_id", "milk_wgt", "milkng_temp", "milk_flow_avg", "milk_flow_max", "fat_pcnt", "prot_pcnt", "scc" ]], 
                  on="cca_id", how="right")

print(result.head())
 
        