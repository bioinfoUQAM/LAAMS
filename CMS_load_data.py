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
file_paths = ["cms_Animals.cpickle", "cms_Herds.cpickle", "cms_Milkings.cpickle"]
datasets = []

# Load each dataset in the folder and save to a pandas dataframe (df) 
for i, file in enumerate(os.listdir(input_path)): 
    if file.endswith(".cpickle"):
        datasets.append(pickle.load(open(input_path + file, "rb")))
        # Print an overview of the dataset in the terminal 
        print("Loaded Dataset: " + file)
        print(datasets[i].head())
