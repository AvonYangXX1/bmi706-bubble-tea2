# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import streamlit as st

# # Load the dataset
# def load_data():
#     df = pd.read_csv('VIW_FNT.csv', low_memory=False)
#     return df

# # Fill missing values with zeros for numeric columns, assuming NaN means no detections
# def clean_data(df):
#     df_filled = df.fillna({
#         'AH1N12009': 0, 'AH1': 0, 'AH3': 0, 'AH5': 0, 'AH7N9': 0, 'AOTHER_SUBTYPE': 0,
#         'ANOTSUBTYPED': 0, 'ANOTSUBTYPABLE': 0, 'INF_A': 0, 'BVIC_2DEL': 0, 'BVIC_3DEL': 0,
#         'BVIC_DELUNK': 0, 'BVIC_NODEL': 0, 'BYAM': 0, 'BNOTDETERMINED': 0, 'INF_B': 0,
#         'INF_ALL': 0, 'INF_NEGATIVE': 0
#     })
#     # Remove rows where 'HEMISPHERE' is NaN
#     df_filled = df_filled.dropna(subset=['HEMISPHERE'])
#     return df_filled

# # Filter data based on the year, week, selected regions, and virus subtype
# def filter_data(df, year, week, selection_type, selection_value, subtype):
#     df_filtered = df[(df['ISO_YEAR'] == year) & (df['ISO_WEEK'] == week)]
#     if selection_type == 'Country':
#         df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
#     elif selection_type == 'Hemisphere':
#         df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
#     elif selection_type == 'WHO Region':
#         df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
#     return df_filtered

# # Create a choropleth map using Plotly Express
# def create_choropleth(df_filtered, selected_year_week, subtype):
#     fig = px.choropleth(
#         df_filtered,
#         locations="COUNTRY_CODE",  # Assuming 'COUNTRY_CODE' column has ISO 3-letter codes
#         color=subtype,
#         hover_name="COUNTRY_AREA_TERRITORY",
#         hover_data=[subtype],
#         title=f"Positive Samples by {subtype} - {selected_year_week}",
#         labels={subtype: 'Positive Samples (Count)'},
#         color_continuous_scale="Blues",
#         projection="natural earth"
#     )
#     fig.update_geos(showcoastlines=True, showframe=False, visible=True)
#     return fig

# # Create a line plot with brush functionality (trend plot)
# def create_trend_plot(df, selection_type, selection_value, subtype, years):
#     df_filtered = df[df['ISO_YEAR'].isin(years)]  # Filter data by the selected years
#     if selection_type == 'Country':
#         df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
#     elif selection_type == 'Hemisphere':
#         df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
#     elif selection_type == 'WHO Region':
#         df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
#     # Sort by week to ensure the lines are connected sequentially
#     df_filtered = df_filtered.sort_values(by=['ISO_YEAR', 'ISO_WEEK'])
#     # Create the line plot
#     fig = go.Figure()
#     for year in years:
#         df_year = df_filtered[df_filtered['ISO_YEAR'] == year]
#         fig.add_trace(go.Scatter(x=df_year['ISO_WEEK'], y=df_year[subtype], mode='lines+markers', name=str(year)))
#     # Update layout
#     fig.update_layout(
#         title=f"Trend of Positive Samples for {subtype} by Week",
#         xaxis_title="Week",
#         yaxis_title="Number of Positive Samples",
#         hovermode="x unified"
#     )
#     return fig

# # Streamlit layout and filters
# def create_streamlit_app():
#     df = load_data()
#     df_cleaned = clean_data(df)

#     st.title("Visualization of Positive Influenza Samples by Region")

#     selected_years = st.slider("Select Year Range", min_value=1999, max_value=2024, value=(2018, 2021), step=1)
#     selection_type = st.radio("Select Filter Type", options=["Country", "Hemisphere", "WHO Region"], index=0)
#     default_countries = ['United States of America', 'Brazil', 'India', 'China', 'Japan', 'Italy']

#     if selection_type == "Country":
#         options = df_cleaned['COUNTRY_AREA_TERRITORY'].unique()
#         selected_value = st.multiselect("Select Country/Region", options=options, default=default_countries)
#     elif selection_type == "Hemisphere":
#         options = df_cleaned['HEMISPHERE'].unique()
#         selected_value = st.multiselect("Select Hemisphere", options=options, default=options)
#     elif selection_type == "WHO Region":
#         options = df_cleaned['WHOREGION'].unique()
#         selected_value = st.multiselect("Select WHO Region", options=options, default=options)

