"""
Analysis and Visualization: World Happiness Report 2024 (WHR2024)
scraped data from cleaned csv: ./data/clean/world_happiness_report_2024_clean.csv

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
"""
In this dataset Countries are ranked based on their citizens` responses to a life evaluation question (from the Gallup 
World Poll): imagining life as a ladder from 0 (worst) to 10 (best). Rankings are averaged over the preceded three years. 
Each country's score is explained using six explanatory variables. For each variable, three values are shown -> 
Rank: The country's rank on that factor, Value: The current value of the factor, Explains: How much that factor 
contributes to the averaged life evaluation (here also referred to as Happiness Score) 
"""

## exploring df_WHR2024
# df_WHR2024 plot distributions of all variables to get a first impression
df_WHR2024.info()
for column in df_WHR2024.columns[:20]:
    plt.figure(figsize= (10, 6))
    sns.histplot(df_WHR2024[column], kde= True)
    plt.title(f"Distribution of {column}")
    plt.show()

## scatter plots
# scatter plots of the "value" columns, we have actually six explanatory factors but for "Healthy life expectancy" we
# only have a "explains" value
df_WHR2024.columns
key_variables = [
    "Social support Value",
    "GDP per capita Value",
    "Freedom Value",
    "Generosity Value",
    "Perceptions of corruption Value"
]

# create a 3x2 grid
fig, axes = plt.subplots(nrows = 3, ncols = 2, figsize = (14, 8))
axes = axes.flatten()

for i, var in enumerate(key_variables):
    sns.scatterplot(
        data = df_WHR2024,
        x = var,
        y = "Average Life Evaluation",
        ax = axes[i],
        edgecolor = "w"
    )
    axes[i].set_title(f"Happiness Score vs. {var}", fontsize = 14)
    axes[i].set_xlabel("") # no label needed
    axes[i].set_ylabel("") # no label needed

# hide the empty subplot
if len(axes) > len(key_variables):
    axes[-1].axis("off")

plt.tight_layout() # layout adjustment
# save plot
plt.savefig("visuals/WHR2024_scatter_plots.png", dpi = 300, bbox_inches = "tight")
plt.show()

## box plots for Happiness Score by "Region"
# sns.boxplot(x= "Region", y= "Average Life Evaluation", data= df_WHR2024) # bad readability
# boxplot horizontally for readability of "Regions"
sns.boxplot(x = "Average Life Evaluation", y = "Region", color = "skyblue", data = df_WHR2024, orient = "h")
plt.ylabel("") # not needed, we have the region names
plt.xlabel("Happiness Score")
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_happiness_region_boxplots.png", dpi = 300, bbox_inches = "tight")
plt.show() # two outliers, in the lower bound a global outlier and within region "East Asia" a outlier in upper bound

# check for outliers and get Country for the outlier points
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
we have outliers in two regions: South Asia and East Asia. The outlier in South Asia is a global outlier over all Regions.
The outlier in East Asia is just within its region an outlier.
Outliers in South Asia region:
       Country      Region  Average Life Evaluation
0  Afghanistan  South Asia                    1.364

Outliers in East Asia region:
                      Country     Region  Average Life Evaluation
143  Taiwan Province of China  East Asia                    6.669

Regarding outliers we need to keep in mind that we don`t have data for 17 countries. They are listed in the WHR2024 but 
no data is available. The 17 Countries: Angola, Belarus, Bhutan, Burundi, Central African Republic, Cuba, Djibouti, 
Guyana, Haiti, Maldives, Qatar, Rwanda, South Sudan, Sudan, Suriname, Syria, Turkmenistan. Some of these countries are 
currently facing severe political and social unrest or wars which make data gathering impossible. 
Other reasons for not providing any data could be governmental restrictions or lack of infrastructure. All possible 
reasons for low happiness scores which could potentially lead to more outliers.
"""

## Which factors have the biggest impact on happiness?
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

# correlation matrix of the value columns
corr_matrix_val = df_WHR2024[correlation_columns_val].corr()
print("The correlation Matrix for values of the explanatory factors: ", corr_matrix_val)
print(corr_matrix_val.to_string()) # to get an output which is usable for report

# plot correlation heatmap
plt.figure(figsize = (14, 8))
sns.heatmap(corr_matrix_val, annot = True, cmap = "coolwarm", fmt= ".2f") # round it to two digits
plt.title("Correlation Heatmap: Explanatory Factors vs. Happiness Score", fontsize = 14)
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_correlation_heatmap.png", dpi = 300, bbox_inches = "tight")
plt.show()

"""
Social support Value -> 0.78 Very strong pos. correlation — countries where people have strong social support tend to be happier
GDP per capita Value -> 0.74 Very strong pos. correlation — wealthier nations tend to be happier
Freedom Value -> 0.56 Moderate to strong pos. correlation — more personal freedom tend to lead to more happiness
Generosity Value -> 0.33 weakest pos. correlation — generous countries do tend to be happier
Perceptions of corruption -> -0.41 negative correlation — more corruption tend to lead to less happiness
"""

## linear regression plots to visualize the correlation
key_variables = {
    "Social support Value": "Social Support in %",
    "GDP per capita Value": "GDP per capita in USD",
    "Freedom Value": "Freedom in %",
    "Generosity Value": "Generosity in %",
    "Perceptions of corruption Value": "Perceptions of corruption in %"
}

# create a 2x3 grid
fig, axes = plt.subplots(nrows = 3, ncols = 2, figsize = (18, 12))
axes = axes.flatten()

for i, (var, label) in enumerate(key_variables.items()):
    sns.regplot(
        data = df_WHR2024,
        x = var,
        y = "Average Life Evaluation",
        ax = axes[i],
        scatter_kws = {"alpha": 0.6},
        line_kws = {"color": "red"}
    )
    axes[i].set_title(f"Happiness Score vs {label}", fontsize = 14)
    axes[i].set_xlabel("")
    axes[i].set_ylabel("Happiness Score (0–10)", fontsize = 11)
    axes[i].set_ylim(0, 10)

# hide the empty subplot
if len(axes) > len(key_variables):
    axes[-1].axis("off")

plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_linreg_plots.png", dpi=300, bbox_inches = "tight")
plt.show()

## linear model fit
# fit a linear model, predicting Happiness based on the explanatory factors
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

# drop NA and rename columns to have no empty spaces. (lm.model did not work with backticks)
df_WHR2024_droped = df_WHR2024.copy()
df_WHR2024_droped = df_WHR2024_droped.dropna(subset = [
    "Average Life Evaluation",
    "GDP per capita Value",
    "Social support Value",
    "Freedom Value",
    "Generosity Value",
    "Perceptions of corruption Value"
])
print(df_WHR2024_droped.columns)

df_WHR2024_droped = df_WHR2024_droped.rename(columns = {
    "Average Life Evaluation": "Average_Life_Evaluation",
    "GDP per capita Value": "GDP_per_capita_Value",
    "Social support Value": "Social_support_Value",
    "Freedom Value": "Freedom_Value",
    "Generosity Value": "Generosity_Value",
    "Perceptions of corruption Value": "Perceptions_of_corruption_Value"
})

lm_expl_factors = smf.ols("Average_Life_Evaluation ~ GDP_per_capita_Value + Social_support_Value + Freedom_Value + Generosity_Value + Perceptions_of_corruption_Value", data = df_WHR2024_droped).fit()
print(lm_expl_factors.summary())

"""sign. pos. impact on Happiness have GDP, Social support and Freedom. Generosity and Perceptions of corruption are
not statistically significant.
R² = 0.783 -> Model explains 78.3% of the variation in happiness scores. 
F-statistic = 85.01, p < 0.001 -> The model as a whole is significant.
Condition number is large (3.71e+05) -> Potential multicollinearity 
"""

# check VIF
# select numerical variables
X = df_WHR2024_droped[[
    "GDP_per_capita_Value",
    "Social_support_Value",
    "Freedom_Value",
    "Generosity_Value",
    "Perceptions_of_corruption_Value"
]]

# Add constant term for intercept
X_const = add_constant(X)

# calculate VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = X_const.columns
vif_data["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]

print(vif_data)
# no high multicollinearity

## How much of the country’s Happiness score is explained by the factor
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
explains_avg = df_WHR2024[explains_columns].mean().sort_values(ascending = False)
print("Averaged contribution of each factor to Happiness: ", explains_avg)
print(explains_avg.to_string()) # easier output to copy from console, put into report

# plot the average contribution
plt.figure(figsize = (14, 8))
explains_avg.plot(kind = "bar")
plt.title("Average Contribution of Factors to Happiness in %", fontsize = 14)
plt.ylim(0, 25) # adjust axis
plt.xticks(rotation = 45, ha = "right") # rotates x-axis labels for readability
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_barplot_contribution_happiness.png", dpi = 300, bbox_inches = "tight")
plt.show()
"""
Social support Explains -> 23.80
GDP per capita Explains -> 23.70
Freedom Explains -> 13.50
Healthy life expectancy Explains -> 9.70
Generosity Explains -> 2.14
Perceptions of corruption Explains -> 2.60
Almost 50% of Happiness is explained by two factors: Social support and GDP.
"""

# Which factors have the biggest impact on happiness by Region?
# are there differences between Regions and the average "Explains" contribution?
regional_explains_avg = df_WHR2024.groupby("Region")[explains_columns].mean()
print(regional_explains_avg)
print(regional_explains_avg.to_string())

# plot stacked barplot
plt.figure(figsize = (12, 7))
regional_explains_avg.plot(kind = "bar", stacked = True, figsize = (14, 7), colormap = "tab20")
plt.title("Average Contribution of Factor to Happiness by Region (in %)", fontsize = 14)
plt.xlabel("") # no label needed
plt.xticks(rotation = 45, ha = "right") # rotates x-axis labels for readability
plt.legend(title = "Factor Explains", bbox_to_anchor = (1.05, 1), loc = "upper left")
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_stacked_barplot_contribution.png", dpi = 300, bbox_inches = "tight")
plt.show()

# Upon visual examination of the plot, it appears that there are differences between the regions.
# Are these differences statistically significant?

# Anova to check if differences between Regions are sign.
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

print(df_WHR2024[explains_columns].isna().sum()) # the 17 missing countries can cause problems with ANOVA
# drop NA
df_explain_fact= df_WHR2024.copy()
df_explain_fact = df_WHR2024.dropna(subset = explains_columns)

# rename columns because of space-/backtick problem with column names
df_explain_fact = df_explain_fact.rename(columns = {
    "Social support Explains": "Social_support_Explains",
    "GDP per capita Explains": "GDP_per_capita_Explains",
    "Healthy life expectancy Explains": "Healthy_life_expectancy_Explains",
    "Freedom Explains": "Freedom_Explains",
    "Generosity Explains": "Generosity_Explains",
    "Perceptions of corruption Explains": "Perceptions_of_corruption_Explains"
})

factors = ["Social_support_Explains","GDP_per_capita_Explains","Healthy_life_expectancy_Explains","Freedom_Explains",
    "Generosity_Explains","Perceptions_of_corruption_Explains"]
for factor in factors:
    print(f"\nANOVA for {factor}: ")
    model = ols(f"{factor} ~ C(Region)", data = df_explain_fact).fit()
    anova_table = sm.stats.anova_lm(model, typ = 2)
    print(anova_table)

# ANOVA: there are sign. diff. between regions and their contributions of factors to happiness
    # Post-hoc analysis: Tukey HSD. Do pairwise comparison to see if/which regions differ in which factor
    tukey = pairwise_tukeyhsd(df_explain_fact[factor], df_explain_fact["Region"])
    print(f"Tukey HSD Results for {factor}:")
    print(tukey.summary())

"""
GDP and social support are strong contributors in every region. Social support strongest in: Central and Eastern Europe,
Commonwealth of Independent States and Middle East and North Africa. Weakest contribution in South Asia.
For GDP: strongest contribution in South Asia, East Asia and Middle East and North Africa.
Healthy life expectancy stands out in East Asia and Western Europe. 

