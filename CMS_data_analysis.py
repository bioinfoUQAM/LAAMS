"""
HEADER 
CMS_data_analysis.py 
    File created to load the cms data and perform a few basic analyses on it. 
 
Created on Thur Apr  2 16:07:40 2020
@author: Amanda Boatswain Jacques
"""

import pickle
import pandas as pd

# create a list of all the files we will work with
folder_path = "./input/"
file_paths = ["cms_Animals.cpickle", "cms_Herds.cpickle", "cms_Milkings.cpickle"]
datasets = []

# load each dataset in the folder and save to a pandas dataframe 
for i, file in enumerate(file_paths): 
    datasets.append(pickle.load(open(folder_path + file, "rb")))
    
    # extract the headers (column names)
    headers = list(datasets[i])
    # print an overview of the dataset in the terminal 
    print("Loaded Dataset: " + file)
    print(datasets[i].head())

    
    
    
    
    