"""
This script merges the scraped and cleaned data: ./data/clean/world_happiness_report_2024_clean.csv
with the "average life evaluation scores" for the years 2023, 2022, 2021, 2020 from
./data/clean/happinessindex.xlsx.

The data from the World Happiness Report 2024 includes the "Average Life Evaluation" and corresponding globally ranking
averaged over the annual Life Evaluation score of the preceding years 2024, 2023, 2022.
There is data available to download from: https://worldhappiness.report/data-sharing/ which includes the
three-year averages for life evaluation from 2012 onwards. This Excel-File was downloaded and saved as happinessindex.xlsx.


author: Ramona Kölliker
date: 04.04.2025
"""

##
import pandas as pd

## load data
# load data (scraped and cleaned)
df_WHR2024 = pd.read_csv("./data/clean/world_happiness_report_2024_clean.csv")

# load downloaded data
df_happiness = pd.read_excel("./data/clean/happinessindex.xlsx")

# inspect both datasets (df_happiness based on year 2024)
df_WHR2024.head()
df_happiness.head()
df_happiness.info()
len(df_happiness[df_happiness["Year"] == 2024]) #147 countries
len(df_WHR2024) #164 countries

countries_happiness = df_happiness[df_happiness["Year"] == 2024]["Country name"].unique()
countries_WHR = df_WHR2024["Country"].unique()
len(countries_happiness) #147
len(countries_WHR) #164

# check for matching countries
countries_both = set(countries_WHR).intersection(set(countries_happiness))
len(countries_both) #147 -> so all available countries from df_happiness are also in df_WHR2024

print("Countries with no intersection between datasets: ", set(countries_WHR)-countries_both)
# {'Cuba', 'Central African Republic', 'Syria', 'Guyana', 'Bhutan', 'Qatar', 'Turkmenistan', 'South Sudan', 'Burundi',
# 'Angola', 'Rwanda', 'Sudan', 'Belarus', 'Suriname', 'Maldives', 'Haiti', 'Djibouti'}
len(set(countries_WHR)-countries_both) #17; same 17 countries with no data in df_WHR2024 (see clean_world_happiness_report.py:
#Angola,Belarus,Bhutan,Burundi,Central African Republic,Cuba,Djibouti,Guyana,Haiti,Maldives,Qatar,Rwanda,South Sudan,Sudan,Suriname,Syria,Turkmenistan

# according to dataset description df_happiness "ladder score" 2024 and the "average life evaluation" value from df_WHR2024
# should be the same value. let`s check

# filter both datasets to only include the common countries and reset the indices to be able to do comparison
df_happiness_common = df_happiness_common.set_index("Country name").loc[df_WHR2024_common["Country"].values].reset_index()
df_WHR2024_common = df_WHR2024_common.set_index("Country").loc[df_happiness_common["Country name"].values].reset_index()
len(df_happiness_common)
len(df_WHR2024_common)

# create a comparison DataFrame
df_comparison2024 = pd.DataFrame({
    "Country": df_happiness_common["Country name"],
    "Ladder score": df_happiness_common["Ladder score"],
    "Average Life Evaluation": df_WHR2024_common["Average Life Evaluation"],
    "Same": df_happiness_common["Ladder score"].values == df_WHR2024_common["Average Life Evaluation"].values
})

print(df_comparison2024["Same"])

# check now if all entries in the "Same" column are True = all values match between the two dataset for the year 2024
equal_val = df_comparison2024["Same"].all()

if equal_val:
    print("All entries match.")
else:
    print("Some entries do not match.")

"""
conclusion: all entries match -> we have all 147 countries in df_happiness matching the countries in df_WHR2024.
The "Average life Evaluation" value in df_WHR2024 matches with the "Ladder Score" of the year 2024 in df_happiness.
Since the "Average Life Evaluation" value is based on the annual value of the  preceded 3 years (2024-> 2024,2023,2022),
we merge the "Ladder scores" from the Years 2023,2022,2021,2020 from the happinessindex with our main dataset df_WHR24
"""

# filter the years
df_happiness_years = df_happiness[df_happiness["Year"].isin([2023,2022,2021,2020])]
# we only need columns "Country name", "Year", "Ladder score" and "Rank"
df_happiness_years = df_happiness_years[["Country name", "Year", "Ladder score", "Rank"]]

# do a copy of original/main dataset df_WHR2024 before merging
df_WHR2024_copy = df_WHR2024.copy()

# add Ladder score and Rank for each year as new columns
for year in [2023, 2022, 2021, 2020]:
    year_data = df_happiness_years[df_happiness_years["Year"] == year]
    # left merge the data with df_WHR2024_copy
    df_WHR2024_copy.columns
    df_WHR2024_copy = df_WHR2024_copy.merge(year_data[["Country name", "Ladder score", "Rank"]],
                                            how = "left",
                                            left_on = "Country",
                                            right_on = "Country name")

    # rename the columns to see the year
    df_WHR2024_copy = df_WHR2024_copy.rename(columns={"Ladder score": f"Ladder score {year}", "Rank": f"Rank {year}"})

    # drop the redundant 'Country name' column
    df_WHR2024_copy = df_WHR2024_copy.drop(columns=["Country name"])

df_WHR2024_copy.head()
df_WHR2024_copy.info()

## save the merged dataframe in a csv for potential further exploration/combination with other datasets
df_WHR2024_copy.to_csv("./data/clean/WHR2024_merged_happinessindex_2023_2020.csv", index = False)