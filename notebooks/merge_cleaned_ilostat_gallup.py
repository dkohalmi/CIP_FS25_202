

"""
This script merges multiple cleaned ILOSTAT (7 datasets) and 2 x Gallup datasets into two master CSV files:
- ../data/clean/ilostat_merge.csv
- ../data/clean/gallup_merge.csv

For both, the script:
- Standardizes and normalizes country names across sources for consistent merging.
- Adds the 2024 Happiness Index ("Ladder score") from cleaned data sourced from:
  https://data.worldhappiness.report/map
- Prints unmatched countries to assist in troubleshooting merge mismatches.


Authors: Jade Bullock
Date: 05.04.2025
"""
import pandas as pd
import os
from functools import reduce

HAPPINESS_PATH = "../data/clean/happinessindex.xlsx"
HAPPINESS_YEAR = 2024

def normalize_text(s):
    """
    Cleans and standardizes country names to allow for consistent merging across datasets.
    This function:
    - Converts text to lowercase (standardizes casing)
    - Replaces curly quotes and long dashes (common in copied/pasted text)
    - Removes commas and periods (punctuation inconsistencies)
    - Trims whitespace

    Needed because of the different formatting for country names
    (e.g., 'Côte d’Ivoire' vs. 'Cote d'Ivoire').
    """
    if not isinstance(s, str):
        return s
    return (
        s.lower()
        .replace("’", "'")
        .replace("‘", "'")
        .replace("–", "-")
        .replace(",", "")
        .replace(".", "")
        .strip()
    )

def get_country_fixes():
    """Returns a dictionary of known inconsistent country names mapped to standardized names for consistency."""
    fixes = {
        "czech republic": "czechia",
        "cote d'ivoire": "côte d’ivoire",
        "côte d'ivoire": "côte d’ivoire",
        "democratic republic of the congo": "dr congo",
        "democratic republic of congo": "dr congo",
        "congo democratic republic of the": "dr congo",
        "congo": "republic of the congo",
        "the republic of the congo": "republic of the congo",
        "occupied palestinian territory":"state of palestine",
        "dr congo": "dr congo",
        "hong kong": "hong kong sar of china",
        "hong kong (sar of china)": "hong kong sar of china",
        "hong kong, sar of china": "hong kong sar of china",
        "hong kong china":"hong kong sar of china",
        "moldova, republic of": "republic of moldova",
        "moldova republic of": "republic of moldova",
        "republic of moldova": "republic of moldova",
        "netherlands (kingdom of the)": "netherlands",
        "the netherlands": "netherlands",
        "gambia": "gambia",
        "the gambia": "gambia",
        "lao people's democratic republic": "lao pdr",
        "south korea": "republic of korea",
        "korea republic of": "republic of korea",
        "korea": "republic of korea",
        "taiwan, province of china":"taiwan china" ,
        "taiwan province of china":"taiwan china",
        "united states": "united states of america",
        "tanzania united republic of": "tanzania",
        "viet nam": "vietnam",
        "united kingdom of great britain and northern ireland": "united kingdom",
        "iran islamic republic of": "iran",
        "macau china":"macao"
    }
    return {k.lower(): v.lower() for k, v in fixes.items()}

def load_happiness_data():
    """Loads and filters the happiness index data for the selected year, normalizing country names.
    Also standardizes inconsistencies using the get_country_fixes mapping."""
    happiness_df = pd.read_excel(HAPPINESS_PATH)
    happiness_df = happiness_df[happiness_df["Year"] == HAPPINESS_YEAR]
    happiness_df = happiness_df[["Country name", "Ladder score"]].rename(columns={"Country name": "Country", "Ladder score": "Happiness Index"})
    happiness_df["Country"] = happiness_df["Country"].astype(str).apply(normalize_text)
    happiness_df["Country"] = happiness_df["Country"].replace(get_country_fixes())
    return happiness_df

