# Load the dictionary back from the pickle file.
import pickle
#import pandas as pd

# create a list of all the files we will work with
file_paths = ["cms_Animals.cpickle", "cms_Herds.cpickle", "cms_Milkings.cpickle"]
datasets = []

# load each dataset to a pandas dataframe 
for i, file in enumerate(file_paths): 
    datasets.append(pickle.load( open(file_paths[i], "rb" ) ))
    
    # print an overview of the dataset in the terminal 
    print("Loaded Dataset: " + file)
    print(datasets[i].head())
    print(datasets)
    
    
    
    
    