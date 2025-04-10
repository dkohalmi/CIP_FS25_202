"""
Data Acquisition
scraping Table 2.2: Ranking of life evaluations by age group, 2021 - 2023 from
https://worldhappiness.report/ed/2024/happiness-of-the-younger-the-older-and-those-in-between/
This website does not have a robots.txt file. The data presented in their report is publicly available and
can be downloaded. No sensitive or personalized data was scraped.

author: Ramona Kölliker
Date: 26.03.2025
"""
##
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

## scrape
# setup webdriver
driver = webdriver.Firefox()

# load main page
url = "https://worldhappiness.report/ed/2024/happiness-of-the-younger-the-older-and-those-in-between/"
driver.get(url)

# locate the Table 2.2
# basic Xpath structure: //tagName[@AttributeName="Value"]
table = driver.find_element(By.XPATH, '//table[@class= "data-table data-table-compact"][caption[contains(text(),"Table 2.2: Ranking of life evaluations by age group, 2021- 2023")]]')

# extract table headers (=column names)
headers = [th.text for th in table.find_elements(By.TAG_NAME, "th")]
#print(headers)

# create a list to store the collected data
list_happiness_by_age= []

# extract all the row data
for row in table.find_elements(By.TAG_NAME, "tr")[1:]: #skip first row = headers (with tag "th")
    cells = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
    list_happiness_by_age.append(cells)
#print("Headers: ", headers)
#for row in rows:
    #print(row)
driver.quit()

## store scraped data
# convert list into Dataframe, including the headers as columns
df_happiness_by_age = pd.DataFrame(list_happiness_by_age, columns = headers)
print(df_happiness_by_age)

df_happiness_by_age.to_csv("./data/raw/happiness_by_age_raw.csv", index = False)