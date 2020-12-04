import dash
import os
import pandas as pd
from helper_functions import scaler, plot_scatter_map, update_scatter_map_layout, update_bar_chart_layout, plot_points, plot_barchart
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_core_components  as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px

from app import app

#DATA IMPORT/MUNGING + GRAPH INITIALIZATION
##########################################################################################################################
#initialize mapbox access through API
mapbox_access_token = os.environ.get('MAPBOX_API_KEY')
px.set_mapbox_access_token(mapbox_access_token)

#Load data
vets = pd.read_csv('data/updated_pilots.csv')

#create membership total tables for branch and tribes
branch_table_df = vets['Branch'].value_counts()[:4].to_frame().T
branch_table_df['Total'] = branch_table_df.sum(axis=1)
tribe_table_df = vets['Tribe'].value_counts().to_frame().T
tribe_table_df['Total'] = tribe_table_df.sum(axis=1)

#***Use map_df for mapping only!!!***
#rescale sizing and set df for mapping /
map_df = vets[vets['scaled'].notnull()]
map_df = map_df[map_df['CityState'] != 'NC, NC']
map_df = map_df[map_df['Branch'] != 'Coast Guard']

#reate branch and tribe options
branches = map_df['Branch'].unique()
tribes = map_df['Tribe'].unique()
branch_selection = [{'label':val, 'value':val} for val in branches]
tribe_selection = [{'label':val, 'value':val} for val in tribes]

#set color scheme
colors = {
    'background1': '#111111',
    'background2': '#008080',
    'text': '#7FDBFF'}
branch_colors = ['blue', 'green', 'red', 'skyblue']

#create figure object for map
# map_fig = go.Figure(go.Scattermapbox(mode='markers'))
# update_scatter_map_layout(map_fig)

#create figure object for bar graph
barchart = go.Figure(go.Bar())
update_bar_chart_layout(barchart, selector='Branch')

#LAYOUT
##########################################################################################################################

layout = html.Div(id='app-container',
    children = [html.Div(id='border',
                    children=[
                       dbc.Row([
                            dbc.Col(#style=dict(backgroundColor='orange',
                                html.H2(id='title',
                                     children='Elite Meet Membership',
                                     style=dict(
                                         fontSize=40,
                                         fontFamily='Times',
                                         marginLeft='25px',
                                         marginTop='20px')
                                                     )),
                            dbc.Col(width=3, #style=dict(backgroundColor='yellow'),
                                children=html.Div(id='button-container',
                                                  style=dict(fontFamily='Times', textAlign='right'),
                                    children=[
                                            dbc.Button("Homepage",
                                               href="/apps/homepage",
                                               color="primary",
                                               size='lg',
                                               className="mt-3"),
                                           dbc.Button("Marketing",
                                               href="/apps/marketing",
                                               color="primary",
                                               size='lg',
                                               className="mt-3"),
                                           dbc.Button("Growth",
                                               href="/apps/growth",
                                               color="primary",
                                               size='lg',
                                               className="mt-3")
                                                    ])
                                    ),
                            dbc.Col(width=2,
                                    children=
                                        html.Img(id='em-logo',
                                             style=dict(marginTop=20, height='10vh'),
                                             src=app.get_asset_url('EM-logo.svg')
                                                 )),
                            ])]),

#Branch dropdown
    dbc.Row(id='dropdowns',children=[
            dbc.Col(id='scatter-map-label', width=3, children=html.Label('National Distribution of Members',
                                                                style=dict(
                                                                    fontSize=28,
                                                                    fontFamily='Times',
                                                                    marginLeft='35px',
                                                                    marginTop='55px')
                                                                )),
            dbc.Col(id='branch-dropdown', width=3, style=dict(marginLeft='25px'), #backgroundColor='orange'),
                children=[
                    html.Label('Select Service Branch to plot points',
                             style=dict(
                             fontSize=18,
                             fontFamily='Times',
                             marginLeft='20px',
                             marginTop='15px')
                               ),
                    dcc.Dropdown(
                        id='Branches',
                        style=dict(marginLeft='10px'),
                        options=branch_selection,
                        value=['Navy', 'Army', 'Marine Corps', 'Air Force'],
                        multi=True,
                        clearable=True,
                        placeholder='Select Service Branch'
                                )
                        ]
                    ),
            dbc.Col(id='scatter-map-label', width=dict(size=3, offset=1),
                    children=html.Label('Breakout of Members by City',
                            style=dict(
                                fontSize=28,
                                fontFamily='Times',
                                #marginLeft='35px',
                                marginTop='55px')
                                                                )),
                ]
            ),
#scatter map block
    html.Div(id='graph-container', style=dict(marginLeft='25px', backgroundColor="#252e3f"),
             children=[
                 dbc.Row([
                     dbc.Col(width=7,
                            children=html.Div(id='scatter-div', style=dict(marginLeft='20px', ),
                                           children=dcc.Graph(id='scatter-map',
                                                    style=dict(height='70vh',
                                                    padding='10px'),
                                                    responsive=True))
                             ),
#bar chart block
                     dbc.Col(width=5,
                             children=[
                                       html.Div(id='bar-chart-div2', style=dict(marginRight='25px'),
                                                children=dcc.Graph(id='bar-chart2',
                                                                   style=dict(height='35vh'),
                                                                   figure=barchart,
                                                                   responsive=True)),
                                        html.Div(id='bar-chart-div', style=dict(marginRight='25px'),
                                                  children=dcc.Graph(id='bar-chart',
                                                                 style=dict(height='35vh'),
                                                                 figure=barchart,
                                                                 responsive=True))
                                       ])

                        ])

                    ]),


])

