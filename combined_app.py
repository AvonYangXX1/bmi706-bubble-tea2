import altair as alt # type: ignore
import pandas as pd # type: ignore
import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

 #Load the dataset
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
def filter_data(df, year, week, selection_type, selection_value, subtype):
    df_filtered = df[(df['ISO_YEAR'] == year) & (df['ISO_WEEK'] == week)]
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
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

# Create a line plot with brush functionality (trend plot)
def create_trend_plot(df, selection_type, selection_value, subtype, years):
    df_filtered = df[df['ISO_YEAR'].isin(years)]  # Filter data by the selected years
    if selection_type == 'Country':
        df_filtered = df_filtered[df_filtered['COUNTRY_AREA_TERRITORY'].isin(selection_value)]
    elif selection_type == 'Hemisphere':
        df_filtered = df_filtered[df_filtered['HEMISPHERE'].isin(selection_value)]
    elif selection_type == 'WHO Region':
        df_filtered = df_filtered[df_filtered['WHOREGION'].isin(selection_value)]
    # Sort by week to ensure the lines are connected sequentially
    df_filtered = df_filtered.sort_values(by=['ISO_YEAR', 'ISO_WEEK'])
    # Create the line plot
    fig = go.Figure()
    for year in years:
        df_year = df_filtered[df_filtered['ISO_YEAR'] == year]
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
    df = load_data()
    df_cleaned = clean_data(df)

    st.title("Visualization of Positive Influenza Samples by Region")

    selected_years = st.slider("Select Year Range", min_value=1999, max_value=2024, value=(2018, 2021), step=1)
    selection_type = st.radio("Select Filter Type", options=["Country", "Hemisphere", "WHO Region"], index=0)
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

    selected_subtype = st.selectbox("Select Virus Subtype", options=subtypes, index=default_subtype)

    trend_fig = create_trend_plot(df_cleaned, selection_type, selected_value, selected_subtype, list(range(selected_years[0], selected_years[1]+1)))
    st.plotly_chart(trend_fig)

    selected_year = st.slider("Select a Specific Year for the Map", min_value=1999, max_value=2024, value=2021, step=1)
    selected_week = st.slider("Select Week", min_value=1, max_value=52, value=32, step=1)

    df_filtered = filter_data(df_cleaned, selected_year, selected_week, selection_type, selected_value, selected_subtype)
    choropleth_fig = create_choropleth(df_filtered, f"{selected_year}-W{selected_week:02d}", selected_subtype)

    st.plotly_chart(choropleth_fig)
    total_tested = df_filtered[selected_subtype].sum()
    st.metric(label=f"Positive Samples ({selected_subtype})", value=f"{total_tested:,}")
    st.metric(label="Total Samples Tested", value=f"{total_tested:,}")

# Run the app
if __name__ == "__main__":
    create_streamlit_app()

def load_data_2():
    #fid_df = pd.read_csv("VIW_FID.csv",low_memory=False,encoding = 'utf_8_sig')

    flu_df = pd.read_csv("VIW_FNT.csv",low_memory=False,encoding = 'utf_8_sig')

    # drop na for some columns
    flu_df = flu_df.dropna(subset=['FLUSEASON','ISOYW'],axis=0)

    # correct for the isoyw
    flu_df.loc[flu_df['ISOYW']=='MK','ISO2'] = 'MK'
    flu_df.loc[flu_df['ISOYW']=='MK','ISOYW'] = flu_df.loc[flu_df['ISOYW']=='MK','MMWRYW']
    flu_df = flu_df.astype({'ISOYW': 'float64'})

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
    new_df_flu_positive = pd.DataFrame(index=new_df_flu.index)
    for col in influenza_a_types+influenza_b_types+statistics:
        new_df_flu_positive[col] = new_df_flu[col] / new_df_flu['SPEC_PROCESSED_NB']
    
    # melt df
    melted_counts = new_df_flu.melt(id_vars=id_vars,var_name='subtype', value_name='count', 
                            value_vars=influenza_a_types+influenza_b_types+statistics)

    melted_positive_rates = new_df_flu_positive.melt(var_name='subtype', value_name='positive_rate', 
                                    value_vars=influenza_a_types+influenza_b_types+statistics)
    
    melted_new_df = melted_counts.copy()
    melted_new_df['positive_rate'] = melted_positive_rates['positive_rate']

    return flu_df, melted_new_df

