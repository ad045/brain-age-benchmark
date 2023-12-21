# %% TUAB DOES NOT WORK YET!! 




# functions: 
    # plot_time_plot
    # plot_freq_plot
    # plot_histogram_durations

# helper-functions: 
    # get_raw_data
    # get_durations_of_measurements

# Best: Run in interactive window, to get plots directly

import os
import mne
import mne.io
from pathlib import Path
from mne_bids import read_raw_bids, BIDSPath
import matplotlib.pyplot as plt
import matplotlib as mpl
#!%matplotlib qt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import json
# mpl.use("Qt5Agg")

# %%
BIDS_ROOTS = {
    "LEMON": "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/bids_LEMON/data", 
    "CHBP": "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/CHBP", 
    "CamCAN": "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/CamCAN/storage/raw_data/cc700/meg/pipeline/release005/BIDSsep/rest",
    "TUAB_eval": "/vol/aimspace/users//u/home/dena/Documents/clean_brain_age/brain-age-benchmark/processed_TUAB", 
    # "TUAB_train": "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/TUAB/train/normal/01_tcp_ar"
}

EXAMPLE_PARTICIPANTS = {
    "LEMON": "010010", 
    "CHBP": "CBM00266",  
    "CamCAN": "CC110101",
    "TUAB": "aaaaajez",
    # "TUAB_train": "aaaaaaff"
}

# dataset = "LEMON"
# bids_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/bids_LEMON/data" #_one_participant" #/data"

# %%

def get_raw_data(dataset, subject, datatype): 
    # datatype: "eeg" or "meg"
    bids_root = BIDS_ROOTS[dataset]
    bids_path = BIDSPath(root=bids_root)
    bids_path.update(subject=subject, datatype=datatype)

    if dataset == "LEMON": # BRAINVISION
        raw = mne.io.read_raw_brainvision(bids_path)
        print(f"Brainvision file at: {bids_path}")
        return bids_path, raw
    
    elif dataset == "CHBP" or dataset == "TUAB_eval" or dataset == "TUAB_train": # EDF
        raw = mne.io.read_raw_edf(bids_path)
        print(f"EDF file at: {bids_path}")
        return bids_path, raw
    
    elif dataset == "CamCAN": # FIF 
        session_id = 'rest'
        task_name = 'rest'
        # Update the BIDSPath instance
        # bids_path = BIDSPath(subject=participant, , root=bids_root)


        # Get the path to the raw MEG file
        raw_file_path = bids_path.copy().update(session=session_id, task=task_name, datatype='meg', suffix='meg', extension='.fif').fpath

        # Load raw MEG data
        raw = mne.io.read_raw_fif(raw_file_path, preload=True)

        # Print information about the loaded raw data
        # print(raw.info)
        print(f"FiF file at: {raw_file_path}")

        return bids_path, raw
            

    # except Exception as e:
    #     # return False
    #     pass
    # try: 
    #     raw = mne.io.read_raw_edf(bids_path)
    #     print(f"EDF file at: {bids_path}")
    # except Exception as e:
    #     return False
    # # else:                           # important for example for CHBP, where some participants do not have an eeg/meg (see participant "sub_CBM00005")
    # #     return None


def plot_time_plot(dataset, subject, datatype="eeg"): 
    
    _, raw = get_raw_data(dataset=dataset, subject=subject, datatype=datatype)
    # if raw != None: 
    raw.plot()
    plt.savefig(f"saved_pictures/time_plot_{dataset}_{subject}.svg", format='svg')
    plt.show()


def plot_freq_plot(dataset, subject, datatype="eeg"): 
    bids_root = BIDS_ROOTS[dataset]
    _, raw = get_raw_data(dataset=dataset, subject=subject, datatype=datatype)
    # if raw != None: 
    raw.compute_psd().plot()
    plt.savefig(f"saved_pictures/freq_plot_{dataset}_{subject}.svg", format='svg')
    plt.show()


