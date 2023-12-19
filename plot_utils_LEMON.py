# %% 

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

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# %%
BIDS_ROOTS = {
    "LEMON": "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/bids_LEMON/data", 
    "CHBP": "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/CHBP", 
    # "CamCAN": 
    # "TUAB": 
}

EXAMPLE_PARTICIPANTS = {
    "LEMON": "010010", 
    "CHBP": "CBM00266",  
    # "CamCAN": 
    # "TUAB": 
}

# dataset = "LEMON"
# bids_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/bids_LEMON/data" #_one_participant" #/data"

# %%

def get_raw_data(dataset, subject, datatype): 
    # datatype: "eeg" or "meg"
    bids_root = BIDS_ROOTS[dataset]
    bids_path = BIDSPath(root=bids_root)
    bids_path.update(subject=subject, datatype=datatype)
    # try: #if bids_path != '':
    if bids_path != '': 
        raw = mne.io.read_raw_brainvision(bids_path)
        print(f"Brainvision file at: {bids_path}")
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
    # dataset: "LEMON", "TUAB", ...
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
    return durations
        

def plot_histogram_durations(dataset, datatype="eeg"): 
    # Plot a histogram of recording durations
    # Get durations
    durations = get_durations_of_measurements(dataset, datatype)
    # Plot
    plt.hist(durations, bins=20, color='skyblue', edgecolor='black')
    plt.title(f'Histogram Recording Durations, {dataset}')
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Number measurements')
    # Save and show plot
    plt.savefig(f"saved_pictures/histogram_{dataset}.svg", format='svg')
    plt.show()


# %% 
def plot_demography(dataset, csv_location):
    dataset = "LEMON"

    df = pd.read_csv(csv_location)
    # Get mid ages
    df[['Age_min', 'Age_max']] = df['Age'].str.split('-', expand=True).astype(int)
    df['Age_mid'] = df[['Age_min', 'Age_max']].mean(axis=1)

    # Set up the plot
    plt.figure(figsize=(6, 6))
    # plt.xlim(0,100)
    binwidth=5

    # Create a curvy histogram for females and males 
    sns.histplot(data=df[df['Gender_ 1=female_2=male'] == 2], x='Age_mid', kde=True, label='Male', color='blue', binwidth=binwidth)
    sns.histplot(data=df[df['Gender_ 1=female_2=male'] == 1], x='Age_mid', kde=True, label='Female', color='red', binwidth=binwidth)

    # Set plot labels and title
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Age by Gender, {dataset}')
    plt.legend()

    # Save and show the plot
    plt.savefig(f"saved_pictures/gender_age_{dataset}.svg", format='svg')
    plt.show()

# %%
plot_demography("LEMON", "Participants_LEMON.csv")


# %%
# plot_time_plot("LEMON", "010010", "eeg")
dataset = "LEMON"
participant = EXAMPLE_PARTICIPANTS[dataset]
plot_time_plot(dataset, participant, "eeg")


# %%
plot_freq_plot("LEMON", "010010", "eeg")


#%%
plot_histogram_durations("LEMON", "eeg") # CHBP



# %%

bids_path, raw = get_raw_data("LEMON", "010010", "eeg")


