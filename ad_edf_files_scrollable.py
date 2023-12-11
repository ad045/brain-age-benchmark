# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from pyedflib import highlevel
import pyedflib as plib
import os
import seaborn as sns
import pandas as pd

# plt.subplots_adjust(bottom=0.25)

# %% Parameters and path
fig, ax = plt.subplots()

dataset = "TUAB" # "LEMON", "CHBP", "TUAB", "CamCAN"  
path = None
id = None

if dataset == "LEMON": 
    id = ""
    path = ""
elif dataset == "CHBP":
    id = ""
    path = "storage/store3/data/CHBMP_EEG_AND_MRI/ds_bids_chbmp/sub-CBM00002/eeg/sub-CBM00002_task-protmap_eeg.edf"
elif dataset == "CamCAN": 
    id = ""
    path = ""
elif dataset == "TUAB": 
    id = "aaaaadjk_s002_t000"
    path = "/vol/aimspace/users/dena/Documents/clean_brain_age/raw_data/storage/TUAB/eval/normal/01_tcp_ar/"+id+".edf"
else: 
    print("The dataset '{dataset}' does not exist.")

signals, signal_headers, header = highlevel.read_edf(path)


n = len(signals)
fig = plt.figure(figsize=(150,50))
ax = plt.axes()
for i in np.arange(n):
    ax.plot(signals[i] , color='gray', alpha=0.2)

l = plt.plot(signals[5], color="purple")

# Choose the Slider color
slider_color = 'White'

# Set the axis and slider position in the plot
axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
						facecolor = slider_color)
slider_position = Slider(axis_position,
						'Pos', 0.1, 90.0)

# update() function to change the graph when the
# slider is in use
def update(val):
	pos = slider_position.val
	ax.axis([pos, pos+10, -1, 1])
	fig.canvas.draw_idle()

# update function called using on_changed() function
slider_position.on_changed(update)

# Display the plot
plt.show()
plt.savefig("visualized_unprocessed_data/fig_{dataset}_{id}.svg")
