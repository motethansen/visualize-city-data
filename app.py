# app.py
#import dash
#from dash import dcc, html
import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import StripePattern
import branca
from streamlit_folium import folium_static
import geopandas as gpd



# Coordinates for Bangkok city
bangkok_coordinates = [13.7563, 100.5018]
filename = "map_df.pkl"
traffy_df = []
district_boundary_data = []


def load_data(nrows):
    data = pd.read_csv(filename, nrows=nrows)
    #data=data.drop(columns=['Complaint','Suggestion','Homeless','Journey','Inquiry','Bathroom','PM2.5','Traffic Signs'])

    return data

type = [
"Bridge",
"Canal",
"Cleanliness",
"Drain",
"Electric Wires",
"Flood",
"Light",
"Noise",
"Obstruction",
"Road",
"Safety",
"Sidewalk",
"Signage",
"Stray animals",
"Traffic",
"Tree"]



def bkk_map(ctype, map_df, bound):
    # create a folium map centered on Bangkok
    m = folium.Map(location=[13.7563, 100.5618],zoom_start=11)

    comlaint_string = ctype +" "+"complaints"
    # add the district boundary to the map as a PolyLine
    #GeoJson(district_boundary_data).add_to(m)
    colorscale = branca.colormap.step.RdYlBu_11.to_linear().scale(0, 1500)
    colorscale.caption = '# of complaints'
    # Set up Choropleth map
    folium.Choropleth(
    geo_data=map_df,
    data=map_df,
    columns=['district', ctype], #'Road'],
    key_on="feature.properties.district",
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=comlaint_string, #"Road complaints",
    smooth_factor=0,
    Highlight= True,
    #line_color = "#0000",
    name = "Road complaints",
    show=False,
    overlay=True,
    nan_fill_color = 'lightgrey', #"White"
    nan_fill_opacity = 0.5
    ).add_to(m)

    # Not exactly a crosshatch, but its close.  Maybe you can find a better pattern
    sp = StripePattern(angle=45, color='grey', space_color='white', fill_opacity=0.5, opacity=1)
    sp.add_to(m)

    # adding the nan layer with `sp` as the fillPattern
    folium.GeoJson(data=bound, style_function=lambda x :{'fillPattern': sp}).add_to(m)
    return m

def main():
    st.title("Traffy Fondue complaints data.")
    st.subheader("District based visualization")
    district_boundary_data = gpd.read_file("bkk_districts.geojson")

    # Create a text element and let the reader know the data is loading.
    #data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = pd.read_pickle(filename)#load_data(50)
    # Notify the reader that the data was successfully loaded.
    #data_load_state.text('Loading data...done!')
    
    complaint_type = st.selectbox('Select complaint type: ',
        type,
        index=5)
    

    traffy_df = data
    #st.text(traffy_df.shape)
    #st.text(traffy_df.columns)

    # Map of Bangkok
    folium_map = bkk_map(complaint_type, traffy_df, district_boundary_data)

    # Display the Folium map in Streamlit
    #st_data = st_folium(folium_map, width = 725)
    folium_static(folium_map)
    

if __name__ == '__main__':
    main()