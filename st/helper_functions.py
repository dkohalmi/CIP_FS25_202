####################################################################
# Helper functions for the Happiness around the World Streamlit App
#
# Author: Dora Kohalmi
# Date: 08.04.2025
#
# This modules contains helper functions for the Streamlit App.
####################################################################
"""
helper_functions.py

This module contains utility functions for loading, preparing, and merging data
used in the World Happiness Streamlit application.

Functions:
----------
- load_csv_data: Load and cache CSV files
- load_xlsx_data: Load and cache Excel files
- prepare_betterlife: Clean the OECD Better Life Index dataset
- prepare_happiness: Clean the World Happiness Index dataset
- merge_betterlife: Merge the two datasets on country names

Author: Dora Kohalmi
Created: 2025-04-08
"""

import pandas as pd
import numpy as np
import streamlit as st


# Function to load and cache data from a csv file:
@st.cache_data
def load_csv_data(path):
    """
    Load and cache a CSV file into a pandas DataFrame.

    Parameters:
       path (str): Path to the CSV file.

    Returns:
       pd.DataFrame: DataFrame containing the loaded data.
    """
    return pd.read_csv(path)


# Function to load and cache data from a xlsx file:
@st.cache_data
def load_xlsx_data(path):
    """
    Load and cache an Excel (.xlsx) file into a pandas DataFrame.

    Parameters:
       path (str): Path to the Excel file.

    Returns:
       pd.DataFrame: DataFrame containing the loaded data.
    """
    return pd.read_excel(path)


# Function for preparing the Better Life dataframe:
def prepare_betterlife(df):
    """
    Clean and transform the raw Better Life Index dataset.
    
        Parameters: 
           df (pandas DataFrame): Raw Better Life data)

        Output: 
           pandas DataFrame: clean and transformed Better Life data (Inequality columns removed)
    """
    # Make a copy of the original dataframe:
    df_new=df.copy()
    try:
        # Choose column names that contain "Inequality":
        inequality_columnnames= [col for col in df_new.columns if "Inequality" in col]
        
        # Drop all Inequality columns:
        df_new.drop(columns=inequality_columnnames, inplace=True)
        return df_new
   
    except KeyError as e:
        print(f"Error: Some columns could not be found - {e}")
    except Exception as e:
        print(f"Unexpected error while preparing the Better Life dataframe: {e}")

    # Return original dataframe unchanged in case of an error
    return df_new    


# Function for preparing the Happiness dataframe:
def prepare_happiness(df):
    """ 
    Clean and filter the World Happiness Index dataframe.
    
        Parameters:
           df (pandas DataFrame): Happiness Index dataframe with "Country name", "Ladder score", "Year" , etc. columns

        Output:
           pandas DataFrame: contains only data for 2024,  only the columns "Country name", "Ladder score", "Year" columns
    """

    try:
        # Required columns:
        columns_to_keep = ["Country name", "Ladder score", "Year"]

        # Check if all required columns exist:
        missing_cols = [col for col in columns_to_keep if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Missing columns in DataFrame: {missing_cols}")

        # Filter for the year 2024 and create a deep copy to avoid potential issues:
        df_filtered = df[df["Year"] == 2024][["Country name", "Ladder score"]].copy()

        # Rename column:
        df_filtered.rename(columns={"Ladder score": "Happiness_Index"}, inplace=True)

        # Return cleaned dataframe:
        return df_filtered 
    
    except KeyError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error while preparing the Happiness dataframe: {e}")
    
    # Return None if an error occurs:
    return None  
        

def merge_betterlife(df1, df2):
    """ 
    Merges Better Life dataframe with Happiness Index dataframe on country name.
    
    Parameters:
        df1 (pandas DataFrame): Better Life Index dataframe with "Country" column
        df2 (pandas DataFrame): Happiness Index dataframe with "Country name" column

    Returns::
        pandas DataFrame: merged dataframe  
    """
    try:

        # Define Country name replacement dictionary:
        country_replacements = {
                                "Slovak Republic": "Slovakia",
                                "Republic of Korea": "Korea"
                                }

        # Make copies of the original dataframes:
        df1_new = df1.copy()
        df2_new = df2.copy()

        # Replace "Slovak Republic" with "Slovakia":
        df1_new["Country"].replace(country_replacements, inplace=True)

        # Replace "Republic of Korea" with "Korea":
        df2_new["Country name"].replace(country_replacements, inplace=True)

        # Left-merge Better Life Index dataframe and Happiness Index dataframe:
        df_merged = df1_new.merge(df2_new, left_on='Country', right_on='Country name',
               suffixes=('_left', '_right'))
    
        # Remove "Country name" column:
        df_merged.drop( columns=["Country name"], inplace=True)

        return df_merged
    
    except KeyError as e:
        print(f"Error: Missing column in dataframe - {e}")

    except Exception as e:
        print(f"Unexpected error while merging data: {e}")
    
    # Return None if an error occurs
    return None  
