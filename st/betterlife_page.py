###########################################
# Happiness Streamlit App - Better Life page
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

# Function to toggle visibility
def toggle_betterlife_table():
    """"Switch between the states 'Show'/'Hide' the Better Life Index table."""
    st.session_state.show_betterlife_table = not st.session_state.show_betterlife_table


##################################################
# TAB 1: Better Life Index 
##################################################
def betterlife_page():


    # Set the background color:
    #st.markdown(
    #"""
    #<style>
    #    [data-testid="stAppViewContainer"] {
    #        background-color: lightblue;
    #    }
    #</style>
    #""",
    #unsafe_allow_html=True
    #)




    # Initialize session state variable 
    if "show_betterlife_table" not in st.session_state:
        st.session_state.show_betterlife_table = False

    st.write(
        f"""
        <div style="text-align:center;">
            <h1>Better Life Index</h1>
        </div>
        """,
        unsafe_allow_html=True)
    
    #st.title("Better Life Index")
    df_betterlife = st.session_state.df_betterlife  # Access the shared data
    df_happiness = st.session_state.df_happiness  # Access the shared data

    #st.write(df_betterlife.head())
   
    st.button("Show/Hide Better Life Index Data",
               key="button_show_betterlife",
               on_click=toggle_betterlife_table,
               type="secondary",
               disabled=False,
               use_container_width=False)

    
    # Display table if show_betterlife_table is True:
    if st.session_state.show_betterlife_table:
    
        st.dataframe(
           df_betterlife,
           column_config={
                #"name": "App name",
                "Population": st.column_config.NumberColumn(
                "Population",
                help="Population of the Country",
                format="%d Million",
                ),
        
        
             },
           hide_index=True,
        )

    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(df_betterlife[["Population"]])


    betterlife_variables=df_betterlife.columns
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
         index=None,
        placeholder="Select contact method...",
    )

    st.write("You selected:", option)

    # Create a box plot
    fig = px.bar(df_betterlife, x="Country", y="Population", title="Population by Country")
    st.plotly_chart(fig)

    # Create a choropleth map
    fig = px.choropleth(
        df_betterlife,
        locations="Country",  # Column with country names
        locationmode="country names",  # Match names to countries
        color="Population",  # Data to visualize
        color_continuous_scale="Viridis",  # Color scale (you can change it)
        title="World Population by Country"
    )

    #st.pyplot(fig)
    st.plotly_chart(fig)




