###################################################
# Happiness Streamlit App - Better Life Index page
#
# Author: Dora Kohalmi
# Date: 07.04.2025
#
# This file contains the Better Life Index page of the Happiness around the World Streamlit App.
################################################################################################
import streamlit as st

from helper_functions import load_all_data, prepare_all_data, create_var_dict
from utils import get_var_name, render_betterlife_table, render_bar_plot, render_world_map
from utils import render_scatter_vs_happiness, render_correlation_plot, render_correlation_heatmap
from utils import render_metric_comparison, render_country_comparison_charts


##################################################
# TAB 1: Better Life Index 
##################################################
def betterlife_page():
    """Contains the Better Life Index page of the Happiness Around the World Streamlit App."""

    # Title:
    st.markdown("""<div style="text-align:center;"><h1>Better Life Index</h1></div>""", unsafe_allow_html=True)    
    
    # Introduction:
    st.markdown("""
In this section, you can explore the fundamental question: What makes a country truly happy? Which factors have the biggest
 impact on happiness?

To answer this, we bring together two powerful datasets:
- The [World Happiness Index](https://worldhappiness.report/ed/2025/#appendices-and-data): A global survey that captures how 
                people perceive their own happiness and life satisfaction.
- The [OECD Better Life Index](https://www.oecdbetterlifeindex.org/): A comprehensive dataset covering 11 essential dimensions
                 of well-being — from Income and Education to Health, Safety, and Work-Life Balance — across 41 OECD countries.

Each of these Better Life dimensions is built on several measurable indicators. For instance, the Housing score 
considers factors like housing expenditure, access to basic facilities, and rooms per person. You'll also find 
country-specific data on population, renewable energy use, and tourism — offering a well-rounded view of societal well-being.

By analyzing how these dimensions correlate with the World Happiness Index, this page helps uncover:
- Which aspects of life are most strongly linked to happiness?
- Are there patterns across countries and cultures?
- How do objective living conditions shape subjective well-being?

""")


    # Ensure everything is loaded into session_state:
    if "df_betterlife" not in st.session_state or "df_betterlife_merged" not in st.session_state or "betterlife_var_dict" not in st.session_state:
        load_all_data()
        prepare_all_data()
        create_var_dict()

    # Load session_state data:
    df_betterlife = st.session_state.df_betterlife
    df_betterlife_merged = st.session_state.df_betterlife_merged
    betterlife_var_dict = st.session_state.betterlife_var_dict


    # Init toggle state for data table:
    if "show_betterlife_table" not in st.session_state:
        st.session_state.show_betterlife_table = False

    # Tabs at the bottom:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Data Table", "Explore a Country", "World Map", "Happiness Index",
                                                         "Compare Metrics", "Country Comparison", "Correlation Insights"])

    with tab1:
        st.subheader("Explore Better Life Index Data")
        render_betterlife_table(df_betterlife_merged, betterlife_var_dict)

    with tab2: 
        st.subheader("Explore Better Life Metrics by Country")
        render_bar_plot(df_betterlife, betterlife_var_dict)

    with tab3:
        st.subheader("Explore Better Life Metrics on a Map")
        render_world_map(df_betterlife, betterlife_var_dict)
   
    with tab4:
        col1, _, col2 = st.columns([3,1,3])
        with col1:
            st.subheader("Happiness Index vs Better Life Index")
            render_scatter_vs_happiness(df_betterlife_merged, betterlife_var_dict)
        with col2:
            st.subheader("Correlation of Better Life Indices with Happiness Index")   
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            render_correlation_plot(df_betterlife_merged, betterlife_var_dict)
           
    with tab5:
        # Scatter plot - "Compare Any Two Better Life Metrics":
        render_metric_comparison(df_betterlife_merged, betterlife_var_dict, get_var_name)  

    with tab6:
        # Radar plot, bar plot for max 3 countries - "Compare Countries Across All Metrics":
        render_country_comparison_charts(df_betterlife_merged, betterlife_var_dict)
        
    with tab7:
        # Correlation Heatmap:
        col1, col2 =st.columns([2,1])
        with col1:
            render_correlation_heatmap(df_betterlife_merged, betterlife_var_dict)


betterlife_page()
    
