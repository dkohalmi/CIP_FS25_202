###########################################
# Happiness Streamlit App - Better Life page
#
# Author: Dora Kohalmi
#
###########################################
""" This .... """
import json
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import streamlit as st
#from sklearn.cluster import KMeans
#from sklearn.preprocessing import StandardScaler
#import scipy.cluster.hierarchy as sch
#import scipy.stats as stats
#from sklearn.cluster import DBSCAN, KMeans
#from sklearn.decomposition import PCA
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.neighbors import NearestNeighbors
#from sklearn.metrics import silhouette_score

#from datetime import datetime

####################################
# Functions used by Better Life page
####################################

# Toggle visibility of Better Life Index table:
def toggle_betterlife_table():
    """"Switch between the states 'Show'/'Hide'  of the Better Life Index table."""
    st.session_state.show_betterlife_table = not st.session_state.show_betterlife_table


def get_var_name(name, dict):
    return dict.get(name, f"'{name}' not found")
 

############# Display Better Life Table ############:
def render_betterlife_table(df):
    st.button("Show/Hide Better Life Index Data",
              key="button_show_betterlife",
              on_click=toggle_betterlife_table,
              type="secondary",
              disabled=False,
              use_container_width=False)

    # Display table if show_betterlife_table is True:
    if st.session_state.show_betterlife_table:
    
        st.dataframe(
           df,
           column_config={
                #"name": "App name",
                "Population": st.column_config.NumberColumn(
                "Population",
                help="Population of the Country",
                format="%.1f Million",
                ),
                "Visitors": st.column_config.NumberColumn(
                "Visitors", 
                help="Visitors of the Country in a year",
                format="%.1f Million",
                ),
                "Renewable_Energy": st.column_config.NumberColumn(
                "Renewable Energy",
                help="Renewable Energy",
                format="%.1f %%",
                ),
                "Housing": st.column_config.NumberColumn(
                "Housing",
                help="Average Housing Score (1-10)",
                format="%.1f",
                ),
                "Income": st.column_config.NumberColumn(
                "Income",
                help="Average Income Score (1-10)",
                format="%.1f",
                ),
                "Jobs": st.column_config.NumberColumn(
                "Jobs",
                help="Average Jobs Score (1-10)",
                format="%.1f",
                ),
                "Community": st.column_config.NumberColumn(
                "Community", 
                help="Average Community Score (1-10)",
                format="%.1f",
                ),
                "Education": st.column_config.NumberColumn(
                "Education", 
                help="Average Education Score (1-10)",
                format="%.1f",
                ),
                "Environment": st.column_config.NumberColumn(
                "Environment",
                help="Average Environment Score (1-10)",
                format="%.1f",
                ),
                "Civic_Engagement": st.column_config.NumberColumn(
                "Civic Engagement",
                help="Average Civic Engagement Score (1-10)",
                format="%.1f",
                ),
                "Health": st.column_config.NumberColumn(
                "Health",
                help="Average Health Score (1-10)",
                format="%.1f",
                ),
                "Life_Satisfaction": st.column_config.NumberColumn(
                "Life Satisfaction", 
                help="Average Life Satisfaction Score (1-10)",
                format="%.1f",
                ),
                "Safety": st.column_config.NumberColumn(
                "Safety",
                help="Average Safety Score (1-10)",
                format="%.1f",
                ),
                "Work_Life_Balance": st.column_config.NumberColumn(
                "Work Life Balance",
                help="Average Work Life Balance Score (1-10)",
                format="%.1f",
                ),
                "Rooms_per_person": st.column_config.NumberColumn(
                "Rooms per person",
                help="Average number of rooms per person",
                #format="%d.2 Million",
                ),

             },
           hide_index=True,
        )




