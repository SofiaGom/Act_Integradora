#librerias
import streamlit as st
import pandas as pd 
import numpy as np
import plotly as px 
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt 

#cambios:
#1: Agregué una imagen para la representación visual del caso policial y su repporte
#2: Cambié el formato de título y agregué un subtítulo
#3: Gráfico para ver daños cometidos por subcategoria
#4: Agregué filtro por año
#5: Agregúe filtro por descripcion del incidcente
#6: Agregué gráfica de crimenes ocurridos por tiempo

#imagen
img_path =  "police.png" 
with open(img_path, "rb") as f:
    img_bytes = f.read()
st.image(img_bytes, width=500, caption="Image 1.0 - Police")
#estilo de título y subtítulo
st.markdown(
    '<h1 style="color: darkblue; font-family: Chiller, sans-serif;">Police Report',
    unsafe_allow_html=True
)
st.markdown(
    '<h2 style="color: blue; font-family: Chiller, sans-serif;">Police Incident Reports from 2018 to 2020 in San Francisco',
    unsafe_allow_html=True
)

data = pd.read_csv("Police.csv")
df = data.fillna(method='bfill')
#agregué las columnas y datos necesarios para gráficos y filtros
st.sidebar.title('SFPD Category Filter')
st.markdown("The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 t0 2020 which details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution")
mapa=pd.DataFrame()
mapa['Date'] = df['Incident Date']
mapa['Day'] = df['Incident Date']
mapa['Time'] = df['Incident Date']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['Incident Year'] = df['Incident Year']
mapa['Incident Description'] = df['Incident Description']
mapa['lon'] = df['Longitude']
subset_data2= mapa

police_district_input=st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input)>0:
    subset_data2 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data1=subset_data2
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data2.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len(neighborhood_input) >0:
    subset_data1 = subset_data2[subset_data2['Neighborhood'].isin(neighborhood_input)]
    
    
subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data1.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len(incident_input) >0:
    subset_data = subset_data1[subset_data1['Incident Category'].isin(incident_input)]
   
#filtros añadidos    
subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Year',
    subset_data1.groupby('Incident Year').count().reset_index()['Incident Year'].tolist())
if len(incident_input) >0:
    subset_data = subset_data1[subset_data1['Incident Year'].isin(incident_input)]
    
subset_data = subset_data1
incident_input = st.sidebar.multiselect(
    'Incident Description',
    subset_data1.groupby('Incident Description').count().reset_index()['Incident Description'].tolist())
if len(incident_input) >0:
    subset_data = subset_data1[subset_data1['Incident Description'].isin(incident_input)]


#gra´ficas añadidas
st.markdown("It is important to mention that any police district can answer to any incident, the neighborhood in which it happened is not related to the police district.")
st.markdown("Crime location in San Francisco")
st.map(subset_data)
st.subheader("Crimes ocurred per day of the week")
st.bar_chart(subset_data['Day'].value_counts())
st.subheader('Crimes ocurred per date')
st.line_chart(subset_data['Date'].value_counts())
st.subheader('Crimes ocurred per neighborhood')
st.line_chart(subset_data['Neighborhood'].value_counts())
st.subheader('Type of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts())
st.subheader('Type of crimes committed in subcategories')
st.bar_chart(subset_data['Incident Subcategory'].value_counts())


agree = st.button('Click to see Incident Subcategories')
if agree:
    st.subheader('Subtype of crimes committed')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())
st.markdown('Resolution status')
figi, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels = labels, autopct='%1.1f%%', startangle = 20)
st.pyplot(figi)