#     subtypes = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'AOTHER_SUBTYPE', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 
#                 'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_DELUNK', 'BVIC_NODEL', 'BYAM', 'BNOTDETERMINED', 
#                 'INF_B', 'INF_ALL', 'INF_NEGATIVE']
#     default_subtype = subtypes.index('INF_B')

#     selected_subtype = st.selectbox("Select Virus Subtype", options=subtypes, index=default_subtype)

#     trend_fig = create_trend_plot(df_cleaned, selection_type, selected_value, selected_subtype, list(range(selected_years[0], selected_years[1]+1)))
#     st.plotly_chart(trend_fig)

#     selected_year = st.slider("Select a Specific Year for the Map", min_value=1999, max_value=2024, value=2021, step=1)
#     selected_week = st.slider("Select Week", min_value=1, max_value=52, value=32, step=1)

#     df_filtered = filter_data(df_cleaned, selected_year, selected_week, selection_type, selected_value, selected_subtype)
#     choropleth_fig = create_choropleth(df_filtered, f"{selected_year}-W{selected_week:02d}", selected_subtype)

#     st.plotly_chart(choropleth_fig)
#     total_tested = df_filtered[selected_subtype].sum()
#     st.metric(label=f"Positive Samples ({selected_subtype})", value=f"{total_tested:,}")
#     st.metric(label="Total Samples Tested", value=f"{total_tested:,}")

# # Run the app
# if __name__ == "__main__":
#     create_streamlit_app()
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import altair as alt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('VIW_FNT.csv', low_memory=False)
    return df

# Fill missing values with zeros for numeric columns, assuming NaN means no detections
def clean_data(df):
    df_filled = df.fillna({
        'AH1N12009': 0, 'AH1': 0, 'AH3': 0, 'AH5': 0, 'AH7N9': 0, 'AOTHER_SUBTYPE': 0,
        'ANOTSUBTYPED': 0, 'ANOTSUBTYPABLE': 0, 'INF_A': 0, 'BVIC_2DEL': 0, 'BVIC_3DEL': 0,
        'BVIC_DELUNK': 0, 'BVIC_NODEL': 0, 'BYAM': 0, 'BNOTDETERMINED': 0, 'INF_B': 0,
        'INF_ALL': 0, 'INF_NEGATIVE': 0
    })
    # Remove rows where 'HEMISPHERE' is NaN
    df_filled = df_filled.dropna(subset=['HEMISPHERE'])
    return df_filled

# Filter data based on the year, week, selected regions, and virus subtype
def filter_data(df, year_range, selection_type, selection_value, subtype):
    df_filtered = df[(df['ISO_YEAR'] >= year_range[0]) & (df['ISO_YEAR'] <= year_range[1])]
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
    df_filtered = df_filtered[df_filtered['subtype'].isin(subtype)]
    return df_filtered

# Create a choropleth map using Plotly Express
def create_choropleth(df_filtered, selected_year_week, subtype):
    fig = px.choropleth(
        df_filtered,
        locations="COUNTRY_CODE",  # Assuming 'COUNTRY_CODE' column has ISO 3-letter codes
        color=subtype,
        hover_name="COUNTRY_AREA_TERRITORY",
        hover_data=[subtype],
        title=f"Positive Samples by {subtype} - {selected_year_week}",
        labels={subtype: 'Positive Samples (Count)'},
        color_continuous_scale="Blues",
        projection="natural earth"
    )
    fig.update_geos(showcoastlines=True, showframe=False, visible=True)
    return fig

# Create a stacked area chart for total counts of positive samples
def create_stacked_area_chart(df_filtered):
    chart = alt.Chart(df_filtered).mark_area().encode(
        x=alt.X('yearweek(ISO_WEEKSTARTDATE):T', title='Year'),
        y=alt.Y('sum(count):Q', title='Total Counts'),
        color='subtype:N',
        tooltip=['yearweek(ISO_WEEKSTARTDATE):T', 'sum(count):Q', 'subtype:N']
    ).properties(
        width=800,
        height=400,
        title='Total Counts of Positive Samples'
    ).interactive()
    return chart

# Create a stacked area chart for average positive rates of positive samples
def create_positive_rate_chart(df_filtered):
    chart = alt.Chart(df_filtered).mark_area().encode(
        x=alt.X('yearweek(ISO_WEEKSTARTDATE):T', title='Year'),
        y=alt.Y('mean(positive_rate):Q', title='Average Positive Rate'),
        color='subtype:N',
        tooltip=['yearweek(ISO_WEEKSTARTDATE):T', 'mean(positive_rate):Q', 'subtype:N']
    ).properties(
        width=800,
        height=400,
        title='Average Positive Rate of Samples'
    ).interactive()
    return chart

