"""
Analysis and Visualization: World Happiness Report 2024
data from csv: ./data/clean/world_happiness_report_2024.csv
in this script we also merge this dataset with the average life evaluation from the years 2023, 2022, 2021, 2020 from
./data/clean/happinessindex.xlsx, excel file downloaded from https://worldhappiness.report/data-sharing/

author: Ramona Kölliker
date: 04.04.2025
"""
##
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## load data
# load data (scraped and cleaned)
df_WHR2024 = pd.read_csv("./data/clean/world_happiness_report_2024_clean.csv")
"""From WHR Homepage https://data.worldhappiness.report/country: 
Happiness Ranking: Our global ranking is based on a single life evaluation question: Please imagine a ladder with steps 
numbered from 0 at the bottom to 10 at the top. The top of the ladder represents the best possible life for you and the 
bottom of the ladder represents the worst possible life for you. On which step of the ladder would you say you personally 
feel you stand at this time? We rank countries by their average life evaluation score over the three preceding years.
Each year, we conduct economic modelling to explain countries’ average life evaluation scores using 
six variables. Taken together, these six variables explain more than three-quarters of the variation in national 
life evaluation scores across countries and years. In the table below, we present three data points for each factor: 
[Rank] The country’s ranking for that factor compared to other nations, [Value] The value of the factor for the most 
recent year, [Explains] How much of the country’s life evaluation score is explained by the factor." 
The data from the World Happiness Report 2024 includes the "Average Life Evaluation" and corresponding globally ranking 
averaged over the annual Life Evaluation score of the years 2024, 2023, 2022.
There is data available to download from: https://worldhappiness.report/data-sharing/ which includes the 
three-year averages for life evaluation from 2012 onwards. We downloaded the Excel-File and saved ii as happinessindex.xlsx.
"""
## load downloaded data (from https://worldhappiness.report/data-sharing/) and merge it with main dataset
df_happiness = pd.read_excel("./data/clean/happinessindex.xlsx")
# inspect both datasets (df_happiness based on year 2024)
df_WHR2024.head()
df_happiness.head()
df_happiness.info()
len(df_happiness[df_happiness["Year"] == 2024]) #147 countries
len(df_WHR2024) #164 countries

countries_happiness= df_happiness[df_happiness["Year"] == 2024]["Country name"].unique()
countries_WHR = df_WHR2024["Country"].unique()
len(countries_happiness) #147
len(countries_WHR) #164
# check for matching countries
countries_both = set(countries_WHR).intersection(set(countries_happiness))
len(countries_both) #147 -> so all available countries from df_happiness are also in df_WHR2024
print("Countries with no intersection between datasets: ", set(countries_WHR)-countries_both)
# {'Cuba', 'Central African Republic', 'Syria', 'Guyana', 'Bhutan', 'Qatar', 'Turkmenistan', 'South Sudan', 'Burundi', 'Angola', 'Rwanda', 'Sudan', 'Belarus', 'Suriname', 'Maldives', 'Haiti', 'Djibouti'}
len(set(countries_WHR)-countries_both) #17; same 17 countries with no data in df_WHR2024 (see clean_world_happiness_report.py:
#Angola,Belarus,Bhutan,Burundi,Central African Republic,Cuba,Djibouti,Guyana,Haiti,Maldives,Qatar,Rwanda,South Sudan,Sudan,Suriname,Syria,Turkmenistan

# according to dataset description df_happiness "ladder score" 2024 and the "average life evaluation" value from df_WHR2024
# should be the same value. let`s check
# filter both datasets to only include the common countries, reseting the indices to be able to do comparison
df_happiness_common = df_happiness_common.set_index("Country name").loc[df_WHR2024_common["Country"].values].reset_index()
df_WHR2024_common = df_WHR2024_common.set_index("Country").loc[df_happiness_common["Country name"].values].reset_index()
len(df_happiness_common)
len(df_WHR2024_common)