Post-hoc TukeyS HSD reveals that there are sign. differences between regions for the contribution to happiness for the 
following factors: Social support, GDP per capita, Healthy life expectancy, Generosity and Perceptions of corruption.
There is no difference between the regions for the factor freedom.

                                           Social support Explains  GDP per capita Explains  Healthy life expectancy Explains  Freedom Explains  Generosity Explains  Perceptions of corruption Explains
Region                                                                                                                                                                                                  
Central and Eastern Europe                               25.811765                25.205882                          9.982353         12.388235             1.523529                            1.423529
Commonwealth of Independent States                       26.200000                23.850000                         10.540000         13.320000             1.920000                            2.550000
East Asia                                                24.816667                26.900000                         13.333333         11.783333             1.550000                            3.150000
Latin America and the Caribbean                          23.642857                20.461905                          8.600000         13.519048             1.247619                            1.595238
Middle East and North Africa                             25.644444                26.450000                         10.755556         12.116667             1.727778                            2.411111
North America, Australia, and New Zealand                24.100000                25.700000                         11.250000         11.575000             2.450000                            4.350000
South Asia                                               16.550000                28.983333                         11.000000         14.683333             3.416667                            3.266667
Southeast Asia                                           23.955556                23.377778                          9.533333         16.188889             3.322222                            2.711111
Sub-Saharan Africa                                       22.266667                20.275000                          6.872222         15.058333             2.841667                            2.647222
Western Europe                                           23.870000                26.300000                         12.305000         12.220000             1.985000                            4.035000
"""
## How does GDP influence happiness?
# scatter plot of GDP vs Happiness Score
plt.figure(figsize= (14, 8))
sns.scatterplot(
    data = df_WHR2024,
    x = "GDP per capita Value",
    y = "Average Life Evaluation",
    hue = "Region",
    palette = "Set2",
    alpha = 0.8
)

plt.title("Relationship Between GDP and Happiness", fontsize = 14)
plt.xlabel("GDP per Capita in USD", fontsize = 12)
plt.ylabel("Happiness Score (points from 0 to 10)", fontsize = 12)
#plt.ylim(0, 10)
plt.legend(title = "Region", bbox_to_anchor= (1.05, 1), loc = "upper left")
plt.grid(True)
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_scatterplot_GDP_happiness_byRegion.png", dpi = 300, bbox_inches = "tight")
plt.show()

"""
in general there is a pos. correlation: higher GDP higher happiness score. 
But there are some richer countries with moderate happiness scores and some very poor countries with moderate scoring.
clusters: from visual inspection around 3 clusters, but not clearly seperated.
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
cluster_gdp = cluster_gdp.dropna()  # remove rows with missing values
# check how many rows were droped
print(f"Original rows: {len(df_WHR2024)}")
print("Original rows: ", len(df_WHR2024))
print(f"Used for clustering: {len(cluster_gdp)}")
print(f"Dropped due to NaNs: {df_WHR2024.shape[0] - cluster_gdp.shape[0]}")

