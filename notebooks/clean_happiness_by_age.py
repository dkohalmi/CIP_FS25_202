"""
Data Transformation / Cleansing: Happiness by Age
scraped data from https://worldhappiness.report/ed/2024/happiness-of-the-younger-the-older-and-those-in-between/
raw csv: ./data/raw/happiness_by_age_raw.csv
clean csv: ./data/clean/happiness_by_age_2021_2023_clean.csv

author: Ramona Kölliker
date: 02.04.2025
"""
##
import pandas as pd

## Missing Data Check
# read raw data, making sure pandas treats different "N/A" as missing values
df_raw_happiness_by_age = pd.read_csv("./data/raw/happiness_by_age_raw.csv", na_values= ["N/A", "-", "nan", "NaN"])

# inspect raw data
df_raw_happiness_by_age
# check column names:
df_raw_happiness_by_age.columns

# information about missing values and data type of the columns
df_raw_happiness_by_age.info() # 5 int and 3 objects, no missing values

# checking the 3 object columns
# check column "Country"
print(df_raw_happiness_by_age["Country"].unique())
print("Number of unique values in this column: ", df_raw_happiness_by_age["Country"].nunique())
print("Length of data frame: ", len(df_raw_happiness_by_age))

# check column "Happiest"
print(df_raw_happiness_by_age["Happiest"].unique())
print("Number of unique values in this column: ", df_raw_happiness_by_age["Happiest"].nunique())

# check column "Least Happy"
print(df_raw_happiness_by_age["Least Happy"].unique())
print("Number of unique values in this column: ", df_raw_happiness_by_age["Least Happy"].nunique())

# conclusion: no missing values, column types are correct, no cleaning needed for the categorical labels

## Cleaning
# no further cleaning needed
# deep copy of the original dataframe to preserve the raw data
df_by_age_clean = df_raw_happiness_by_age.copy()

## Checking expected ranges of values
# select numerical columns and get a summary statistics
cols_to_evaluate = [col for col in df_by_age_clean.columns if col not in ["Country", "Happiest", "Least Happy"]]

# loop through the columns and print the statistics
for col in cols_to_evaluate:
    print("Description of column: ", col)
    print(df_by_age_clean[col].describe())

# conclusion: everything seems plausible

## Save dataframe to csv
df_by_age_clean.to_csv("./data/clean/happiness_by_age_2021_2023_clean.csv", index = False)