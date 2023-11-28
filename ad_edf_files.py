# %% Imports (activate "testing" env and make sure to change to that env in vsc)
from pyedflib import highlevel
import pyedflib as plib
import numpy as np
import matplotlib.pyplot as plt


# %% Get data 
path = "storage/store3/data/CHBMP_EEG_AND_MRI/ds_bids_chbmp/sub-CBM00002/eeg/sub-CBM00002_task-protmap_eeg.edf"
signals, signal_headers, header = highlevel.read_edf(path)

# %%
# path = "storage/store3/data/CHBMP_EEG_AND_MRI/ds_bids_chbmp/sub-CBM00042/eeg/sub-CBM00042_task-protmap_eeg.edf"
# path = "/u/home/dena/Documents/brain-age-benchmark/storage/store/data/tuh_eeg/www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/edf/eval/normal/01_tcp_ar/aaaaaoav_s002_t000.edf"
path = "../raw_data/storage/TUAB/eval/storage/store5/aaaaapxm_s001_t001.edf"
signals, signal_headers, header = highlevel.read_edf(path)

# %% Plot data
n = len(signals)
fig = plt.figure(figsize=(150,50))
ax = plt.axes()
for i in np.arange(n):
    ax.plot(signals[i] , color='purple' )
    plt.show()

#%% Show header, with removed sensitive data 
header
#%% Get birthday 
header["birthdate"]

# %% Get technical data from signals
signal_headers