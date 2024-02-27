# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                min=0,
                max=10000,
                step=1000,
                marks={0: '0', 10000: '10000'},
                value=[0, 10000]
                ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])
                                
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Filter the dataframe for all sites
        filtered_df = df
        # Count the number of successful launches
        success_count = filtered_df[filtered_df['Class'] == 'Success']['Class'].count()
        # Count the number of failed launches
        failure_count = filtered_df[filtered_df['Class'] == 'Failure']['Class'].count()
        # Create a pie chart figure
        fig = px.pie(values=[success_count, failure_count], 
                     names=['Success', 'Failure'], 
                     title='Total Success Launches for All Sites')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = df[df['LaunchSite'] == entered_site]
        # Count the number of successful launches
        success_count = filtered_df[filtered_df['Class'] == 'Success']['Class'].count()
        # Count the number of failed launches
        failure_count = filtered_df[filtered_df['Class'] == 'Failure']['Class'].count()
        # Create a pie chart figure
        fig = px.pie(values=[success_count, failure_count], 
                     names=['Success', 'Failure'], 
                     title=f'Total Success Launches for {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        # Filter the dataframe for all sites
        filtered_df = df[(df['PayloadMass'] >= payload_range[0]) & (df['PayloadMass'] <= payload_range[1])]
        # Create a scatter plot figure
        fig = px.scatter(filtered_df, x='PayloadMass', y='Class', color='BoosterVersion',
                         title='Payload vs. Launch Outcome for All Sites',
                         labels={'PayloadMass': 'Payload Mass (kg)', 'Class': 'Launch Outcome'})
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = df[(df['LaunchSite'] == entered