# define some variables
influenza_a_types = ['AH1N12009','AH1','AH3','AH5','AH7N9','ANOTSUBTYPED','ANOTSUBTYPABLE','AOTHER_SUBTYPE']
influenza_b_types = ['BVIC_2DEL','BVIC_3DEL','BVIC_NODEL','BVIC_DELUNK','BYAM','BNOTDETERMINED']
statistics = ['SPEC_PROCESSED_NB','INF_A','INF_B','INF_ALL']
# non_influenza_respiratory_virus_types = ['ADENO','BOCA','HUMAN_CORONA','METAPNEUMO','PARAINFLUENZA','RHINO','RSV','OTHERRESPVIRUS']
id_vars = ['WHOREGION','FLUSEASON','HEMISPHERE','ITZ','COUNTRY_CODE','COUNTRY_AREA_TERRITORY','ISO_WEEKSTARTDATE', 'ISO_YEAR', 'ISO_WEEK']

flu_df, melted_new_df = load_data_2()

# year slider
minyear, maxyear = st.slider('Year',min_value=flu_df['ISO_YEAR'].min(),max_value=flu_df['ISO_YEAR'].max(),value=(2012,2013))

# multiselect of subtypes
subtype_list = influenza_a_types + influenza_b_types + ['INF_A','INF_B','INF_ALL']
subtype = st.multiselect('Subtype',subtype_list,default=['AH1N12009'])

## vis 3
country_list = flu_df['COUNTRY_AREA_TERRITORY'].dropna().unique()
region_list = flu_df['WHOREGION'].dropna().unique()
hemisphere_list = flu_df['HEMISPHERE'].dropna().unique()

# either multiselect country, region or hemisphere
choice_of_region_or_country_or_hemisphere = st.radio("Select Data By:", ("Country", "WHO Region", "Hemisphere"))

if choice_of_region_or_country_or_hemisphere == "Country":
    country = st.multiselect("Country", country_list, "United States of America")
    # Filter data by selected country
    q3_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR']>=minyear) & (melted_new_df['ISO_YEAR']<=maxyear) & (melted_new_df['COUNTRY_AREA_TERRITORY'].isin(country)) & (melted_new_df['subtype'].isin(subtype))]

elif choice_of_region_or_country_or_hemisphere == "WHO Region":
    # checkbox of "select all" for multiselection of WHO regionß
    all_options_who_region = st.checkbox("Select all options for WHO Region",value=True)
    container_who_region = st.container()
    if all_options_who_region:
        who_region = container_who_region.multiselect("WHO Region",
            region_list,region_list)
    else:
        who_region = container_who_region.multiselect("WHO Region",
            region_list)
    # Filter data by selected region
    q3_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR']>=minyear) & (melted_new_df['ISO_YEAR']<=maxyear) & (melted_new_df['WHOREGION'].isin(who_region)) & (melted_new_df['subtype'].isin(subtype))]

else:
    hemisphere = st.multiselect("Hemisphere", hemisphere_list, "NH")
    # Filter data by selected hemishphere
    q3_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR']>=minyear) & (melted_new_df['ISO_YEAR']<=maxyear) & (melted_new_df['HEMISPHERE'].isin(hemisphere)) & (melted_new_df['subtype'].isin(subtype))]

q3_filtered_melted_new_df['ISO_WEEKSTARTDATE'] = pd.to_datetime(q3_filtered_melted_new_df['ISO_WEEKSTARTDATE'])

