import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('ev_data_2010_2024.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div(className='container', children=[
    html.H1(children='Advanced EV Dashboard'),

    html.Div([
        html.Label('Select Region:', className='dropdown-label'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region}
                     for region in df['region'].unique()],
            value=df['region'].unique()[0]
        )
    ]),

    html.Div([
        html.Label('Select Category:', className='dropdown-label'),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category}
                     for category in df['category'].unique()],
            value=df['category'].unique()[0]
        )
    ]),

    html.Div([
        html.Label('Select Parameter:', className='dropdown-label'),
        dcc.Dropdown(
            id='parameter-dropdown',
            options=[{'label': param, 'value': param}
                     for param in df['parameter'].unique()],
            value=df['parameter'].unique()[0]
        )
    ]),

    html.Div(className='graph-container', children=[
        dcc.Graph(id='time-series-plot'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='scatter-plot')
    ])
])

# Callbacks to update graphs based on selected filters


@app.callback(
    Output('time-series-plot', 'figure'),
    Output('bar-chart', 'figure'),
    Output('scatter-plot', 'figure'),
    Input('region-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('parameter-dropdown', 'value')
)
def update_graphs(selected_region, selected_category, selected_parameter):
    # Filter data based on dropdown selections
    filtered_df = df[(df['region'] == selected_region) & (
        df['category'] == selected_category) & (df['parameter'] == selected_parameter)]

    # Time Series Plot
    fig_time_series = px.line(
        filtered_df,
        x='year',
        y='value',
        title=f'{selected_parameter} Over Time',
        labels={'value': 'Value', 'year': 'Year'}
    )
    fig_time_series.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # Bar Chart
    fig_bar_chart = px.bar(
        filtered_df,
        x='powertrain',
        y='value',
        title=f'{selected_parameter} by Powertrain',
        labels={'value': 'Value', 'powertrain': 'Powertrain'}
    )
    fig_bar_chart.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # Scatter Plot
    scatter_data = df[(df['region'] == selected_region) & (
        df['category'] == selected_category) & (df['parameter'] != selected_parameter)]
    fig_scatter_plot = px.scatter(
        scatter_data,
        x='value',
        y='value',
        color='parameter',
        title=f'Scatter Plot of {selected_parameter} vs Other Parameters',
        labels={'value': 'Value'}
    )
    fig_scatter_plot.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    return fig_time_series, fig_bar_chart, fig_scatter_plot


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
