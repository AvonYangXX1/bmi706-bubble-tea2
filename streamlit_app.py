
"""
Author: Siying (Avon) Yang, Shuhua Xu
Email: avon_yang@hms.harvard.edu, shuhuaxu@hsph.harvard.edu
Date: 2024 Oct 15
"""


# Import Necessary Packages 
import altair as alt # type: ignore
import pandas as pd # type: ignore
import streamlit as st # type: ignore
import plotly.express as px
import plotly.graph_objects as go


# Load the dataset
@st.cache_data
def load_data():
    flu_df = pd.read_csv('VIW_FNT.csv', low_memory=False)
    return flu_df

# Data cleaning
@st.cache_data
def clean_data(flu_df, influenza_a_types, influenza_b_types, statistics, id_vars):
    # drop na for some columns
    flu_df = flu_df.dropna(subset=['FLUSEASON'],axis=0)

    # a new df
    new_df_flu = flu_df[id_vars+influenza_a_types+influenza_b_types+statistics]

    # select the data with spec_processed_nb not na or 0
    new_df_flu = new_df_flu.dropna(subset=['SPEC_PROCESSED_NB'],axis=0)
    new_df_flu = new_df_flu[new_df_flu['SPEC_PROCESSED_NB']!=0]

    # fill na
    new_df_flu[influenza_a_types+influenza_b_types] = new_df_flu[influenza_a_types+influenza_b_types].fillna(0)
    new_df_flu['INF_A'] = new_df_flu['INF_A'].fillna(new_df_flu[influenza_a_types].sum(axis=1))
    new_df_flu['INF_B'] = new_df_flu['INF_B'].fillna(new_df_flu[influenza_b_types].sum(axis=1))
    new_df_flu['INF_ALL'] = new_df_flu['INF_ALL'].fillna(new_df_flu[['INF_A','INF_B']].sum(axis=1))

    # filter some problematic rows with positive rate > 100% or with errors in calculation of INF_ALL
    for flu_type in influenza_a_types + influenza_b_types + ['INF_A', 'INF_B', 'INF_ALL']:
        condition = new_df_flu[flu_type] > new_df_flu['SPEC_PROCESSED_NB']
        new_df_flu = new_df_flu[~condition]

    for flu_type in influenza_a_types:
        condition = new_df_flu[flu_type] > new_df_flu['INF_A']
        new_df_flu = new_df_flu[~condition]

    for flu_type in influenza_b_types:
        condition = new_df_flu[flu_type] > new_df_flu['INF_B']
        new_df_flu = new_df_flu[~condition]

    condition = new_df_flu['INF_A']+new_df_flu['INF_B'] != new_df_flu['INF_ALL']
    new_df_flu = new_df_flu[~condition]

    # calculate positive rate
    new_df_flu_positive = new_df_flu.copy()
    for col in influenza_a_types+influenza_b_types+statistics:
        new_df_flu_positive[col] = new_df_flu[col] / new_df_flu['SPEC_PROCESSED_NB'] * 100

    # melt df
    melted_counts = new_df_flu.melt(id_vars=id_vars,var_name='subtype', value_name='count', 
                            value_vars=influenza_a_types+influenza_b_types+statistics)

    melted_positive_rates = new_df_flu_positive.melt(var_name='subtype', value_name='positive_rate', 
                                    value_vars=influenza_a_types+influenza_b_types+statistics)
    
    melted_new_df = melted_counts.copy()
    melted_new_df['positive_rate'] = melted_positive_rates['positive_rate']

    return new_df_flu, melted_new_df


# Filter data based on the year, week, selected regions
def filter_data(df, year, week, selection_type, selection_value):
    df_filtered = df[(df['ISO_YEAR']>=year[0]) & (df['ISO_YEAR']<=year[1]) & (df['ISO_WEEK']>=week[0]) & (df['ISO_WEEK']<=week[1])]
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
    return df_filtered


