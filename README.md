# Visualizing city data
### Traffy Fondue data from Bangkok

This example will draw some illustrations of data visualization drawn from a Jupyter notebook analysis
and then converted to an interactive web frontend.

You can see the app here: [![Streamlit](https://badgen.net/badge/Powered%20by/Streamlit/red)](https://visualize-city-data.streamlit.app/)


---
Plan
|ToDo|Doing|Done|
|----|-----|----|
| |Setup basic visual platform| Sample Dash app|
|| | Import processed Traffy fondue data|
|||Display data in dynamic map|
|||Add interactive options:  district|
|Add interactive options date, type||
|Build import module -scrape API|||
|Build clean module|||
|Update visual app with new data|||
|||Deploy to streamlit cloud|
---
LOG

Date May 30, 2025

Did some modification and added a bargraph to the page.

I also added dockerfile and docker compose

use the command

docker-compose up --build

docker-compose down
---

LOG

Date November 19, 2023

I did some reading into streamlit, and noticed that you can deploy the platform onto streamlit cloud.
This might shorten my develop to deploy cycle, at least for the POC.
So I have decided to move from dash to [streamlit](https://streamlit.io/).

Keep up with the progress, here is the link to [streamlit cloud and community.](https://streamlit.io/cloud)

in order to test the initial visuals, the processed dataframe from the jupyter notebook with geo locations will be used to be passed in this example.




---

Date: November 18, 2023

Initial code creation.
This code should run with no sample data, and just display the web application and use the basic library [dash](https://dash.plotly.com/)

The sample code should take the sample data and create a barchart

run with docker commands:

docker build -t dash-example .
docker run -p 8050:8050 dash-example

and open [http://localhost:8050](http://localhost:8050) in a browser

---