# === Bar Plot ===
def render_bar_plot(df, var_dict):
    # Select topic from Better Life Index column names:
    selected_topic = st.selectbox("Select a topic",
                                   options=list(var_dict.keys()),
                                   index=None,
                                   placeholder="Select a Better Life topic.."
                                   )
    sort_option = st.radio("Sort countries by:", ["Value", "Alphabetical"], horizontal=True)

    if selected_topic:
        # Map display name to actual column name:
        selected_column = get_var_name(selected_topic, var_dict)

        if selected_column in df.columns:
            # Let's assume you're only showing one metric at a time (e.g., "Income")
      
            df_metric = df[["Country", selected_column]].copy()

            # Apply sorting
            if sort_option == "Value":
                df_metric = df_metric.sort_values(selected_column, ascending=False)
            else:
                df_metric = df_metric.sort_values("Country")
            
            fig = px.bar(df_metric, x="Country", y=selected_column, title=f"{selected_topic} by Country")
            st.plotly_chart(fig)

        else:
            st.warning(f"'{selected_column}' not found in dataframe.")


# === Choropleth Map ===
def render_world_map(df, var_dict):
    selected_topic = st.selectbox("Select a metric to display on the world map:", options=list(var_dict.keys()),
                                   index=0,
                                   #placeholder="Select a Better Life topic.."
                                   )
    if selected_topic:
        # Map display name to actual column name:
        selected_column = get_var_name(selected_topic, var_dict)
        if selected_column in df.columns:
   
            fig = px.choropleth(
                    df,
                    locations="Country",
                    locationmode="country names",
                    color=selected_column,
                    hover_name="Country",
                    hover_data={"Population": True},
                    color_continuous_scale="Viridis",
                    title=f"World Map: {selected_column}"
            )
            fig.update_layout(
                geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
                margin={"r":0,"t":50,"l":0,"b":0},
                coloraxis_colorbar=dict(title=selected_column)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"'{selected_column}' not found in dataframe.")


# === Scatter Plot ===
def render_scatter_vs_happiness(df, var_dict):
    selected_topic = st.selectbox("Scatterplot: Select a topic", options=list(var_dict.keys()), index=0)
    if selected_topic:
        selected_column = get_var_name(selected_topic, var_dict)
        if selected_column in df.columns:
            fig = px.scatter(df, x=selected_column, y="Happiness_Index", title=f"{selected_topic} vs Happiness")
            st.plotly_chart(fig)
        else:
            st.warning(f"'{selected_column}' not found in data.")



"""
def render_correlation_plot(df, var_dict):
    st.subheader("Correlation with Happiness Index")

    # Extract relevant columns (drop NaNs to avoid issues)
    selected_columns = ["Happiness_Index"] + list(var_dict.values())
    df_corr = df[selected_columns].dropna()

    # Compute correlation matrix
    corr_matrix = df_corr.corr()

    # Optional: sort by strongest correlation with Happiness_Index
    #corr_sorted = corr_matrix["Happiness_Index"].sort_values(ascending=False).reset_index()
    corr_sorted = corr_matrix["Happiness_Index"].sort_values(ascending=False)
    corr_sorted = corr_sorted.drop("Happiness_Index")  # optional: remove self-correlation
    corr_sorted = corr_sorted.reset_index()
    corr_sorted.columns = ["Metric", "Correlation"]




    corr_sorted = corr_sorted[corr_sorted["index"] != "Happiness_Index"]

    #fig = px.bar(corr_sorted,
    #             x="index", y="Happiness_Index",
    #             title="Correlation of Better Life Metrics with Happiness Index",
    #             labels={"index": "Metric", "Happiness_Index": "Correlation"},
    #             color="Happiness_Index",
    #             color_continuous_scale="Viridis")
    fig = px.bar(
        corr_sorted,
        x="Metric",
        y="Correlation",
        title="Correlation of Better Life Metrics with Happiness Index",
        color="Correlation",
        color_continuous_scale="Viridis"
    )  


    st.plotly_chart(fig, use_container_width=True)
"""

