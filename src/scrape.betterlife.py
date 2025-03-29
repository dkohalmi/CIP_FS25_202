#############################################
# Better Life Index Cleaning Script
# Author: Dora Kohalmi
#############################################
#
# This Python script cleans the data that was scraped from the "Country" section of the Better Life Index 
# webpage by the scrape.betterlife.ipynb Jupyter Notebook or scrape.betterlife.py script.
# This file is the script version of the clean.betterlife.ipynb Notebook.
#
# The scraped data (raw data) was saved into the "/data/raw folder as betterlife_index.raw.csv". 
# In this script we read this csv file containing the raw data,
# clean all the columns and write the cleaned dataframe into the "/data/clean/betterlife.clean.csv" file.
###############################################################################################################

import pandas as pd
import numpy as np
import re

# Function to remove all not numeric characters from a string:
def clean_mixed_column2(column):
    """
    Cleans a DataFrame column by removing not numeric characters such as '%','~' symbols and letters,
    and after that converting the value to float.
    
    Parameters:
    column (Pandas.Series): The column of a data frame to clean.
    
    Returns:
    Pandas.Series: The cleaned column as a Pandas.Series
    """
    return column.astype(str).apply(lambda x: float(re.sub(r'[^0-9.]', '', x)))


def main():
    """
    Cleans the raw Better Life Index csv file and write it into a csv file.

    There are columns that should be numeric but the scraped data contains characters 
    (%, 'years', 'USD'), too. The script removes these unnecessary characters and write the clean data frame
    into /data/clean/betterlife.clean.csv .

    Parameters:
        None

    Output: 
       /data/clean/betterlife.clean.csv: the cleaned Better Life Index data       
    """
    # Set path to raw data file:
    path_to_betterlife_raw="/data/raw/betterlife_index.raw.csv"

    # Read raw data:
    df_raw = pd.read_csv(path_to_betterlife_raw)
   
    # Select all "object" columns of the dataframe:
    object_columns = df_raw.select_dtypes(include=['object'])

    # We want to clean all "object" columns of the dataframe except for "Country":
    # Select "object" (string) columns except for "Country" column:
    filtered_columns = [col for col in object_columns if col != 'Country']

    # Creating a deep copy of the original dataframe and clean it:
    df_clean = df_raw.copy()
    for col in filtered_columns:
        df_clean[col] = clean_mixed_column2(df_raw[col])

    # Save cleaned data frame into the /data/clean folder as betterlife.clean.csv :
    df_clean.to_csv("../data/clean/betterlife.clean.csv", index=False)    

if __name__ == '__main__':
    main()
    