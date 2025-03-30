###########################################
# Happiness Streamlit App
#
# Author: Dora Kohalmi
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

from betterlife_page import betterlife_page
from happiness_page import happiness_page
from emotions_page import emotions_page
##################################################
# Page decoration
##################################################


st.set_page_config(page_title="World Happiness App", # page title, displayed on the window/tab bar
        		   page_icon="blue", # favicon: icon that shows on the window/tab bar (tip: you can use emojis)
                   layout="wide", # use full width of the page
                   menu_items={
                       'About': "App to explore happiness and life satisfaction around the World"
                   })



##################################################
# Load data
##################################################
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
if "df_betterlife" not in st.session_state:
    st.session_state.df_betterlife=load_csv_data(PATH_BETTERLIFE)
if "df_happiness" not in st.session_state:    
    st.session_state.df_happiness=load_xlsx_data(PATH_HAPPINESSINDEX)


##################################################
# Different pages
##################################################

tab1, tab2, tab3 = st. tabs(["Better Life Index", "World Happiness", "Emotions"])

with tab1:
    betterlife_page()

with tab2:
    happiness_page()

with tab3:
    emotions_page()        



