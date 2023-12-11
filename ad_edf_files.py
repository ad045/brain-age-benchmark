# %% Imports (activate "testing" env and make sure to change to that env in vsc)
from pyedflib import highlevel
import pyedflib as plib
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import pandas as pd


# code for automatically scanning extracting data from edf headers (or search the web)
# 1) get list of all path filenames 
# from typing import List
# path_dir: str = r"C:\Users\sselt\Documents\blog_demo"
# content_dir: List[str] = os.listdir(path_dir)

# %% Parameters 
dataset = "TUAB" # "LEMON", "CHBP", "TUAB", "CamCAN"  

# %% Get path 

path = None

if dataset == "LEMON": 
    path = ""
elif dataset == "CHBP":
    path = "storage/store3/data/CHBMP_EEG_AND_MRI/ds_bids_chbmp/sub-CBM00002/eeg/sub-CBM00002_task-protmap_eeg.edf"
    # path = "storage/store3/data/CHBMP_EEG_AND_MRI/ds_bids_chbmp/sub-CBM00042/eeg/sub-CBM00042_task-protmap_eeg.edf"
elif dataset == "CamCAN": 
    path = ""
elif dataset == "TUAB": 
    path = "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/storage/TUAB/eval/normal/01_tcp_ar/aaaaadjk_s002_t000.edf"
    # path = "../raw_data/storage/TUAB/eval/storage/store5/aaaaapxm_s001_t001.edf"
    # path = "/u/home/dena/Documents/brain-age-benchmark/storage/store/data/tuh_eeg/www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/edf/eval/normal/01_tcp_ar/aaaaaoav_s002_t000.edf"
else: 
    print("The dataset '{dataset}' does not exist.")



signals, signal_headers, header = highlevel.read_edf(path)

# %%
signals, signal_headers, header = highlevel.read_edf(path)

# %% Plot data
n = len(signals)
fig = plt.figure(figsize=(150,50))
ax = plt.axes()
for i in np.arange(n):
    ax.plot(signals[i] , color='purple' )
    plt.show()


# %% Plot gray data! 

n = len(signals)
fig = plt.figure(figsize=(150,50))
ax = plt.axes()
for i in np.arange(n):
    ax.plot(signals[i] , color='gray', alpha=0.2)

plt.plot(signals[5], color="purple")
plt.show()



# %%
sns.set_context("notebook")
# plot zoomed-in data
fig = plt.figure(figsize=(150,50))
ax = plt.axes()
limit = 100
plt.ylim([-limit, limit])
for i in np.arange(n):
    ax.plot(signals[i] , color='purple' )
    plt.show()

# Assuming 'signals' is a DataFrame with n columns
n = 5  # Replace this with the actual number of columns in your DataFrame
signals = pd.DataFrame(np.random.randn(100, n), columns=[f'Signal_{i}' for i in range(n)])

# Set the limit for the y-axis
limit = 100

# Create a figure and axis
fig, axes = plt.subplots(n, 1, figsize=(10, 5 * n), sharex=True, gridspec_kw={'hspace': 0.5})

# Plot zoomed-in data for each column
for i, column in enumerate(signals.columns):
    ax = axes[i]
    sns.lineplot(data=signals[[column]], ax=ax, color='purple')
    ax.set_ylim([-limit, limit])
    ax.set_ylabel(column)

# Display the plot
plt.show()


#%% Show header, with removed sensitive data 
header
#%% Get birthday 
header["birthdate"]

# %% Get technical data from signals
signal_headers