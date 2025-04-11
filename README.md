# CIP_FS25_202
# Happiness around the World Project

What Drives Happiness? A Comparative Analysis Using Betterlife, Gallup, ILOSTAT & World Happiness Data

### Authors: Jade Bullock, Ramona Kölliker, Dora Köhalmi
------
### Contributions:

__Jade Bullock__:
  - /notebooks/analyse_illostat.ipynb
  - /notebooks/analyse_gallup.ipynb
  - /notebooks/scrape_gallup_emotions.py
  - /notebooks/scrape_gallup_safety.py
  - /notebooks/scrape_ilostat_employment.py
  - /notebooks/scrape_ilostat_all.py
  - /notebooks/clean_gallup_emotions.py
  - /notebooks/clean_gallup_safety.py
  - /notebooks/clean_ilostat_all.py
  - /notebooks/merge_cleaned_ilostat_gallup.py
  - /st/pages/Emotions.py

__Ramona Kölliker__:
  - /notebooks/analyse_happiness_by_age_2021_2023.py
  - /notebooks/analyse_world_happiness_report_2024.py
  - /notebooks/clean_happiness_by_age.py
  - /notebooks/clean_world_happiness_report.py
  - /notebooks/merge_WHR2024_happinessindex.py
  - /notebooks/scrape_happiness_by_age.py
  - /notebooks/scrape_world_happiness_report.py

__Dora Köhalmi__:
  - /src/clean.betterlife.py
  - /src/scrape.betterlifeindex.py
  - /notebooks/scrape.betterlifeindex.ipynb
  - /notebooks/clean.betterlife.ipynb
  - /notebooks/analyse_betterlife.ipynb
  - /st/streamlit_app.py
  - /st/helper_functions.py
  - /st/utils/plotting_betterlife.py
  - /st/pages/Better_Life.py
  - /st/pages/Happiness.py 

----

# Project Description

This project explores the following questions:

- Which factors have the biggest impact on happiness?
- Is there a difference in happiness between old people and young people?
- Do people's experienced emotions affect happiness?

We scraped open data from:

- Gallup Global (emotions and safety survey data):
  - https://news.gallup.com/interactives/248240/global-emotions.aspx
  - https://www.gallup.com/analytics/356996/gallup-law-and-order-research-center.aspx
  
- ILOSTAT (labour and employment indicators)
  - https://ilostat.ilo.org/topics/employment/  
  - https://ilostat.ilo.org/topics/safety-and-health-at-work/",  
  - https://ilostat.ilo.org/topics/working-time/",  
  - https://ilostat.ilo.org/topics/wages/"  
  - https://ilostat.ilo.org/topics/unemployment-and-labour-underutilization/
  - https://ilostat.ilo.org/topics/working-poverty/
  - https://ilostat.ilo.org/topics/labour-productivity/

  
- World Happiness Report 
  - https://data.worldhappiness.report/map
- Happiness by Age (Table 2.2: Ranking of life evaluations by age group, 2021 - 2023)
  - https://worldhappiness.report/ed/2024/happiness-of-the-younger-the-older-and-those-in-between/


- Better Life
  - https://www.oecdbetterlifeindex.org/

We scraped, collected, cleaned, and merged these datasets, then applied visual analytics as well as statistical and 
machine learning methods to evaluate which indicators most strongly relate to happiness. To show our results we created a Streamlit Application.

# Key Objectives
Understand which social and economic indicators predict happiness:

  - Scrape information from multiple websites
  
  - Clean and standardize multiple raw datasets 
  
  - Merge global datasets using country alignment techniques
  
  - Analyse the data through appropriate means:
  
    - visualisation, correlation analysis, linear regression, and random forest models
    
  - Visualize results and evaluate model performance
  - Create a Streamlit Application to enable the user to explore the data we collected
    
  - Rank top predictors of happiness


# Folder Structure

Storing our small, collected data files directly in the GitHub repository, while generally discouraged for larger datasets, was a deliberate decision. This ensures the long-term functionality of our analysis, visualization, and modeling code, as well as the Streamlit application. Given the potential for website changes to break our scraping code, having the data directly accessible within the repository guarantees reproducibility even if the original sources become unavailable.

