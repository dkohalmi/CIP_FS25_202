"""\
scrape happiness data from
https://news.gallup.com/interactives/248240/global-emotions.aspx.
https://www.gallup.com/analytics/356996/gallup-law-and-order-research-center.aspx?thank-you-report-form=1
In the 'tr'-tags of the table, find all values of the 'span' - tag.

authors:    Jade Bullock
date:       21.03.2025
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import os


# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Do not see the browser
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Initialize WebDriverWait once
wait = WebDriverWait(driver, 10)

# Open the Gallup Global Emotions interactive page
url = "https://news.gallup.com/interactives/248240/global-emotions.aspx"
driver.get(url)

# Wait for the page to fully load
time.sleep(10)

# Create list to store the data
data = []

# Find all emotion buttons and their attributes
emotion_buttons = driver.find_elements(By.CLASS_NAME, "c-interactive__toggle")
emotion_info = [
    {
        "label": b.text.strip(),
        "data_q": b.get_attribute("data-q")
    }
    for b in emotion_buttons
]

# Loop through emotion_info (using tqdm for a progress bar)
for info in tqdm(emotion_info, desc="Scraping emotions", unit="emotion"):
    emotion = info["label"]
    data_q = info["data_q"]
    print(f"Scraping data for: {emotion}")

    try:
        # Get current table HTML (to detect when it updates)
        table_elem = driver.find_element(By.ID, "emotions-table")
        old_table_html = table_elem.get_attribute("outerHTML")

        # Call the page's updateTable function directly with the emotion code
        driver.execute_script("updateTable(arguments[0]);", data_q)

        # Wait until the table's HTML changes
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "emotions-table").get_attribute("outerHTML") != old_table_html
        )

        # Parse the new table with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", id="emotions-table")
        if not table:
            print(f"Table not found for {emotion}")
            continue

        # Extract table rows
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                country = cells[0].text.strip()
                yes = cells[1].text.strip()
                no = cells[2].text.strip()
                dont_know = cells[3].text.strip()
                data.append([emotion, country, yes, no, dont_know])

    except Exception as e:
        print(f"Error processing {emotion}: {e}")

# Close browser
driver.quit()

#  Convert to DataFrame and save
df = pd.DataFrame(data, columns=["Emotion", "Country", "YES", "NO", "DON'T KNOW/REFUSED"])

# Remove duplicates
gallup_emotions_df = df.drop_duplicates(subset=["Emotion", "Country"])

# Ensure the parent-level data folder exists
os.makedirs("../data", exist_ok=True)

# Save to data folder one level up
gallup_emotions_df.to_csv("../data/gallup_emotions.csv", index=False)

print("Data saved to ../data/gallup_emotions.csv")