# %% Change the Participants_LEMON file to include true ID. 
from tkinter import BOTTOM
import numpy as np
import pandas as pd

# update the participants file as LEMON has no official age data
participants = pd.read_csv(
    "Participants_LEMON.csv", sep=',')

matching_df = pd.read_csv("name_match_LEMON.csv")    

for (initial_ID, INDI_ID) in zip(matching_df.Initial_ID, matching_df.INDI_ID): # ad
    participants.loc[participants["Unnamed: 0"] == INDI_ID,"ID"] =   initial_ID    # ad

participants.to_csv("Participants_LEMON.csv")