"""
Extracts Gallup Law & Order and Safety perception data from public Datawrapper CSV sources.

It downloads two datasets (Safety and Law & Order indices),
merges them on country name, and saves the result to a CSV file.

The robots.txt on this website was checked to ensure that information scrapped was allowed.

Source:
https://www.gallup.com/analytics/356996/gallup-law-and-order-research-center.aspx
authors:    Jade Bullock
date:       23.03.2025
"""
import pandas as pd
import requests
from io import StringIO

# URLs for the datasets
url_law_order = "https://datawrapper.dwcdn.net/7i1nV/5/dataset.csv"
url_safety = "https://datawrapper.dwcdn.net/jqGCk/6/dataset.csv"

# Custom headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download the CSVs manually using requests
resp_safety = requests.get(url_safety, headers=headers)
resp_law_order = requests.get(url_law_order, headers=headers)

# Read the CSV content into pandas
df_safety = pd.read_csv(StringIO(resp_safety.text))
df_law_order = pd.read_csv(StringIO(resp_law_order.text))

# Preview columns
print("Safety:", df_safety.columns.tolist())
print("Law & Order:", df_law_order.columns.tolist())

# Merge and save
df_safety.rename(columns={"DW_NAME": "Country"}, inplace=True)
df_law_order.rename(columns={"DW_NAME": "Country"}, inplace=True)

merged_df = pd.merge(
    df_safety, df_law_order,
    on="Country", suffixes=("_Safety", "_LawOrder")
)

merged_df.to_csv("Gallup_Safety_and_Law_Index_raw.csv", index=False)
print("CSV saved: Gallup_Safety_and_Law_Index.csv")
