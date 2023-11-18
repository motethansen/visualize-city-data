# Visualizing city data
### Traffy Fondue data from Bangkok

This example will draw some illustrations of data visualization drawn from a Jupoyter notebook analysis
and then converted to an interactive web frontend.

---

LOG

Date: November 18, 2023

Initial code creation.
This code should run with no sample data, and just display the web application and use the basic library [dash](https://dash.plotly.com/)

The sample code should take the sample data and create a barchart

run with docker commands:

docker build -t dash-example .
docker run -p 8050:8050 dash-example

and open [http://localhost:8050](http://localhost:8050) in a browser