
#######################################################
# Happiness Around the World Streamlit App - Main Page
#
# Author: Dora Kohalmi
# Date: 06.04.2025
#_______________________________________________________
# This script contains the main page of the Happiness Around the World Streamlit App.
#
# It also loads, prepares and merges the data, save some dataframes into session_state 
# so that it will be available across pages.
#####################################################################################

import streamlit as st  
from helper_functions import load_all_data, prepare_all_data, create_var_dict

#################
# Page decoration
#################
st.set_page_config(
    page_title="World Happiness App",  # Page title, displayed on the window/tab bar
    page_icon="🌍",  # Emoji or favicon
    layout="wide",  # Full width
    menu_items={'About': "Explore happiness and life satisfaction around the world using data and interactive visualizations."}
)

#####################
# Main Streamlit page
#####################
def main_page():
    """Contains the main page of the Happiness Around the World Streamlit App."""

    # Title:
    st.markdown("""<div style="text-align:center;"><h1>Happiness around the World</h1></div>""", unsafe_allow_html=True)
    st.image("st/images/happiness_cut.jpg", use_container_width=True)

    st.subheader("🌍 Welcome to the Global Happiness Explorer!")
    st.write("")

    # Introduction:
    st.markdown(
        """
        Happiness is a rich and complex concept -- shaped by both how we feel and the conditions we live in.
        From economic stability and healthcare to personal freedom and community support, 
        many factors come together to define what it means to live a fulfilling life.

    This interactive app invites you to explore the **multifaceted nature of happiness** across the globe.
    Using data from the **World Happiness Index**, the **OECD Better Life Index**, **Gallup** and **Ilostat**. you'll dive 
    into both **subjective experiences** (how people report their well-being) and **objective indicators** (such as income, 
    health, and education).

    #### Discover for yourself:
    - What factors most strongly correlate with happiness?
    - How do countries differ in life satisfaction and living standards?
    - Which elements of well-being are most impactful?

    Whether you're curious about global trends, social research, or simply what makes people happy -- this tool is designed 
    to help you **explore, compare,** and **uncover insights** in a visual and engaging way.

    👉 Get started by selecting a page from the sidebar to begin your exploration.

    """)

    st.divider() 


    # Load Better Life and Happiness data from file and cache them:
    load_all_data()

    # Clean Better Life data and Happiness data, merge them and save them in session_state:
    prepare_all_data()

    # Create dictionary to map display name into column name:
    create_var_dict()


# Run the main page:
main_page()



