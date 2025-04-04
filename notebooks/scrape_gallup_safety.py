"""
Extracts Gallup Law & Order and Safety perception data from public Datawrapper CSV sources.

It downloads two datasets (Safety and Law & Order indices),
for use in the clean_gallup_safety file

Source:
https://www.gallup.com/analytics/356996/gallup-law-and-order-research-center.aspx

The robots.txt on this website was checked to ensure that information scrapped was allowed.

authors:    Jade Bullock
date:       23.03.2025
"""
import pandas as pd
import requests
from io import StringIO

def get_gallup_dataframes():
    # URLs for the datasets
    url_law_order = "https://datawrapper.dwcdn.net/7i1nV/5/dataset.csv"
    url_safety = "https://datawrapper.dwcdn.net/jqGCk/6/dataset.csv"

    #headers to mimic a browser
    headers = {"User-Agent": "Mozilla/5.0"}

    # Download the CSVs manually using requests
    resp_safety = requests.get(url_safety, headers=headers)
    resp_law_order = requests.get(url_law_order, headers=headers)

    df_safety = pd.read_csv(StringIO(requests.get(url_safety, headers=headers).text))
    df_law_order = pd.read_csv(StringIO(requests.get(url_law_order, headers=headers).text))

    return df_safety, df_law_order

if __name__ == "__main__":
    df_safety, df_law_order = get_gallup_dataframes()
    print(df_safety.head())
    print(df_law_order.head())

