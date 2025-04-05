"""
Cleans and validates 7 ILOSTAT raw datasets and saves a cleaned CSV for each topic.

Due to a website change (02/04/2025), data is sourced from raw CSV files
instead of scraped DataFrames.

This script defines reusable cleaning and validation functions to:
- Load raw ILOSTAT CSVs (7 total, across different labor topics)
- Standardize country names (remove year/region info)
- Clean and convert numeric columns (remove %, $, commas → float)
- Rename key indicator columns for clarity and consistency
- Check for missing values, data types, and statistical outliers
- Validate values against expected ranges
- Save a cleaned CSV for each dataset to ../data/clean/

Authors: Jade Bullock
Date: 04.04.2025
"""

import pandas as pd
import os

#def check_data_type(df):
    #'"""Checks the data type of the columns in the dataframe. """
    #print("\nColumn data types:")
    #print(df.dtypes)
    #return df

def clean_numeric_columns(df: pd.DataFrame, skip_first: bool = True) -> pd.DataFrame:
    """Removes thousands comma, dollar sign and percentage sign from numeric columns."""
    start_idx = 1 if skip_first else 0

    for col in df.columns[start_idx:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def rename_column(df: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """Renames 1st column to country and provides means to rename other columns"""
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "Country"})
    if old_name in df.columns:
        df = df.rename(columns={old_name: new_name})
    return df