# Standardize data for K-Means
scaler = StandardScaler()
cluster_gdp_scaled = scaler.fit_transform(cluster_gdp)

# Elbow Method ->WCSS within-cluster sum of squares. Elbow=point where adding more clusters no longer sign.# reduces the WCSS.
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, random_state = 42)
    kmeans.fit(cluster_gdp_scaled)
    wcss.append(kmeans.inertia_)

plt.figure(figsize = (10, 6))
plt.plot(range(1, 11), wcss, marker = "o", linestyle = "--")
plt.title("Cluster Analysis (Elbow Method) for Relationship Between GDP and Happiness", fontsize = 14)
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
# save plot
plt.savefig("visuals/WHR2024_clusters_GDP_Happiness_elbow_method.png", dpi = 300, bbox_inches = "tight")
plt.show()
# There's a sharp drop from k=1 to k=3, and then it starts to level off. The “elbow” clearly appears around k = 3 or 4.

# add Silhouette Analysis for comparison with Elbow-Method
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters = n_clusters, random_state = 42)
    cluster_labels = kmeans.fit_predict(cluster_gdp_scaled)
    silhouette_avg = silhouette_score(cluster_gdp, cluster_labels)
    silhouette_scores.append(silhouette_avg)

plt.figure(figsize = (14, 8))
plt.plot(range(2, 11), silhouette_scores, marker = "o", linestyle = "--", color = "r")
plt.title("Silhouette Analysis")
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette Score")
# save plot
plt.savefig("visuals/WHR2024_clusters_GDP_Happiness_silhouette.png", dpi = 300, bbox_inches = "tight")
plt.show()
# highest score at 2. The more clusters the more overlap and less-defined boundaries
"""Elbow-Method: k= 3 or 4; Silhouette: k=2
Looking at the plot: k= 3.
"""

