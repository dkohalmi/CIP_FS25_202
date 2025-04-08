# helper functions for the streamlit app
import pandas as pd
import numpy as np

# Function for preparing the Better Life dataframe:
def prepare_betterlife(df):
    """ Deletes all Inequality columns from a dataframe.
    
        Parameters: 
           df: dataframe (Better Life dataframe)

        Output: 
           dataframe without the Inequality columns if there were such columns in the dataframe ,
           otherwise returns the original dataframe
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
    """ Filter necessary data from Happiness dataframe.
    
        Parameters:
           df: dataframe (expects Happiness dataframe with "Country name", "Ladder score", "Year" columns)

        Output:
           dataframe with 2024 data and "Country name", "Ladder score", "Year" columns if no errors occurred,
           None otherwise  
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
    """ Merges Better Life dataframe with Happiness Index dataframe.
    
        Parameters:
           df1: dataframe (Better Life Index dataframe with "Country" column)
           df2: dataframe (Happiness Index dataframe with "Country name" column)

        Output:
           dataframe: merged dataframe if no error occurs,
           None otherwise   
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