"""
def render_correlation_plot(df, var_dict):
    st.subheader("Correlation with Happiness Index")

    # Extract relevant columns (drop NaNs to avoid issues)
    selected_columns = ["Happiness_Index"] + list(var_dict.values())
    df_corr = df[selected_columns]      #.dropna()

    # Compute correlation matrix
    corr_matrix = df_corr.corr()

    # Sort by strongest correlation (excluding self-correlation)

    corr_sorted = corr_matrix["Happiness_Index"].sort_values(ascending=False)
    corr_sorted = corr_sorted.drop("Happiness_Index")  # Remove self
    corr_sorted = corr_sorted.reset_index()
    corr_sorted.columns = ["Metric", "Correlation"]

    # Plot
    fig = px.bar(
        corr_sorted,
        x="Metric",
        y="Correlation",
        title="Correlation of Better Life Metrics with Happiness Index",
        color="Correlation",
        color_continuous_scale="Viridis"
    )  

    st.plotly_chart(fig, use_container_width=True)

"""



def render_correlation_plot(df, var_dict):
    st.subheader("Correlation with Happiness Index")

    # 1. Extract relevant columns: Happiness Index + Better Life Index metrics
    selected_columns = list(var_dict.values())

    # 2. Drop rows with NaNs to avoid issues during correlation calculation
    df_corr = df[selected_columns].dropna()

    # 3. Compute correlation matrix
    corr_matrix = df_corr.corr()

    #st.write(type(corr_matrix["Happiness_Index"]))
    # 4. Get correlation values with Happiness_Index (excluding self-correlation)
    corr_with_happiness = corr_matrix["Happiness_Index"].drop("Happiness_Index")

    # 5. Sort correlations by absolute strength (descending)
    corr_sorted = corr_with_happiness.sort_values(ascending=False).reset_index()
    corr_sorted.columns = ["Metric", "Correlation"]

    # 6. Plot bar chart
    fig = px.bar(
        corr_sorted,
        x="Metric",
        y="Correlation",
        title="Correlation of Better Life Metrics with Happiness Index",
        color="Correlation",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)






import seaborn as sns
import matplotlib.pyplot as plt

def render_correlation_heatmap(df, var_dict):
    st.subheader("Correlation Heatmap")

    selected_columns = ["Happiness_Index"] + list(var_dict.values())
    df_corr = df[selected_columns].dropna()

    corr_matrix = df_corr.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                square=True,
                linewidths=0.5)

    st.pyplot(fig)