## apply K-Means
# apply K-Means with 3 clusters based on a Trade_off of Elbow Method/Silhouette  and visual inspection of scatter plot
kmeans = KMeans(n_clusters = 3, random_state = 42)
cluster_labels = kmeans.fit_predict(cluster_gdp_scaled)

df_WHR2024.loc[cluster_gdp.index, "Cluster"] = cluster_labels

# plot clusters
plt.figure(figsize = (14, 8))
sns.scatterplot(
    data = df_WHR2024,
    x = "GDP per capita Value",
    y = "Average Life Evaluation",
    hue = "Cluster",
    palette = "Set1",
    alpha = 0.8
)

plt.title("K-Means Clusters: GDP vs Happiness", fontsize = 14)
plt.xlabel("GDP per Capita (USD)", fontsize = 12)
plt.ylabel("Happiness Score", fontsize = 12)
plt.legend(title = "Cluster", bbox_to_anchor = (1.05, 1), loc = "upper left")
plt.grid(True)
plt.tight_layout()
# save plot
plt.savefig("visuals/WHR2024_plot_3clusters_GDP_Happiness.png", dpi = 300, bbox_inches = "tight")
plt.show()

# get the country names to the points. readability is bad, not useful visualization
subset = df_WHR2024.loc[cluster_gdp.index]
plt.figure(figsize = (12, 8))
sns.scatterplot(
    data = subset,
    x = "GDP per capita Value",
    y = "Average Life Evaluation",
    hue = "Cluster",
    palette = "Set1",
    alpha = 0.8
)
for _, row in subset.iterrows():
    plt.text(row["GDP per capita Value"], row["Average Life Evaluation"], row["Country"], fontsize = 10)
