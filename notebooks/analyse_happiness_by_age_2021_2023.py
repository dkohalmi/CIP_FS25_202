"""
Analysis and Visualization: Happiness by Age
scraped data from cleaned csv: ./data/clean/happiness_by_age_2021_2023_clean.csv

author: Ramona Kölliker
date: 05.04.2025
"""
##
import pandas as pd
import matplotlib.pyplot as plt

## load data
df_happiness_by_age = pd.read_csv("./data/clean/happiness_by_age_2021_2023_clean.csv")
"""
scraped data about happiness during different life stages. For each country there is a ranking of life evaluations for 
the whole population (All Ages) and then divided in four age groups: under 30, 30-44, 45-59, and 60+.
Countries are ranked according to their self-assessed life evaluations (answers to the Cantril ladder question in the 
Gallup World Poll), averaged over the years 2021-2023.
"""
## How does happiness compare between younger and older people?

# categorical variables "Happiest" and "Least Happy" with groups: Old, Young, LowerMiddle, UpperMiddle
df_happiness_by_age.columns
df_happiness_by_age.info()
df_happiness_by_age["Happiest"].unique()
df_happiness_by_age["Least Happy"].unique()

# count number of the four age groups Old, Young, LowerMiddle, UpperMiddle within the "Happiest" category
happiest_counts = df_happiness_by_age["Happiest"].value_counts()
print(happiest_counts)
# plot
plt.figure(figsize = (14, 8))
happiest_counts.plot(kind = "bar", color = "cornflowerblue")
plt.title("Happiest Age Groups")
plt.xlabel("")
plt.xticks(rotation = 45, ha = "right") # rotates x-axis labels for readability
plt.ylabel("in Number of Countries")
plt.grid(axis = "y")
plt.tight_layout()
# save plot
plt.savefig("visuals/age_happiest_counts_barplot.png", dpi = 300, bbox_inches = "tight")
plt.show()

# count number of the four age groups Old, Young, LowerMiddle, UpperMiddle within the "Least Happy" category
least_happy_counts = df_happiness_by_age["Least Happy"].value_counts()
print(least_happy_counts)
# plot
plt.figure(figsize=(14, 8))
least_happy_counts.plot(kind = "bar", color = "cornflowerblue")
plt.title("Least Happy Age Groups")
plt.xlabel("")
plt.xticks(rotation = 45, ha = "right")
plt.ylabel("in Number of Countries")
plt.grid(axis = "y")
plt.tight_layout()
# save plot
plt.savefig("visuals/age_least_happy_counts_barplot.png", dpi = 300, bbox_inches = "tight")
plt.show()

# Happiest Age Group: Young; Least Happy Age Group: Old

# looking at the dataset there is a big gap between the happiness score ranking from the young to the old within some countries
# explore countries with a big gap between young and old

# calculate the difference in ranking score between "The Young" and "The Old" and add a new Column to dataframe
df_happiness_by_age["Diff. Young vs Old"] = df_happiness_by_age["The Young"] - df_happiness_by_age["The Old"]
print(df_happiness_by_age["Diff. Young vs Old"])

# sort by difference to see where The Younger are happier than the Older (the more negative the value the happier the
# younger compared to the older (higher happiness score ranking of the young age group)
df_diff_young_old = df_happiness_by_age[["Country", "All Ages", "The Young", "The Old", "Diff. Young vs Old"]].copy()
df_diff_young_old_sorted_asc = df_diff_young_old.sort_values(by = "Diff. Young vs Old", ascending = True).head(20)
print("Top 20 Countries with happier young people: ", df_diff_young_old_sorted_asc)

# sort by difference to see where The Old are happier than the Young (the more positive the value the happier the
# Old compared to the Young (higher happiness score ranking of the Old age group)
df_diff_young_old_sorted_desc = df_diff_young_old.sort_values(by = "Diff. Young vs Old", ascending = False).head(20)
print("Top 20 Countries with happier old people: ", df_diff_young_old_sorted_desc)

# set a threshold at 30 Ranking score difference (with this difference we have around ten countries to select for
# happier young/happier old. countries with <= -30 diff -> happier young people;
# countries with >= 30 diff -> happier old people;
happier_young = df_diff_young_old[df_diff_young_old["Diff. Young vs Old"] <= -30].sort_values(by = "Diff. Young vs Old", ascending = True)
happier_old= df_diff_young_old[df_diff_young_old["Diff. Young vs Old"] >= 30].sort_values(by = "Diff. Young vs Old", ascending = False)

# combine both groups into one dataframe and print countries
df_extreme_diff_by_age = pd.concat([happier_young, happier_old])
print("Countries with big diff. in Happiness between Young vs. Old: ", df_extreme_diff_by_age[["Country", "Diff. Young vs Old"]])
df_extreme_diff_by_age.head()

# Plot
plt.figure(figsize = (14, 8))
# old people happier
plt.barh(happier_old["Country"], happier_old["Diff. Young vs Old"], color = "lightgreen", label = "Old people happier")
# young people happier
plt.barh(happier_young["Country"], happier_young["Diff. Young vs Old"], color = "skyblue", label = "Young people happier")
plt.axvline(0, color = "black", linewidth = 0.8)
plt.xlabel("Happiness Rank Difference: Young - Old")
plt.title("Countries with Happiness Rank Differences between Young and Old (±30 Threshold)")
plt.legend()
plt.tight_layout()
# save plot
plt.savefig("visuals/age_happiness_difference_hbarplot.png", dpi = 300, bbox_inches = "tight")
plt.show()

## save these countries/dataframe in a csv for potential further exploration/combination with other datasets
df_extreme_diff_by_age.to_csv("./data/clean/extreme_diff_happiness_by_age_2021_2023_clean.csv", index= False)