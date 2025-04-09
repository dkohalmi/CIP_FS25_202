"""
This script scrapes employment data from the ILOSTAT topic page:
https://ilostat.ilo.org/topics/employment/  #has been updated/changed 2/4/25,

This script uses Selenium to interact with an iframe-based datawrapper chart,
clicks the "Show more" button if present, and extracts country-level employment
data from the HTML table using BeautifulSoup.

The final data is saved as a CSV file in the /data folder.
The robots.txt on this website was checked to ensure that information scrapped was allowed.

authors:    Jade Bullock
date:       23.03.2025

!!Important Note!! Information on the website was update 2/4/25 - Details changed!

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Setup WebDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment to run in background
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# Load main page
url = "https://ilostat.ilo.org/topics/employment/"
driver.get(url)

# Wait for iframe to load
try:
    iframe = wait.until(EC.presence_of_element_located((By.ID, "datawrapper-chart-HI0nK")))
    driver.switch_to.frame(iframe)
    print("Switched into iframe.")
except Exception as e:
    print("Failed to find or switch to iframe:", e)
    driver.quit()
    exit()


# Try to click the "Show more" button
try:
    # Find the button with visible "Show" text inside the iframe
    expand_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[contains(@class, 'expand-button')]/a[contains(text(), 'Show')]")
    ))
    expand_button.click()
    print("Clicked 'Show more' button.")
    time.sleep(2)  # wait for more rows to load
except Exception as e:
    print("Expand button not found or already clicked:", e)

# Parse the expanded content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Select information to scrape
rows = soup.select("table.medium tbody tr")

data = []
for row in rows:
    country_cell = row.find("th")
    value_cell = row.find("div", class_="sr-only")

    if country_cell and value_cell:
        country = country_cell.get_text(strip=True)
        value = value_cell.get_text(strip=True)
        data.append((country, value))

# Switch back to main page
driver.switch_to.default_content()
driver.quit()

# Save to CSV
#want file to go to data file
os.makedirs("data", exist_ok=True)

# Save to CSV
if data:
    ilosat_employment = pd.DataFrame(data, columns=["Country", "Employment to Population ratio"])
    ilosat_labour.to_csv("../data/employment.csv", index=False)
    print("Data saved to ../data/employment.csv")
else:
    print("No data found.")