def merge_dataframes(file_paths):
    """
     Merges multiple CSV files into a single dataframe using outer joins.
    - Normalizes country names from each file (using function)
    - Applies country fixes for naming consistency (using function)
    - Deduplicates any repeated column names
    - Removes aggregate-only rows with no relevant data
    """
    dataframes = []
    for path in file_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            df.columns.values[0] = "Country" # Ensures consistent merging by renaming first column
            df["Country"] = df["Country"].astype(str).apply(normalize_text)
            df["Country"] = df["Country"].replace(get_country_fixes()) # Standardize country names
            dataframes.append(df)
        else:
            print(f" File not found: {path}")

    if not dataframes:
        print(" No files to merge.")
        return pd.DataFrame()

    merged_df = reduce(lambda left, right: pd.merge(left, right, on="Country", how="outer", suffixes=('', '_dup')), dataframes)

    for col in merged_df.columns:
        if col.endswith('_dup'):
            base_col = col.replace('_dup', '')
            merged_df[base_col] = merged_df[base_col].combine_first(merged_df[col])
            merged_df.drop(columns=[col], inplace=True)

    #Remove the rows that only have values in "Employment to Population ratio %" to reduce noise from data
    #Also displays the rows removed to check that useful rows not accidently deleted
    if "Employment to Population ratio %" in merged_df.columns:
        employment_only = merged_df.drop(columns=["Country", "Employment to Population ratio %"], errors='ignore').isna().all(axis=1)
        employment_only_rows = merged_df[employment_only & merged_df["Employment to Population ratio %"].notna()]
        if not employment_only_rows.empty:
            print("\n Removing rows that only contain data in 'Employment to Population ratio %':")
            pd.set_option("display.max_rows", None)
            pd.set_option("display.max_columns", None)
            pd.set_option("display.width", None)
            print(employment_only_rows[["Country", "Employment to Population ratio %"]])
            merged_df = merged_df[~(employment_only & merged_df["Employment to Population ratio %"].notna())]

    return merged_df.sort_values("Country").reset_index(drop=True)

def merge_with_happiness(df, label):
    """Merges the provided dataset with the happiness index dataset using standardized country names.
    Prints unmatched countries for troubleshooting."""
    df["Country"] = df["Country"].astype(str).apply(normalize_text)
    df["Country"] = df["Country"].replace(get_country_fixes())

    happiness_df = load_happiness_data()

    print("\nUnique countries in df:")
    print(sorted(df["Country"].unique()))
    print("\nUnique countries in happiness_df:")
    print(sorted(happiness_df["Country"].unique()))

    merged = pd.merge(df, happiness_df, on="Country", how="left")
    merged = merged.drop_duplicates(subset=merged.columns.tolist()) #removes duplicate rows
    merged["Country"] = merged["Country"].str.title()

    columns = merged.columns.tolist()
    if "Happiness Index" in columns:
        columns.insert(1, columns.pop(columns.index("Happiness Index")))
        merged = merged[columns]

    missing = merged[merged["Happiness Index"].isna()]["Country"].tolist()
    if missing:
        print(f"\n Countries in {label} data with no happiness match (total {len(missing)}):")
        for country in missing:
            print(f"- {country}")

    missing_from_df = set(happiness_df["Country"]) - set(df["Country"])
    if missing_from_df:
        print(f"\n Countries in Happiness Index not found in {label} dataset:")
        for country in sorted(missing_from_df):
            print(f"- {country}")

    return merged

def save_and_preview(df, output_path, label):
    """Saves the cleaned merged dataframe to CSV and prints the first few rows for quick verification."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n {label} saved to {output_path}")
    print(df.head())

def main():
    """
    Main function that runs the entire workflow:
    - Merges ILOSTAT files
    - Merges Gallup files
    - Adds happiness index to both
    - Saves final datasets to CSV.
    """
    print("\n=== Merging ILOSTAT datasets ===")
    ilostat_paths = [
        "../data/clean/ilostat_unemployment_clean.csv",
        "../data/clean/ilostat_labour_productivity_clean.csv",
        "../data/clean/ilostat_safety_and_health_clean.csv",
        "../data/clean/ilostat_wages_clean.csv",
        "../data/clean/ilostat_working_poverty_clean.csv",
        "../data/clean/ilostat_working_time_cleaned.csv",
        "../data/clean/ilostat_employment_cleaned.csv"
    ]
    ilostat_df = merge_dataframes(ilostat_paths)
    ilostat_df = merge_with_happiness(ilostat_df, label="ILOSTAT")
    save_and_preview(ilostat_df, "../data/clean/ilostat_merge.csv", "ILOSTAT merged dataset")

    print("\n=== Merging Gallup datasets ===")
    gallup_paths = [
        "../data/clean/gallup_emotions_clean.csv",
        "../data/clean/gallup_safety_clean.csv"
    ]
    gallup_df = merge_dataframes(gallup_paths)
    gallup_df = merge_with_happiness(gallup_df, label="Gallup")
    save_and_preview(gallup_df, "../data/clean/gallup_merge.csv", "Gallup merged dataset")

if __name__ == "__main__":
    main()


