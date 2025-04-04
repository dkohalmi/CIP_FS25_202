"""
This script defines a Python class ILOScraper to automate the scraping of country-level
labor statistics from the ILOSTAT website as the setup of each page is similar.
 https://ilostat.ilo.org/topics/safety-and-health-at-work/",
 https://ilostat.ilo.org/topics/working-time/",
 https://ilostat.ilo.org/topics/wages/"
 https://ilostat.ilo.org/topics/unemployment-and-labour-underutilization/
 https://ilostat.ilo.org/topics/working-poverty/
 https://ilostat.ilo.org/topics/labour-productivity/

The data is scraped from iframes, which are navigated using Selenium and parsed using BeautifulSoup.
The robots.txt on this website was checked to ensure that information scrapped was allowed.

authors:    Jade Bullock
date:       25.03.2025

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
import re

# Define a class for scraping the different ILOSTAT pages
class ILOScraper:
    def __init__(self, headless=False):
        # Initialize Chrome WebDriver
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.dataframes = {}  # Store DataFrames by topic name

    def scrape_page(self, url):
        print(f"\n Scraping: {url}")
        self.driver.get(url) # Load the URL
        time.sleep(3) # Allow for page to load

        # Extract from the URL a name to name the output file
        topic = url.rstrip("/").split("/")[-1].replace("-", "_")

        # Try command for switching into the iframe
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            print("Switched into iframe.")
        except Exception as e:
            print("Could not switch to iframe:", e)
            return

        # Try command for clicking the "Show more" button to expand the full table
        try:
            expand_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'expand-button')]/a[contains(text(), 'Show')]")
            ))
            expand_button.click()
            print("Clicked expand button.")
            time.sleep(2)
        except:
            print("️No expand button found or needed.")

        # Parse the iframe content using BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = soup.select_one("table.medium")

        # Extract headers from <thead> and use default if there are no headers
        thead = table.find("thead")
        if thead:
            header_cells = thead.find_all("th")
            headers = [cell.get_text(strip=True) for cell in header_cells]
        else:
            print("️ No <thead> found — using default headers.")
            headers = ["Country", {topic}]

        # Extract rows from <tbody>
        data = []
        for row in table.select("tbody tr" ):
            row_data = []

            #Extract country name from <th> cell
            country_cell = row.find("th")
            country = country_cell.get_text(strip=True) if country_cell else ""
            row_data.append(country)

            #Extract values from <div class="sr-only"> inside <td>
            value_cells = row.select("td")
            for cell in value_cells:
                sr_value = cell.find("div", class_="sr-only")
                value = sr_value.get_text(strip=True) if sr_value else ""
                row_data.append(value)

            data.append(row_data) # Append row to data list

        self.driver.switch_to.default_content() #Switch out of iframe

        if data:
            df = pd.DataFrame(data, columns=headers)
            self.dataframes[topic] = df #save each dataframe individually
            df.to_csv(f"../data/{topic}_raw.csv", index=False)
            print(f" Data saved to ../data/{topic}_raw.csv")
        else:
            print(f" No data found for {topic}")

    def scrape_multiple(self, url_list):
        for url in url_list:
            self.scrape_page(url)

    def close(self):
        self.driver.quit()
        print("\n Closed browser.")

# === Example Usage ===
if __name__ == "__main__":
    urls = [
        "https://ilostat.ilo.org/topics/safety-and-health-at-work/",# has been updated/changed 2/4/25,
        "https://ilostat.ilo.org/topics/working-time/", # has been updated/changed 2/4/25,
        "https://ilostat.ilo.org/topics/wages/", # has been updated/changed 2/4/25,
        "https://ilostat.ilo.org/topics/unemployment-and-labour-underutilization/", # has been updated/changed 2/4/25,
        "https://ilostat.ilo.org/topics/working-poverty/", # has been updated/changed 2/4/25,
        "https://ilostat.ilo.org/topics/labour-productivity/" # has been updated/changed 2/4/25,

    ]

    scraper = ILOScraper()
    scraper.scrape_multiple(urls)
    scraper.close()