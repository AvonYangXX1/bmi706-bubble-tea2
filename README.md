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
Please create aconda environment with required packages specified in `requirements.txt`:

```
conda create --name influenza_vis --file requirements.txt
```

Then, activate this environment:

```
conda activate influenza_vis
```

Then, run streamlit locally to visualize the data:

```
streamlit run streamlit_app.py
```

## Visualization Features 
**Choropleth Maps**: Map of positive influenza cases by country or region.
<img width="637" alt="Screenshot 2024-10-15 at 11 11 53 AM" src="https://github.com/user-attachments/assets/47109e80-007d-4766-bdec-9dcfb2e9f3e9">




**Trend Line Plot**: Line plot showing the trend of positive influenza cases over weeks and years.
<img width="580" alt="Screenshot 2024-10-15 at 11 13 55 AM" src="https://github.com/user-attachments/assets/654301b1-fcf2-4bac-96db-b7cd224a4832">


**Stacked Area Charts**: Area charts displaying the distribution of positive cases for various influenza subtypes.
<img width="689" alt="Screenshot 2024-10-15 at 11 14 11 AM" src="https://github.com/user-attachments/assets/6a9caa62-c214-4fb6-9f0c-a8e10c59e6f4">


**Pie Charts**: Pie charts showing the regional distribution of positive cases and positive rates.
<img width="586" alt="Screenshot 2024-10-15 at 11 14 13 AM" src="https://github.com/user-attachments/assets/edf59ced-9910-416f-81c6-b0f33147eeb1">

## User Selection 
The dashboard provides interactive filtering options that allow users to customize the data visualization according to their specific needs. Users can:
<img width="627" alt="Screenshot 2024-10-15 at 11 14 18 AM" src="https://github.com/user-attachments/assets/fe3f5d45-b6e4-48b6-9d85-ef912a206b2a">

- Select Time Period: Use the year and week sliders to filter the data by a specific range of years and weeks. This allows for a detailed analysis of influenza trends over time.
- Choose Region Type: Users can select between filtering by country, hemisphere, or WHO region. Depending on the selection, a corresponding list of available regions will be provided to choose from. For instance, selecting "Country" enables a multi-selection option for different countries, while selecting "Hemisphere" or "WHO Region" allows filtering based on those classifications.
- Influenza Subtypes: Users can select specific influenza subtypes to visualize, such as AH1N12009, AH1, AH3, BVIC, or INF_ALL. This selection controls what data is displayed in the trend plots, choropleth maps, and pie charts. The ability to focus on individual subtypes or combinations of subtypes helps users understand the distribution and impact of specific influenza strains over time and across regions.
- Positive Rates and Counts: The dashboard allows users to switch between viewing the total count of positive samples or the positive rate (as a percentage of total samples processed), enabling insights into both absolute numbers and relative rates of infection.