def clean_country_names(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans country names to remove additional text"""
    df.iloc[:, 0] = df.iloc[:, 0].str.replace(r"\s*\(.*", "", regex=True).str.strip()
    return df


def validate_column(df: pd.DataFrame, column: str, expected_range=(0, 100)) -> None:
    """ Checks for the following: missing values, data type, values outside expected range, and outliers"""

    print(f"\n--- Validation for '{column}' ---")

    if column not in df.columns:
        print(f"Column '{column}' not found.")
        return

    # 1. Missing values
    missing_mask = df[column].isnull()
    missing_count = missing_mask.sum()
    print(f"Missing values: {missing_count}")
    if missing_count > 0:
        print("Countries with missing values:")
        print(df.loc[missing_mask, "Country"].tolist())

    # 2. Data type
    print(f"Data type: {df[column].dtype}")

    # 3. Values outside expected range
    min_val, max_val = expected_range
    out_of_range = df[(df[column] < min_val) | (df[column] > max_val)]
    if not out_of_range.empty:
        print(f"\nValues outside range {expected_range}:")
        print(out_of_range)

    # 4. Outliers using IQR method
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    if not outliers.empty:
        print(f"\nStatistical outliers (IQR method):")
        print(outliers)

    print("--- End of Validation ---")

def clean_unemployment_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans unemployment raw dataset by:
    - Removing (year) from country names
    - Converting percentage strings to numeric values
    - Dropping the 3rd, 4th, and 5th columns
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning unemployment data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = df.drop(df.columns[[2, 3, 4]], axis=1)
    df = rename_column(df, "Unemployment rate (LU1)", "Unemployment rate (%)")
    validate_column(df, "Unemployment rate (%)")
    return df

def clean_labour_productivity_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans labour productivity dataset by:
    - Renaming the productivity column to 'GDP per hour worked'
    - Converting string values like "$123.4" to float
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning labour productivity data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = rename_column(df, "{'labour_productivity'}", "GDP per hour worked ($)")
    validate_column(df, "GDP per hour worked ($)", (0,200))
    return df


def clean_safety_and_health_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the safety and health at work dataset by:
    - Removing thousands separators (e.g., '9,421' → 9421)
    - Converting all non-country columns to numeric
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning safety data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    validate_column(df, "Non-fatal occupational injuries per 100'000 workers", (0,10000))
    validate_column(df,"Occupational fatalities per 100'000 workers")
    validate_column(df,"Inspectors per 10'000 employed persons")
    return df

def clean_wages_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the wages dataset by:
    - Extracting just the country name (before any brackets or extra details)
    - Dropping the '$US' column
    - Converting 'PPP $' values to float
    - Renaming column to 'min. monthly wage (PPP$)'
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning wages data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = df.drop(df.columns[[2]], axis=1)
    df = rename_column(df, "PPP $", "min. monthly wage (PPP $)")
    validate_column(df, "min. monthly wage (PPP $)", (0,4000))
    return df


def clean_working_poverty_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the working poverty dataset by:
    - Converting all percentage strings to numeric values
    - Appending '%' to column names (except for 'Country')
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning working poverty data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = rename_column(df, "Extremely poor", "Extremely poor (%)")
    df = rename_column(df, "Moderately poor", "Moderately poor (%)")
    df = rename_column(df, "Not extremely or moderately poor", "Not extremely or moderately poor (%)")
    validate_column(df, "Extremely poor (%)")
    validate_column(df, "Moderately poor (%)")
    validate_column(df, "Not extremely or moderately poor (%)")
    return df

def clean_working_time_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the working time dataset by:
    - Converting percentage strings to float values
    - Appending '%' to 'Share of employed working 49 or more hours per week' column title
    - Checking for missing values and outliers
    """

    print(f"\n--- Cleaning working time data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = rename_column(df, "Share of employed working 49 or more hours per week", "Share of employed working 49 or more hours per week (%)")
    validate_column(df, "Average hours per week per employed person")
    validate_column(df, "Share of employed working 49 or more hours per week (%)")
    return df


def clean_employment_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the employment dataset by:
    - Converting the employment ratio to numeric (removes '%')
    - Renaming the column to include '%' in the title
    - Checking for missing values and outliers

    """
    print(f"\n--- Cleaning employment data ---")
    df = clean_country_names(df)
    df = clean_numeric_columns(df)
    df = rename_column(df, "Employment to Population ratio", "Employment to Population ratio %")
    validate_column(df, "Employment to Population ratio %")
    return df


def main():
    # === UNEMPLOYMENT ===
    unemployment_raw_path = "../data/raw/unemployment_and_labour_underutilization_raw.csv"
    unemployment_output_path = "../data/clean/ilostat_unemployment_clean.csv"
    unemployment_df = pd.read_csv(unemployment_raw_path)
    unemployment_cleaned = clean_unemployment_data(unemployment_df)
    os.makedirs(os.path.dirname(unemployment_output_path), exist_ok=True)
    unemployment_cleaned.to_csv(unemployment_output_path, index=False)
    print("\nUnemployment cleaned preview:")
    print(unemployment_cleaned.head())
    print(f"Unemployment cleaned file saved to {unemployment_output_path}")

    # === LABOUR PRODUCTIVITY ===
    labour_raw_path = "../data/raw/labour_productivity_raw.csv"
    labour_output_path = "../data/clean/ilostat_labour_productivity_clean.csv"
    labour_df = pd.read_csv(labour_raw_path)
    labour_cleaned = clean_labour_productivity_data(labour_df)
    labour_cleaned.to_csv(labour_output_path, index=False)
    print("\nLabour productivity cleaned preview:")
    print(labour_cleaned.head())
    print(f"Labour productivity cleaned file saved to {labour_output_path}")

    # === SAFETY AND HEALTH ===
    safety_raw_path = "../data/raw/safety_and_health_at_work_raw.csv"
    safety_output_path = "../data/clean/ilostat_safety_and_health_clean.csv"
    safety_df = pd.read_csv(safety_raw_path)
    safety_cleaned = clean_safety_and_health_data(safety_df)
    safety_cleaned.to_csv(safety_output_path, index=False)
    print("\nSafety and health cleaned preview:")
    print(safety_cleaned.head())
    print(f"Safety and health cleaned file saved to {safety_output_path}")

    # === WAGES ===
    wages_raw_path = "../data/raw/wages_raw.csv"
    wages_output_path = "../data/clean/ilostat_wages_clean.csv"
    wages_df = pd.read_csv(wages_raw_path)
    wages_cleaned = clean_wages_data(wages_df)
    wages_cleaned.to_csv(wages_output_path, index=False)
    print("\nWages cleaned preview:")
    print(wages_cleaned.head())
    print(f"Wages cleaned file saved to {wages_output_path}")

    # === WORKING POVERTY ===
    poverty_raw_path = "../data/raw/working_poverty_raw.csv"
    poverty_output_path = "../data/clean/ilostat_working_poverty_clean.csv"
    poverty_df = pd.read_csv(poverty_raw_path)
    poverty_cleaned = clean_working_poverty_data(poverty_df)
    poverty_cleaned.to_csv(poverty_output_path, index=False)
    print("\nWorking poverty cleaned preview:")
    print(poverty_cleaned.head())
    print(f"Working poverty cleaned file saved to {poverty_output_path}")

    # === WORKING TIME ===
    working_time_raw_path = "../data/raw/working_time_raw.csv"
    working_time_output_path = "../data/clean/ilostat_working_time_cleaned.csv"
    working_time_df = pd.read_csv(working_time_raw_path)
    working_time_cleaned = clean_working_time_data(working_time_df)
    working_time_cleaned.to_csv(working_time_output_path, index=False)
    print("\nWorking time cleaned preview:")
    print(working_time_cleaned.head())
    print(f"Working time cleaned file saved to {working_time_output_path}")

    # Clean and save employment data
    employment_raw_path = "../data/raw/employment_raw.csv"
    employment_output_path = "../data/clean/ilostat_employment_cleaned.csv"
    employment_df = pd.read_csv(employment_raw_path)
    employment_cleaned = clean_employment_data(employment_df)
    employment_cleaned.to_csv(employment_output_path, index=False)
    print("\nCleaned Employment Data Preview:")
    print(employment_cleaned.head())
    print(f"Employment cleaned file saved to {employment_output_path}")

if __name__ == "__main__":
    main()




