"""
Data Transformation / Cleansing: World Happiness Report 2024
scraped data from website https://data.worldhappiness.report/map
raw csv: ./data/raw/world_happiness_report_raw.csv
clean csv: ./data/clean/world_happiness_report_2024_clean.csv

author: Ramona Kölliker
date: 02.04.2025
"""
##
import pandas as pd

## Missing Data Check
# read raw data, making sure pandas treats different "N/A" as missing values
df_raw_world_happiness = pd.read_csv("./data/raw/world_happiness_report_raw.csv", na_values= ["N/A", "-", "nan", "NaN"])

# inspect raw data
df_raw_world_happiness
# check column names:
df_raw_world_happiness.columns
# information about missing values and data type of the columns
df_raw_world_happiness.info()

# exploring the missing data
df_raw_world_happiness.isnull().sum()
print("Total number of missing values per column: ", df_raw_world_happiness.isnull().sum())
# "Country" is the only column without missing values
# "Healthy life expectancy Rank" and "Healthy life expectancy Value" have missing values for all 164 entries

# we exclude these two empty columns for the further data exploration
cols_to_exclude = ["Healthy life expectancy Rank", "Healthy life expectancy Value"]

# rows with at least one missing value
df_raw_world_happiness.drop(columns = cols_to_exclude).isnull().any(axis = 1)
print("Total number of rows with missing values: ", df_raw_world_happiness.drop(columns = cols_to_exclude).isnull().any(axis = 1).sum())
# we have 40 rows with missing values

# check if we have complete empty rows, no data at all for a country
#df_raw_world_happiness.drop(columns = ["Country"]).isnull().all(axis = 1)
countries_without_data = df_raw_world_happiness[df_raw_world_happiness.drop(columns = ["Country"]).isnull().all(axis = 1)]
print("Total number of countries without data: ", len(countries_without_data)) #17 countries without data
print(countries_without_data["Country"])

# check column "Country"
print(df_raw_world_happiness["Country"].unique())
print("Number of unique values in this column: ", df_raw_world_happiness["Country"].nunique())
print("Length of data frame: ", len(df_raw_world_happiness))

"""
conclusions: column "Country" is unique and complete, we have 17 countries without data.
We have 40 rows with at least one missing value
The columns "Healthy life expectancy Rank" and "Healthy life expectancy Value" have missing values for all 164 entries.
"""
## Cleaning
# fix column types: converting "objects" (strings) to "float"
# select object columns
object_cols = df_raw_world_happiness.select_dtypes(include = "object")
print("Object columns: ", object_cols.columns)

# we want to clean and convert all "object" columns of the dataframe except for "Country"
# select "object" (string) columns
cols_to_convert = [col for col in object_cols if col != "Country"]
print("Columns to convert; ", cols_to_convert)

# deep copy of the original dataframe to preserve the raw data
df_clean = df_raw_world_happiness.copy()

# function to clean and convert mixed-format strings (objects) to float
def clean_mixed_column(col):
    return pd.to_numeric(
        col.astype(str)
           .str.replace("%", "", regex = False)
           .str.replace("$", "", regex = False)
           .str.replace(",", "", regex = False)
           .str.replace("-", "", regex = False)
           .str.strip(),
        errors= "coerce" #N/A
    )

# apply cleaning function to each selected column
for col in cols_to_convert:
    df_clean[col] = clean_mixed_column(df_clean[col])

# check data type of cleaned dataframe
df_clean.info()

# since the columns "Healthy life expectancy Rank" and "Healthy life expectancy Value"
# have no data for all 164 entries = countries, we drop them
cols_to_exclude = ["Healthy life expectancy Rank", "Healthy life expectancy Value"]
df_clean.drop(columns = cols_to_exclude, inplace = True)

df_clean.head()

