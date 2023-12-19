study_name = "eeg_matchingpennies"
bids_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/eeg_matchingpennies"
deriv_root = "/vol/aimspace/users/dena/Documents/clean_brain_age/eeg_matchingpennies/derivative"

subjects = ["05"]
task = "matchingpennies"
ch_types = ["eeg"]
interactive = False
reject = {"eeg": 150e-6}
conditions = ["raised-left", "raised-right"]
contrasts = [("raised-left", "raised-right")]
decode = True

interpolate_bads_grand_average = False