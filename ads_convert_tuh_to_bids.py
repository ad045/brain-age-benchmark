#%%

"""Convert TUH Abnormal Dataset to the BIDS format.

See "The Temple University Hospital EEG Corpus: Electrode Location and Channel
Labels" document on TUH EEG's website for more info on the dataset conventions:
https://www.isip.piconepress.com/publications/reports/2020/tuh_eeg/electrodes/

E.g., to run on drago:
>>> python convert_tuh_to_bids.py \
    --tuab_data_dir /storage/store/data/tuh_eeg/www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/edf \
    --bids_data_dir /storage/store2/data/TUAB-healthy-bids \
    --healthy_only True \
    --reset_session_indices True
"""

import re
import argparse
import datetime

import mne
import numpy as np
from braindecode.datasets import TUHAbnormal
from mne_bids import write_raw_bids, print_dir_tree, make_report, BIDSPath

# %%
import re
ads_names =['EEG FP1-REF', 'EEG FP2-REF', 'EEG F3-REF', 
                'EEG F4-REF', 'EEG C3-REF', 'EEG C4-REF', 
                'EEG P3-REF', 'EEG P4-REF', 'EEG O1-REF', 
                'EEG O2-REF', 'EEG F7-REF', 'EEG F8-REF', 
                'EEG T3-REF', 'EEG T4-REF', 'EEG T5-REF', 
                'EEG T6-REF', 'EEG A1-REF', 'EEG A2-REF', 
                'EEG FZ-REF', 'EEG CZ-REF', 'EEG PZ-REF', 
                'EEG ROC-REF', 'EEG LOC-REF', 'EEG EKG1-REF', 
                'EEG T1-REF', 'EEG T2-REF', 'PHOTIC-REF', 'IBI',
                'BURSTS', 'SUPPR']

# match = re.findall(r'^([A-Z]\w+)-REF$', ads_names)

# matches = [re.findall(r'^([A-Z]\w+)-REF$', ch_name)[0] for ch_name in ads_names if re.match(r'^([A-Z]\w+)-REF$', ch_name)]
# matches = [ch_name for ch_name in ads_names if re.match(r'^([A-Z]\w+)-REF$', ch_name)]
matches = [re.findall(r'^EEG ([A-Z]\w+)-REF$', ch_name) for ch_name in ads_names]

# for ch_name in ads_names: 
#     print()
#%%

import mne

# Define the path to the EDF file
edf_file_path = '/u/home/dena/Documents/clean_brain_age/TUAB_2/edf/eval/abnormal/01_tcp_ar/aaaaabdo_s003_t000.edf'

# Load the EDF file
raw = mne.io.read_raw_edf(edf_file_path, preload=False)

# Print the channel names
print("Channel Names:", raw.ch_names)

#%%
Channel Names: ['EEG FP1-REF', 'EEG FP2-REF', 'EEG F3-REF', 
                'EEG F4-REF', 'EEG C3-REF', 'EEG C4-REF', 
                'EEG P3-REF', 'EEG P4-REF', 'EEG O1-REF', 
                'EEG O2-REF', 'EEG F7-REF', 'EEG F8-REF', 
                'EEG T3-REF', 'EEG T4-REF', 'EEG T5-REF', 
                'EEG T6-REF', 'EEG A1-REF', 'EEG A2-REF', 
                'EEG FZ-REF', 'EEG CZ-REF', 'EEG PZ-REF', 
                'EEG ROC-REF', 'EEG LOC-REF', 'EEG EKG1-REF', 
                'EEG T1-REF', 'EEG T2-REF', 'PHOTIC-REF', 'IBI',
                'BURSTS', 'SUPPR']

Fehlermeldung: ['EEG FP1-REF', 'EEG FP2-REF', 'EEG F3-REF', 
                'EEG F4-REF', 'EEG C3-REF', 'EEG C4-REF', 
                'EEG P3-REF', 'EEG P4-REF', 'EEG O1-REF', 
                'EEG O2-REF', 'EEG F7-REF', 'EEG F8-REF', 
                'EEG T3-REF', 'EEG T4-REF', 'EEG T5-REF', 
                'EEG T6-REF', 'EEG A1-REF', 'EEG A2-REF', 
                'EEG FZ-REF', 'EEG CZ-REF', 'EEG PZ-REF', 
                'EEG ROC-REF', 'EEG LOC-REF', 'EEG EKG1-REF', 
                'EEG T1-REF', 'EEG T2-REF', 'PHOTIC', 'IBI', 
                'BURSTS', 'SUPPR'].