##################################################
# TAB 1: Better Life Index 
##################################################
def betterlife_page():

    st.markdown("""<div style="text-align:center;"><h1>Better Life Index</h1></div>""", unsafe_allow_html=True)
    st.write("Data Source: https://www.oecdbetterlifeindex.org/")
    st.write("""
Which factors have the biggest impact on happiness?
Data Analysis of the Better Life Index and the World Happiness Index

Explore the question of which factors have the biggest impact on happiness. 
             To answer this question we use two datasets: the World Happiness dataset containing the World Happiness 
             Index for 2024 for many countries and the Better Life Index dataset containing in


This Jupyter Notebook aims to analyse the OECD Better Life Index data set that contains information about
              11 aspects of life in 41 OECD countries. These 11 aspects are Housing, Income, Jobs, Community, Education,
              Environment, Civic Engagement, Health, Life Satisfaction, Safety and Work-Life Balance. For each of these
              aspects an average score between 0 and 10 for each country can be found in the data set. These indices are 
             calculated based on three or four Indicators describing important subaspects of the particular area. For example 
             the Housing index was calculated based on Housing Expenditure (defined as the ratio of housing costs on 
             households' gross adjusted disposable income), Basic Facilities (percentage of people with indoor flushing
              toilets in their home) and Rooms per Person (average number of rooms shared per person in a dwelling). The 
             data for all these Indicators are also contained in the dataset, together with the information about Population,
              number of Visitors per year and the percentage of Renewable Energy used in the country. For many Indicators 
             there are also information about the gender and social inequalities experienced in that aspect of life. This 
             information though is not consistently available for all the countries.

This Jupyter Notebook analyses the Better Life Index data set and the correlation between these indices and the World
              Happiness Index with the goal to better understand which spects of life play the most important role in the 
             experience happiness.

To do the analysis we first explore the Better Life Index data set, then wee merge it with the dataframe containing the
              World Happiness Index and analyses the correlation between the Happiness Index and the parameters of different
              aspects of life to investigate the most important factors influencing Happiness and Life satisfaction around 
             the world.

The Better Life Index dataset contains information about different aspects of life for 41 OECD countries. The data was 
             extracted from the OECD Better Life Index webpage from the Country section using the /src/scrape.betterlife.py 
             Python script. The extracted raw data can be found in /data/raw/betterlife.raw.csv file. 
             The /src/clean.betterlife.py Python script cleans the extracted raw data and save it into the
              /data/clean/betterlife.csv file.

The World Happiness Index data was downloaded as an xlsx file from the 
             [https://worldhappiness.report/ed/2025/#appendices-and-data] webpage.

""")






    # Load session state data
    df_betterlife = st.session_state.df_betterlife
    df_betterlife_merged = st.session_state.df_betterlife_merged
    betterlife_var_dict = st.session_state.betterlife_var_dict
    df_happiness = st.session_state.df_happiness  

    # Init toggle state
    if "show_betterlife_table" not in st.session_state:
        st.session_state.show_betterlife_table = False

    st.subheader("Explore Better Life Index Data")
    render_betterlife_table(df_betterlife)

    st.subheader("Explore Better Life Metrics by Country")
    render_bar_plot(df_betterlife, betterlife_var_dict)

    st.subheader("Explore Better Life Metrics on a Map")
    render_world_map(df_betterlife, betterlife_var_dict)

    st.subheader("Happiness vs Better Life Indicators")
    render_scatter_vs_happiness(df_betterlife_merged, betterlife_var_dict)


    render_correlation_heatmap(df_betterlife_merged, betterlife_var_dict)
    render_correlation_plot(df_betterlife_merged, betterlife_var_dict)



    st.subheader("Compare Any Two Better Life Metrics")

    col1, col2 = st.columns(2)
    with col1:
        x_metric = st.selectbox("Select X-axis", betterlife_var_dict, index=0)
        x_column = get_var_name(x_metric, betterlife_var_dict)
    with col2:
        y_metric = st.selectbox("Select Y-axis", betterlife_var_dict, index=1)
        y_column = get_var_name(y_metric, betterlife_var_dict)

    normalize = st.checkbox("Normalize values (Min-Max Scale)")

    df_plot = df_betterlife_merged.copy()
    df_plot["Population"] = df_plot["Population"].fillna(1)  # or df_plot["Happiness_Index"].mean()
    df_plot["Visitors"] = df_plot["Visitors"].fillna(1)  # or df_plot["Happiness_Index"].mean()
    df_plot["Renewable_Energy"] = df_plot["Renewable_Energy"].fillna(1)  # or df_plot["Happiness_Index"].mean()

    #if normalize:
     #   df_plot[betterlife_var_dict] = (df_plot[betterlife_var_dict] - df_plot[betterlife_var_dict].min()) / (df_plot[betterlife_var_dict].max() - df_plot[betterlife_var_dict].min())

    if normalize:
        for col in betterlife_var_dict.values():
            min_val = df_plot[col].min(skipna=True)
            max_val = df_plot[col].max(skipna=True)
            range_val = max_val - min_val
            if range_val != 0:
                df_plot[col] = (df_plot[col] - min_val) / range_val
            else:
                df_plot[col] = 0


    fig_scatter = px.scatter(
        df_plot, 
        x=x_metric, 
        y=y_metric, 
        color="Country",
        hover_name="Country",
        size="Population",
        title=f"{y_column} vs {x_column}"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)




    st.subheader("Compare Countries Across All Metrics")

    countries_to_compare = st.multiselect("Select up to 3 countries", df_betterlife["Country"].unique(), max_selections=3)

    if countries_to_compare:
        fig_radar = go.Figure()

        for country in countries_to_compare:
            row = df_betterlife_merged[df_betterlife_merged["Country"] == country].iloc[0]
            values = [row[var] for var in betterlife_var_dict.values()]

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=list(betterlife_var_dict.keys()),
                fill='toself',
                name=country
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title="Better Life Radar Comparison"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.info("Please select at least one country to display the radar chart.")





    # Limit selection to 3 countries max
    all_countries = df_betterlife_merged["Country"].unique().tolist()
    selected_countries = st.multiselect("Select up to 3 countries to compare", all_countries, default=["Switzerland", "Norway"], max_selections=3)

    # Normalization toggle
    #normalize = st.checkbox("Normalize metrics (0-1 scale)", value=True)


    # If countries are selected
    if selected_countries:
        # Get all metric columns
        metric_display_names = list(betterlife_var_dict.keys())
        metric_columns = [betterlife_var_dict[name] for name in metric_display_names]

        # Filter for selected countries and drop rows with missing data
        df_selected = df_betterlife_merged[df_betterlife_merged["Country"].isin(selected_countries)]
        df_selected = df_selected[["Country"] + metric_columns].dropna()


   
        ## Normalize if selected
        #df_norm = df_selected.copy()
        #if normalize:
        #    for col in metric_columns:
        #        min_val = df_norm[col].min()
        #        max_val = df_norm[col].max()
        #        df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)



        # Melt dataframe to long format
        df_melted = df_selected.melt(id_vars="Country", var_name="Metric", value_name="Value")

        # Optional: Replace column names with display names for better readability
        reverse_dict = {v: k for k, v in betterlife_var_dict.items()}
        df_melted["Metric"] = df_melted["Metric"].map(reverse_dict)

        # Plot
        fig = px.bar(
            df_melted,
            x="Metric",
            y="Value",
            color="Country",
            barmode="group",
            text_auto=".2f",  # Value labels on bars
            hover_name="Country",
            title="Better Life Index Comparison Across Selected Countries",
        )

        #fig.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels if needed
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_title="Normalized Score" if normalize else "Original Value",
            margin=dict(t=60, b=100),
            legend_title="Country",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True, key="bar_chart")