<pre> ```CIP_FS25_GXX/
│
├── data/
│   ├── raw/                # Original downloaded CSV and scraped data
│   ├── clean/              # Cleaned and merged versions of the data
│   
│
├── notebooks/
│   ├── scrape_...          # Scrape Data from each source
│   ├── clean_...           # Data cleaning for each source
│   ├── merge_...           # Merging and harmonizing datasets
│   ├── analyse_...         # Correlation, regression, random forest
│   └── visuals/            # Optional saved plots and figures
│
├── src/                    # Python scripts
│
├── st/
│   ├── streamlit_app.py     # Main Streamlit file 
│   ├── pages/               # Streamlit pages files
│   ├── helper_functions.py  # Helper functions to load and clean data
│   ├── utils/               # Functions for the page (Plotting functions for Better_Life Page)
│   
│
├── report/
│   ├── CIP_Final_Report.pdf    # Final project write-up
│   └── figures/                # Exported charts and tables for the report
│
├── README.md
├── requirements.txt        # Python libraries to install
└── LICENSE (if applicable) ``` </pre>



# Packages used
- numpy
- pandas
- selenium
- beautifulsoup4
- webdriver-manager
- matplotlib
- seaborn
- plotly
- streamlit
- tqdm
- openpyxl
- scikit-learn
- requests
- python-kaleido


# Key Insights

Our analysis shows that while income and economy matter, they aren't everything. Once a country reaches a certain income level, extra money doesn't lead to big gains in happiness. Instead, social support, emotional well-being, and personal freedom take center stage.

We also saw that emotions and safety perceptions strongly relate to happiness. Feeling safe and supported can often mean more to people than material wealth. 

Age-based analysis revealed that younger people tend to report higher life satisfaction than older adults. In many countries, this generational gap is wide—sometimes exceeding 30 ranking points—highlighting important demographic dynamics in well-being. One contributing factor may be the increased experience of physical pain among older adults, as reflected in our Gallup Emotions data. Pain was one of the strongest emotional correlations of unhappiness, and its prevalence rises with age due to chronic health conditions and declining mobility. This connection highlights how both physical and emotional health contribute to the drop in happiness often observed later in life.

Importantly, the OECD Better Life Index data added a complementary perspective. Happiness scores were strongly correlated with Environment, Jobs, and Health—three key areas not directly covered in the WHR regression model. Income, Housing, and Community also showed notable positive correlations, whereas Work-Life Balance had a surprisingly weak association. These findings suggest that economic stability alone isn't enough—people also need clean environments, decent work, and good health to thrive. 

These findings reinforce the idea that happiness is not determined by any single factor, but instead emerges from the complex interaction of emotional experiences, socioeconomic conditions, physical health, and environmental quality. By bringing together diverse datasets—from Gallup’s emotional and safety metrics to ILO labor indicators and the OECD Better Life Index—we were able to explore happiness through multiple lenses. Importantly, the inclusion of both subjective perceptions and objective conditions revealed that neither emotional well-being nor economic prosperity alone can fully explain global variations in happiness. This multidimensional approach offers a more holistic understanding of what shapes people’s lives and where policy efforts might most effectively be focused to support well-being across populations.


# How to Reproduce
- Clone the repo
<pre lang="markdown"> git clone https://github.com/yourname/CIP_FS25_202.git cd CIP_FS25_202  </pre>

- Create a virtual environment and install dependencies
<pre lang="markdown"> 
  # Create a virtual environment 
  python -m venv venv 
  # Activate the virtual environment 
  source venv/bin/activate    # On macOS/Linux 
  # OR 
  venv\Scripts\activate # On Windows 
  # Install the required Python packages 
  pip install -r requirements.txt  </pre>


- File names: 
  - scrape_..   → scrapes data
  - clean_ ...  → cleans  datasets
  - merge_....  → merges + adds happiness index
  - analyse.... → regression, random forest, and plots

#Team Contributions


| Name            | GitHub Name | Data Sources Scraped, Cleaned, and Analyzed |Streamlit App
|-----------------|-------------|---------------------------------------------|-----------------
| Jade Bullock    | jbull999    | Gallup Global, ILOSTAT                      |st/pages/Emotions.py
| Dora Köhalmi    | dkohalmi    | Better Life Index                           |st/streamlit_app.py, st/helper_functions, st/pages/Better_Life.py
| Ramona Kölliker | Ra-Mona09   | World Happiness Report, Happiness by Age    |


# Report
The final project report is available in 

/report/CIP_202_Final_Report.pdf.

It includes research questions, methodology, visuals, findings, and conclusions.
