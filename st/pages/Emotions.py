###########################################
# Happiness Streamlit App - Emotions page
#
# Author: Jade Bullock
#
###########################################
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

##################################################
# TAB 3: Emotions 
##################################################
def emotions_page():
    st.markdown("<h1 style='text-align:center;'>Emotions & Happiness</h1>", unsafe_allow_html=True)

    # === Blurb introduction ===
    st.markdown("""
        ####  Explore the Emotional Side of Happiness

        In this section, we explore the emotional fabric of well-being:  
        - **What emotions do people experience most often in happier countries?**  
        - **Are positive feelings like enjoyment and respect more predictive of happiness than the absence of negative ones like stress or pain?**

        To answer these questions, we draw on data from:

        - **The [Gallup Global Emotions Survey](https://news.gallup.com/interactives/248240/global-emotions.aspx):** A worldwide measure of how people **actually feel** on a day-to-day basis — capturing responses about enjoyment, sadness, worry, stress, anger, respect, and more.
        - **The [World Happiness Index](https://worldhappiness.report/ed/2025/#appendices-and-data):** An annual index that ranks countries based on **life satisfaction**, built from both emotional and structural factors.



        **Select an emotion from the dropdown to see how it relates to happiness around the world**
        """)

    # === Load Data ===
    try:
        df = pd.read_csv("data/clean/gallup_merge.csv")
        #st.success(" Gallup Emotions data loaded successfully.")


        # List of available emotion-related features (ending in _yes)
        emotion_features = [col for col in df.columns if col.endswith("_yes")]

        # Select one feature to analyze
        selected_emotion = st.selectbox("Select an emotion to compare with Happiness Index:", sorted(emotion_features))

        # Drop rows with missing data
        plot_df = df[["Country", selected_emotion, "Happiness Index"]].dropna()

        # Compute correlation
        correlation = plot_df[selected_emotion].corr(plot_df["Happiness Index"])

        # Show scatter plot
        fig = px.scatter(
            plot_df,
            x=selected_emotion,
            y="Happiness Index",
            hover_name="Country",
            trendline="ols",
            title=f"Happiness Index vs. {selected_emotion.replace('_', ' ').title()} <br><sub>Correlation = {correlation:.2f}</sub>",
            labels={selected_emotion: selected_emotion.replace("_", " ").title()}
        )

        st.plotly_chart(fig, use_container_width=True)

        # Show raw data
        with st.expander("Show data table"):
            st.dataframe(plot_df.sort_values("Happiness Index", ascending=False))

    except FileNotFoundError:
        st.error(" File not found: data/gallup_merge.csv")
    except Exception as e:
        st.error(f"️ Error loading or processing data: {e}")

emotions_page()

