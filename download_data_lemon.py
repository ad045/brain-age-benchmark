# %% 

import os
import pathlib
import urllib.request
import pandas as pd


DEBUG = False
url_lemon = ('https://ftp.gwdg.de/pub/misc/MPI-Leipzig_Mind-Brain-Body-LEMON'
             '/EEG_MPILMBB_LEMON/EEG_Raw_BIDS_ID')                             # removed a dash at the end

lemon_info = pd.read_csv(
  "./META_File_IDs_Age_Gender_Education_Drug_Smoke_SKID_LEMON.csv")

#%% start: added by ad                                                         # ad
matching_df = pd.read_csv("name_match_LEMON.csv")                              

lemon_info["ID"] = None                                                        # ad

for (initial_ID, INDI_ID) in zip(matching_df.Initial_ID, matching_df.INDI_ID): # ad
    lemon_info.loc[lemon_info["Unnamed: 0"] == INDI_ID,"ID"] = initial_ID      # ad

# end
#%%

data_path = pathlib.Path("storage/store3/data/LEMON_RAW")                      # ad: removed /, since that would need higher permission

if not data_path.exists():
    os.makedirs(data_path)

subjects = sorted(lemon_info.ID)

# print(subjects)

# %% 

if DEBUG:
    subjects = subjects[:1]

extensions = ["eeg", "vhdr", "vmrk"]
good_subjects = list()

for sub in subjects:
    for ext in extensions:
        sub_url = f"{sub}/RSEEG/{sub}.{ext}"
        url = f"{url_lemon}/{sub_url}"
        out_path = data_path / sub / "RSEEG"
        if not out_path.exists():
            os.makedirs(out_path)
        out_name = out_path / f"{sub}.{ext}"
        try:
            urllib.request.urlretrieve(url, out_name)
            good_subjects.append(sub)
        except Exception as err:
            print(err)

good_subs_df = pd.DataFrame(dict(subject=list(set(good_subjects))))
good_subs_df.to_csv('good_subjects.csv')
