"""\
scrape happiness data from
https://ilostat.ilo.org/topics/labour-productivity/
https://www.gallup.com/analytics/356996/gallup-law-and-order-research-center.aspx?thank-you-report-form=1
In the 'tr'-tags of the table, find all values of the 'span' - tag.

authors:    Jade Bullock
date:       21.03.2025
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
url = "https://ilostat.ilo.org/topics/labour-productivity/"
driver.get(url)

# Wait for iframe to load
try:
    iframe = wait.until(EC.presence_of_element_located((By.ID, "datawrapper-chart-pUHnK")))
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

# You might need to adjust the selector below after inspecting the actual structure
rows = soup.select("table.medium tbody tr")

data = []
for row in rows:
    country_cell = row.find("th")
    value_cell = row.find("div", class_="sr-only")

    if country_cell and value_cell:
        country = country_cell.get_text(strip=True)
        value = value_cell.get_text(strip=True)
        data.append((country, value))

# Switch back to main page (optional)
driver.switch_to.default_content()
driver.quit()

#want file to go to data file
data_folder = "../data"
os.makedirs(data_folder, exist_ok=True)

# Save to CSV
if data:
    ilosat_labour = pd.DataFrame(data, columns=["Country", "Labour Productivity (USD/hour)"])
    ilosat_labour.to_csv(f"{data_folder}/labour_productivity.csv", index=False)
    print("Data saved to ..data/labour_productivity.csv")
else:
    print("No data found.")