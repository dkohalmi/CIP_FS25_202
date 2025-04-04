"""
authors:    Jade Bullock
date:       21.03.2025


"""
import pandas as pd
from scrape_gallup_safety import get_gallup_dataframes

def clean_gallup_safety():
    """
    Cleans and validates Gallup Safety and Law & Order index data.

    This function:
    - Retrieves raw Safety and Law & Order dataframes from the scraper module
    - Standardizes country names and merges the datasets
    - Checks for mismatched countries before merging
    - Detects and reports missing data
    - Ensures appropriate column data types and converts them as needed
    - Identifies and handles outliers in numeric columns (e.g., percentage and values outside 0–100)
    - Sorts and resets the index for consistency
    - Saves the final cleaned and validated dataset as 'Gallup_Cleaned.csv'

    Intended for preparing the dataset for further analysis or visualization.
    """
    # Get the dataframes from scrape_gallup_safety for cleaning
    df_safety, df_law_order = get_gallup_dataframes()

    # Rename column to enable a consistent merge
    df_safety.rename(columns={"DW_NAME": "Country"}, inplace=True)
    df_law_order.rename(columns={"DW_NAME": "Country"}, inplace=True)

    # Country name fixes - normalise cases.  Strips whitespace
    df_safety["Country"] = df_safety["Country"].str.strip().str.title()
    df_law_order["Country"] = df_law_order["Country"].str.strip().str.title()

    # Check mismatches before merge
    safety_countries = set(df_safety["Country"])
    law_order_countries = set(df_law_order["Country"])

    print("In Safety but not in Law & Order:", safety_countries - law_order_countries)
    print("In Law & Order but not in Safety:", law_order_countries - safety_countries)

    # Make sure value columns are numeric before merge - remove % for safety values and rename
    df_safety["VALUE"] = pd.to_numeric(df_safety["VALUE"].str.replace("%", "").str.strip(), errors="coerce")
    df_safety.rename(columns={"VALUE": "PERCENTAGE_Safety"}, inplace=True)
    df_law_order["VALUE"] = pd.to_numeric(df_law_order["VALUE"], errors="coerce")
    df_law_order.rename(columns={"VALUE": "SCORE_law_order"}, inplace=True)

    #Check column names
    print(df_safety.head())
    print(df_law_order.head())

    # Merge dataframes
    merged_df = pd.merge(df_safety, df_law_order)
    print("\n Dataset merged. Shape:", merged_df.shape)

    # Check for gaps/missing data
    print("\n Missing values:")
    print(merged_df.isnull().sum())

    # Check datatypes of the columns and change if needed
    print("\n Column datatypes:")
    print(merged_df.dtypes)


    # Check value ranges & detect outliers
    print("\n Value ranges:")
    print(merged_df.describe())

    # Flags values outside expected 0–100 range
    for col in merged_df.columns:
        if col != "Country":
            outliers = merged_df[(merged_df[col] < 0) | (merged_df[col] > 100)]
            if not outliers.empty:
                print(f"\n️  Outliers detected in '{col}':")
                print(outliers[["Country", col]])

                #Sets any values outside of upper and lower parameters to upper and lower parameters
                merged_df[col] = merged_df[col].clip(lower=0, upper=100)

    #Sort and reset index
    merged_df.sort_values("Country", inplace=True)
    merged_df.reset_index(drop=True, inplace=True)

    # Save cleaned output
    merged_df.to_csv("data/clean/Gallup_safety_clean.csv", index=False)
    print("Cleaned & merged CSV saved: Gallup_safety_clean.csv")

if __name__ == "__main__":
    clean_gallup_safety()
