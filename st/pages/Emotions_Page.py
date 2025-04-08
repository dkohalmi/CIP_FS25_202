###########################################
# Happiness Streamlit App - Emotions page
#
# Author: 
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
    st.write(
        f"""
        <div style="text-align:center;">
            <h1>Emotions</h1>
        </div>
        """,
        unsafe_allow_html=True)

emotions_page()

