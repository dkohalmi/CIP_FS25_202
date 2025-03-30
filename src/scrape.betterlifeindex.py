#######################################
# Better Life Index Scraping Script
#
# Author: Dora Kohalmi
# #####################################
#  This Python script scrapes the numerical data from the Country section of the Better Life Index webpage
# ("https://www.oecdbetterlifeindex.org/#/11111111111"). There is no robots.txt on this page.
#
#  Output: 
#      csv file with the raw data frame: "/data/raw/betterlife_index.raw.csv"
# 
# This file is the script version of the scraping Jupyter Notebook scrape.betterlifeindex.ipynb .
#
###########################################################################################################

import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_value_by_data_indicator_id(driver, id, key, gender= False, social=False, gender_key="Gender_Inequality", 
                                      social_key="Social_Inequality"):
    ''' Function to scrape data from the Indicator sections 
    
        Parameters: 
           driver: web-driver instance to use
           id: data-indicator-id
           key: name of the variable stored in the dictionary (column name in the dataframe/csv file)
           gender: if True, we want to scrape Gender Inequality measure
           social: if True, we want to scrape Social Inequality measure
           gender_key: if Gender Inequality measure was scraped, this will be the name of the variable 
           social_key: if Social Inequality measure was scraped, this will be the name of the variable

        Output: 
           dict_country: as a global variable to collect all the data belonging to one particular country   
        ''' 
    # Define dict_country as a global variable so that we can collect all data for a particular country into the same dictionary:
    global dict_country

    try:
        # Find the section with the id and collect all "values" from this element:
        element = driver.find_element(By.CSS_SELECTOR, "div[data-indicator-id='"+ id +"']")
        values = element.find_elements(by=By.CLASS_NAME, value="value")
        list_of_values = [value.text for value in values]

        # Add the first value to the dictionary:
        dict_country.update({key:list_of_values[0] if len(list_of_values) > 0 else "N/A"})
       
        # Find out whether there is a "trend section" or not, because it also has a "value" in which case the gender and social inequality 
        # values are shifted below in the list_of_values:
        trend_shift=0
        try:
            if element.find_element(By.CSS_SELECTOR, ".trend.section"):
                trend_true=True
        except:
            trend_true=False
            
        # We need a shift in list_of_values if there is a trend section:    
        if trend_true:
            trend_shift=1

        # Check whether there is Gender or Social inequality section and find the value belonging to it in list_of_values, 
        # if gender = True or social = True
        if gender:
            try:
                gender=element.find_element(by=By.CSS_SELECTOR, value=".gender.inequality.section")
                dict_country.update({gender_key:list_of_values[1+trend_shift] if len(list_of_values) >(1+trend_shift) else "N/A"})
            except:    
                dict_country.update({gender_key:"N/A"})
                print('No gender inequality section for ',id)
            if social:
                try:
                    social=element.find_element(by=By.CSS_SELECTOR, value=".social.inequality.section")
                    dict_country.update({social_key: list_of_values[2+trend_shift]if len(list_of_values) >2+trend_shift else "N/A"}) 
                except:
                    dict_country.update({social_key:"N/A"})
                    print('No social inequality section for ',id)
        elif social:
            try:
                social=element.find_element(by=By.CSS_SELECTOR, value=".social.inequality.section")
                dict_country.update({social_key: list_of_values[-1] if len(list_of_values) >1 else "N/A"})
            except:
                dict_country.update({social_key:"N/A"}) 
                print('No social inequality section for ',id)
        return
    except:
        # If we haven't found a section with this id we set the value in the dictionary to N/A:
        print('No section for ',id)
        # Add "N/A" to the dictionary:
        dict_country.update({key:"N/A"})
        
        # If the gender or social flag was set but we haven't found such sections or values for them.
        if gender:
            dict_country.update({gender_key:"N/A"})
        if social:
            dict_country.update({social_key:"N/A"})   
        return


