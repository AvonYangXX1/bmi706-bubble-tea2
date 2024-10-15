import altair as alt # type: ignore
import pandas as pd # type: ignore
import streamlit as st # type: ignore

@st.cache_data
def load_data():
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

flu_df, melted_new_df = load_data()

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
    # checkbox of "select all" for multiselection of WHO region
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