# Influenza Data Visualization Dashboard


## Author: 
Siying(Avon) Yang, Shuhua Xu


## Link to Streamlit: 
https://bmi706-bubble-tea2-99vzhczzdfy2kxcmwofvch.streamlit.app/

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
Please use python (>=3.8) and install packages including:
```
plotly=5.24.1
pandas=2.2.3
streamlit=1.38.0
altair=5.4.1
```

Run streamlit locally to visualize the data:

```
streamlit run streamlit_app.py
```

## Visualization Features 
**Choropleth Maps**: Map of positive influenza cases by country or region, we have both the total number of count and the %positive sample rate
<img width="642" alt="Screenshot 2024-10-17 at 1 25 56 PM" src="https://github.com/user-attachments/assets/2b1c6092-ea9a-42ee-8ea5-b1076c7bf8b0">
<img width="573" alt="Screenshot 2024-10-17 at 1 26 05 PM" src="https://github.com/user-attachments/assets/4b91931d-1d6c-4127-9950-0aca5800817e">






**Trend Line Plot**: Line plot showing the trend of positive influenza cases over weeks and years.
<img width="653" alt="Screenshot 2024-10-17 at 1 26 19 PM" src="https://github.com/user-attachments/assets/e7772b5e-4e4d-442f-b94e-da6f2bd40f17">
The users can also use the vertical line to view at one speicfic week what is the total number of the cases sum across different countries

<img width="616" alt="Screenshot 2024-10-17 at 1 26 54 PM" src="https://github.com/user-attachments/assets/58538214-7edf-49fa-b007-8118d69179a5">


**Stacked Area Charts**: Area charts displaying the distribution of positive cases for various influenza subtypes.
<img width="638" alt="Screenshot 2024-10-17 at 1 27 11 PM" src="https://github.com/user-attachments/assets/ab0a1530-48bc-4a79-a064-f3e484bda66d">
<img width="558" alt="Screenshot 2024-10-17 at 1 27 21 PM" src="https://github.com/user-attachments/assets/9f78b02f-4da1-44b0-9d7e-367a41605476">

The interactive features are using the brush to select the certain time window 
<img width="586" alt="Screenshot 2024-10-17 at 1 28 51 PM" src="https://github.com/user-attachments/assets/71052f1c-3fb6-4c17-8f7a-3bbe0d8cba8d">



**Pie Charts**: Pie charts showing the regional distribution of positive cases and positive rates.
<img width="557" alt="Screenshot 2024-10-17 at 1 27 29 PM" src="https://github.com/user-attachments/assets/3346714d-f3f9-4978-a56a-a90f79a30faa">


## User Selection 
The dashboard provides interactive filtering options that allow users to customize the data visualization according to their specific needs. Users can:
<img width="627" alt="Screenshot 2024-10-15 at 11 14 18 AM" src="https://github.com/user-attachments/assets/fe3f5d45-b6e4-48b6-9d85-ef912a206b2a">

- Select Time Period: Use the year and week sliders to filter the data by a specific range of years and weeks. This allows for a detailed analysis of influenza trends over time.
- Choose Region Type: Users can select between filtering by country, hemisphere, or WHO region. Depending on the selection, a corresponding list of available regions will be provided to choose from. For instance, selecting "Country" enables a multi-selection option for different countries, while selecting "Hemisphere" or "WHO Region" allows filtering based on those classifications.
- Influenza Subtypes: Users can select specific influenza subtypes to visualize, such as AH1N12009, AH1, AH3, BVIC, or INF_ALL. This selection controls what data is displayed in the trend plots, choropleth maps, and pie charts. The ability to focus on individual subtypes or combinations of subtypes helps users understand the distribution and impact of specific influenza strains over time and across regions.
- Positive Rates and Counts: The dashboard allows users to switch between viewing the total count of positive samples or the positive rate (as a percentage of total samples processed), enabling insights into both absolute numbers and relative rates of infection.

