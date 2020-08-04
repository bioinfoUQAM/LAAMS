"""
HEADER
CMS_data_analysis.py
    File created to load the cms data and perform a few basic analyses on it.

Created on Thur Apr 2 16:07:40 2020
@author: Amanda Boatswain Jacques
"""

# import the necessary packages
import argparse
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from readdata import plot_features


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input path", required=True,
    help="Path to the input data")
args = vars(ap.parse_args())


# Create a list of all the files we will work with
input_path = args["input path"]
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
 

# Next, start working on the combined dataset using the included files

# Rename some of the columns for clarity and to be able to merge later
datasets["cms_Animals"].rename(columns={"id": "cca_id", "crtn_date": "animals_crtn_date"}, inplace=True)
datasets["cms_Herds"].rename(columns={"id": "cch_id", "crtn_date": "herds_crtn_date"}, inplace=True)
datasets["cms_Start_Lactations"].rename(columns={"start_date": "lactation_start_date"}, inplace=True)
datasets["cms_End_Lactations"].rename(columns={"end_date": "lactation_end_date"}, inplace=True)
datasets["cms_Milkings"].rename(columns={"crtn_date": "milkings_crtn_date"}, inplace=True)

# Drop the columns we don't need
datasets["cms_Animals"].drop(["last_modfd_by", "last_modfd_date"], inplace=True, axis = 1)
datasets["cms_Breeding_Dates"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_End_Lactations"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_Start_Lactations"].drop(["last_modfd_by", "last_modfd_date", "crtn_date"], inplace=True, axis = 1)
datasets["cms_Herds"].drop(["last_modfd_by", "last_modfd_date"], inplace=True, axis = 1)
datasets["cms_Milkings"].drop(["milkng_code", "lr_scc", "lf_scc", "rf_scc",
              "rr_scc", "lactose", "urea", "last_modfd_by", "last_modfd_date"], inplace=True, axis =1)

# Start with cms_Herds
# Rearrange the columns and sort the values
datasets["cms_Herds"] = datasets["cms_Herds"][["cch_id", "hrd_prv_cd", "hrd_id", "export_start_date", "exported_date", "export_end_date", "herds_crtn_date"]]
datasets["cms_Herds"].sort_values(by=['hrd_prv_cd', 'hrd_id', 'exported_date'])

# Next join animals and herds
datasets["cms_Animals"] = datasets["cms_Animals"][["cca_id", "cch_id", "anm_ident", "visible_id_no_6", "birth_date", "animals_crtn_date"]]
result = pd.merge(datasets["cms_Animals"], datasets["cms_Herds"][["cch_id", "hrd_id", "hrd_prv_cd", "export_start_date", "exported_date", "export_end_date", "herds_crtn_date"]], on="cch_id", how="outer")

# remove the keys since we no longer need them
#result.drop(["cca_id", "cch_id"], axis=1, inplace=True)

# Sort all the final values
result.sort_values(by=["anm_ident", "visible_id_no_6", "birth_date","hrd_prv_cd", "hrd_id", "animals_crtn_date", "herds_crtn_date"])
result = result[["cca_id", "anm_ident", "visible_id_no_6", "birth_date","hrd_prv_cd", "hrd_id", "export_start_date", "exported_date", "export_end_date", "animals_crtn_date", "herds_crtn_date"]]

result = pd.merge(result, datasets["cms_Milkings"][["cca_id", "milkng_date", "milk_wgt", "milkng_temp", "milk_flow_avg", "milk_flow_max", "fat_pcnt", "prot_pcnt", "scc", "milkings_crtn_date" ]],
                  on="cca_id", how="outer")
result = pd.merge(result, datasets["cms_Start_Lactations"][["cca_id","lact_no", "lactation_start_date"]], on ="cca_id", how="outer")
result = pd.merge(result, datasets["cms_End_Lactations"][["cca_id","lactation_end_date"]], on ="cca_id", how="outer")


print(result.head())
# Drop the cca id and visible id columns since we no longer need them anymore
result.drop(["cca_id","visible_id_no_6"], inplace=True, axis=1)

# Do a final sort on the values for the matrix
result.sort_values(by=["anm_ident", "birth_date","hrd_prv_cd", "hrd_id","milkng_date", "animals_crtn_date", "herds_crtn_date"])
result = result[["anm_ident", "birth_date","hrd_prv_cd", "hrd_id", "export_start_date", "lact_no", "lactation_start_date", "lactation_end_date",
                 "exported_date", "export_end_date", "milkng_date", "milk_wgt", "milkng_temp", "milk_flow_avg", "milk_flow_max", "fat_pcnt", "prot_pcnt", "scc", "milkings_crtn_date","animals_crtn_date", "herds_crtn_date"]]

print("Final Dataframe")
print(result.head())