# plot: use week start date to plot
# title
if choice_of_region_or_country_or_hemisphere == "Country":
    st.subheader(f"Stacked Area Charts of Outbreak Trends of Influenza in Countries: ({ ', '.join(country)}) and Years: ({minyear} to {maxyear})")

elif choice_of_region_or_country_or_hemisphere == "WHO Region":
    st.subheader(f"Stacked Area Charts of Outbreak Trends of Influenza in WHO Regions: ({', '.join(who_region)}) and Years: ({minyear} to {maxyear})")

else:
    st.subheader(f"Stacked Area Charts of Outbreak Trends of Influenza in Hemispheres: ({', '.join(hemisphere)}) and Years: ({minyear} to {maxyear})")

q3_count_chart = alt.Chart(q3_filtered_melted_new_df).mark_area().encode(
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
     tooltip=[alt.Tooltip('yearweek(ISO_WEEKSTARTDATE):T',title='Time '), 'sum(count):Q', 'subtype:N']
 ).properties(
     width=800,
     height=400,
     title='Total Counts of Positive Samples'
).interactive()

st.altair_chart(q3_count_chart, use_container_width=False)

q3_positive_rate_chart = alt.Chart(q3_filtered_melted_new_df).mark_area().encode(
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
     y=alt.Y('mean(positive_rate):Q', title='Average Positive Rate'),
     color='subtype:N',
     tooltip=[alt.Tooltip('yearweek(ISO_WEEKSTARTDATE):T',title='Time '), alt.Tooltip('mean(positive_rate):Q', format=".2f"), 'subtype:N']
 ).properties(
     width=800,
     height=400,
     title='Average Positive Rate of Samples'
).interactive()

st.altair_chart(q3_positive_rate_chart, use_container_width=False)


## vis 4
q4_filtered_melted_new_df = melted_new_df[(melted_new_df['ISO_YEAR']>=minyear) & (melted_new_df['ISO_YEAR']<=maxyear) & (melted_new_df['subtype'].isin(subtype))]

for ind_subtype in subtype:
    subtype_q4 = q4_filtered_melted_new_df[q4_filtered_melted_new_df['subtype']==ind_subtype]
    if subtype_q4['count'].sum(axis=0) == 0:
        st.write(f"Total count of positive samples is 0 for given subset (year = ({minyear}, {maxyear}), subtype={ind_subtype}).")

    else:
        st.subheader(f"Pie Charts of Outbreak Regions of Influenza of Subtype '{ind_subtype}' in Years ({minyear} to {maxyear})")
        cols = st.columns(2)
        col1 = cols[0]
        with col1:
            pie_1 = alt.Chart(subtype_q4).mark_arc(innerRadius=50, outerRadius=90).encode(
                theta="sum(count):Q",
                color=alt.Color("WHOREGION:N",title="WHO Region"),
                tooltip=[
                    alt.Tooltip("sum(count):Q"),
                    alt.Tooltip("WHOREGION:N", title="WHO Region"),
                    alt.Tooltip("subtype:N"),
                ]).properties(
                    width=300,
                    height=300,
                    title='Total counts of positive samples'
                )
            st.altair_chart(pie_1, use_container_width=False)
        col2 = cols[1]
        with col2:
            pie_2 = alt.Chart(subtype_q4).mark_arc(innerRadius=50, outerRadius=90).encode(
                theta="mean(positive_rate):Q",
                color=alt.Color("WHOREGION:N",title="WHO Region"),
                tooltip=[
                    alt.Tooltip("mean(positive_rate):Q",format='.2f'),
                    alt.Tooltip("WHOREGION:N", title="WHO Region"),
                    alt.Tooltip("subtype:N"),
                ]).properties(
                    width=300,
                    height=300,
                    title=f'Average positive rates of positive samples'
                )
            st.altair_chart(pie_2, use_container_width=False)