def get_durations_of_measurements(dataset, datatype): 
    if dataset == "CamCAN": 
        bids_root = BIDS_ROOTS[dataset]
        bids_path = BIDSPath(root=bids_root)
        # directory_path = "/u/home/dena/Documents/clean_brain_age/raw_data/CamCAN/storage/raw_data/cc700/meg/pipeline/release005/BIDSsep/rest"
        durations = []
        # Iterate through all folders in the specified directory
        for root, dirs, files in os.walk(bids_root):
            # Check if there are JSON files in the current folder
            json_files = [file for file in files if file.endswith(".json") and "meg" in file.lower()]
            
            # If JSON files are found, export them
            if json_files:
                for json_file in json_files:
                    # Read the JSON content
                    json_file_path = os.path.join(root, json_file)
                    with open(json_file_path, 'r') as f:
                        data = json.load(f)
                    # f.close()

                    # Extract the "RecordingDuration" value
                    recording_duration = data.get("RecordingDuration")
                    # print(recording_duration)
                    durations.append(recording_duration)

    if dataset == "CHBP": 
        bids_root = BIDS_ROOTS[dataset]
        bids_path = BIDSPath(root=bids_root)
        # directory_path = "/u/home/dena/Documents/clean_brain_age/raw_data/CamCAN/storage/raw_data/cc700/meg/pipeline/release005/BIDSsep/rest"
        durations = []
        # Iterate through all folders in the specified directory
        for root, dirs, files in os.walk(bids_root):
            # Check if there are JSON files in the current folder
            json_files = [file for file in files if file.endswith(".json") and "eeg" in file.lower()] #eeg instead of meg
            
            # If JSON files are found, export them
            if json_files:
                for json_file in json_files:
                    # Read the JSON content
                    json_file_path = os.path.join(root, json_file)
                    with open(json_file_path, 'r') as f:
                        data = json.load(f)
                    # f.close()

                    # Extract the "RecordingDuration" value
                    recording_duration = data.get("RecordingDuration")
                    # print(recording_duration)
                    durations.append(recording_duration)


    elif dataset == "LEMON" or dataset == "TUAB": 
    # Get durations# dataset: "LEMON", "TUAB", ...
    # datatpye: "eeg", "meg", ...
    # bids_root: Path to the BIDS dataset folder, where the BIDS from all subjects are in
        bids_root = BIDS_ROOTS[dataset]
        bids_path = BIDSPath(root=bids_root)
        subjects = os.listdir(bids_root)

        durations = []
        filtered_subjects = [subject for subject in subjects if 'sub-' in subject]
        subject_ids = []
        subject_ids = [subject.split('-')[1] for subject in filtered_subjects]

        for subject in subject_ids: 
            bids_path, raw = get_raw_data(dataset, subject, datatype)
            # raw = mne.io.read_raw_brainvision(bids_path)
            # duration = raw.__len__()/2500.0 #2500 Hz sampling frequency, according to paper. 

            # if raw != None: 
            print(bids_path)
            duration_seconds = raw.times[-1]
            durations.append(duration_seconds)
    else: 
        print("Dataset is not yet supported.")
    return durations
        

def plot_histogram_durations(dataset, datatype="eeg", constrain_duration=False, duration_span=[500, 750]): 
    if dataset != "TUAB": 
        durations = get_durations_of_measurements(dataset, datatype)
        if constrain_duration: 
            durations = [dur for dur in durations if duration_span[0] <= dur <= duration_span[1]]
        # Plot
        plt.hist(durations, bins=20, color='skyblue', edgecolor='black')
        plt.title(f'Histogram Recording Durations, {dataset}')
        plt.xlabel('Duration (seconds)')
        plt.ylabel('Number measurements')
        # Save and show plot
        plt.savefig(f"saved_pictures/histogram_{dataset}.svg", format='svg')
        plt.show()
    else: 
        print("Wrong function for TUAB. Try plot_histogram_durations_tuab")


def plot_histogram_durations_tuab(csv_location, tuab_only_first_trial=False, duration_shorter_than_x_sec=10800):
    # default: 10800 seconds >> 3 hours. 
    dataset = "TUAB"
    df = pd.read_csv(csv_location)
    # binwidth = 5

    number_invalid_runs = len(df.loc[df["age"] >= 120]) 
    print(f"There are {number_invalid_runs} samples that have an unlikely age (age < 120), and thus were removed.")
    
    df = df.where(df["age"] <= 120)
    df = df.where(df["duration-sec"] <= duration_shorter_than_x_sec) 
    
    if tuab_only_first_trial == True: 
        df = df[df['run_id'].str.contains('_s001_t000.', na=False)]        
        # Non-aesthetic way to include first trial in title
        dataset = "TUAB, only first trial"

    plt.hist(df["duration-sec"], bins=20, color='skyblue', edgecolor='black')
    plt.title(f'Histogram Recording Durations, {dataset}')
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Number measurements')
    # Save and show plot
    plt.savefig(f"saved_pictures/histogram_{dataset}.svg", format='svg')
    plt.show()


