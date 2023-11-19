# app.py
#import dash
#from dash import dcc, html
import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import folium_static



# Coordinates for Bangkok city
bangkok_coordinates = [13.7563, 100.5018]


# Sample dataset
data = [10, 20, 30, 40, 50]

# Create a DataFrame for plotting
df = pd.DataFrame(data, columns=["Values"])

def main():
    st.title("Streamlit Example with Folium Map")

    # Map of Bangkok
    folium_map = folium.Map(location=bangkok_coordinates, zoom_start=10)

    # Display the Folium map in Streamlit
    folium_static(folium_map)


    # Display the dataset
    st.write("Dataset:", data)

    # Create a DataFrame for plotting
    df = pd.DataFrame(data, columns=["Values"])

    # Plotting
    st.bar_chart(df)

if __name__ == '__main__':
    main()