## Adding one column
# add one column of helpful additional information: creating another column "Region". The regions are according
# to the World Happiness Report MAP-Dashboard on https://data.worldhappiness.report/map
# the assignment of every country to one region was made by ChatGPT 4o and then cross-checked with the dashboard
region_dict = {
    # Western Europe
    "Austria": "Western Europe", "Belgium": "Western Europe", "Denmark": "Western Europe",
    "Finland": "Western Europe", "France": "Western Europe", "Germany": "Western Europe",
    "Iceland": "Western Europe", "Ireland": "Western Europe", "Luxembourg": "Western Europe",
    "Netherlands": "Western Europe", "Norway": "Western Europe", "Spain": "Western Europe",
    "Sweden": "Western Europe", "Switzerland": "Western Europe", "United Kingdom": "Western Europe",

    # Central and Eastern Europe
    "Albania": "Central and Eastern Europe", "Bosnia and Herzegovina": "Central and Eastern Europe",
    "Bulgaria": "Central and Eastern Europe", "Croatia": "Central and Eastern Europe",
    "Czechia": "Central and Eastern Europe", "Estonia": "Central and Eastern Europe",
    "Hungary": "Central and Eastern Europe", "Kosovo": "Central and Eastern Europe",
    "Latvia": "Central and Eastern Europe", "Lithuania": "Central and Eastern Europe",
    "North Macedonia": "Central and Eastern Europe", "Montenegro": "Central and Eastern Europe",
    "Poland": "Central and Eastern Europe", "Romania": "Central and Eastern Europe",
    "Serbia": "Central and Eastern Europe", "Slovakia": "Central and Eastern Europe",
    "Slovenia": "Central and Eastern Europe",

    # Commonwealth of Independent States
    "Armenia": "Commonwealth of Independent States", "Azerbaijan": "Commonwealth of Independent States",
    "Belarus": "Commonwealth of Independent States", "Kazakhstan": "Commonwealth of Independent States",
    "Kyrgyzstan": "Commonwealth of Independent States", "Republic of Moldova": "Commonwealth of Independent States",
    "Russian Federation": "Commonwealth of Independent States", "Tajikistan": "Commonwealth of Independent States",
    "Turkmenistan": "Commonwealth of Independent States", "Ukraine": "Commonwealth of Independent States",
    "Uzbekistan": "Commonwealth of Independent States",

    # East Asia
    "China": "East Asia", "Hong Kong SAR of China": "East Asia", "Japan": "East Asia",
    "Republic of Korea": "East Asia", "Taiwan Province of China": "East Asia", "Mongolia": "East Asia",

    # Southeast Asia
    "Cambodia": "Southeast Asia", "Indonesia": "Southeast Asia", "Lao PDR": "Southeast Asia",
    "Malaysia": "Southeast Asia", "Myanmar": "Southeast Asia", "Philippines": "Southeast Asia",
    "Singapore": "Southeast Asia", "Thailand": "Southeast Asia", "Vietnam": "Southeast Asia",

    # South Asia
    "Afghanistan": "South Asia", "Bangladesh": "South Asia", "Bhutan": "South Asia",
    "India": "South Asia", "Nepal": "South Asia", "Pakistan": "South Asia", "Sri Lanka": "South Asia",
    "Maldives": "South Asia",

    # Latin America and the Caribbean
    "Argentina": "Latin America and the Caribbean", "Belize": "Latin America and the Caribbean",
    "Bolivia": "Latin America and the Caribbean", "Brazil": "Latin America and the Caribbean",
    "Chile": "Latin America and the Caribbean", "Colombia": "Latin America and the Caribbean",
    "Costa Rica": "Latin America and the Caribbean", "Cuba": "Latin America and the Caribbean",
    "Dominican Republic": "Latin America and the Caribbean", "Ecuador": "Latin America and the Caribbean",
    "El Salvador": "Latin America and the Caribbean", "Guatemala": "Latin America and the Caribbean",
    "Guyana": "Latin America and the Caribbean", "Haiti": "Latin America and the Caribbean",
    "Honduras": "Latin America and the Caribbean", "Jamaica": "Latin America and the Caribbean",
    "Mexico": "Latin America and the Caribbean", "Nicaragua": "Latin America and the Caribbean",
    "Panama": "Latin America and the Caribbean", "Paraguay": "Latin America and the Caribbean",
    "Peru": "Latin America and the Caribbean", "Suriname": "Latin America and the Caribbean",
    "Trinidad and Tobago": "Latin America and the Caribbean", "Uruguay": "Latin America and the Caribbean",
    "Venezuela": "Latin America and the Caribbean",

    # Middle East and North Africa
    "Algeria": "Middle East and North Africa", "Bahrain": "Middle East and North Africa",
    "Egypt": "Middle East and North Africa", "Iran": "Middle East and North Africa",
    "Iraq": "Middle East and North Africa", "Israel": "Middle East and North Africa",
    "Jordan": "Middle East and North Africa", "Kuwait": "Middle East and North Africa",
    "Lebanon": "Middle East and North Africa", "Libya": "Middle East and North Africa",
    "Morocco": "Middle East and North Africa", "Oman": "Middle East and North Africa",
    "Qatar": "Middle East and North Africa", "Saudi Arabia": "Middle East and North Africa",
    "State of Palestine": "Middle East and North Africa", "Sudan": "Middle East and North Africa",
    "Syria": "Middle East and North Africa", "Tunisia": "Middle East and North Africa",
    "United Arab Emirates": "Middle East and North Africa", "Yemen": "Middle East and North Africa",

    # Sub-Saharan Africa
    "Angola": "Sub-Saharan Africa", "Benin": "Sub-Saharan Africa", "Botswana": "Sub-Saharan Africa",
    "Burkina Faso": "Sub-Saharan Africa", "Burundi": "Sub-Saharan Africa", "Cameroon": "Sub-Saharan Africa",
    "Central African Republic": "Sub-Saharan Africa", "Chad": "Sub-Saharan Africa", "Comoros": "Sub-Saharan Africa",
    "Congo": "Sub-Saharan Africa", "Côte d’Ivoire": "Sub-Saharan Africa", "DR Congo": "Sub-Saharan Africa",
    "Djibouti": "Sub-Saharan Africa", "Eswatini": "Sub-Saharan Africa", "Ethiopia": "Sub-Saharan Africa",
    "Gabon": "Sub-Saharan Africa", "Gambia": "Sub-Saharan Africa", "Ghana": "Sub-Saharan Africa",
    "Guinea": "Sub-Saharan Africa", "Kenya": "Sub-Saharan Africa", "Lesotho": "Sub-Saharan Africa",
    "Liberia": "Sub-Saharan Africa", "Madagascar": "Sub-Saharan Africa", "Malawi": "Sub-Saharan Africa",
    "Mali": "Sub-Saharan Africa", "Mauritania": "Sub-Saharan Africa", "Mauritius": "Sub-Saharan Africa",
    "Mozambique": "Sub-Saharan Africa", "Namibia": "Sub-Saharan Africa", "Niger": "Sub-Saharan Africa",
    "Nigeria": "Sub-Saharan Africa", "Rwanda": "Sub-Saharan Africa", "Senegal": "Sub-Saharan Africa",
    "Sierra Leone": "Sub-Saharan Africa", "Somalia": "Sub-Saharan Africa", "South Africa": "Sub-Saharan Africa",
    "South Sudan": "Sub-Saharan Africa", "Tanzania": "Sub-Saharan Africa", "Togo": "Sub-Saharan Africa",
    "Uganda": "Sub-Saharan Africa", "Zambia": "Sub-Saharan Africa", "Zimbabwe": "Sub-Saharan Africa",

    # North America, Australia, and New Zealand
    "Australia": "North America, Australia, and New Zealand", "Canada": "North America, Australia, and New Zealand",
    "New Zealand": "North America, Australia, and New Zealand", "United States": "North America, Australia, and New Zealand"
}