# create a comparison DataFrame
df_comparison2024 = pd.DataFrame({
    "Country": df_happiness_common["Country name"],
    "Ladder score": df_happiness_common["Ladder score"],
    "Average Life Evaluation": df_WHR2024_common["Average Life Evaluation"],
    "Same": df_happiness_common["Ladder score"].values == df_WHR2024_common["Average Life Evaluation"].values
})
print(df_comparison2024["Same"])

# check now if all entries in the "Same" column are True = all values match between the two dataset for the year 2024
equal_val = df_comparison2024["Same"].all()

if equal_val:
    print("All entries match.")
else:
    print("Some entries do not match.")

# conclusion: all entries match -> we have all 147 countries in df_happiness matching the countries in df_WHR2024
# the "Average life Evaluation" value in df_WHR2024 matches with the "Ladder Score" of the year 2024 in df_happiness
# since the "Average Life Evaluation" value is based on the annual value of the  preceded 3 years (2024-> 2024,2023,2022),
# we merge the "Ladder scores" from the Years 2023,2022,2021,2020 from the happinessindex with our main dataset df_WHR24

# filter the years
df_happiness_years = df_happiness[df_happiness["Year"].isin([2023,2022,2021,2020])]
# we only need columns "Country name", "Year", "Ladder score" and "Rank"
df_happiness_years = df_happiness_years[["Country name", "Year", "Ladder score", "Rank"]]

# do a copy of original/main dataset df_WHR2024 before merging
df_WHR2024_copy = df_WHR2024.copy()

# Add Ladder score and Rank for each year as new columns
for year in [2023, 2022, 2021, 2020]:
    year_data = df_happiness_years[df_happiness_years["Year"] == year]
    # left merge the data with df_WHR2024_copy
    df_WHR2024_copy.columns
    df_WHR2024_copy = df_WHR2024_copy.merge(year_data[["Country name", "Ladder score", "Rank"]],
                                            how= "left",
                                            left_on= "Country",
                                            right_on= "Country name")

    # Rename the columns to see the year
    df_WHR2024_copy = df_WHR2024_copy.rename(columns={"Ladder score": f"Ladder score {year}", "Rank": f"Rank {year}"})

    # drop the redundant 'Country name' column
    df_WHR2024_copy = df_WHR2024_copy.drop(columns=["Country name"])

df_WHR2024_copy.head()
df_WHR2024_copy.info()

## save the merged dataframe in a csv for potential further exploration/combination with other datasets
# we will later compare the rankings/happiness scores of diff. years in this script
df_WHR2024_copy.to_csv("./data/clean/WHR2024_merged_happinessindex_2023_2020.csv", index=False)

## exploring df_WHR2024
# df_WHR2024 plot distributions of all variables to get a first impression
df_WHR2024.info()
for column in df_WHR2024.columns[:20]:
    plt.figure(figsize= (10, 6))
    sns.histplot(df_WHR2024[column], kde= True)
    plt.title(f"Distribution of {column}")
    plt.show()

# scatterplots of the "value" columns, we have actually six explanatory factors but for Healthy life expectancy we only have "explains"
df_WHR2024.columns
sns.scatterplot(data= df_WHR2024, x= "Social support Value", y= "Average Life Evaluation")
plt.show()
sns.scatterplot(data= df_WHR2024, x= "GDP per capita Value", y= "Average Life Evaluation")
plt.show()
sns.scatterplot(data= df_WHR2024, x= "Freedom Value", y= "Average Life Evaluation")
plt.show()
sns.scatterplot(data= df_WHR2024, x= "Generosity Value", y= "Average Life Evaluation")
plt.show()
sns.scatterplot(data= df_WHR2024, x= "Perceptions of corruption Value", y= "Average Life Evaluation")
plt.show()

# boxplots for the average life evaluation by "Region"
# sns.boxplot(x= "Region", y= "Average Life Evaluation", data= df_WHR2024) # bad readability
sns.boxplot(x= "Average Life Evaluation", y= "Region", color= "skyblue", data=df_WHR2024, orient= "h") # boxplot horizontally for readability of "Regions"
plt.ylabel("") # not needed, we have the region names
plt.xlabel("Happiness Score")
plt.savefig("boxplotsHappinessRegion.png")
plt.tight_layout()
plt.show() # two outliers, in the lower bound a global outlier and within region "East Asia" a outlier in upper bound