betterlife_page()
    

#st.bar_chart(df_betterlife_merged["Population"])
"""
    # Add title and header
    st.title("Renewable Energy in Switzerland")
    st.write()
    st.write("The charts show all renewable-energy power plants in Switzerland in the selected category supported by the feed-in-tariff KEV (Kostendeckende Einspeisevergütung.)")

    # Yearly production in MWh
    st.subheader("Yearly production in MWh")

    #Make columns:
    first_column,second_column=st.columns([1,1])
    with first_column:

        
    # Barplot:
    #st.subheader("The yearly production in MWh") 
    # Flow control and plotting

    fig=go.Figure(
        data=[
          go.Bar(x=df_productionsum_sources['canton'],y=df_productionsum_sources[df_productionsum_sources['energy_source_level_2']=='Bioenergy']['production'],name='Bioenergy'),
          go.Bar(x=df_productionsum_sources['canton'],y=df_productionsum_sources[df_productionsum_sources['energy_source_level_2']=='Hydro']['production'],name='Hydro'),
          go.Bar(x=df_productionsum_sources['canton'],y=df_productionsum_sources[df_productionsum_sources['energy_source_level_2']=='Solar']['production'],name='Solar'),
          go.Bar(x=df_productionsum_sources['canton'],y=df_productionsum_sources[df_productionsum_sources['energy_source_level_2']=='Wind']['production'],name='Wind'),
        ],layout={'barmode':'stack','title': {'text': "The yearly production in MWh", "font": {"size": 24}}})
    st.plotly_chart(fig)

"""

