"""
This script cleans and validates Gallup Emotions data.

This function:
    - Retrieves raw emotion data using the scrape_gallup_emotions() function
    - Standardizes country and emotion names
    - Drops the 'Don't Know/Refused' column before reshaping
    - Cleans and converts percentage strings to numeric values
    - Checks for missing data values
    - Identifies and handles outliers in numeric columns (e.g., percentage and values outside 0–100)
    - Creates composite column names
    - Ensures appropriate column data types and converts them as needed
    - Sorts and resets the index for consistency
    - Saves the final cleaned and validated dataset as 'Gallup_Cleaned.csv'

Intended for preparing the dataset for further analysis or visualization.

authors:    Jade Bullock
date:       04.04.2025


"""

import pandas as pd
import os
from scrape_gallup_emotions import scrape_gallup_emotions

def clean_gallup_emotions():
    # Get the dataframes from scrape_gallup_emotions for cleaning
    df = scrape_gallup_emotions()
    print("Raw data preview:\n", df.head())

    # Normalize column names and strip whitespace
    df.columns = df.columns.str.strip()
    df["Country"] = df["Country"].str.strip().str.title()
    df["Emotion"] = df["Emotion"].str.strip().str.title()

    # Drop 'Don't Know/Refused' before reshaping
    if "DON'T KNOW/REFUSED" in df.columns:
        df = df.drop(columns=["DON'T KNOW/REFUSED"])

    # Reshape the dataframe (only YES and NO remain)
    reshaped = df.melt(
    id_vars=["Emotion", "Country"],
    value_vars=["YES", "NO"],
    var_name="Response",
    value_name="Percentage"
    )
    print("Reshaped data preview:\n", reshaped.head())

    #Clean and convert 'Percentage' to numeric (remove % and invalid entries)
    reshaped["Percentage"] = reshaped["Percentage"].str.replace("%", "", regex=False).str.strip()
    reshaped["Percentage"] = pd.to_numeric(reshaped["Percentage"], errors="coerce")

    #Check for missing values
    missing = reshaped.isnull().sum()
    if missing.any():
        print("Missing values found:\n", missing)

    #Check and handle outliers (outside 0–100 range)
    outlier_mask = (reshaped["Percentage"] < 0) | (reshaped["Percentage"] > 100)
    if outlier_mask.any():
        print("Outliers detected:")
        print(reshaped[outlier_mask])
        # You could drop or cap them here, e.g.:
        reshaped.loc[outlier_mask, "Percentage"] = pd.NA


    # Create composite column names like 'anger_yes'
    reshaped["Column"] = (
        reshaped["Emotion"].str.lower().str.replace(" ", "_") + "_" +
        reshaped["Response"].str.lower().str.replace(" ", "_") + "%"
    )

    # Pivot so that each row is Country with all emotion responses as columns (country only once in the row)
    final_df = reshaped.pivot_table(
        index="Country",
        columns="Column",
        values="Percentage",
        aggfunc="first"
    ).reset_index()
    print("Data preview:\n", final_df.head())

    # Ensure numeric types for all response columns
    for col in final_df.columns:
        if col != "Country":
            final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

    # Print column data types to verify
    print("\nColumn data types after conversion:")
    print(final_df.dtypes)

    # Reorder columns
    cols = final_df.columns.tolist()
    reordered = ["Country"] + sorted([col for col in cols if col != "Country"])
    final_df = final_df[reordered]

    # Sort and reset index
    final_df = final_df.sort_values(["Country"]).reset_index(drop=True)

    # Save cleaned data to CSV
    os.makedirs("../data/clean", exist_ok=True)
    final_df.to_csv("../data/clean/gallup_emotions_clean.csv", index=False)
    print("Cleaned data saved to ../data/clean/gallup_emotions_clean.csv")

    return final_df

if __name__ == "__main__":
    clean_gallup_emotions()