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

#added stackbar
import plotly.express as px

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

def create_bar_chart(map_df):
    # Pivot the data to get complaint counts by district and type
    pivot_df = map_df.melt(
        id_vars=['dname_e'],
        value_vars=type,
        var_name='Complaint Type',
        value_name='Number of Complaints'
    )
    
    # Aggregate to sum complaints per district and type (handling NaN as 0)
    pivot_df = pivot_df.groupby(['dname_e', 'Complaint Type'])['Number of Complaints'].sum().reset_index()
    
    # Create a stacked bar chart with Plotly
    fig = px.bar(
        pivot_df,
        x='Number of Complaints',
        y='dname_e',
        color='Complaint Type',
        orientation='h',
        title='Complaint types per district',
        labels={'Number of Complaints': '# of complaints', 'district': 'District'},
        height=800,
        width=800,
        color_discrete_map={
            'Road': '#1f77b4', 'Safety': '#ff7f0e', 'Obstruction': '#2ca02c',
            'Tree': '#d62728', 'Sidewalk': '#9467bd', 'Cleanliness': '#8c564b',
            'Traffic': '#e377c2', 'Flood': '#7f7f7f', 'Drain': '#bcbd22',
            'Light': '#17becf', 'Noise': '#1a55FF', 'Bridge': '#FF5555',
            'Electric Wires': '#55FF55', 'Stray animals': '#FFAA00',
            'Signage': '#00AAAA', 'Canal': '#AA00AA'
        }
    )
    
    # Update layout for better readability
    fig.update_layout(
        barmode='stack',
        xaxis_title='# of complaints',
        yaxis_title='District',
        legend_title='Complaint Type',
        hovermode='closest'
    )
    
    # Customize hover template to show complaint type and number
   
    fig.update_traces(
        hovertemplate='<b>District:</b> %{y}<br><b>Complaint Type:</b> %{customdata}<br><b>Number of Complaints:</b> %{x}<extra></extra>',
        customdata=pivot_df['Complaint Type']
    )

    for trace, complaint_type in zip(fig.data, pivot_df['Complaint Type'].unique()):
        mask = pivot_df['Complaint Type'] == complaint_type
        trace.customdata = pivot_df[mask]['Complaint Type']
        trace.hovertemplate = (
            '<b>District:</b> %{y}<br>'
            '<b>Complaint Type:</b> %{customdata}<br>'
            '<b>Number of Complaints:</b> %{x}<extra></extra>'
    )
    
    return fig

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

    # Create and display bar chart below the map
    st.subheader("Complaint Distribution by District")
    bar_chart = create_bar_chart(traffy_df)
    st.plotly_chart(bar_chart)

if __name__ == '__main__':
    main()