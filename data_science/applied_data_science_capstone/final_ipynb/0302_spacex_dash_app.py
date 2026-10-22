"""
LAB by Gabriel Galvez
Hands-on Lab: Build an Interactive Dashboard with Plotly Dash
"""

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'}
                                    ] + [
                                        {'label': site, 'value': site}
                                        for site in spacex_df['Launch Site'].unique()
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site',
                                    searchable=True
                                    )
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=max_payload,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={0: '0', 25000: '25.000', 50000: '50.000', 75000: '75.000'}
                                    )
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
spacex_df['Outcome'] = spacex_df['class'].map({
    0: 'Failed',
    1: 'Success'
})
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Outcome',
            color='Outcome',
            color_discrete_map={
                'Failed': 'red',
                'Success': 'green'
                },
            title='Launch Successes for All Sites'
        )
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='Outcome',
            color='Outcome',
            color_discrete_map={
                'Failed': 'red',
                'Success': 'green'
                },
            title=f'Launch Successes for {entered_site}'
        )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def get_scatter_chart(entered_site, payload_range):
    low = payload_range[0]
    high = payload_range[1]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='Outcome',
            color='Outcome',
            color_discrete_map={
                'Failed': 'red',
                'Success': 'green'
            },
            category_orders={'Outcome': ['Failed', 'Success']},
            opacity=0.7,
            title='Payload Mass for All Launches'
        )
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='Outcome',
            color='Outcome',
            color_discrete_map={
                'Failed': 'red',
                'Success': 'green'
            },
            category_orders={'Outcome': ['Failed', 'Success']},
            opacity=0.7,
            title=f'Payload Mass for Launches from {entered_site}'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
