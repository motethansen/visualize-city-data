import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import StripePattern
import branca
from streamlit_folium import folium_static
import geopandas as gpd
from folium.features import GeoJsonTooltip

# Coordinates for Bangkok city
bangkok_coordinates = [13.7563, 100.5018]
filename = "map_df.pkl"
traffy_df = []
district_boundary_data = []

def load_data(nrows):
    data = pd.read_csv(filename, nrows=nrows)
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
    "Tree"
]

def bkk_map(ctype, map_df, bound):
    # Create a folium map centered on Bangkok with scale control
    m = folium.Map(
        location=[13.7563, 100.5618],
        zoom_start=11,
        tiles="CartoDB positron",
        control_scale=True
    )

    comlaint_string = ctype + " complaints"
    colorscale = branca.colormap.step.RdYlBu_11.to_linear().scale(0, 1500)
    colorscale.caption = '# of complaints'

    # Set up Choropleth map
    folium.Choropleth(
        geo_data=map_df,
        data=map_df,
        columns=['district', ctype],
        key_on="feature.properties.district",
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=comlaint_string,
        smooth_factor=0,
        highlight=True,
        name="Road complaints",
        show=True,
        overlay=True,
        nan_fill_color='lightgrey',
        nan_fill_opacity=0.5
    ).add_to(m)

    # Add separate GeoJson layer for tooltips
    folium.features.GeoJson(
        map_df,
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0,
            'zIndexOffset': 1000  # Ensure GeoJson layer renders above Choropleth
        },
        highlight_function=lambda x: {
            'weight': 3,
            'color': 'blue'
        },
        tooltip=GeoJsonTooltip(
            fields=['dname_e', ctype],
            aliases=['District:', f'{ctype} Complaints:'],
            localize=True,
            sticky=True,
            labels=True,
            style="""
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid black;
                border-radius: 5px;
                box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
                padding: 8px;
                font-size: 14px;
                color: black;
                z-index: 1000;
            """,
            max_width=800
        ),
        zoom_on_click=False,
        name="District Tooltips",
        overlay=True,
        show=True
    ).add_to(m)

    # Add stripe pattern for NaN values
    # sp = StripePattern(angle=45, color='grey', space_color='white', fill_opacity=0.5, opacity=1)
    # sp.add_to(m)
    # folium.features.GeoJson(
    #     data=bound,
    #     style_function=lambda x: {'fillPattern': sp},
    #     name="NaN Areas",
    #     overlay=True,
    #     show=True
    #).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    return m

def main():
    st.title("Traffy Fondue complaints data.")
    st.subheader("District based visualization")
    district_boundary_data = gpd.read_file("bkk_districts.geojson")

    # Load data
    data = pd.read_pickle(filename)
    
    # Debug: Display available properties in GeoJSON
    # if not district_boundary_data.empty:
    #     st.write("Available GeoJSON properties:", list(district_boundary_data.columns))
    #     # Debug: Show sample GeoJSON properties
    #     sample_feature = district_boundary_data.iloc[0]
    #     st.write("Sample GeoJSON feature properties:", sample_feature.to_dict())
    
    complaint_type = st.selectbox('Select complaint type: ', type, index=5)
    
    traffy_df = data

    # Create and display map
    folium_map = bkk_map(complaint_type, traffy_df, district_boundary_data)
    folium_static(folium_map, width=725, height=500)

if __name__ == '__main__':
    main()