# get Name of Country for the outlier points
outliers= {}
# calculate IQR for each region
for region in df_WHR2024["Region"].unique():
    region_data = df_WHR2024[df_WHR2024["Region"] == region]
    Q1 = region_data["Average Life Evaluation"].quantile(0.25)
    Q3 = region_data["Average Life Evaluation"].quantile(0.75)
    IQR = Q3 - Q1
    # calculate bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    lower_outliers = region_data[region_data["Average Life Evaluation"] < lower_bound]
    upper_outliers = region_data[region_data["Average Life Evaluation"] > upper_bound]
    region_outliers = pd.concat([lower_outliers, upper_outliers])

    outliers[region] = region_outliers

# print outliers(the countries) for each region
for region, data in outliers.items():
    print(f"Outliers in {region} region:")
    print(data[["Country", "Region", 'Average Life Evaluation']])
    print("\n")

"""
we have outliers in two regions:
Outliers in South Asia region:
       Country      Region  Average Life Evaluation
0  Afghanistan  South Asia                    1.364
Outliers in East Asia region:
                      Country     Region  Average Life Evaluation
143  Taiwan Province of China  East Asia                    6.669
"""

## Research question: Which factors have the biggest impact on happiness?
# select Average Life Evaluation and all "value"-columns for a correlation Analysis
df_WHR2024.columns
correlation_columns_val = [
    "Average Life Evaluation", # points from 0 to 10
    "Social support Value", # in %
    "GDP per capita Value", # in USD
    "Freedom Value", # in %
    "Generosity Value", # in %
    "Perceptions of corruption Value" # in %
]
# correlation matrix
corr_matrix_val = df_WHR2024[correlation_columns_val].corr()
print("The correlation Matrix for values of the explanatory factors: ", corr_matrix_val)
print(corr_matrix_val.to_string()) # to get a output which is usable for report

# plot correlation heatmap
plt.figure(figsize= (10, 6))
sns.heatmap(corr_matrix_val, annot= True, cmap= "coolwarm", fmt= ".2f") # round it to two digits
plt.title("Correlation Heatmap: Explanatory Factors Value vs. Average Life Evaluation (Happiness Score)", fontsize= 14)
plt.tight_layout()
plt.savefig("HeatmapExplFactHappiness.png")
plt.show()

"""
Social support Value -> 0.78 Very strong pos. correlation — countries where people have strong social support tend to be happier
GDP per capita Value -> 0.74 Very strong pos. correlation — wealthier nations tend to be happier
Freedom Value -> 0.56 Moderate to strong pos. correlation — more personal freedom tend to leas to more happiness
Generosity Value -> 0.33 weakest pos. correlation — generous countries do tend to be happier
Perceptions of corruption -> -0.41 negative correlation — more corruption tend to lead to less happiness
"""

plot= sns.lmplot(data= df_WHR2024, x= "Social support Value", y= "Average Life Evaluation")
plot.set_axis_labels("Social Support in %", "Happiness Score (points from 0 to 10)", fontsize= 12) # reset labels for clarity in report
plt.ylim(0,10)
plt.savefig("lmplotSocialSupportHappiness.png")
plt.show()

plot= sns.lmplot(data= df_WHR2024, x= "GDP per capita Value", y= "Average Life Evaluation")
plot.set_axis_labels("GDP per capita in USD", "Happiness Score (points from 0 to 10)", fontsize= 12)
plt.ylim(0,10)
plt.savefig("lmplotGDPHappiness.png")
plt.show()

plot= sns.lmplot(data= df_WHR2024, x= "Freedom Value", y= "Average Life Evaluation")
plot.set_axis_labels("Freedom in %", "Happiness Score (points from 0 to 10)", fontsize= 12)
plt.ylim(0, 10)
plt.savefig("lmplotFreedomHappiness.png")
plt.show()

