study_name = "eeg_matchingpennies"
# bids_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/eeg_matchingpennies"
# deriv_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/eeg_matchingpennies/derivative"
# bids_root = "/u/home/dena/Documents/clean_brain_age/brain-age-benchmark/eeg_matchingpennies"
# deriv_root = 
# bids_root = "eeg_matchingpennies"
# deriv_root = "/u/home/dena/Documents/clean_brain_age/brain-age-benchmark/eeg_matchingpennies_derivative"

bids_root = "/u/home/dena/Documents/clean_brain_age/brain-age-benchmark/bullshit"
deriv_root = "/u/home/dena/Documents/clean_brain_age/brain-age-benchmark/eeg_matchingpennies_derivative"

subjects = ["05"]
task = "matchingpennies"
ch_types = ["eeg"]
interactive = False
reject = {"eeg": 150e-6}
conditions = ["raised-left", "raised-right"]
contrasts = [("raised-left", "raised-right")]
decode = True

interpolate_bads_grand_average = False

# cd Documents/clean_brain_age/brain-age-benchmark/
# module load python/anaconda3
# source activate
# conda activate clean
# mne_bids_pipeline --config config_matching_pennies.py --steps=preprocessing


# mne_bids_pipeline --config config_matching_pennies.py --steps=preprocessing