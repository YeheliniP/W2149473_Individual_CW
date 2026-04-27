import streamlit as st
import pandas as pd
import plotly.express as px

#renaming the columns for better understanding
data = pd.read_csv('asap-cleaned.csv')
renamed_columns = {
    'asap0_id': 'Country_id',
    'asap0_name': 'Country',
    'date': 'Date',
    'hs_code': 'Hotspot_code',
    'hs_name': 'Hotspot_severity',
    'comment': 'Comment',
    'g1_w_crop': 'Cropland_anomaly',
    'g1_w_range': 'Rangeland_anomaly',
    'g1_w_any': 'Total_anomaly',
    'ISO3': 'Country_code'


}

data.rename(columns=renamed_columns, inplace=True)
data.to_csv('asap-cleaned.csv', index=False)

st.title("Global Anomaly Hotspots Dashboard")
st.write("This dashboard analyzes food security hotspots around the world. ")
st.subheader("Dataset Overview")
st.write(data.head())
st.set_page_config(page_title="Global Anomaly Hotspots Dashboard", layout="wide")
data = pd.read_csv('asap-cleaned.csv')
st.sidebar.title("Filters")  #Sidebar 
country = sorted(data['Country'].unique())
selected_country = st.sidebar.multiselect("Select a country", country, default=country[:2])
filtered_data = data[data['Country'].isin(selected_country)] #Filtering the dataset
#Visualizations
#Map of hotspot locations 
fig = px.choropleth(filtered_data,
                   locations="Country_code",
                   color="Total_anomaly",
                   hover_name="Country",
                   color_continuous_scale=px.colors.sequential.Reds,
                   title="Global Anomaly Hotspots Intensity")
st.plotly_chart(fig, use_container_width=True)

#Donut Chart to show the propotion of Major hotspots vs. Regular hotspots
st.header("Hotspot severity distribution")
severity_counts = filtered_data[filtered_data['Hotspot_severity'] != 'No hotspot']
fig_donut = px.pie(severity_counts, names='Hotspot_severity', hole=0.5, title="Breakdown of Anomaly Severity",
                   color_discrete_sequence=px.colors.sequential.Reds)
st.plotly_chart(fig_donut, use_container_width=True)

#Bar chart to show the most affected countries 
st.header("Top Affected countries")
hotspot_countries = filtered_data[filtered_data['hs_code'] > 0]['Country'].value_counts().head(10).reset_index()
hotspot_countries.columns = ['Country', 'Hotspot Count']
fig_bar = px.bar(hotspot_countries, x='Country', y='Hotspot Count', title="Top 10 Most Affected Countries")
st.plotly_chart(fig_bar, use_container_width=True)

#Crop vs. rangeland comparison
st.header("Crop vs. Rangeland comparison")
impact_total = filtered_data[['Cropland_Anomaly', 'Rangeland_Anomaly']].sum().reset_index()
impact_total.columns = ['Category', 'Total Impact']
fig_impact = px.bar(impact_total, x='Category', y='Total Impact', title="Global Impact of Anomalies on Crops vs. Rangeland")
st.plotly_chart(fig_impact, use_container_width=True)

#Comment explorer
st.header("Detailed Analysis of countries")
selected_country = st.selectbox("Select a country for a detailed analysis", filtered_data['Country'].unique())
comment = filtered_data[filtered_data['Country'] == selected_country]['Comment'].iloc[0]
st.info(f"Comment for {selected_country}: {comment}")

#Monthly trend analysis 
monthly_trend = filtered_data.groupby('date').size().reset_index(name='Hotspot Count')
trend = px.line(monthly_trend, x='date', y='Hotspot Count', title="Anomaly Hotspot Trends over time")
st.plotly_chart(trend, use_container_width=True)