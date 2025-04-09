# CIP_FS25_202
Happiness around the World Project

What Drives Happiness? A Comparative Analysis Using Betterlife, Gallup, ILOSTAT & World Happiness Data

# Project Description

This project explores the following questions:

- Which factors have the biggest impact on happiness?
- How have happiness levels changed globally over the past decade?
- Do people's experienced emotions effect happiness and is there a difference in happiness between old people and young people?

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

We scraped, collected, cleaned, and merged these datasets, then applied visual analytics as well as statistical and 
machine learning methods to evaluate which indicators most strongly relate to happiness.

# Key Objectives
Understand which social and economic indicators predict happiness:

  - Scrape information from multiple websites
  
  - Clean and standardize multiple raw datasets 
  
  - Merge global datasets using country alignment techniques
  
  - Analyse the data through appropriate means:
  
    - visualisation, correlation analysis, linear regression, and random forest models
    
  - Visualize results and evaluate model performance
    
Rank top predictors of happiness


# Folder Structure
<pre> ```CIP_FS25_GXX/
│
├── data/
│   ├── raw/                # Original downloaded CSV and scraped data
│   ├── clean/              # Cleaned versions of the data
│   ├── merged/             # Final merged datasets (with happiness index)
│
├── notebooks/
│   ├── clean_scripts.py    # Data cleaning for each source
│   ├── merge_datasets.py   # Merging and harmonizing datasets
│   ├── analysis.py         # Correlation, regression, random forest
│   └── visuals/            # Optional saved plots and figures
│
├── report/
│   ├── CIP_Final_Report.pdf    # Final project write-up
│   └── figures/                # Exported charts and tables for the report
│
├── README.md
├── requirements.txt        # Python libraries to install
└── LICENSE (if applicable) ``` </pre>



# Packages used
- Python 3.11+
- pandas
- numpy
- matplotlib, seaborn
- scikit-learn
- Selenium + BeautifulSoup
- openpyxl 

# Key Insights
.....

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


- Run scripts from notebooks or command line:
  - clean_scripts.py → cleans all source datasets
  - merge_datasets.py → merges + adds happiness index
  - analysis.py → regression, random forest, and plots

#Team Contributions


| Name            | GitHub Name | Data Sources Scraped, Cleaned, and Analyzed |
|-----------------|-------------|---------------------------------------------|
| Jade Bullock    | jbull999    | Gallup Global, ILOSTAT                      |
| Dora            |             |                                             |
| Ramona Kölliker | Ra-Mona09   | World Happiness Report, Happiness by Age    |


# Report
The final project report is available in 

/report/CIP_202_Final_Report.pdf.

It includes research questions, methodology, visuals, findings, and conclusions.