plot= sns.lmplot(data= df_WHR2024, x= "Generosity Value", y= "Average Life Evaluation")
plot.set_axis_labels("Generosity in %", "Happiness Score (points from 0 to 10)", fontsize= 12)
plt.ylim(0, 10)
plt.savefig("lmplotGenerosityHappiness.png")
plt.show()

plot= sns.lmplot(data= df_WHR2024, x= "Perceptions of corruption Value", y= "Average Life Evaluation")
plot.set_axis_labels("Perceptions of corruption in %", "Happiness Score (points from 0 to 10)", fontsize= 12)
plt.ylim(0, 10)
plt.savefig("lmplotCorruptionHappiness.png")
plt.show()

# fit a linear model, predicting Happiness based on the explanatory factors
# drop NA and rename columns to have no empty spaces. (lm.model did not work with backticks)
df_WHR2024_droped = df_WHR2024.copy()
df_WHR2024_droped = df_WHR2024_droped.dropna(subset=["Average Life Evaluation", "GDP per capita Value", "Social support Value", "Freedom Value", "Generosity Value", "Perceptions of corruption Value"])
print(df_WHR2024_droped.columns)
df_WHR2024_droped = df_WHR2024_droped.rename(columns={
    "Average Life Evaluation": "Average_Life_Evaluation",
    "GDP per capita Value": "GDP_per_capita_Value",
    "Social support Value": "Social_support_Value",
    "Freedom Value": "Freedom_Value",
    "Generosity Value": "Generosity_Value",
    "Perceptions of corruption Value": "Perceptions_of_corruption_Value"
})

import statsmodels.formula.api as smf
lm_expl_factors = smf.ols("Average_Life_Evaluation ~ GDP_per_capita_Value + Social_support_Value + Freedom_Value + Generosity_Value + Perceptions_of_corruption_Value", data = df_WHR2024_droped).fit()
print(lm_expl_factors.summary())


## Research question: Which factors have the biggest impact on happiness?
# exploring the "explains" columns: How much of the country’s life evaluation score is explained by the factor in %.
# how much does each factor contributes to Happiness

# select relevant columns
df_WHR2024.columns
explains_columns = [
    "Social support Explains",
    "GDP per capita Explains",
    "Healthy life expectancy Explains",
    "Freedom Explains",
    "Generosity Explains",
    "Perceptions of corruption Explains"
]
# calculate the means of each column (mean() in pandas ignores NA by default)
explains_avg = df_WHR2024[explains_columns].mean().sort_values(ascending=False)
print("Averaged contribution of each factor to Happiness: ", explains_avg)
print(explains_avg.to_string()) # easier output to copy from console

# Plot the average contribution
plt.figure(figsize=(10, 6))
explains_avg.plot(kind= "bar")
plt.title("Average Contribution of Factor to Happiness in %", fontsize= 14)
plt.ylim(0, 25)
plt.xticks(rotation= 45, ha= "right") # rotates x-axis labels for readability
#plt.ylabel("Average Explains-Value in %")
#plt.xlabel("Factor")
plt.tight_layout()
plt.savefig("BarContributionExplainFactorHappiness.png")
plt.show()
"""
Social support Explains -> 23.80
GDP per capita Explains -> 23.70
Freedom Explains -> 13.50
Healthy life expectancy Explains -> 9.70
Generosity Explains -> 2.14
Perceptions of corruption Explains -> 2.60
"""

##
# are there differences between Regions and the average "Explains" contribution?
regional_explains_avg = df_WHR2024.groupby("Region")[explains_columns].mean()
print(regional_explains_avg)
print(regional_explains_avg.to_string())

# plot
plt.figure(figsize=(12, 7))
regional_explains_avg.plot(kind= "bar", stacked= True, figsize= (14, 7), colormap= "tab20")
plt.title("Average Contribution of Factor to Happiness by Region (in %)", fontsize= 14)
#plt.ylabel("Average Contribution (%)")
plt.xlabel("") # no label needed
plt.xticks(rotation= 45, ha= "right") # rotates x-axis labels for readability
plt.legend(title= "Factor Explains", bbox_to_anchor= (1.05, 1), loc= "upper left")
plt.tight_layout()
plt.savefig("RegionalContributionExplainFactorHappiness.png")
plt.show()