Channel Names in DigMontage: ['Fp1', 'Fpz', 'Fp2', 
                              'AF9', 'AF7', 'AF5', 'AF3', 'AF1', 'AFz',
                               'AF2', 'AF4', 'AF6', 'AF8', 'AF10', 
                               'F9', 'F7', 'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', 'F10', 'FT9', 'FT7', 
                               'FC5', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'FC6', 'FT8', 'FT10', 
                               'T9', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6',
                                'T8', 'T10', 'TP9', 'TP7', 
                                'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6', 
                                'TP8', 'TP10', 'P9', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'P10', 
                                'PO9', 'PO7', 'PO5', 'PO3', 'PO1', 'POz', 'PO2', 'PO4', 'PO6', 'PO8', 'PO10', 
                                'O1', 'Oz', 'O2', 'I1', 'Iz', 'I2', 'AFp9h', 'AFp7h', 'AFp5h', 'AFp3h', 'AFp1h', 'AFp2h', 'AFp4h', 
                                'AFp6h', 'AFp8h', 'AFp10h', 'AFF9h', 'AFF7h', 'AFF5h', 'AFF3h', 'AFF1h', 'AFF2h', 'AFF4h', 'AFF6h', 
                                'AFF8h', 'AFF10h', 'FFT9h', 'FFT7h', 'FFC5h', 'FFC3h', 'FFC1h', 'FFC2h', 'FFC4h', 'FFC6h', 'FFT8h',
                                'FFT10h', 'FTT9h', 'FTT7h', 'FCC5h', 'FCC3h', 'FCC1h', 'FCC2h', 'FCC4h', 'FCC6h', 'FTT8h', 'FTT10h', 
                                'TTP9h', 'TTP7h', 'CCP5h', 'CCP3h', 'CCP1h', 'CCP2h', 'CCP4h', 'CCP6h', 'TTP8h', 'TTP10h', 'TPP9h', 
                                'TPP7h', 'CPP5h', 'CPP3h', 'CPP1h', 'CPP2h', 'CPP4h', 'CPP6h', 'TPP8h', 'TPP10h', 'PPO9h', 'PPO7h', 
                                'PPO5h', 'PPO3h', 'PPO1h', 'PPO2h', 'PPO4h', 'PPO6h', 'PPO8h', 'PPO10h', 'POO9h', 'POO7h', 'POO5h', 
                                'POO3h', 'POO1h', 'POO2h', 'POO4h', 'POO6h', 'POO8h', 'POO10h', 'OI1h', 'OI2h', 'Fp1h', 'Fp2h', 
                                'AF9h', 'AF7h', 'AF5h', 'AF3h', 'AF1h', 'AF2h', 'AF4h', 'AF6h', 'AF8h', 'AF10h', 'F9h', 'F7h',
                                'F5h', 'F3h', 'F1h', 'F2h', 'F4h', 'F6h', 'F8h', 'F10h', 'FT9h', 'FT7h', 'FC5h', 'FC3h', 'FC1h', 
                                'FC2h', 'FC4h', 'FC6h', 'FT8h', 'FT10h', 'T9h', 'T7h', 'C5h', 'C3h', 'C1h', 'C2h', 'C4h', 'C6h', 
                                'T8h', 'T10h', 'TP9h', 'TP7h', 'CP5h', 'CP3h', 'CP1h', 'CP2h', 'CP4h', 'CP6h', 'TP8h', 'TP10h',
                                'P9h', 'P7h', 'P5h', 'P3h', 'P1h', 'P2h', 'P4h', 'P6h', 'P8h', 'P10h', 'PO9h', 'PO7h', 'PO5h', 'PO3h', 
                                'PO1h', 'PO2h', 'PO4h', 'PO6h', 'PO8h', 'PO10h', 'O1h', 'O2h', 'I1h', 'I2h', 'AFp9', 'AFp7', 'AFp5', 'AFp3', 
                                'AFp1', 'AFpz', 'AFp2', 'AFp4', 'AFp6', 'AFp8', 'AFp10', 'AFF9', 'AFF7', 'AFF5', 'AFF3', 'AFF1', 
                                'AFFz', 'AFF2', 'AFF4', 'AFF6', 'AFF8', 'AFF10', 'FFT9', 'FFT7', 'FFC5', 'FFC3', 'FFC1', 'FFCz', 
                                'FFC2', 'FFC4', 'FFC6', 'FFT8', 'FFT10', 'FTT9', 'FTT7', 'FCC5', 'FCC3', 'FCC1', 'FCCz', 'FCC2', 
                                'FCC4', 'FCC6', 'FTT8', 'FTT10', 'TTP9', 'TTP7', 'CCP5', 'CCP3', 'CCP1', 'CCPz', 'CCP2', 'CCP4', 
                                'CCP6', 'TTP8', 'TTP10', 'TPP9', 'TPP7', 'CPP5', 'CPP3', 'CPP1', 'CPPz', 'CPP2', 'CPP4', 'CPP6',
                                'TPP8', 'TPP10', 'PPO9', 'PPO7', 'PPO5', 'PPO3', 'PPO1', 'PPOz', 'PPO2', 'PPO4', 'PPO6', 'PPO8', 
                                'PPO10', 'POO9', 'POO7', 'POO5', 'POO3', 'POO1', 'POOz', 'POO2', 'POO4', 'POO6', 'POO8', 'POO10', 
                                'OI1', 'OIz', 'OI2', 'T3', 'T5', 'T4', 'T6', 'M1', 'M2', 'A1', 'A2']
