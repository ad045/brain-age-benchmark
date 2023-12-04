# %%

# python 3.12.* needed >> use env testing_py_3_12
import os
import pandas as pd
import pyedflib

#%%

folder_path_eval = '/u/home/dena/Documents/clean_brain_age/raw_data/storage/TUAB/eval/normal/01_tcp_ar'
folder_path_train = '/u/home/dena/Documents/clean_brain_age/raw_data/storage/TUAB/train/normal/01_tcp_ar'


# %%

def read_edf_header(file_path):
    # Open the EDF file
    f = pyedflib.EdfReader(file_path)
    
    # Get basic information from the header
    file_info = {
        'file_duration': f.file_duration,
        'startdate': f.getStartdatetime(),
        'patient_info': f.getPatientInfo(),
        'signals_in_file': f.signals_in_file,
        'labels': f.getSignalLabels(),
        'sample_frequency': f.getSampleFrequencies(),
        'digital_maximum': f.getDigitalMaximum(),
        'digital_minimum': f.getDigitalMinimum(),
        'physical_maximum': f.getPhysicalMaximum(),
        'physical_minimum': f.getPhysicalMinimum(),
        'transducer_type': f.getTransducer(0),  # Change the index (0) as needed
        'prefilter': f.getPrefilter(0),  # Change the index (0) as needed
    }
    
    # Close the EDF file
    f.close()
    
    return file_info


# %% 

# Iterate through all files in the folder
for filename in os.listdir(folder_path_eval):
    file_path = os.path.join(folder_path_eval, filename)
    
    # Check if it's a regular file
    if os.path.isfile(file_path):
        print(file_path)
        edf_header = read_edf_header(file_path)
    else:
        print("Unable to read EDF header.")


# %%


# Example usage
file_path = '/path/to/your/file.edf'
edf_header = read_edf_header(file_path)
print(edf_header)