plt.tight_layout()
plt.show()

df_WHR2024.loc[cluster_gdp.index].groupby("Cluster")[["GDP per capita Value", "Average Life Evaluation"]].mean()
"""          
Cluster          GDP per capita Value         Average Life Evaluation                                  
0.0              23687.803922                 6.081863
1.0              59543.645161                 6.829226
2.0               7129.865385                 4.394135

GDP matters but it is not the only thing. lower-income countries still report medium-high happiness scores.
There is a positive correlation between GDP per capita and happiness — but not linear. Some mid-income countries are
happier than expected (Cluster 1). Once GDP is high enough (Cluster 2),the happiness gained from additional income diminishes.

Non-economic factors (e.g., social support, freedom, health) likely play a big role in middle-range GDP countries.
Cluster 0: modest Income, medium-high happiness (no big difference to high GDP cluster)
Cluster 1: high GDP, highest happiness
CLuster 2: lowest GDP, lowest happiness
"""

## comparing happiness score over years 2024-2020
# load merged dataset
df_merged = pd.read_csv("./data/clean/WHR2024_merged_happinessindex_2023_2020.csv")
df_merged.columns

# calculate change in happiness score from 2020 to 2024
df_merged_copy= df_merged.copy()
df_merged_copy["Happiness Score Change (2020-2024)"] = df_merged_copy["Average Life Evaluation"] - df_merged_copy["Ladder score 2020"]

# sort countries by the absolute value of the change in happiness (largest changes first)
sorted_by_change = df_merged_copy[["Country", "Happiness Score Change (2020-2024)"]].sort_values(by = "Happiness Score Change (2020-2024)", ascending = False)
print("Changes of Happiness Score from 2020 to 2024 by Country: ", sorted_by_change)

# select top 20 countries with the largest changes
top_20_countries = sorted_by_change.head(20)["Country"].values
print("Top 20 Countries with biggest changes: ", top_20_countries)

# filter the data to only include the top 20 countries
df_top_20_countries = df_merged_copy[df_merged_copy["Country"].isin(top_20_countries)]

# plot the trends for Happiness Scores between 2020 and 2024 for these countries
plt.figure(figsize=(14, 8))
# Plot average life evaluation (for 2024)
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Average Life Evaluation"], label = "Happiness Score 2024", color = "blue", marker = "o")
# Plot ladder scores 2023, 2022, 2021, 2022
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2020"], label = "Happiness Score 2020", color = "green", marker = "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2021"], label = "Happiness Score 2021", color = "orange", marker = "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2022"], label = "Happiness Score 2022", color = "red", marker = "s")
plt.plot(df_top_20_countries["Country"], df_top_20_countries["Ladder score 2023"], label = "Happiness Score 2023", color = "purple", marker = "s")

plt.xlabel("")
plt.ylabel("")
plt.title("Top 20 Countries with biggest Changes in Happiness Score between 2020 to 2024)", fontsize = 14)
plt.xticks(rotation = 45, ha = "right")
plt.legend()
plt.tight_layout()
plt.savefig("visuals/WHR2024_trend_changes_happiness2020-2024.png", dpi = 300, bbox_inches = "tight")
plt.show()

"""
countries with biggest changes from 2020 to 2024: 'Viet Nam' 'Venezuela' 'Algeria' 'Mexico' 'China' 'Lithuania' 'Malaysia' 'India' 
'Serbia' 'Kuwait' 'Paraguay' 'Georgia' 'Poland' 'Russian Federation' 'Argentina' 'El Salvador' 'Romania' 'Libya'
'North Macedonia' 'Mozambique'. From 2020 to 2024 every country improved in their Happiness Scores
"""