# Load the dictionary back from the pickle file.
import pickle
#import pandas as pd

# create a list of all the files we will work with
file_paths = ["./input/cms_Animals.cpickle", "./input/cms_Herds.cpickle", "./input/cms_Milkings.cpickle"]
datasets = []

# load each dataset to a pandas dataframe 
for i, file in enumerate(file_paths):
    datasets.append(pickle.load(open(file, "rb")))
    
    print("Reading File: ", file)
    headers = list(datasets[i])
    print("Categories in cms file: ", headers)    
    
    
    # print an overview of the dataset in the terminal 
    print("Loaded Dataset: " + file)
    print(datasets[i].head())
    print(datasets)
    
    
    
    
    