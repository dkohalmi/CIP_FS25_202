"""
Data Acquisition
scraping the World Happiness Report 2024 from https://data.worldhappiness.report/map
This website does not have a robots.txt file. The data presented on their dashboard is publicly available and
can be downloaded. No sensitive or personalized data was scraped.

author: Ramona Kölliker
date: 17.03.2025
"""
##
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

## scrape
# setup webdriver
driver = webdriver.Firefox()

# load main page
url = "https://data.worldhappiness.report/map"
driver.get(url)
time.sleep(3) # wait to fully load webpage/dashboards

# find "Country" button and click it
dropdown_countries = driver.find_element(By.ID, ":r2:")
dropdown_countries.click()
time.sleep(5)

# wait for dropdown options to load
wait = WebDriverWait(driver, 20)
options_locator = (By.CSS_SELECTOR, ".MuiAutocomplete-popper .MuiAutocomplete-option")
wait.until(EC.presence_of_all_elements_located(options_locator))

# get all dropdown options = countries
options = driver.find_elements(*options_locator)

# get the text of the countries into a list
dropdown_countries = [country.text for country in options]
print("Dropdown Countries: ", dropdown_countries)

#options[0].click() -> select first country in the dropdown menu
number_of_countries = len(options)
print("Number of countries: ", number_of_countries)

# create a list of dictionaries to store the collected data
list_world_happiness_report = []

# looping through the country list
for country in dropdown_countries:
    time.sleep(3)

    # locate the dropdown input field
    dropdown_input = driver.find_element(By.ID, ":r2:")

    # click the input field to activate the dropdown
    dropdown_input.click()
    time.sleep(5)

    # "Keys module" simulates key presses in the browser (mimicking human-like keyboard interaction)
    # deleting any existing input to be able to "select"/typing in the next dropdown option
    dropdown_input.send_keys(Keys.CONTROL + "a")  # selecting all text like Ctrl+A (select all)
    dropdown_input.send_keys(Keys.BACKSPACE)  # delete selected text
    time.sleep(5)

    # type in the current country name from the loop (dropdown_countries list)
    dropdown_input.send_keys(country)
    time.sleep(5)

    # press "Enter" to select the next matching option
    dropdown_input.send_keys(Keys.RETURN)

    # wait for the remaining option to be visible
    option = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiAutocomplete-option")))

    # click on the option (country name)
    option.click()
    time.sleep(5)

    # extract the data
    try:
        # extract Overall Rank and Average Life Evaluation score per country
        element = driver.find_element(By.CSS_SELECTOR, ".ml-4.shrink")
        text = element.text
        print("Extracted Text:", text)

        # use regex
        rank_match = re.search(r"Rank:\s*(\d+)", text) #\s* zero or more spaces, \d+ one or more digits
        life_eval_match = re.search(r"Average Life Evaluation:\s*([\d.]+)", text) #\d. digit or decimal point

        # convert text into integer/float, if there is no match -> N/A
        rank = int(rank_match.group(1)) if rank_match else "N/A"
        life_eval = float(life_eval_match.group(1)) if life_eval_match else "N/A"

        # scrape table with the explanatory factors
        # initialize dictionaries to store the data for each factor/each row in table
        factors_dict = {
            "Social support": {},
            "GDP per capita": {},
            "Healthy life expectancy": {},
            "Freedom": {},
            "Generosity": {},
            "Perceptions of corruption": {}
        }

        rows = driver.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-row")

        # get all column values for each row; removing possible whitespaces.
        # for missing data -> store N/A
        for row in rows:
            try:
                factor_name = row.find_element(By.CSS_SELECTOR, '[data-field="Factor"]').text.strip()
                rank_val = row.find_element(By.CSS_SELECTOR, '[data-field="Rank"]').text.strip() or "N/A"
                value_val = row.find_element(By.CSS_SELECTOR, '[data-field="Value"]').text.strip() or "N/A"
                explains_val = row.find_element(By.CSS_SELECTOR, '[data-field="Explains"]').text.strip() or "N/A"

                print(f"Factor row: {factor_name}, Rank: {rank_val}, Value: {value_val}, Explains: {explains_val}")

                # store extracted values into the corresponding dictionary
                if factor_name in factors_dict:
                    factors_dict[factor_name]["Rank"] = rank_val
                    factors_dict[factor_name]["Value"] = value_val
                    factors_dict[factor_name]["Explains"] = explains_val
            except Exception as e:
                print(f"Skipping a row due to error: {e}")
                continue

        # merge all extracted data into one row (single dictionary), country leveled
        row_data = {
            "Country": country,
            "Overall Rank": rank, #overall life evaluation score-ranking
            "Average Life Evaluation": life_eval,
        }

        # create new keys and get values from sub-dictionaries
        # new key names to uniquely define the columns in DF/CSV
        for factor, values in factors_dict.items():
            row_data[f"{factor} Rank"] = values.get("Rank", "N/A")
            row_data[f"{factor} Value"] = values.get("Value", "N/A")
            row_data[f"{factor} Explains"] = values.get("Explains", "N/A")

        list_world_happiness_report.append(row_data)

    except Exception as e:
        print(f"Could not extract data for {country}: {e}")
        continue

    # keep track of scraping progress
    print("Scraping complete. Total countries: ", len(list_world_happiness_report))

driver.quit()
#print(list_world_happiness_report)

## store scraped data
import pandas as pd

# convert list into Dataframe
df_world_happiness_report = pd.DataFrame(list_world_happiness_report)

# fill any missing cells with "N/A"
df_world_happiness_report.fillna("N/A", inplace = True)

# print a preview
print(df_world_happiness_report.head())

# save the Dataframe to a CSV file
df_world_happiness_report.to_csv("./data/raw/world_happiness_report_raw.csv", index = False)