# map country names to the corresponding region
df_clean["Region"] = df_clean["Country"].map(region_dict)

# check for missing assignments
missing_regions = df_clean[df_clean["Region"].isnull()]["Country"].unique()
print("Countries with missing region assignment:", missing_regions)

# adding the missed countries to the dict
region_dict.update({
    "Cyprus": "Western Europe",
    "Georgia": "Commonwealth of Independent States",
    "Greece": "Western Europe",
    "Italy": "Western Europe",
    "Malta": "Western Europe",
    "Portugal": "Western Europe",
    "Türkiye": "Middle East and North Africa",
    "Viet Nam": "Southeast Asia"
})

# re-do the region mapping
df_clean["Region"] = df_clean["Country"].map(region_dict)
missing_regions = df_clean[df_clean["Region"].isnull()]["Country"].unique()
print("Countries with missing region assignment:", missing_regions)

df_clean.info()

## Checking expected ranges of values
# select numerical columns and get a summary statistics
cols_to_evaluate = [col for col in df_clean.columns if col not in ["Country", "Region"]]

# loop through the columns and print the statistics
for col in cols_to_evaluate:
    print("Description of column: ", col)
    print(df_clean[col].describe())
# conclusion: everything seems plausible

## Saving dataframe to csv
df_clean.to_csv("./data/clean/world_happiness_report_2024_clean.csv", index = False)