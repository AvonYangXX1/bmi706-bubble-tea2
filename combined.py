
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
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
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig)

# Create pie charts using Altair
def create_pie_charts(df_filtered, minyear, maxyear, subtypes):
    melted_new_df = pd.melt(df_filtered, id_vars=['WHOREGION', 'ISO_YEAR'], value_vars=subtypes, 
                            var_name='subtype', value_name='count')
    filtered_melted_df = melted_new_df[(melted_new_df['ISO_YEAR'] >= minyear) & 
                                       (melted_new_df['ISO_YEAR'] <= maxyear) & 
                                       (melted_new_df['subtype'].isin(subtypes))]
    
    for ind_subtype in subtypes:
        subtype_df = filtered_melted_df[filtered_melted_df['subtype'] == ind_subtype]
        if subtype_df['count'].sum(axis=0) == 0:
            st.write(f"Total count of positive samples is 0 for given subset (year=({minyear}, {maxyear}), subtype={ind_subtype}).")
        else:
            st.subheader(f"Pie Charts of Outbreak Regions of Influenza Subtype '{ind_subtype}' in Years ({minyear} to {maxyear})")
            cols = st.columns(2)
            with cols[0]:
                pie_1 = alt.Chart(subtype_df).mark_arc(innerRadius=50, outerRadius=90).encode(
                    theta="sum(count):Q",
                    color=alt.Color("WHOREGION:N", title="WHO Region"),
                    tooltip=[alt.Tooltip("sum(count):Q"), alt.Tooltip("WHOREGION:N"), alt.Tooltip("subtype:N")]
                ).properties(width=300, height=300, title='Total counts of positive samples')
                st.altair_chart(pie_1, use_container_width=False)
            
            with cols[1]:
                pie_2 = alt.Chart(subtype_df).mark_arc(innerRadius=50, outerRadius=90).encode(
                    theta="mean(count):Q",
                    color=alt.Color("WHOREGION:N", title="WHO Region"),
                    tooltip=[alt.Tooltip("mean(count):Q", format='.2f'), alt.Tooltip("WHOREGION:N"), alt.Tooltip("subtype:N")]
                ).properties(width=300, height=300, title='Average positive rates')
                st.altair_chart(pie_2, use_container_width=False)

# Create trend plots using Altair
def create_trend_plots(df_filtered, subtype):
    trend_df = df_filtered.groupby(['ISO_YEAR', 'ISO_WEEK'])[subtype].sum().reset_index()
    line_chart = alt.Chart(trend_df).mark_line().encode(
        x=alt.X('ISO_WEEK', title='Week'),
        y=alt.Y(subtype, title=f'Positive Samples of {subtype}'),
        color=alt.Color('ISO_YEAR:N', title='Year'),
        tooltip=['ISO_YEAR', 'ISO_WEEK', subtype]
    ).properties(width=700, height=400, title=f'Trend of Positive Samples for {subtype} Over Time')
    st.altair_chart(line_chart, use_container_width=True)

# Main function to run the app
def main():
    st.title("Influenza Surveillance Dashboard")
    
    # Load and clean data
    df = load_data()
    df_cleaned = clean_data(df)
    
    # Shared sidebar selections for year, week, and region
    year = st.sidebar.slider("Select Year", int(df_cleaned['ISO_YEAR'].min()), int(df_cleaned['ISO_YEAR'].max()))
    week = st.sidebar.slider("Select Week", 1, 52)
    selection_type = st.sidebar.selectbox("Select by", ["Country", "Hemisphere", "WHO Region"])
    
    # Adjusting the selection_value based on selection_type
    if selection_type == "Country":
        selection_value = st.sidebar.multiselect(f"Select {selection_type}", df_cleaned['COUNTRY_AREA_TERRITORY'].unique())
    elif selection_type == "Hemisphere":
        selection_value = st.sidebar.multiselect(f"Select {selection_type}", df_cleaned['HEMISPHERE'].unique())
    else:
        selection_value = st.sidebar.multiselect(f"Select {selection_type}", df_cleaned['WHOREGION'].unique())
    
    # Sidebar option for visualization type
    option = st.sidebar.selectbox("Select Visualization Type", ("Choropleth Map", "Pie Charts", "Trend Plots"))
    
    if option == "Choropleth Map":
        subtype = st.sidebar.selectbox("Select Subtype", df_cleaned.columns[7:18])
        
        # Filter and display map
        df_filtered = filter_data(df_cleaned, year, week, selection_type, selection_value, subtype)
        selected_year_week = f"{year} - Week {week}"
        create_choropleth(df_filtered, selected_year_week, subtype)
    
    elif option == "Pie Charts":
        minyear, maxyear = st.sidebar.slider("Select Year Range", 
                                             int(df_cleaned['ISO_YEAR'].min()), int(df_cleaned['ISO_YEAR'].max()), (2010, 2020))
        subtypes = st.sidebar.multiselect("Select Subtypes", df_cleaned.columns[7:18])
        
        # Filter and display pie charts
        if len(subtypes) > 0:
            create_pie_charts(df_cleaned, minyear, maxyear, subtypes)
        else:
            st.write("Please select at least one subtype for the pie charts.")
    
    elif option == "Trend Plots":
        subtype = st.sidebar.selectbox("Select Subtype", df_cleaned.columns[7:18])
        
        # Filter and display trend plot
        df_filtered = filter_data(df_cleaned, year, week, selection_type, selection_value, subtype)
        create_trend_plots(df_filtered, subtype)

if __name__ == "__main__":
    main()
