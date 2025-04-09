##################################################################
# Plotting and rendering functions for the Better Life Index page
#
# Author: Dora Kohalmi
# Date: 08.04.2025
##################################################################
"""
plotting_betterlife.py

This module contains plotting functions for the Better Life page of
 the World Happiness Streamlit application.

Functions:
----------
- toggle_betterlife_table: Switch between the states 'Show'/'Hide'  of the Better Life Index table
- get_var_name: Returns the column name belonging to a displayed variable name
- render_betterlife_table: Display Better Life Index table
- render_bar_plot: Render bar plot for selected Better Life Index for all countries
- render_world_map: Render World map for a selected Better Life Index
- render_scatter_vs_happiness: Render scatter plot to show Happiness vs a selected Better Life Index
- render_correlation_plot: Render a horizontal bar chart to show the correlation between Happiness Index and Better Life metrics.
- render_correlation_heatmap: Render correlation heatmap for Better Life Indices
- render_metric_comparison: Render an interactive scatter plot comparing any two Better Life Index metrics
- render_country_comparison_charts: Render a radar chart and a grouped bar plot to compare countries


Author: Dora Kohalmi
Created: 2025-04-08
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


########## Toggle visibility of Better Life Index table ###############:
def toggle_betterlife_table():
    """"Switch between the states 'Show'/'Hide'  of the Better Life Index table."""
    st.session_state.show_betterlife_table = not st.session_state.show_betterlife_table


########## Return column name ################:
def get_var_name(name, dict):
    """
    Returns the column name belonging to a displayed variable name.
    
    Parameters:
        name (str): Displayed name 
        
        dict (dict): Dictionary containing the displayed name - column name pairs
            
    Returns:
        str: the column name belonging to 'name'
    """
    return dict.get(name, f"'{name}' not found")
 

########### Display Better Life Table ############:
def render_betterlife_table(df, var_dict):
    """
    Displays the Better Life Index table.
    
    Parameters:
        df (pandas DataFrame): Better Life Index dataframe
    """
    st.button("Show/Hide Better Life Index Data",
              key="button_show_betterlife",
              on_click=toggle_betterlife_table,
              type="secondary",
              disabled=False,
              use_container_width=False)

    # Display table if show_betterlife_table is True:
    if st.session_state.show_betterlife_table:
        selected_columns = ["Country"]+list(var_dict.values())
        df = df[selected_columns]
        st.dataframe(
           df,
           column_config={
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
             },
           hide_index=True,
        )


################### Bar Plot for one topic and all countries ###############
def render_bar_plot(df, var_dict):
    """
    Renders a bar plot to show the valueof a selected Happiness Index across all OECD countries.

    Parameters:
    - df (pd.DataFrame): Merged Better Life DataFrame 
    - var_dict (dict): Dictionary mapping display names to column names.
    """
    # Select topic from Better Life Index column names:
    col1, _, col2 = st.columns([1,1,1])
    with col1:
        selected_topic = st.selectbox("Select a topic",
                                   options=list(var_dict.keys()),
                                   index=0,
                                   placeholder="Select a Better Life topic.."
                                   )
    with col2:    
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


##################### Choropleth Map ###################
def render_world_map(df, var_dict):
    """
    Renders a Chloropleth map to show a selected Better Life metrics across all OECD countries.

    Parameters:
    - df (pd.DataFrame): Merged Better Life DataFrame 
    - var_dict (dict): Dictionary mapping display names to column names.
    """
    col1, col2 = st.columns([1,2])
    with col1:    
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
                    color_continuous_scale="Blues",
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


###################  Scatter Plot ###############
def render_scatter_vs_happiness(df, var_dict):
    """
    Renders a scatter plot between Happiness Index and a selected Better Life metrics.

    Parameters:
    - df (pd.DataFrame): Merged Better Life DataFrame 
    - var_dict (dict): Dictionary mapping display names to column names.
    """
    selected_topic = st.selectbox("Scatterplot: Select a topic", options=list(var_dict.keys()), index=0)
    if selected_topic:
        selected_column = get_var_name(selected_topic, var_dict)
        if selected_column in df.columns:
            fig = px.scatter(df, x=selected_column, y="Happiness_Index", title=f"Happiness vs {selected_topic}")
            st.plotly_chart(fig)
        else:
            st.warning(f"'{selected_column}' not found in data.")


################## Correlation Plot ##################
def render_correlation_plot(df, var_dict):
    """
    Renders a horizontal bar chart to show the correlation between Happiness Index and Better Life metrics.

    Parameters:
    - df (pd.DataFrame): Merged Better Life DataFrame 
    - var_dict (dict): Dictionary mapping display names to column names.
    """
    # Extract relevant columns: Happiness Index + Better Life Index metrics
    selected_columns = list(var_dict.values())

    # Drop rows with NaNs to avoid issues during correlation calculation
    df_corr = df[selected_columns].dropna()

    # Compute correlation matrix
    corr_matrix = df_corr.corr()

    # Get correlation values with Happiness_Index (excluding self-correlation)
    corr_with_happiness = corr_matrix["Happiness_Index"].drop("Happiness_Index")

    # Sort correlations by absolute strength (descending)
    corr_sorted = corr_with_happiness.sort_values(ascending=False).reset_index()
    corr_sorted.columns = ["Metric", "Correlation"]

    # Plot bar chart
    fig = px.bar(
        corr_sorted,
        y="Metric",
        x="Correlation",
        #title="Correlation of Better Life Metrics with Happiness Index",
        color="Correlation",
        color_continuous_scale="RdBu",
        range_color=[-1, 1]
    )

    st.plotly_chart(fig, use_container_width=True)


