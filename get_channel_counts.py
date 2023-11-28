# %%
from pathlib import Path
import pandas as pd
import mne
from config_chbp_eeg import bids_root, deriv_root

subjects_list = list(Path("../raw_data/storage").glob('*'))#.glob('*')) #bids_root.glob('*'))

subjects_df = pd.read_csv("processed_CHBM/participants.csv", sep='\t') #bids_root / "participants.tsv", sep='\t')

# %%
subjects = [sub for sub in subjects_df.participant_id if
            (Path("../raw_data/storage") / sub / 'eeg').exists()]

eeg_template_montage = mne.channels.make_standard_montage(
    'standard_1005'
)
eeg_template_montage.rename_channels(
    {'FFT7h': 'FFC7h', 'FFT8h': 'FFC8h'})

channels = list()
for sub in subjects:
    fname = deriv_root / sub / 'eeg' / f'{sub}_task-protmap_epo.fif'
    count = None
    if fname.exists():
        info = mne.io.read_info(fname)
        count = len(info['ch_names'])
    channels.append(count)

ch_counts = pd.DataFrame({"count": channels, "subject": subjects})
ch_counts.to_csv('outputs/channel_counts.csv')                  # ad: removed "./" in beginning