def main():
    """
    Function to scrape the numerical data from the Country section of the Better Life Index webpage 
    ("https://www.oecdbetterlifeindex.org/#/11111111111").

    Parameters: None

    Output:
        csv file: "/data/raw/betterlife_index.raw.csv" with the scraped data
    """
    PATH = "C:/Program Files (x86)/chromedriver.exe"
    # We will use Chrome browser. The location of the webdriver to Chrome is in PATH. We don't need it anymore.

    # Create a list of dictionaries to store the collected data:
    list_better_life_index=[]
 
    # Create an instance of the Chrome webdriver:
    driver=webdriver.Chrome()

    # Go to Better Life Index webpage:
    driver.get("https://www.oecdbetterlifeindex.org/#/11111111111")

    # Wait to load the page:
    time.sleep(5) 

    # Find "Countries" button and click it:
    dropdown_countries = driver.find_element(by=By.CLASS_NAME, value="nav-dropdown")
    dropdown_countries.click()
    time.sleep(5)


    # Wait until Dropdown list of countries is located:
    try:
        list_countries = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-dropdown__list"))
        )
    except:
        print("No dropdown list with countries found.")
        driver.quit()


    # Collect the links of each country in the dropdown list:
    list_c=list_countries.find_elements(by=By.TAG_NAME, value="a")

    list_links=[elem.get_attribute("href") for elem in list_c]


    # Loop through each link, each Country:
    for link in list_links:
        # Open each link
        driver.get(link) 
   
        # Wait for the page to load:
        time.sleep(5)  

        # Create dictionary to store the collected data for this particular country
        # It will be used as a global variable in the scraping function:
        dict_country={}
 
        country_name=driver.find_element(by=By.TAG_NAME, value="h1")
        print("Scraping: ", country_name.text)

        # Scrape  section "Did you know?" 
        block_did_you_know = driver.find_element(by=By.CLASS_NAME, value="span3")
        table = block_did_you_know.find_element(by=By.TAG_NAME, value="table")
        table_body = table.find_element(by= By.TAG_NAME, value="tbody")
        table_rows = table_body.find_elements(by=By.TAG_NAME, value="tr")
        table_values=[]
        for row in table_rows:
            value=row.find_element(by=By.TAG_NAME, value="td")
            table_values.append(value.text)
        
   
        # Add table data to the dictionary:
        dict_country.update({"Country": country_name.text,
                             "Population": table_values[0] if len(table_values) > 0 else "N/A",
                             "Visitors": table_values[1] if len(table_values) > 1 else "N/A",
                             "Renewable_Energy": table_values[2]} if len(table_values) > 2 else "N/A")

        # Scrape Section "Topics":
        element_topics = driver.find_element(by=By.ID, value="topics")
        topics_values = element_topics.find_elements(by=By.CLASS_NAME, value="value")

        list_values = [topic.text for topic in topics_values]

        # Add values to the dictionary:
        dict_country.update({"Housing":list_values[0] if len(list_values) > 0 else "N/A",
                             "Income":list_values[1] if len(list_values) > 1 else "N/A",
                             "Jobs":list_values[2] if len(list_values) > 2 else "N/A",
                             "Community":list_values[3] if len(list_values) > 3 else "N/A",
                             "Education":list_values[4] if len(list_values) > 4 else "N/A",
                             "Environment":list_values[5] if len(list_values) > 5 else "N/A",
                             "Civic_Engagement":list_values[6] if len(list_values) > 6 else "N/A",
                             "Health":list_values[7] if len(list_values) > 7 else "N/A",
                             "Life_Satisfaction":list_values[8] if len(list_values) > 8 else "N/A",
                             "Safety":list_values[9] if len(list_values) > 9 else "N/A",
                             "Work_Life_Balance":list_values[10] if len(list_values) > 10 else "N/A",
                            })


        # Scrape section "Housing --  Indicators":
        scrape_value_by_data_indicator_id(driver, 'HO_NUMR',  "Rooms_per_person")
        scrape_value_by_data_indicator_id(driver, 'HO_BASE',  "Basic_Facilities")
        scrape_value_by_data_indicator_id(driver, 'HO_HISH',  "Housing_Expenditure")


        # Scrape Section "Income -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'IW_HADI',  "Net_Disposable_Income", social=True, social_key="Social_Inequality_Income")
        scrape_value_by_data_indicator_id(driver, 'IW_HNFW',  "Net_wealth") 


        # Scrape Section "Jobs -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'JE_EMPL',  "Employment_Rate", gender=True, social=True,
                                          gender_key="Gender_Inequality_Employment", social_key="Social_Inequality_Employment")
        scrape_value_by_data_indicator_id(driver, 'JE_LTUR', "Long_Term_Unemployment", gender=True, social=True,
                                         gender_key="Gender_Inequality_Unemployment", social_key="Social_Inequality_Unemployment") 
        scrape_value_by_data_indicator_id(driver, 'JE_PEARN', "Personal_Earnings", gender=True, social=True,
                                         gender_key="Gender_Inequality_Earnings", social_key="Social_Inequality_Earnings")
        scrape_value_by_data_indicator_id(driver, 'JE_JT', "Job_Security")
  
    
        # Scrape Section "Community -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'SC_SNTWS',  "Quality_of_Support_Network", gender=True, social=True,
                                          gender_key="Gender_Inequality_Community", social_key="Social_Inequality_Community")

    
        # Scrape Section "Education -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'ES_EDUA',  "Educational_Attainment", gender=True, 
                                          gender_key="Gender_Inequality_Education")
        scrape_value_by_data_indicator_id(driver, 'ES_STCS',  "Student_Skills", gender=True, social=True,
                                          gender_key="Gender_Inequality_Skills", social_key="Social_Inequality_Skills")
        scrape_value_by_data_indicator_id(driver, 'ES_EDUEX',  "Years_in_Education", gender=True, 
                                          gender_key="Gender_Inequality_Years_Education")

    
        ## Scrape Section "Environment -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'EQ_AIRP',  "Air_Pollution")
        scrape_value_by_data_indicator_id(driver, 'EQ_WATER',  "Water_Quality")


        ## Scrape Section "Civic_Engagement -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'CG_VOTO',  "Voter_Turnout", gender=True, social=True,
                                          gender_key="Gender_Inequality_Voter", social_key="Social_Inequality_Voter")
        scrape_value_by_data_indicator_id(driver, 'CG_TRASG',  "Stakeholder_Engagement")
    

        # Scrape Section "Health -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'HS_LEB',  "Life_Expectancy", gender=True, 
                                          gender_key="Gender_Inequality_Life_Expectancy")
    
        scrape_value_by_data_indicator_id(driver, 'HS_SFRH',  "Self_Reported_Health", gender=True, social=True, 
                                          gender_key="Gender_Inequality_Health", social_key= "Social_Inequality_Health")


        # Scrape Section "Life_Satisfaction -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'SW_LIFS',  "Life_Satisfaction_2", gender=True, social= True,  
                                          gender_key="Gender_Inequality_Satisfaction", social_key="Social_Inequality_Satisfaction")
    

        # Scrape Section "Safety -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'PS_SFRV',  "Safe_at_Night", gender=True, 
                                          gender_key="Gender_Inequality_Safety")
        scrape_value_by_data_indicator_id(driver, 'PS_REPH',  "Homicide_Rate", gender=True, 
                                          gender_key="Gender_Inequality_Homicide")


        # Scrape Section "Work-Life Balance -- Indicators":
        scrape_value_by_data_indicator_id(driver, 'WL_EWLH',  "Long_Hours", gender=True, 
                                          gender_key="Gender_Inequality_Long_Hours")
        scrape_value_by_data_indicator_id(driver, 'WL_TNOW',  "Free_Time", gender=True, 
                                          gender_key="Gender_Inequality_Free_Time")
    
    
        # Add the dictionary to the list:
        list_better_life_index.append(dict_country)

    driver.quit()

    # Convert list of dicts into DataFrame:
    df_better_life = pd.DataFrame(list_better_life_index)

    # Write data frame into csv file:
    df_better_life.to_csv("../data/raw/betterlife_index.raw.csv", index=False)


if __name__=='__main__':
    main()