# %%

import mne
# Load the DigMontage
montage = mne.channels.make_standard_montage('standard_1005')

# Print the channel names
print("Channel Names in DigMontage:", montage.ch_names)

# %% 

mne.channels.get_builtin_montages()
# %%

SEX_TO_MNE = {'n/a': 0, 'm': 1, 'f': 2}


def rename_tuh_channels(ch_name):
    """Rename TUH channels and ignore non-EEG and custom channels.

    Rules:
    - 'Z' should always be lowercase.
    - 'P' following a 'F' should be lowercase.
    """
    exclude = [  # Defined by hand - do we really want to remove them?
        'LOC',
        'ROC',
        'EKG1',
    ]

    Channel Names: ['EEG FP1-REF', 'EEG FP2-REF', 'EEG F3-REF', 
                'EEG F4-REF', 'EEG C3-REF', 'EEG C4-REF', 
                'EEG P3-REF', 'EEG P4-REF', 'EEG O1-REF', 
                'EEG O2-REF', 'EEG F7-REF', 'EEG F8-REF', 
                'EEG T3-REF', 'EEG T4-REF', 'EEG T5-REF', 
                'EEG T6-REF', 'EEG A1-REF', 'EEG A2-REF', 
                'EEG FZ-REF', 'EEG CZ-REF', 'EEG PZ-REF', 
                'EEG ROC-REF', 'EEG LOC-REF', 'EEG EKG1-REF', 
                'EEG T1-REF', 'EEG T2-REF', 'PHOTIC-REF', 'IBI',
                'BURSTS', 'SUPPR']
    

    print(ch_name)
    # match = re.findall(r'^EEG\s([A-Z]\w+)-REF$', ch_name)
    match = re.findall(r'^([A-Z]\w+)-REF$', ch_name)
    if len(match) == 1:
        out = match[0]
        out = out.replace('FP', 'Fp').replace('Z', 'z')  # Apply rules
    else:
        out = ch_name

    if out in exclude:
        out = ch_name

    return out


def _convert_tuh_recording_to_bids(ds, bids_save_dir, desc=None):
    """Convert single TUH recording to BIDS.

    Parameters
    ----------
    ds : braindecode.datasets.BaseDataset
        TUH recording to convert to BIDS.
    bids_save_dir : st
        Directory where to save the BIDS version of the dataset.
    desc : None | pd.Series
        Description of the recording, containing subject and recording
        information. If None, use `ds.description`.
    """
    raw = ds.raw
    raw.pick_types(eeg=True)  # Only keep EEG channels
    if desc is None:
        desc = ds.description

    # Extract reference
    # XXX Not supported yet in mne-bids: see mne-bids/mne_bids/write.py::766
    ref = re.findall(r'\_tcp\_(\w\w)', desc['path'])
    if len(ref) != 1:
        raise ValueError('Expecting one directory level with tcp in it.')
    elif ref[0] == 'ar':  # average reference
        reference = ''
    elif ref[0] == 'le':  # linked ears
        reference = ''
    else:
        raise ValueError(f'Unknown reference found in file name: {ref[0]}.')

    # Rename channels to a format readable by MNE
    raw.rename_channels(rename_tuh_channels)
    # Ignore channels that are not in the 10-5 system
    montage = mne.channels.make_standard_montage('standard_1005')
    ch_names = np.intersect1d(raw.ch_names, montage.ch_names)
    raw.pick_channels(ch_names)
    raw.set_montage(montage)

    # Add pathology and train/eval labels
    # XXX The following will break if it's not TUAB
    # XXX Also, should be written to the `..._scans.tsv` file instead of being
    #     annotations
    # onset = raw.times[0]
    # duration = raw.times[-1] - raw.times[0]
    # raw.annotations.append(
    #     onset, duration, 'abnormal' if desc['pathological'] else 'normal')
    # raw.annotations.append(
    #     onset, duration, 'train' if desc['train'] else 'eval')

    # Make up birthday based on recording date and age to allow mne-bids to
    # compute age
    birthday = datetime.datetime(desc['year'] - desc['age'], desc['month'], 1)
    birthday -= datetime.timedelta(weeks=4)
    sex = desc['gender'].lower()  # This assumes gender=sex

    # Add additional data required by BIDS
    mrn = str(desc['subject']).zfill(8)  # MRN: Medical Record Number
    session_nb = str(desc['session']).zfill(3)
    subject_info = {
        'participant_id': mrn,
        'birthday': (birthday.year, birthday.month, birthday.day),
        'sex': SEX_TO_MNE[sex],
        'handedness': None  # Not available
    }
    raw.info['line_freq'] = 60  # Data was collected in North America
    raw.info['subject_info'] = subject_info
    task = 'rest'

    bids_path = BIDSPath(
        subject=mrn, session=session_nb, task=task, run=desc['segment'],
        root=bids_save_dir, datatype='eeg', check=True)

    write_raw_bids(raw, bids_path, overwrite=True, allow_preload=True,
                   format='BrainVision')


