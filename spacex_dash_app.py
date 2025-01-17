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

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                                    value='ALL',
                                    placeholder="Select the site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                #marks={min_payload: 'min_payload', max_payload: 'max_payload'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    if entered_site =='ALL':
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site',
                     title='Total successful launches count for all sites')
        return fig
    else:
        if entered_site =='CCAFS LC-40' :
            fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40'].groupby('class').size().reset_index(name='count'), values = 'count',
                         names = 'class',
                         title='Total Success(1) vs. Failed(0) launches count for site CCAFS LC-40')
        elif entered_site =='VAFB SLC-4E' :
            fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E'].groupby('class').size().reset_index(name='count'), values = 'count',
                         names = 'class',
                         title='Total Success(1) vs. Failed(0) launches count for site VAFB SLC-4E')
        elif entered_site =='KSC LC-39A' :
            fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A'].groupby('class').size().reset_index(name='count'), values = 'count',
                         names = 'class',
                         title='Total Success(1) vs. Failed(0) launches count for site KSC LC-39A')
        else :
            fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40'].groupby('class').size().reset_index(name='count'), values = 'count',
                         names = 'class',
                         title='Total Success(1) vs. Failed(0) launches count for site CCAFS SLC-40')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    mask = (spacex_df['Payload Mass (kg)']>payload_range[0]) & (spacex_df['Payload Mass (kg)']<payload_range[1])
    if entered_site =='ALL':
        fig = px.scatter(
            spacex_df[mask],
            x = 'Payload Mass (kg)',
            y = 'class',
            color = 'Booster Version Category'
        )
        return fig
    else :
        if entered_site =='CCAFS LC-40' :
            spacex_dff = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
            fig = px.scatter(
                spacex_dff[(spacex_dff['Payload Mass (kg)']>payload_range[0]) & (spacex_dff['Payload Mass (kg)']<payload_range[1])],
                x = 'Payload Mass (kg)',
                y = 'class',
                color = 'Booster Version Category'
            )
        elif entered_site =='VAFB SLC-4E' :
            spacex_dff = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
            fig = px.scatter(
                spacex_dff[(spacex_dff['Payload Mass (kg)']>payload_range[0]) & (spacex_dff['Payload Mass (kg)']<payload_range[1])],
                x = 'Payload Mass (kg)',
                y = 'class',
                color = 'Booster Version Category'
            )
        elif entered_site =='KSC LC-39A' :
            spacex_dff = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
            fig = px.scatter(
                spacex_dff[(spacex_dff['Payload Mass (kg)']>payload_range[0]) & (spacex_dff['Payload Mass (kg)']<payload_range[1])],
                x = 'Payload Mass (kg)',
                y = 'class',
                color = 'Booster Version Category'
            )
        else :
            spacex_dff = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            fig = px.scatter(
                spacex_dff[(spacex_dff['Payload Mass (kg)']>payload_range[0]) & (spacex_dff['Payload Mass (kg)']<payload_range[1])],
                x = 'Payload Mass (kg)',
                y = 'class',
                color = 'Booster Version Category'
            )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
