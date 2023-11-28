import os
import pathlib
import config_chbp_eeg as cfg
import pandas as pd

"""Fixing the participants.tsv in the derivatives folder

The current release of the CHBP has a faulty participants.tsv
that doesn't include age. This script carries over the info
from the demographics directory shipped by the CHBP and writes a
new 'particpants.tsv' to the root path.
"""

demographics_root = pathlib.Path(
    '../raw_data/storage/store5/CHBMP_Cognitive_Scales')

subjects_df = pd.read_csv(
    demographics_root / 'Demographic_data.csv', skiprows=1)

subjects_df = subjects_df.iloc[:, :3]
subjects_df.columns = ['participant_id', 'sex', 'age']
subjects_df['participant_id'] = 'sub-' + subjects_df.participant_id
subjects_df.to_csv(
    # cfg.bids_root / 'participants.tsv', sep='\t',
    # index=False)
    "processed_CHBM/participants.csv", sep='\t', index=False)


# raw_data/storage/participants.tsv (participants file for CHBP)