def convert_tuab_to_bids(tuh_data_dir, bids_save_dir, healthy_only=True,
                         reset_session_indices=True, concat_split_files=False, # concat split files cd rawas originally true 
                         n_jobs=1):
    """Convert TUAB dataset to BIDS format.

    Parameters
    ----------
    tuh_data_dir : str
        Directory where the original TUAB dataset is saved, e.g.
        `/tuh_eeg/www.isip.piconepress.com/projects/tuh_eeg/downloads/tuh_eeg_abnormal/v2.0.0/edf`.
    bids_save_dir : str
        Directory where to save the BIDS version of the dataset.
    healthy_only : bool
        If True, only convert recordings with "normal" EEG.
    reset_session_indices : bool
        If True, reset session indices so that each subject has a session 001,
        and that there is no gap between session numbers for a subject.
    concat_split_files : bool
        If True, concatenate recordings that were split into a single file.
        This is based on the "token" field of the original TUH file paths.
    n_jobs : None | int
        Number of jobs for parallelization.
    """
    concat_ds = TUHAbnormal(tuh_data_dir, recording_ids=None, n_jobs=n_jobs, target_name = "age") #included target_name in the hope to overwrite the pathological stuff

    # if healthy_only:
    #     concat_ds = concat_ds.split(by='pathological')['False']
        
    description = concat_ds.description  # Make a copy because `description` is
    # made on-the-fly
    if concat_split_files:
        n_segments_per_session = description.groupby(
            ['subject', 'session'])['segment'].apply(list).apply(len)
        if n_segments_per_session.unique() != np.array([1]):
            raise NotImplementedError(
                'Concatenation of split files is not implemented yet.')
        else:
            description['segment'] = '001'

    if reset_session_indices:
        description['session'] = description.groupby(
            'subject')['session'].transform(lambda x: np.arange(len(x)) + 1)

    for ds, (_, desc) in zip(concat_ds.datasets, description.iterrows()):
        assert ds.description['path'] == desc['path']
        _convert_tuh_recording_to_bids(
            ds, bids_save_dir, desc=desc)


# %%
        
orig_data_dir = "/vol/aimspace/users/home/dena/Documents/clean_brain_age/raw_data/TUAB" #/eval/normal/01_tcp_ar"
bids_data_dir = "/vol/aimspace/users/dena/Documents/clean_brain_age/brain-age-benchmark/processed_TUAB/eval"
healthy_only = True
reset_session_indices = True
n_jobs = 1
concat_split_files = True 

# convert_tuab_to_bids(orig_data_dir, bids_data_dir, healthy_only, reset_session_indices, n_jobs)
# %%

concat_ds = TUHAbnormal(orig_data_dir, recording_ids=None, n_jobs=n_jobs, target_name = "age") #included target_name in the hope to overwrite the pathological stuff

# if healthy_only:
#     concat_ds = concat_ds.split(by='pathological')['False']
    
description = concat_ds.description  # Make a copy because `description` is
# made on-the-fly
if concat_split_files:
    n_segments_per_session = description.groupby(
        ['subject', 'session'])['segment'].apply(list).apply(len)
    if n_segments_per_session.unique() != np.array([1]):
        raise NotImplementedError(
            'Concatenation of split files is not implemented yet.')
    else:
        description['segment'] = '001'

if reset_session_indices:
    description['session'] = description.groupby(
        'subject')['session'].transform(lambda x: np.arange(len(x)) + 1)

for ds, (_, desc) in zip(concat_ds.datasets, description.iterrows()):
    assert ds.description['path'] == desc['path']
    _convert_tuh_recording_to_bids(
        ds, bids_data_dir, desc=desc)
    
# %%
    
print_dir_tree(bids_data_dir)
print(make_report(bids_data_dir))