# Create a pie chart for positive counts and positive rates per WHO region
def create_pie_charts(df_filtered):
    pie_1 = alt.Chart(df_filtered).mark_arc(innerRadius=50, outerRadius=90).encode(
        theta="sum(count):Q",
        color=alt.Color("WHOREGION:N", title="WHO Region"),
        tooltip=[alt.Tooltip("sum(count):Q"), alt.Tooltip("WHOREGION:N", title="WHO Region")]
    ).properties(width=300, height=300, title='Total Counts of Positive Samples')
    
    pie_2 = alt.Chart(df_filtered).mark_arc(innerRadius=50, outerRadius=90).encode(
        theta="mean(positive_rate):Q",
        color=alt.Color("WHOREGION:N", title="WHO Region"),
        tooltip=[alt.Tooltip("mean(positive_rate):Q", format='.2f'), alt.Tooltip("WHOREGION:N", title="WHO Region")]
    ).properties(width=300, height=300, title='Average Positive Rates of Positive Samples')
    
    return pie_1, pie_2

# Streamlit layout and filters
def create_streamlit_app():
    df = load_data()
    df_cleaned = clean_data(df)

    st.title("Visualization of Positive Influenza Samples by Region")

    # Common selection: year range, subtype, country/region/hemisphere
    selected_years = st.slider("Select Year Range", min_value=1999, max_value=2024, value=(2018, 2021), step=1)
    selection_type = st.radio("Select Data By:", options=["Country", "Hemisphere", "WHO Region"], index=0)
    default_countries = ['United States of America', 'Brazil', 'India', 'China', 'Japan', 'Italy']

    if selection_type == "Country":
        options = df_cleaned['COUNTRY_AREA_TERRITORY'].unique()
        selected_value = st.multiselect("Select Country/Region", options=options, default=default_countries)
    elif selection_type == "Hemisphere":
        options = df_cleaned['HEMISPHERE'].unique()
        selected_value = st.multiselect("Select Hemisphere", options=options, default=options)
    elif selection_type == "WHO Region":
        options = df_cleaned['WHOREGION'].unique()
        selected_value = st.multiselect("Select WHO Region", options=options, default=options)

    subtypes = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'AOTHER_SUBTYPE', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 
                'INF_A', 'BVIC_2DEL', 'BVIC_3DEL', 'BVIC_DELUNK', 'BVIC_NODEL', 'BYAM', 'BNOTDETERMINED', 
                'INF_B', 'INF_ALL', 'INF_NEGATIVE']
    default_subtype = subtypes.index('INF_B')

    selected_subtype = st.multiselect("Select Virus Subtype", options=subtypes, default=['AH1N12009'])

    # Filter data based on the selection
    df_filtered = filter_data(df_cleaned, selected_years, selection_type, selected_value, selected_subtype)

    # Plot 1: Stacked Area Chart - Total Counts
    st.subheader("Stacked Area Charts of Positive Influenza Cases")
    stacked_area_chart = create_stacked_area_chart(df_filtered)
    st.altair_chart(stacked_area_chart, use_container_width=True)

    # Plot 2: Stacked Area Chart - Positive Rates
    st.subheader("Stacked Area Charts of Positive Rates")
    positive_rate_chart = create_positive_rate_chart(df_filtered)
    st.altair_chart(positive_rate_chart, use_container_width=True)

    # Plot 3: Pie Charts
    st.subheader("Pie Charts of Outbreak Regions of Influenza")
    pie_1, pie_2 = create_pie_charts(df_filtered)
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(pie_1, use_container_width=False)
    with col2:
        st.altair_chart(pie_2, use_container_width=False)

    # Map section: Select specific year and week for choropleth
    selected_year = st.slider("Select a Specific Year for the Map", min_value=1999, max_value=2024, value=2021, step=1)
    selected_week = st.slider("Select Week", min_value=1, max_value=52, value=32, step=1)

    df_filtered_week = filter_data(df_cleaned, (selected_year, selected_year), selection_type, selected_value, selected_subtype)
    choropleth_fig = create_choropleth(df_filtered_week, f"{selected_year}-W{selected_week:02d}", selected_subtype)

    st.plotly_chart(choropleth_fig)
    total_tested = df_filtered[selected_subtype].sum()
    st.metric(label=f"Positive Samples ({selected_subtype})", value=f"{total_tested:,}")
    st.metric(label="Total Samples Tested", value=f"{total_tested:,}")

# Run the app
if __name__ == "__main__":
    create_streamlit_app()