"""
GDP and social support are strong contributors in every region, social support lower contribution in South Asia
Healthy life expectancy stands out in East Asia and North America.
Generosity and corruption perception have smaller impacts across the board but still vary by region.
Regions like South Asia and Southeast Asia show a greater role for freedom compared to the other regions.
"""
## Research question: How does GDP influence happiness?
# scatter plot of GDP vs Average Life Evaluation (Happiness Score)
plt.figure(figsize= (10, 6))
sns.scatterplot(
    data= df_WHR2024,
    x= "GDP per capita Value",
    y= "Average Life Evaluation",
    hue= "Region",
    palette= "Set2",
    alpha=0.8
)

plt.title("Relationship Between GDP and Happiness", fontsize= 14)
plt.xlabel("GDP per Capita in USD", fontsize= 12)
plt.ylabel("Happiness Score (points from 0 to 10)", fontsize= 12)
#plt.ylim(0, 10)
plt.legend(title= "Region", bbox_to_anchor= (1.05, 1), loc= "upper left")
plt.grid(True)
plt.tight_layout()
#plt.savefig("RelationshipBetweenGDPAndHappiness0to10.png")
plt.savefig("RelationshipBetweenGDPAndHappiness.png")
plt.show()

"""
in general there tends to be a pos. correlation: higher GDP higher happiness score. 
But there are some richer countries with moderate happiness scores and some very poor countries 
with moderate scoring.
clusters: 
western europe at the top right
sub-saharan in lower-left
"""
## cluster analysis
# according to the lecture notes of Data Quality and webpage:
# https://medium.com/@nomannayeem/clustering-with-confidence-a-practical-guide-to-data-clustering-in-python-15d82d8a7bfb

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

cluster_gdp = df_WHR2024[["GDP per capita Value", "Average Life Evaluation"]].copy()
cluster_gdp = cluster_gdp.dropna()  # Remove rows with missing values
# check how many rows were droped
print(f"Original rows: {len(df_WHR2024)}")
print("Original rows: ", len(df_WHR2024))
print(f"Used for clustering: {len(cluster_gdp)}")
print(f"Dropped due to NaNs: {df_WHR2024.shape[0] - cluster_gdp.shape[0]}")

# Step 1: Standardize the data for K-Means
scaler = StandardScaler()
cluster_gdp_scaled = scaler.fit_transform(cluster_gdp)
# Elbow Method ->  WCSS within-cluster sum of squares. Elbow= point where adding more clustrers no longer sign.
# reduces the WCSS.
# There's a sharp drop from k=1 to k=3, and then it starts to level off.
# The “elbow” clearly appears around k = 3 or 4.
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters= i, random_state= 42)
    kmeans.fit(cluster_gdp_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker= "o", linestyle= "--")
plt.title("Elbow Method")
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
#plt.savefig('elbow_method.png')
plt.show()

# Silhouette Analysis -> highest score at 2, more clusters, more overlap and less-defined boundaries
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(cluster_gdp_scaled)
    silhouette_avg = silhouette_score(cluster_gdp, cluster_labels)
    silhouette_scores.append(silhouette_avg)

plt.figure(figsize=(10, 6))
plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='--', color='r')
plt.title('Silhouette Analysis')
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette Score')
plt.savefig('silhouette_analysis.png')
plt.show()

##
# apply K-Means with 5 clusters based on Elbow Method and visual inspection of scatter plot. fit model
kmeans = KMeans(n_clusters= 5, random_state= 42)
cluster_labels = kmeans.fit_predict(cluster_gdp_scaled)

df_WHR2024.loc[cluster_gdp.index, "Cluster"]= cluster_labels

# Step 4: Visualize the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data= df_WHR2024,
    x="GDP per capita Value",
    y="Average Life Evaluation",
    hue="Cluster",
    palette="Set1",
    alpha=0.8
)

