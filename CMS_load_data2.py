"""
HEADER
CMS_data_analysis.py
    File created to load the cms data and perform a few basic analyses on it.

Created on Thur Apr 2 16:07:40 2020
@author: Amanda Boatswain Jacques
"""

# import the necessary packages
# import argparse
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from readdata import plot_features

"""
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input path", required=True,
    help="Path to the input data")
args = vars(ap.parse_args())
"""

# Create a list of all the files we will work with
input_path = "./input/cms_Extracts_03Jun2020/"
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
        

 
"""
clean up code using this:
import pandas as pd

df = pd.read_csv(
    "groupby-data/airqual.csv",
    parse_dates=[["Date", "Time"]],
    na_values=[-200],
    usecols=["Date", "Time", "CO(GT)", "T", "RH", "AH"]
).rename(
    columns={
        "CO(GT)": "co",
        "Date_Time": "tstamp",
        "T": "temp_c",
        "RH": "rel_hum",
        "AH": "abs_hum",
    }
).set_index("tstamp")

"""    


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

# Drop the cca id and visible id columns since we no longer need them anymore
result.drop(["cca_id","visible_id_no_6"], inplace=True, axis=1)

# Do a final sort on the values for the matrix
result.sort_values(by=["anm_ident", "birth_date","hrd_prv_cd", "hrd_id","milkng_date", "animals_crtn_date", "herds_crtn_date"])
result = result[["anm_ident", "birth_date","hrd_prv_cd", "hrd_id", "export_start_date", "lact_no", "lactation_start_date", "lactation_end_date",
                 "exported_date", "export_end_date", "milkng_date", "milk_wgt", "milkng_temp", "milk_flow_avg", "milk_flow_max", "fat_pcnt", "prot_pcnt", "scc", "milkings_crtn_date","animals_crtn_date", "herds_crtn_date"]]

print("Final Dataframe")
print(result.head())
print("Before dropping the NA :", result.shape)

# create months after birth (MAB)

# Dropping the NA when there is no value on the current columns
result= result.dropna(how="any",subset=["birth_date", "milkng_date"])
print("After dropping the NA :", result.shape)

#Creating custom columns for MaB, MaBint, seasons, profits
result["MaB"]= (pd.to_datetime(result.milkng_date) - pd.to_datetime(result.birth_date)).astype('timedelta64[D]')/365.25*12
result["MaBint"] = round(result.MaB)

#print(result.head())
result["SPRI"]=result.milkng_date.astype(str).str[5:7].astype(int).isin([4,5,6])
result["SUMM"]=result.milkng_date.astype(str).str[5:7].astype(int).isin([7,8,9])
result["FALL"]=result.milkng_date.astype(str).str[5:7].astype(int).isin([10,11,12])
result["WINT"]=result.milkng_date.astype(str).str[5:7].astype(int).isin([1,2,3])


print(result.head())

subsample = result[["anm_ident", "milkng_date", "milk_wgt","scc", "MaB", "SPRI", "SUMM", "FALL", "WINT"]]
print(subsample.head())
pd.to_datetime(subsample["milkng_date"])
new = subsample[["milk_wgt", "scc"]].groupby([subsample["anm_ident"], subsample['milkng_date'].dt.date]).milk_wgt.agg(['count','min','max','mean']).rename_axis(["ANM_IDENT", "Date"])
new.index


new["count"].plot.hist(alpha=0.5)
#new.iloc[0]
plt.legend(title = "Milkings", loc='upper right', labels = ["milking count", "minimum ", "maximum", "mean"])
plt.title("Milking Activity for " + "anm_0")
plt.ylabel("Weight (kg)")




# Create a simple plot of the correlations between the different variables
"""
for name in sorted(list((set(new.index.get_level_values(0))))): 
    ("Cow ident: ", name)
    new.loc[name].plot()
    plt.legend(title = "Milkings", loc='upper right', labels = ["milking count", "minimum ", "maximum", "mean"])
    plt.title("Milking Activity for " + name)
    plt.ylabel("Weight (kg)")
    plt.ylim(0, 30)
    #plt.show()
    plt.savefig('milking_'+name)
    #format dates on x-axis 
    
"""




"""
#new.index = new.index.set_names(["ANM_IDENT", "Week", "Month", "Day"])
#print(new.unstack())

print(new.index[0])

for state, frame in new:
    print(f"First 2 entries for {state!r}")
    print("------------------------")
    print("State:", state)
    print("Frame:", frame)
    #print(frame.head(2), end="\n\n")

#print(new.loc[new["count"]=="anm_0"])


# playing around with Dataframe structures 
#new2 = pd.MultiIndex.from_frame(new)
#print(new2.columns)


#(new.index.get_level_values)
#new.unstack(level=0).plot(kind='bar', subplots=True, figsize=(15, 4))
"""