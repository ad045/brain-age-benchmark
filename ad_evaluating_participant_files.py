# %%

import pandas as pd
import numpy as np

# %%
dataset = "CamCAN" #"LEMON" # "CHBP", ...

if dataset == "CHBP": 
    df = pd.read_csv("processed_CHBP/participants.csv", sep="\t")
elif dataset == "LEMON": 
    df = pd.read_csv("processed_LEMON/data/participants.csv", sep="\t")
    # /u/home/dena/Documents/clean_brain_age/brain-age-benchmark/processed_LEMON/data/participants.csv
elif dataset == "TUAB": 
    df = pd.read_csv("processed_TUAB/participants.csv", sep="\t") # !!
elif dataset == "CamCAN":  # curr wrong! They are too many...
    df = pd.read_csv("../raw_data/CamCAN/storage/raw_data/cc700/mri/pipeline/release004/BIDS_20190411/fmap_rest/participants.tsv", sep="\t") # !!

# %%
# Count the number of male and female participants
sex = "sex"
if dataset == "CamCAN": 
    sex = "gender_text" # obv not correct physically, but seems to be the idea in the dataset. 
gender_counts = df[sex].value_counts()

# Calculate the range of ages
age_range = df['age'].min(), df['age'].max()

# Calculate the mean age
mean_age = df['age'].mean()

# Calculate the mean age for male and female participants
female = "F"
male = "M"
if dataset == "CamCAN": 
    female = "FEMALE"
    male = "MALE"
mean_male_age = df[df[sex] == male]['age'].mean()
mean_female_age = df[df[sex] == female]['age'].mean()

# Calculate the standard deviation of the age
std_age = df['age'].std()

# Display the results
print("Number of Male Participants:", gender_counts[male])
print("Number of Female Participants:", gender_counts[female])
print("Age Range:", age_range)
print("Mean Age:", mean_age)
print("Mean Male Age:", mean_male_age)
print("Mean Female Age:", mean_female_age)
print("Standard Deviation of Age:", std_age)
# %%