# Create a choropleth map using Plotly Express
def create_choropleth(df_filtered, selected_year_week, subtype, subtype_list):
    agg_dict = {col: 'sum' for col in subtype_list+['SPEC_PROCESSED_NB',]}
    agg_dict.update({
        'COUNTRY_AREA_TERRITORY': 'first'
    })

    # Group by 'country' and aggregate
    df_counts_group_by_country = df_filtered.groupby('COUNTRY_CODE', as_index=False).agg(agg_dict)

    fig = px.choropleth(
        df_counts_group_by_country,
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


def create_choropleth_positive_rate(df_filtered, selected_year_week, subtype, subtype_list):
    agg_dict = {col: 'sum' for col in subtype_list+['SPEC_PROCESSED_NB',]}
    agg_dict.update({
        'COUNTRY_AREA_TERRITORY': 'first'
    })

    # Group by 'country' and aggregate
    df_counts_group_by_country = df_filtered.groupby('COUNTRY_CODE', as_index=False).agg(agg_dict)
    # calculate positive rate
    for col in subtype_list:
        df_counts_group_by_country[col] = df_counts_group_by_country[col]/df_counts_group_by_country['SPEC_PROCESSED_NB'] * 100
        df_counts_group_by_country[col] = df_counts_group_by_country[col].round(2)

    fig = px.choropleth(
        df_counts_group_by_country,
        locations="COUNTRY_CODE",  # Assuming 'COUNTRY_CODE' column has ISO 3-letter codes
        color=subtype,
        hover_name="COUNTRY_AREA_TERRITORY",
        hover_data=[subtype],
        title=f"Positive Rates by {subtype} - {selected_year_week}",
        labels={subtype: 'Positive Rates (%)'},
        color_continuous_scale="Greens",
        projection="natural earth"
    )
    fig.update_geos(showcoastlines=True, showframe=False, visible=True)
    return fig


# Create a line plot with brush functionality (trend plot)
def create_trend_plot(df, selection_type, selection_value, subtype, years, weeks, subtype_list):
    # Filter data by the selected years and weeks
    df_filtered = df[(df['ISO_YEAR'].isin(years)) & (df['ISO_WEEK'].isin(weeks))]
    
    # Apply the filter based on the selection type
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
    
    # Sort by week to ensure the lines are connected sequentially
    df_filtered = df_filtered.sort_values(by=['ISO_YEAR', 'ISO_WEEK'])
    
    agg_dict = {col: 'sum' for col in subtype_list+['SPEC_PROCESSED_NB',]}

    # Group by 'date' and aggregate
    df_counts_group_by_country = df_filtered.groupby(['ISO_YEAR', 'ISO_WEEK'], as_index=False).agg(agg_dict)

    # Check if data is available after filtering
    if df_counts_group_by_country.empty:
        return go.Figure()  # Return an empty figure if no data is available
    
    # Create the line plot
    fig = go.Figure()
    for year in years:
        df_year = df_counts_group_by_country[df_counts_group_by_country['ISO_YEAR'] == year]
        fig.add_trace(go.Scatter(x=df_year['ISO_WEEK'], y=df_year[subtype], mode='lines+markers', name=str(year)))
    
    # Update layout
    fig.update_layout(
        title=f"Trend of Positive Samples for {subtype} by Week",
        xaxis_title="Week",
        yaxis_title="Number of Positive Samples",
        hovermode="x unified"
    )
    return fig



# Streamlit layout and filters
def create_streamlit_app():
    st.title("Influenza Visualizer")

    # define some variables
    influenza_a_types = ['AH1N12009', 'AH1', 'AH3', 'AH5', 'AH7N9', 'ANOTSUBTYPED', 'ANOTSUBTYPABLE', 'AOTHER_SUBTYPE']
    influenza_b_types = ['BVIC_2DEL', 'BVIC_3DEL', 'BVIC_NODEL', 'BVIC_DELUNK', 'BYAM', 'BNOTDETERMINED']
    statistics = ['SPEC_PROCESSED_NB', 'INF_A', 'INF_B', 'INF_ALL']
    id_vars = ['WHOREGION', 'FLUSEASON', 'HEMISPHERE', 'ITZ', 'COUNTRY_CODE', 'COUNTRY_AREA_TERRITORY', 'ISO_WEEKSTARTDATE', 'ISO_YEAR', 'ISO_WEEK']

    df = load_data()
    new_df_flu, melted_new_df = clean_data(df, influenza_a_types, influenza_b_types, statistics, id_vars)

    # global selections
    selected_years = st.slider("Select Year Range for All Charts", min_value=1999, max_value=2024, value=(2018, 2021), step=1, key="year_slider")
    selected_weeks = st.slider("Select Week Range for All Charts", min_value=1, max_value=52, value=(1, 52), step=1, key="week_slider")
    # q1 and 2
    selection_type = st.radio("Select Filter Type for the Line Chart and the Choropleth Map (Single Selection)", options=["Country", "Hemisphere", "WHO Region"], index=0, key="selection_radio")
    default_countries = ['United States of America', 'Brazil', 'India', 'China', 'Italy']

    if selection_type == "Country":
        options = new_df_flu['COUNTRY_AREA_TERRITORY'].unique()
        selected_value = st.multiselect("Select Country/Region for the Line Chart and the Choropleth Map (Multiselection)", options=options, default=default_countries, key="country_multiselect")
    elif selection_type == "Hemisphere":
        options = new_df_flu['HEMISPHERE'].unique()
        selected_value = st.multiselect("Select Hemisphere for the Line Chart and the Choropleth Map (Multiselection)", options=options, default=options, key="hemisphere_multiselect")
    elif selection_type == "WHO Region":
        options = new_df_flu['WHOREGION'].unique()
        selected_value = st.multiselect("Select WHO Region for the Line Chart and the Choropleth Map (Multiselection)", options=options, default=options, key="region_multiselect")
    
    
    subtype_list = influenza_a_types + influenza_b_types + ['INF_A', 'INF_B', 'INF_ALL']
    default_single_subtype = subtype_list.index('INF_B')
    selected_subtype = st.selectbox("Select Virus Subtype for the Line Chart and the Choropleth Map (Single Selection)", options=subtype_list, index=default_single_subtype, key="subtype_selectbox")
    
    st.write('Full Name of Hemisphere:  North Hemisphere (NH), South Hemisphere (SH)')

    st.write('Full Name of WHO Region: African Region (AFR),Region of the Americas (AMR),South-East Asian Region (SEAR),European Region (EUR),Eastern Mediterranean Region (EMR), Western Pacific Region (WPR)')

    ## vis 1
    st.subheader(f"Line Chart of Positive Influenza Samples in Regions:{','.join(selected_value)} in Years: ({selected_years[0]} to {selected_years[1]}) and Weeks: ({selected_weeks[0]} to {selected_weeks[1]})")
    trend_fig = create_trend_plot(new_df_flu, selection_type, selected_value, selected_subtype, list(range(selected_years[0], selected_years[1] + 1)), list(range(selected_weeks[0], selected_weeks[1] + 1)), subtype_list)
    st.plotly_chart(trend_fig, key="trend_fig")
    
    ## vis 2
    st.subheader(f"Choropleth Map of Positive Influenza Samples in Regions: {', '.join(selected_value)} in Years: ({selected_years[0]} to {selected_years[1]}) and Weeks: ({selected_weeks[0]} to {selected_weeks[1]})")
    df_filtered = filter_data(new_df_flu, selected_years, selected_weeks, selection_type, selected_value)
    choropleth_fig = create_choropleth(df_filtered, f"years: {selected_years[0]} - {selected_years[1]}, weeks:{selected_weeks[0]} - {selected_weeks[1]}", selected_subtype, subtype_list)
    st.plotly_chart(choropleth_fig, key="choropleth_fig")
    choropleth_fig_1 = create_choropleth_positive_rate(df_filtered, f"years: {selected_years[0]} - {selected_years[1]}, weeks:{selected_weeks[0]} - {selected_weeks[1]}", selected_subtype, subtype_list)
    st.plotly_chart(choropleth_fig_1, key="choropleth_fig_1")
    st.write('Positive Rates = number of positive samples for each selected country in the selected ranges of years and weeks / number of total tested samples for each selected country in the selected ranges of years and weeks')

    total_tested_positive = df_filtered[selected_subtype].sum()
    st.metric(label=f"Positive Samples ({selected_subtype})", value=f"{total_tested_positive:,}")

    total_tested = df_filtered['SPEC_PROCESSED_NB'].sum()
    st.metric(label=f"Total Tested ({selected_subtype})", value=f"{total_tested:,}")

    total_tested_positive_rate = df_filtered[selected_subtype].sum() / df_filtered['SPEC_PROCESSED_NB'].sum()
    st.metric(label=f"Positive Rate ({selected_subtype})", value=f"{total_tested_positive_rate:.2%}")

    st.write('Positive Rate = number of positive samples for all selected countries in the selected ranges of years and weeks / number of total tested samples for all selected countries in the selected ranges of years and weeks')

    ## vis 3
    
    subtypes = st.multiselect('Select Virus Subtype for the Stacked Area Chart and the Pie Chart (Multiselection)', subtype_list, default=['AH1N12009'], key="subtypes_multiselect")
    options = new_df_flu['COUNTRY_AREA_TERRITORY'].unique()


# # Determine the default index based on the presence of specific countries
#     if 'United States of America' in options:
#         default_index = options.tolist().index('United States of America')
#     elif 'NH' in options:
#         default_index = options.tolist().index('NH')
#     elif 'EUR' in options:
#         default_index = options.tolist().index('EUR')
#     else:
#         default_index = 0   

# Create the selectbox with the determined default index

    country = st.selectbox('Select Country for the Stacked Area Chart (Single Selection)',options=options, index= options.tolist().index('United States of America'), key='country_selectbox')
    q3_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR'].isin(list(range(selected_years[0], selected_years[1] + 1)))) & (melted_new_df['ISO_WEEK'].isin(list(range(selected_weeks[0], selected_weeks[1] + 1)))) & (melted_new_df['subtype'].isin(subtypes)) & (melted_new_df['COUNTRY_AREA_TERRITORY']==country)]
    q3_filtered_melted_new_df['ISO_WEEKSTARTDATE'] = pd.to_datetime(q3_filtered_melted_new_df['ISO_WEEKSTARTDATE'])
    
    st.subheader(f"Stacked Area Charts of Outbreak Trends of Influenza in {country}, Years: ({selected_years[0]} to {selected_years[1]}) and Weeks: ({selected_weeks[0]} to {selected_weeks[1]})")
    if q3_filtered_melted_new_df.empty:
      #  st.write('Only Supports Country Selection for the Stacked Chart ! ')
       # st.write('Please Go back to Top and Reselect the Country Button ')
      st.write(f'No positive samples for Subtypes: {", ".join(subtypes)}, Country: {country}, Years: ({selected_years[0]} to {selected_years[1]}) and Weeks: ({selected_weeks[0]} to {selected_weeks[1]})!')
    else:
        # add brush to link the two charts
        brush = alt.selection_interval(encodings=['x'])
        q3_count_chart = (alt.Chart().mark_area().encode(
            x=alt.X(
                'yearweek(ISO_WEEKSTARTDATE):T',
                title='Year',
                axis=alt.Axis(
                    format='%Y',
                    tickCount='year',
                    labelAngle=0,
                    labelAlign='center'
                )
            ),
            y=alt.Y('sum(count):Q', title='Total Counts'),
            color='subtype:N',
            tooltip=[alt.Tooltip('yearweek(ISO_WEEKSTARTDATE):T', title='Time '), 'sum(count):Q', 'subtype:N']
        ).properties(
            width=800,
            height=400,
            title='Total Counts of Positive Samples'
        ).add_params(brush))

        q3_positive_rate_chart = (alt.Chart().mark_area().encode(
            x=alt.X(
                'yearweek(ISO_WEEKSTARTDATE):T',
                title='Year',
                axis=alt.Axis(
                    format='%Y',
                    tickCount='year',
                    labelAngle=0,
                    labelAlign='center'
                )
            ),
            y=alt.Y('mean(positive_rate):Q', title='Positive Rate (%)'),
            color='subtype:N',
            tooltip=[alt.Tooltip('yearweek(ISO_WEEKSTARTDATE):T', title='Time '), alt.Tooltip('mean(positive_rate):Q', format=".2f"), 'subtype:N']
        ).properties(
            width=800,
            height=400,
            title='Positive Rate of Samples'
        ).transform_filter(brush))

        combined = alt.vconcat(q3_count_chart, q3_positive_rate_chart, data=q3_filtered_melted_new_df)
        st.altair_chart(combined, use_container_width=True)
        st.write('Positive Rate = mean(number of positive samples for this country in each week / number of total tested samples for this country in each week)')


    ## vis 4
    q4_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR'] >= selected_years[0]) & (melted_new_df['ISO_YEAR'] <= selected_years[1]) & (melted_new_df['ISO_WEEK'] >= selected_weeks[0]) & (melted_new_df['ISO_WEEK'] <= selected_weeks[1]) & melted_new_df['subtype'].isin(subtypes)]

    st.subheader(f"Pie Chart of Outbreak Regions of Influenza of Subtypes '{', '.join(subtypes)}' in Years ({selected_years[0]} to {selected_years[1]}) and Weeks ({selected_weeks[0]} to {selected_weeks[1]})")
    
    if q4_filtered_melted_new_df['count'].sum(axis=0) == 0:
        st.write(f"No positive samples for Subtypes '{', '.join(subtypes)}' in Years ({selected_years[0]} to {selected_years[1]}) and Weeks ({selected_weeks[0]} to {selected_weeks[1]})!")
    else:
        pie_1 = alt.Chart(q4_filtered_melted_new_df).mark_arc(innerRadius=50, outerRadius=90).encode(
            theta="sum(count):Q",
            color=alt.Color("WHOREGION:N", title="WHO Region"),
            tooltip=[
                alt.Tooltip("sum(count):Q"),
                alt.Tooltip("WHOREGION:N", title="WHO Region"),
                alt.Tooltip("subtype:N"),
            ]).properties(
                width=400,
                height=400,
                title='Total counts of positive samples'
            )
        st.altair_chart(pie_1, use_container_width=False)


# Run the app
if __name__ == "__main__":
    create_streamlit_app()