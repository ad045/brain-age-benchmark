# %%
import pandas as pd
import os 
  
# current directory 
path = os.path.realpath(__file__) 
dir = os.path.dirname(path) 
dir = os.path.dirname(dir) 
path_of_raw_TUAB_data = os.path.join(dir, "raw_data", "storage", "header_TUAB", "headers.txt")

# %%
# Function to extract information from a block
def extract_info(block):
    print(block)
    patient_id = block[block.find("[") + 1:block.find("]")]
    pat_id = patient_id
    # run_id = block[block[block.find(pat_id+"_s")].find(pat_id+"_s") : block[block.find(pat_id+"_s")].find(pat_id+"_s") + block.find(".edf")]
    patient_id = block[4:12] #igitt
    run_id = block[39:58]
    age_index = block.find("lpti_age")
    gender_index = block.find("lpti_gender")
    # dob_index = block.find("lpti_dob")                    # anonymous 
    eeg_id_index = block.find("lrci_eeg_id")
    duration_index = block.find("duration of recording (secs)")
    start_date_index = block.find("lrci_start_date = ")
    
    if age_index != -1: 
        age_str = block[age_index + len("lpti_age = [Age:"):block.find("]", age_index)]
        if age_str != '': 
            age = float(age_str)
        else: 
            age = None
    else:
        age = None
    
    if gender_index != -1 and gender_index != '':
        gender = block[gender_index + len("lpti_gender = ["):block.find("]", gender_index)]
    else:
        gender = None

    # if dob_index != -1:
    #     dob = block[dob_index + len("lpti_dob = ["):block.find("]", dob_index)]
    # else:
    #     dob = None

    if eeg_id_index != -1: 
        eeg_id = block[eeg_id_index + len("lrci_eeg_id = ["):block.find("]", eeg_id_index)]
    else:
        eeg_id = None
    
    if duration_index != -1:
        duration_str = block[duration_index + len("duration of recording (secs) ="):block.find("\n", duration_index)]
        if duration_str != '':
            duration = float(duration_str)
        else:
            duration = None
    else:
        duration = None
    
    if start_date_index != -1 and start_date_index != '':
        start_date = block[start_date_index + len("lrci_start_date = ["):block.find("]", start_date_index)]
    else:
        start_date = None
    
    return {"patient_id": patient_id, 
            "run_id": run_id,                   # hopefully: aaaaaaab_s003_t000
            "age": age, "gender": gender, 
            # "dob": dob, 
            "eeg_id": eeg_id, 
            "duration-sec": duration, 
            "start_date": start_date}

# %%

# Read the text file
with open(path_of_raw_TUAB_data, "r") as file:
    data = file.read()

# Split the data into blocks based on "Block 2:"
blocks = data.split("/data/isip/www/isip/projects/nedc/data/eeg/tuh_eeg/v2.0.0/edf/") #Block 2:")
# print(extract_info(block[0]))
# print(blocks[0])
# %% 

# Extract information from each block, and save as dataframe
info_list = [extract_info(block) for block in blocks if "lpti_patient_id" in block]
df = pd.DataFrame(info_list)
print(df)

# Export dataframe as csv
df.to_csv("patient_TUAB_id_age.csv")

# %%