# %% 
def plot_demography(dataset, csv_location, tuab_only_first_trial=False):
    if dataset == "LEMON" or dataset == "TUAB": 
        df = pd.read_csv(csv_location)
    elif dataset == "CHBP" or dataset == "CamCAN": 
        df = pd.read_csv(csv_location, sep="\t")
        # print(df)
    else: 
        print("ERROR: Dataset name not known.")

    binwidth = 5

    if dataset == "LEMON":
        # Get mid ages
        df[['Age_min', 'Age_max']] = df['Age'].str.split('-', expand=True).astype(int)
        df['Age_mid'] = df[['Age_min', 'Age_max']].mean(axis=1)

        # Set up the plot
        plt.figure(figsize=(6, 6))
        # plt.xlim(0,100)

        # Create a curvy histogram for females and males 
        sns.histplot(data=df[df['Gender_ 1=female_2=male'] == 2], x='Age_mid', kde=True, label='Male', color='blue', binwidth=binwidth)
        sns.histplot(data=df[df['Gender_ 1=female_2=male'] == 1], x='Age_mid', kde=True, label='Female', color='red', binwidth=binwidth)

        # Calculate mean and std of the 'age' column
        mean_age_male = df[df['Gender_ 1=female_2=male'] == 2]['Age_mid'].mean()
        mean_age_female = df[df['Gender_ 1=female_2=male'] == 1]['Age_mid'].mean()
        std_age_male = df[df['Gender_ 1=female_2=male'] == 2]['Age_mid'].std()
        std_age_female = df[df['Gender_ 1=female_2=male'] == 1]['Age_mid'].std()
        print(f"Mean Age Male: {mean_age_male:.2f}")
        print(f"Standard Deviation of Age Male: {std_age_male:.2f}")
        print(f"Mean Age Female: {mean_age_female:.2f}")
        print(f"Standard Deviation of Age Female: {std_age_female:.2f}")

        number_males = len(df[df['Gender_ 1=female_2=male'] == 2])
        number_females = len( df[df['Gender_ 1=female_2=male'] == 1])
        print(f"Number samples: {number_males+number_females} (male: {number_males}, female: {number_females})")

    
    elif dataset == "CHBP" or dataset == "CamCAN": 
        nan_df = df[df.isna().any(axis=1)]
        print(nan_df)
        df = df.drop([138])
        df = df.drop("hand", axis=1)

        nan_df = df[df.isna().any(axis=1)]
        print(nan_df)
        # df = df.where(df["participant_id"]!="sub-CC222120")
        # df[['age']] = df[['age']].astype(float)

        # Create a curvy histogram for females and males 
        sns.histplot(data=df[df['sex'] == "MALE"], x='age', kde=True, label='Male', color='blue', binwidth=binwidth)
        sns.histplot(data=df[df['sex'] == "FEMALE"], x='age', kde=True, label='Female', color='red', binwidth=binwidth)

        # Calculate mean and std of the 'age' column
        mean_age_male = df[df['sex'] == "M"]["age"].mean()
        mean_age_female = df[df['sex'] == "F"]['age'].mean()
        std_age_male = df[df['sex'] == "M"]["age"].std()
        std_age_female = df[df['sex'] == "F"]['age'].std()
        print(f"Mean Age Male: {mean_age_male:.2f}")
        print(f"Standard Deviation of Age Male: {std_age_male:.2f}")
        print(f"Mean Age Female: {mean_age_female:.2f}")
        print(f"Standard Deviation of Age Female: {std_age_female:.2f}")

        number_males = len(df[df['sex'] == "M"])
        number_females = len(df[df['sex'] == "F"])
        print(f"Number Samples: {number_males+number_females} (males: {number_males}, females {number_females})")


        
    
    elif dataset == "TUAB":
        number_invalid_runs = len(df.loc[df["age"] >= 120]) 
        print(f"There are {number_invalid_runs} samples that have an unlikely age (age < 120), and thus were removed.")
        
        df = df.where(df["age"]<= 120)
        
        if tuab_only_first_trial == True: 
            df = df[df['run_id'].str.contains('_s001_t000.', na=False)]
            # df = df.loc[df['run_id'].str.contains('_s001_t000.')]
            
            # Non-aesthetic way to include first trial in title
            dataset = "TUAB, only first trial"

        sns.histplot(data=df[df['gender'] == "M"], x='age', kde=True, label='Male', color='blue', binwidth=binwidth)
        sns.histplot(data=df[df['gender'] == "F"], x='age', kde=True, label='Female', color='red', binwidth=binwidth)

        mean_age_male = df[df['gender'] == "M"]["age"].mean()
        mean_age_female = df[df['gender'] == "F"]['age'].mean()
        std_age_male = df[df['gender'] == "M"]["age"].std()
        std_age_female = df[df['gender'] == "F"]['age'].std()
        print(f"Mean Age Male: {mean_age_male:.2f}")
        print(f"Standard Deviation of Age Male: {std_age_male:.2f}")
        print(f"Mean Age Female: {mean_age_female:.2f}")
        print(f"Standard Deviation of Age Female: {std_age_female:.2f}")

        number_males = len(df[df['gender'] == "M"])
        number_females = len(df[df['gender'] == "F"])
        print(f"Number samples: {number_males+number_females} (male: {number_males}, female: {number_females})")

    else: 
        print("Dataset-Name is wrong")

    # Set plot labels and title
    plt.xlabel('Age')
    plt.ylabel('Number Measurements')
    plt.title(f'Histogram of Age by Gender, {dataset}')
    plt.legend()

    # Save and show the plot
    plt.savefig(f"saved_pictures/gender_age_{dataset}.svg", format='svg')
    plt.show()