################# Correlation Heatmap ##################
def render_correlation_heatmap(df, var_dict):
    """
    Renders a correlation heatmap of Better Life metrics, including Happiness Index.

    Parameters:
        df (pd.DataFrame): The merged dataframe containing all relevant metrics.
        var_dict (dict): Dictionary mapping display names to dataframe column names.
    """
    st.subheader("Correlation Heatmap")

    # Extract unique list: ensure Happiness_Index is first, then add the rest if not already included
    selected_columns = ["Happiness_Index"] + [col for col in var_dict.values() if col != "Happiness_Index"]

    df_corr = df[selected_columns].dropna()

    # Calculate correlation matrix:
    corr_matrix = df_corr.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix,
                annot=True,
                cmap="coolwarm",
                vmin=-1,  # Set the minimum value of the color scale
                vmax=1,   # Set the maximum value of the color scale
                fmt=".2f",
                square=True,
                linewidths=0.5)

    st.pyplot(fig)


############### Scatter Plot of two Metrics #################
def render_metric_comparison(df, var_dict, get_var_name):
    """
    Renders an interactive scatter plot comparing any two Better Life Index metrics.

    Parameters:
    - df (pd.DataFrame): Merged DataFrame containing Better Life Index metrics
    - var_dict (dict): Dictionary mapping user-friendly metric names to column names in the DataFrame.
    - get_var_name (function): Helper function to retrieve column name from a selected display name.

    Features:
    - Users can select any two metrics to compare along the X and Y axes.
    - Option to normalize the selected metrics using Min-Max scaling.
    - Scatter plot with countries as points, colored and sized by population.
    """
    
    st.subheader("Compare Any Two Better Life Metrics")

    # Metric selection:
    col1, col2, _ = st.columns([1,1,1])
    with col1:
        x_metric = st.selectbox("Select X-axis", var_dict, index=0)
        x_column = get_var_name(x_metric, var_dict)
    with col2:
        y_metric = st.selectbox("Select Y-axis", var_dict, index=1)
        y_column = get_var_name(y_metric, var_dict)

    # Normalize checkbox:
    normalize = st.checkbox("Normalize values (Min-Max Scale)")

    # Prepare data and drop rows with missing values in relevant columns:
    df_plot = df.copy()
    required_columns = ["Country", "Population", x_column, y_column]
    df_plot = df_plot.dropna(subset=required_columns)


    # Apply normalization if selected:
    if normalize:
        for col in var_dict.values():
            min_val = df_plot[col].min(skipna=True)
            max_val = df_plot[col].max(skipna=True)
            range_val = max_val - min_val
            if range_val != 0:
                df_plot[col] = (df_plot[col] - min_val) / range_val
            else:
                df_plot[col] = 0

    # Create scatter plot:
    fig_scatter = px.scatter(
        df_plot,
        x=x_column,
        y=y_column,
        color="Country",
        hover_name="Country",
        size="Population",
        title=f"{y_metric} vs {x_metric}"
    )

    # Make the plot square by setting width and height:
    fig_scatter.update_layout(
        height=700,  
        width=500,   
        
    )
    col3, col4 = st.columns([3,1])
    with col3:
        st.plotly_chart(fig_scatter, use_container_width=True)


################### Radar chart and Bar plot for comparing countries ##################
def render_country_comparison_charts(df, var_dict):
    """
    Renders two visualizations comparing countries across Better Life Index metrics:
    - A radar chart for up to 3 selected countries.
    - A grouped bar chart showing metric values per country.

    Parameters:
    - df (pd.DataFrame): Merged DataFrame with country-level metrics.
    - var_dict (dict): Dictionary mapping display names to column names.
    """
    st.subheader("Compare Countries Across All Metrics")

    all_countries = df["Country"].unique().tolist()
    selected_countries = st.multiselect("Select up to 3 countries to compare", all_countries, default=["Switzerland", "Norway"], max_selections=3)

    if not selected_countries:
        st.info("Please select at least one country to display the charts.")
        return

    metric_display_names = list(var_dict.keys())
    metric_columns = [var_dict[name] for name in metric_display_names]

    df_selected = df[df["Country"].isin(selected_countries)].copy()
    df_selected = df_selected[["Country"] + metric_columns].dropna()

  
    # --- Radar Chart ---
    fig_radar = go.Figure()
    for _, row in df_selected.iterrows():
        values = [row[col] for col in metric_columns]
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=metric_display_names,
            fill='toself',
            name=row["Country"]
        ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="Better Life Radar Comparison"
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")

    # --- Bar Chart ---
    df_melted = df_selected.melt(id_vars="Country", var_name="Metric", value_name="Value")
    reverse_dict = {v: k for k, v in var_dict.items()}
    df_melted["Metric"] = df_melted["Metric"].map(reverse_dict)

    fig_bar = px.bar(
        df_melted,
        x="Metric",
        y="Value",
        color="Country",
        barmode="group",
        text_auto=".2f",
        hover_name="Country",
        title="Better Life Index Comparison Across Selected Countries",
    )
    fig_bar.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Metric Value",
        margin=dict(t=60, b=100),
        legend_title="Country",
        height=600
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")