# CALLBACKS
##########################################################################################################################

#Plot points on map based on Branch values
@app.callback(
    Output('scatter-map', 'figure'),
    Input('Branches', 'value')
)
def plot_call(values):
    if values is None:
        plot_scatter_map(values, 'Branch', map_df)
    elif len(values) == 0:
        map_fig = go.Figure(go.Scattermapbox(mode='markers'))
        update_scatter_map_layout(map_fig)
        return map_fig
    else:
        return plot_scatter_map(values, 'Branch', map_df)


# plot barchart based on Branch values on first map
@app.callback(
    Output('bar-chart', 'figure'),
    Input('scatter-map', 'hoverData')
)
def update_bar(hoverData):
    if hoverData is None:
        location = "San Diego, California"
        barchart = plot_barchart(location, map_df, 'Branch')

        return barchart

    else:
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        barchart = plot_barchart(location, map_df, 'Branch')

        return barchart


# plot barchart based on Tribe values on first map
@app.callback(
    Output('bar-chart2', 'figure'),
    Input('scatter-map', 'hoverData')
)
def update_bar(hoverData):
    if hoverData is None:
        location = "San Diego, California"
        barchart = plot_barchart(location, map_df, 'Tribe')

        return barchart

    else:
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        barchart = plot_barchart(location, map_df, 'Tribe')

        return barchart


@app.callback(
    Output('dataframe', 'children'),
    Input('toggle-switch', 'value')
)
def toggle(val):
    if val == None:
        children = [
            html.H3(id='branch-data-table-header',
                    children='Service Branch Total Counts',
                    style=dict(fontFamily='Balto',
                               marginTop=40,
                               textAlign='center')),
            dbc.Table.from_dataframe(branch_table_df,
                                     striped=True,
                                     style=dict(fontFamily='Balto',
                                                textAlign='center',
                                                fontSize=16
                                                ),
                                     dark=True,
                                     responsive=True,
                                     bordered=True)
        ]

        return children

    elif val == False:
        children = [
            html.H3(id='branch-data-table-header',
                    children='Service Branch Total Counts',
                    style=dict(fontFamily='Balto',
                               marginTop=40,
                               textAlign='center')),
            dbc.Table.from_dataframe(branch_table_df,
                                     striped=True,
                                     style=dict(fontFamily='Balto',
                                                textAlign='center',
                                                fontSize=16
                                                ),
                                     dark=True,
                                     responsive=True,
                                     bordered=True)
        ]

        return children

    elif val == True:
        children = [
            html.H3(id='tribes-data-table-header',
                    children='SOF Tribe Total Counts',
                    style=dict(fontFamily='Balto',
                               marginTop=40,
                               textAlign='center')),
            dbc.Table.from_dataframe(tribe_table_df,
                                     striped=True,
                                     style=dict(fontFamily='Balto',
                                                textAlign='center',
                                                fontSize=14
                                                ),
                                     dark=True,
                                     responsive=True,
                                     bordered=True)
                    ]
        return children

if __name__ == "__main__":
    app.run_server(debug=True)



'''
@app.callback(
    Output('title', 'children'),
    Input('scatter-map', 'hoverData'))
def display_click_data(hoverData):
    if hoverData is None:
        return 'San Diego, California'
    else:
        print(json.dumps(hoverData))
        location = hoverData['points'][0]['hovertext'].split(':')[0]
        return html.P(location)
'''