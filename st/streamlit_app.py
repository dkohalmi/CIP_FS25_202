###########################################
# Happiness Streamlit App
#
# Author: Dora Kohalmi
#
###########################################

import streamlit as st  # Streamlit must be imported first

import json
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

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

from helper_functions import prepare_betterlife, prepare_happiness, merge_betterlife
from betterlife_page import betterlife_page
from happiness_page import happiness_page
from emotions_page import emotions_page



#################
# Page decoration
#################

st.set_page_config(
    page_title="World Happiness App",  # Page title, displayed on the window/tab bar
    page_icon="🌍",  # Emoji or favicon
    layout="wide",  # Full width
    menu_items={'About': "App to explore happiness and life satisfaction around the World"}
)


###########
# Load data
###########
# Relative paths to the clean data:
PATH_BETTERLIFE="data/clean/betterlife.clean.csv"
PATH_HAPPINESSINDEX="data/clean/happinessindex.xlsx"
#
# Function to load and cache data from a csv file:
@st.cache_data
def load_csv_data(path):
    """"Read csv file into a Pandas data frame and cache it. """
    df = pd.read_csv(path)
    return df

# Function to load and cache data from a xlsx file:
@st.cache_data
def load_xlsx_data(path):
    """"Read xlsx file into a Pandas data frame and cache it. """
    df = pd.read_excel(path)
    return df

# Load data from files and store them in session state for accessibility across tabs:
if "df_betterlife_raw" not in st.session_state:
    st.session_state.df_betterlife_raw=load_csv_data(PATH_BETTERLIFE)
if "df_happiness_raw" not in st.session_state:    
    st.session_state.df_happiness_raw=load_xlsx_data(PATH_HAPPINESSINDEX)

##############
# Prepare data
##############

# Prepare df_betterlife only if it hasn't been processed yet:
if "df_betterlife" not in st.session_state:
    processed_df = prepare_betterlife(st.session_state.df_betterlife_raw)
    
    # Ensure the function didn't fail before saving it:
    if processed_df is not None:
        st.session_state.df_betterlife = processed_df
    else:
        st.error("Failed to prepare Better Life dataframe.")    


# Prepare df_happiness dataframe:
if "df_happiness" not in st.session_state:    
    processed_df = prepare_happiness(st.session_state.df_happiness_raw)

    # Ensure the function didn't fail before saving it:
    if processed_df is not None:
        st.session_state.df_happiness = processed_df
    else:
        st.error("Failed to prepare Happiness dataframe.")    


# Merge df_betterlife with df_happiness:
if "df_betterlife_merged" not in st.session_state:    
    processed_df = merge_betterlife(st.session_state.df_betterlife, 
                                                  st.session_state.df_happiness)
    # Ensure the function didn't fail before saving it:
    if processed_df is not None:
        st.session_state.df_betterlife_merged = processed_df
    else:
        st.error("Failed to merge Better Life and Happiness dataframe.")    


# Create a joined dataframe

################################
# Create session_state variables
################################
betterlife_var_dict= {"Population": "Population",
                      "Visitors": "Visitors",
                      "Renewable Energy": "Renewable_Energy",
                      "Housing": "Housing",
                      "Income": "Income",
                      "Jobs": "Jobs",
                      "Community": "Community",
                      "Education": "Education",
                      "Environment": "Environment",
                      "Civic Engagement": "Civic_Engagement",
                      "Health": "Health",
                      "Life Satisfaction": "Life_Satisfaction",
                      "Safety": "Safety",
                      "Work-Life Balance": "Work_Life_Balance",
                      "Happiness Index": "Happiness_Index"}
if "betterlife_var_dict" not in st.session_state:
    st.session_state.betterlife_var_dict=betterlife_var_dict

############################
# Pages of the Streamlit App
############################

tab1, tab2, tab3 = st. tabs(["Better Life Index", "World Happiness", "Emotions"])

with tab1:
    betterlife_page()

with tab2:
    happiness_page()

with tab3:
    emotions_page()        



