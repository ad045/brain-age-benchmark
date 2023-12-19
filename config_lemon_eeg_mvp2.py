from pathlib import Path
import mne

study_name = "age-prediction-benchmark"

# On drago
# N_JOBS = 40
# n_jobs = 1 #40       # ad: new version

# bids_root = Path("/storage/store3/data/LEMON_EEG_BIDS")
# /u/home/dena/Documents/clean_brain_age/brain-age-benchmark/raw_LEMON/data/participants.tsv
bids_root = Path("/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/bids_LEMON_one_participant") # ad
# deriv_root = Path("/storage/store3/derivatives/LEMON_EEG_BIDS/")
# deriv_root = Path("/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/processed_LEMON/data") # ad
deriv_root = Path("/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/processed_LEMON/mvp4")

task = "RSEEG"

#maybe change that?  None
subjects = ["010010"]
# subjects_dir = None #Path("/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/processed_LEMON/freesurfer") # ad
              # '/storage/store/data/camcan-mne/freesurfer')


# source_info_path_update = {'processing': 'autoreject',
#                            'suffix': 'epo'}


# process_empty_room is always skipped, since EEG not EMG data 

# task_is_rest = True ad


interactive = False
ch_types = ["eeg"]
reject = {"eeg": 150e-6}

conditions = ["eyes/open", "eyes/closed"]
contrasts = [("eyes/open", "eyes/closed")]
decode = True

interpolate_bads_grand_average = False


''' ausgeklammert von Adrian für Tests. 

inverse_targets = []

noise_cov = 'ad-hoc'

task = "RSEEG"

sessions = []  # keep empty for code flow
# data_type = "eeg" # ad
ch_types = ["eeg"]

analyze_channels = [
  'Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6',
  'T7', 'C3', 'Cz', 'C4', 'T8', 'CP5', 'CP1', 'CP2', 'CP6', 'AFz',
  'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'AF7',
  'AF3', 'AF4', 'AF8', 'F5', 'F1', 'F2', 'F6', 'FT7', 'FC3', 'FC4', 'FT8',
  'C5', 'C1', 'C2', 'C6', 'TP7', 'CP3', 'CPz', 'CP4', 'TP8', 'P5', 'P1', 'P2',
  'P6', 'PO7', 'PO3', 'POz', 'PO4', 'PO8']

eeg_template_montage = mne.channels.make_standard_montage("standard_1005")

l_freq = 0.1
h_freq = 49
raw_resample_sfreq = 200 # ad, 
# resample_sfreq = 200 # previously 

# decim = 5 # LEMON has 1000 Hz; Cuban Human Brain Project 200Hz
# had the hashtag also previously 

eeg_reference = []

eog_channels = ["Fp1"]

find_breaks = False

# n_proj_eog = 1            # ad

reject = None

on_rename_missing_events = "warn"

epochs_tmin = 0
epochs_tmax = 10 - 1 / raw_resample_sfreq # ad
baseline = None

run_source_estimation = True
use_template_mri = "fsaverage_small" #True

conditions = ["eyes/open", "eyes/closed"]

event_repeated = "drop"
l_trans_bandwidth = "auto"
h_trans_bandwidth = "auto"

random_state = 42

shortest_event = 1

log_level = "info"

mne_log_level = "error"
on_error = "continue"
'''


