# Influenza Data Visualization Dashboard

## Overview
This project provides an interactive dashboard for visualizing influenza data across different regions, subtypes, and time periods. It allows users to explore trends in positive samples of influenza, track the positive rates, and compare influenza subtypes across countries, hemispheres, and WHO regions. The dashboard is built using Streamlit and uses packages including Altair and Plotly for data visualization.


## Features
- Choropleth Maps: Visualize the distribution of positive influenza samples across countries and regions.
- Trend Line Plots: Analyze the weekly trends of influenza subtypes over selected years.
- Stacked Area Charts: Explore the outbreak trends of different influenza subtypes over time.
- Pie Charts: Compare the regional distribution of positive influenza samples and positive rates for different subtypes.
- Interactive Filters: Filter the data based on year, week, region type (country, hemisphere, WHO region), and influenza subtype.

## Data 
The dataset used in this dashboard is contained in a CSV file named VIW_FNT.csv. 
The download source is from : https://www.who.int/tools/flunet/flunet-summary
It includes information about influenza subtypes, regions, countries, WHO classifications, positive rates, and other relevant statistics. The data is cleaned and preprocessed using the provided Python functions in the script.


## Getting Started
Prerequisites
Make sure you have Python 3.8 or later installed. You will also need the following Python libraries:
streamlit
pandas
altair
plotly


