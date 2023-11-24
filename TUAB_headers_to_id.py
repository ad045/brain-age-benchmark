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
    patient_id = block[block.find("[") + 1:block.find("]")]
    age_index = block.find("lpti_age")
    gender_index = block.find("lpti_gender")
    # dob_index = block.find("lpti_dob")                    # anonymous 
    eeg_id_index = block.find("lrci_eeg_id")
    duration_index = block.find("duration of recording (secs)")
    start_date_index = block.find("lrci_start_date = ")
    
    if age_index != -1:
        age = block[age_index + len("lpti_age = [Age:"):block.find("]", age_index)]
    else:
        age = None
    
    if gender_index != -1:
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
        duration = block[duration_index + len("duration of recording (secs) ="):block.find("\n", duration_index)]
    else:
        duration = None
    
    if start_date_index != -1:
        start_date = block[start_date_index + len("lrci_start_date = ["):block.find("]", start_date_index)]
    else:
        start_date = None
    
    return {"patient_id": patient_id, 
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
blocks = data.split("Block 2:")

# Extract information from each block
info_list = [extract_info(block) for block in blocks if "lpti_patient_id" in block]

# Create a DataFrame
df = pd.DataFrame(info_list)

# Print the DataFrame
print(df)

df.to_csv("patient_TUAB_id_age.csv")

# %%
