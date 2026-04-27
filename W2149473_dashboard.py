import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Global Anomaly Hotspots Dashboard")
st.write("This dashboard analyzes food security hotspots around the world. ")
asap = pd.read_csv('asap-cleaned.csv') #Loading the cleaned dataset
st.subheader("Dataset Overview")
st.write(asap.head())
st.set_page_config(page_title="Global Anomaly Hotspots Dashboard", layout="wide")
data = pd.read_csv('asap-cleaned.csv')
st.sidebar.title("Filters")  #Sidebar 
country = sorted(data['asap0_name'].unique())
selected_country = st.sidebar.multiselect("Select a country", country, default=country[:2])
filtered_data = data[data['asap0_name'].isin(selected_country)] #Filtering the dataset
#Visualizations
#Map of hotspot locations 
fig = px.choropleth(filtered_data,
                   locations="ISO3",
                   color="g1_w_any",
                   hover_name="asap0_name",
                   color_continuous_scale=px.colors.sequential.Reds,
                   title="Global Anomaly Hotspots Intensity")
st.plotly_chart(fig, use_container_width=True)

#Donut Chart to show the propotion of Major hotspots vs. Regular hotspots
st.header("Hotspot severity distribution")
severity_counts = filtered_data[filtered_data['hs_name'] != 'No hotspot']
fig_donut = px.pie(severity_counts, names='hs_name', hole=0.5, title="Breakdown of Anomaly Severity",
                   color_discrete_sequence=px.colors.sequential.Reds)
st.plotly_chart(fig_donut, use_container_width=True)

#Bar chart to show the most affected countries 
st.header("Top Affected countries")
hotspot_countries = filtered_data[filtered_data['hs_code'] > 0]['asap0_name'].value_counts().head(10).reset_index()
hotspot_countries.columns = ['Country', 'Hotspot Count']
fig_bar = px.bar(hotspot_countries, x='Country', y='Hotspot Count', title="Top 10 Most Affected Countries")
st.plotly_chart(fig_bar, use_container_width=True)

#Crop vs. rangeland comparison
st.header("Crop vs. Rangeland comparison")
impact_total = filtered_data[['g1_w_crop', 'g1_w_range']].sum().reset_index()
impact_total.columns = ['Category', 'Total Impact']
fig_impact = px.bar(impact_total, x='Category', y='Total Impact', title="Global Impact of Anomalies on Crops vs. Rangeland")
st.plotly_chart(fig_impact, use_container_width=True)

#Comment explorer
st.header("Detailed Analysis of countries")
selected_country = st.selectbox("Select a country for a detailed analysis", filtered_data['asap0_name'].unique())
comment = filtered_data[filtered_data['asap0_name'] == selected_country]['comment'].iloc[0]
st.info(f"Comment for {selected_country}: {comment}")

#Monthly trend analysis 
monthly_trend = filtered_data.groupby('date').size().reset_index(name='Hotspot Count')
trend = px.line(monthly_trend, x='date', y='Hotspot Count', title="Anomaly Hotspot Trends over time")
st.plotly_chart(trend, use_container_width=True)