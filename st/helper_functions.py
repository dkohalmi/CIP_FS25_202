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
- load_all_data: Load and cache all necessary files
- prepare_betterlife: Clean the OECD Better Life Index dataset
- prepare_happiness: Clean the World Happiness Index dataset
- merge_betterlife: Merge the two datasets on country names
- prepare_all_data: Clean Better Life and Happiness datasets and merge them 
- create_var_dict: Create a dictionary to map display names to column names

Author: Dora Kohalmi
Created: 2025-04-08
"""

import pandas as pd
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


# Function to load and cache all data for the Application:
def load_all_data():
    """
    Load and cache all required datasets into Streamlit session state.
    
    Loads:
    - OECD Better Life Index data (CSV)
    - World Happiness Index data (XLSX)
    
    Stores them in st.session_state to make them accessible across pages.
    """
    PATH_BETTERLIFE = "data/clean/betterlife.clean.csv"
    PATH_HAPPINESSINDEX = "data/clean/happinessindex.xlsx"

    if "df_betterlife_raw" not in st.session_state:
        st.session_state.df_betterlife_raw = load_csv_data(PATH_BETTERLIFE)

    if "df_happiness_raw" not in st.session_state:
        st.session_state.df_happiness_raw = load_xlsx_data(PATH_HAPPINESSINDEX)


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


def prepare_all_data():
    """
    Prepare and cache all datasets in Streamlit session state:
    - Prepare and store the Better Life dataset.
    - Prepare and store the Happiness dataset.
    - Merge the Better Life and Happiness datasets.

    This function ensures that the data is only processed once and stored for later use.
    """
    
    # Prepare df_betterlife only if it hasn't been processed yet:
    if "df_betterlife" not in st.session_state:
        processed_df = prepare_betterlife(st.session_state.df_betterlife_raw)

        # Ensure the function didn't fail before saving it:
        if processed_df is not None:
            st.session_state.df_betterlife = processed_df
        else:
            st.error("Failed to prepare Better Life dataframe.")    

    # Prepare df_happiness dataframe if it hasn't been processed yet:
    if "df_happiness" not in st.session_state:
        processed_df = prepare_happiness(st.session_state.df_happiness_raw)

        # Ensure the function didn't fail before saving it:
        if processed_df is not None:
            st.session_state.df_happiness = processed_df
        else:
            st.error("Failed to prepare Happiness dataframe.")    

    # Merge df_betterlife with df_happiness if not already merged:
    if "df_betterlife_merged" not in st.session_state:
        processed_df = merge_betterlife(st.session_state.df_betterlife, 
                                        st.session_state.df_happiness)

        # Ensure the function didn't fail before saving it:
        if processed_df is not None:
            st.session_state.df_betterlife_merged = processed_df
        else:
            st.error("Failed to merge Better Life and Happiness dataframe.")


def create_var_dict():
    """
    Create a dictionary mapping display names to column names for Better Life metrics.
    Stores the dictionary in session state for use across multiple pages.
    """
    betterlife_var_dict = {
        "Population": "Population",
        "Visitors": "Visitors",
        "Renewable Energy": "Renewable_Energy",
        "Housing": "Housing",
        "Income": "Income",
        "Jobs": "Jobs",
        "Community": "Community",
        "Education": "Education",
        "Environment": "Environment",
        "Civic Engagement": "Civic_Engagement",
        "Health": "Health",
        "Life Satisfaction": "Life_Satisfaction",
        "Safety": "Safety",
        "Work-Life Balance": "Work_Life_Balance",
        "Happiness Index": "Happiness_Index"
    }

    # Store the dictionary in session state if not already stored
    if "betterlife_var_dict" not in st.session_state:
        st.session_state.betterlife_var_dict = betterlife_var_dict