# %%
    
csv_links = {
    "LEMON": "Participants_LEMON.csv",
    "TUAB": "patient_TUAB_id_age.csv", 
    "CHBP": "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/processed_CHBP/participants.csv",
    "CamCAN": "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/CamCAN/storage/raw_data/cc700/meg/pipeline/release005/BIDSsep/rest/participants.tsv"
}

# %% Gives both the histogram AND the mean and std. 

plot_demography("TUAB", csv_links["TUAB"], tuab_only_first_trial = True)
#%%
plot_demography("LEMON", csv_links["LEMON"])

# %% 
plot_demography("CHBP", csv_links["CHBP"])

# %%
plot_demography("CamCAN", csv_links["CamCAN"])

# %% 
# plot_histogram_durations("CamCAN", datatype="meg", constrain_duration=True, duration_span=[500,750])
plot_histogram_durations("CamCAN", datatype="meg", constrain_duration=True, duration_span=[550,570])

# %%
plot_histogram_durations("CHBP", datatype="eeg", constrain_duration=False) #, duration_span=[550,570])

# %% LEMON
# plot_time_plot("LEMON", "010010", "eeg")
dataset = "LEMON"
participant = EXAMPLE_PARTICIPANTS[dataset]
plot_time_plot(dataset, participant, "eeg")
plot_freq_plot(dataset, participant, "eeg")

# %% CHBP
dataset = "CHBP"
participant = EXAMPLE_PARTICIPANTS[dataset]
plot_time_plot(dataset, participant, "eeg")
plot_freq_plot(dataset, participant, "eeg")

# %% TUAB_eval
dataset = "TUAB_eval"
participant = EXAMPLE_PARTICIPANTS[dataset]
plot_time_plot(dataset, participant, "eeg")
plot_freq_plot(dataset, participant, "eeg")

plot_histogram_durations_tuab("patient_TUAB_id_age.csv", tuab_only_first_trial=True, duration_shorter_than_x_sec=60)

# %% CamCAN
dataset = "CamCAN"
participant = EXAMPLE_PARTICIPANTS[dataset]
plot_time_plot(dataset, participant, "meg")
plot_freq_plot(dataset, participant, "meg")


# %% RAW
# bids_path, raw = get_raw_data("LEMON", "010010", "eeg")
dataset = "TUAB_eval"
participant = EXAMPLE_PARTICIPANTS[dataset]
bids_path, raw = get_raw_data(dataset, participant, "eeg")




# %% Check sampling frequency: For CHBP it is always 200 Hz

dataset = "CHBP" 
bids_root = BIDS_ROOTS[dataset]
bids_path = BIDSPath(root=bids_root)
# directory_path = "/u/home/dena/Documents/clean_brain_age/raw_data/CamCAN/storage/raw_data/cc700/meg/pipeline/release005/BIDSsep/rest"
frequencies = []
# Iterate through all folders in the specified directory
for root, dirs, files in os.walk(bids_root):
    # Check if there are JSON files in the current folder
    json_files = [file for file in files if file.endswith(".json") and "eeg" in file.lower()] #eeg instead of meg
    
    # If JSON files are found, export them
    if json_files:
        for json_file in json_files:
            # Read the JSON content
            json_file_path = os.path.join(root, json_file)
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            # f.close()

            # Extract the "RecordingDuration" value
            sampling_freq = data.get("SamplingFrequency")
            # print(recording_duration)
            frequencies.append(sampling_freq)