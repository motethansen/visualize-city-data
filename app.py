# app.py
import dash
from dash import dcc, html
import pandas as pd

# Sample dataset
data = [10, 20, 30, 40, 50]

# Create a DataFrame for plotting
df = pd.DataFrame(data, columns=["Values"])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Dash Docker Example with Bar Chart"),
    
    # Display the dataset
    html.P("Dataset: {}".format(data)),

        # Bar chart
    dcc.Graph(
        id='bar-chart',
        figure={
            'data': [
                {'x': df.index, 'y': df['Values'], 'type': 'bar', 'name': 'Values'}
            ],
            'layout': {
                'title': 'Bar Chart'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)