plt.title("K-Means Clusters: GDP vs Happiness", fontsize=14)
plt.xlabel("GDP per Capita (USD)", fontsize=12)
plt.ylabel("Average Life Evaluation (Happiness Score)", fontsize=12)
plt.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()


subset = df_WHR2024.loc[cluster_gdp.index]
plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=subset,
    x="GDP per capita Value",
    y="Average Life Evaluation",
    hue="Cluster",
    palette="Set1",
    alpha=0.8
)
for _, row in subset.iterrows():
    plt.text(row["GDP per capita Value"], row["Average Life Evaluation"], row["Country"], fontsize=7)
plt.tight_layout()
plt.show()

df_WHR2024.loc[cluster_gdp.index].groupby("Cluster")[["GDP per capita Value", "Average Life Evaluation"]].mean()
"""
Cluster          GDP per capita Value         Average Life Evaluation                            
0.0              12266.250000                 5.096250
1.0              44272.161290                 6.380097
2.0               5777.161290                 4.001871
3.0              71794.214286                 7.102786
4.0              17486.033333                 6.213367
the ranking from highest to lowest GDP corresponds to the ranking of Average Life Evaluation. But for example clusters
1.0 and 4.0 have almost the same Happiness score whereas cluster 1 has more than the double gdp than cluster 4.0
There is a positive correlation between GDP per capita and happiness — but not linear. Some mid-income countries are
happier than expected (Cluster 4). Once GDP is high enough (Cluster 3),the happiness gained from additional income diminishes.

Non-economic factors (e.g., social support, freedom, health) likely play a big role in middle-range GDP countries.
Cluster 0: Low GDP (2-20k), medium happiness (4.5-5.5)
Cluster 1: middle to high GDP (20-50k), moderate to high happiness (5.5-6.5)
CLuster 2: lowest GDP (<10k), lowest happiness (3-4.5)
Cluster 3: high GDP(uo to 100000k), high happiness (6.8-7.7)
Cluster 4: lower GDP (5-20k), moderate happiness (5.5-6.5)
"""

## comparing happiness score over years 2024-2020
# load merged dataset
df_merged = pd.read_csv("./data/clean/WHR2024_merged_happinessindex_2023_2020.csv")
df_merged.columns

# calculate change in happiness score from 2020 to 2024
df_merged_copy= df_merged.copy()
df_merged_copy["Happiness Score Change (2020-2024)"] = df_merged_copy["Average Life Evaluation"] - df_merged_copy["Ladder score 2020"]

# sort countries by the absolute value of the change in happiness (largest changes first)
sorted_by_change = df_merged_copy[["Country", "Happiness Score Change (2020-2024)"]].sort_values(by= "Happiness Score Change (2020-2024)", ascending=False)
print("Changes of Happiness Score from 2020 to 2024 by Country: ", sorted_by_change)

# Let's pick the top 20 countries with the largest changes (both positive and negative)
top_20_countries = sorted_by_change.head(20)["Country"].values
print("Top 20 Countries with biggest changes: ", top_20_countries)

# Filter the data to only include the top 10 countries with significant ladder score changes
df_top_20_countries = df_merged_copy[df_merged_copy["Country"].isin(top_20_countries)]

# Plot the trends for Life Evaluation and Ladder Scores for these countries
plt.figure(figsize=(12, 8))
# Plot average life evaluation (for 2024)
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Average Life Evaluation"], label= "Happiness Score 2024", color= "blue", marker= "o")
# Plot ladder scores 2023, 2022, 2021, 2022
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2020"], label= "Happiness Score 2020", color= "green", marker= "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2021"], label= "Happiness Score 2021", color= "orange", marker= "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2022"], label= "Happiness Score 2022", color= "red", marker= "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2023"], label= "Happiness Score 2023", color= "purple", marker= "s")

plt.xlabel("")
plt.ylabel("")
plt.title("Top 20 Countries with biggest Changes in Happiness Score (2020-2024)", fontsize= 14)
plt.xticks(rotation= 45, ha= "right")
plt.legend()
plt.tight_layout()
plt.savefig("ChangesHappiness2020-2024.png")
plt.show()