import dash
import os
import pandas as pd
from datetime import date
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from helper_functions import update_bar_chart_layout, plot_overall_marketing_barplot, plot_small_marketing_barplot
import dash_core_components  as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px

from app import app

def color(c='orange'):
    return dict(backgroundColor=c)

#import selected data
df = pd.read_csv('data/updated_pilots.csv', usecols=['Branch', 'Tribe', 'How_did_you_hear_about_Elite_Meet', 'CreatedDate'])
tribes = ['CCT', 'Green Beret', 'Helo Pilot (A)', 'NEOD', 'PJ', 'PSYOPS',
       'Pilot (AF)', 'Pilot (MC)', 'Pilot (N)', 'Raider', 'Ranger',
       'SEAL', 'SWCC']
tribe_selection = [{'label':val, 'value':val} for val in tribes]
months = ['May', 'June', 'July', 'August', 'September']
month_selection = [{'label':val, 'value':val} for val in months]
events = df.iloc[:,:2]

#initiatlize overall bar chart
initial_barchart = go.Figure(go.Bar())
small_chart = go.Figure(go.Bar())

#update_bar_chart_layout(barchart)
initial_barchart = plot_overall_marketing_barplot(df)
update_bar_chart_layout(small_chart)

#HTML caveat filler
caveat = '* Showing channels with only 2 or more responses'

# LAYOUT #################################################################################################################
layout = html.Div(id='container', children=[
        dbc.Row([
            dbc.Col(children= html.H2(id='title',
                                 children='Elite Meet Marketing',
                                 style=dict(
                                 fontSize=40,
                                 fontFamily='Times',
                                 marginLeft='25px',
                                 marginTop='20px'))
                    ),
#EM Logo
            dbc.Col(width=2, children=
                    html.Img(id='em-logo',
                             style=dict(marginTop=20, height='10vh'),
                             src=app.get_asset_url('EM-logo.svg')))
        ]),

# Large Overall Marketing channel bar graph
    dbc.Row(#style=dict(backgroundColor='yellow'),
            children = [
        dbc.Col(width=2, style=dict(fontFamily='Times'),
                children=[
                          dbc.Row(style=dict(marginTop='10vh'),
                              children=dbc.Button("Homepage",
                              href="/apps/homepage",
                              color="primary",
                              size='lg',
                              className="mt-3"),
                                  justify='center'),
                          dbc.Row(dbc.Button("Membership",
                              href="/apps/membership",
                              color="primary",
                              size='lg',
                              className="mt-3"),
                                  justify='center'),
                          dbc.Row(dbc.Button("Growth",
                              href="/apps/growth",
                              color="primary",
                              size='lg',
                              className="mt-3"),
                                  justify='center')
                         ]),
        dbc.Col(width=8,
                children=[
                    dcc.Graph(id='overall', figure=initial_barchart,
                          style=dict(height='70vh')),
                          html.P(caveat)
                          ]
                )
        ]),

# Drop Down row
    dbc.Row([
        dbc.Col(width=4,children=
                    dcc.Dropdown(
                        id='tribes-m',
                        options=tribe_selection,
                        value='SEAL',
                        multi=False,
                        clearable=True,
                        placeholder='Select Tribe',
                        style=dict(marginLeft='20px'))),
dbc.Col(width=(dict(size=4, offset=2)),children=
                        dcc.DatePickerRange(
                                id='date-picker-marketing',
                                clearable=True,
                                first_day_of_week=0,
                                number_of_months_shown=3,
                                #persistence=True,
                                show_outside_days=True,
                                min_date_allowed=date(2018, 10, 22),
                                max_date_allowed=date(2020, 9, 18),
                                initial_visible_month=date(2020, 9, 18),
                                start_date=date(2020, 9, 1),
                                end_date=date(2020, 9, 18),
                                style=dict(marginBottom='30px')
                            ))
            ]),

# Small bar graphs
    dbc.Row([
        dbc.Col(width=6, #style=dict(backgroundColor='blue'),
                children=html.Div(style=dict(marginLeft='20px'),
                            children=[
                                dcc.Graph(id='marketing-tribe', figure=small_chart,
                                          style=dict(height='60vh')),
                                html.P(caveat)
                                     ])),
        dbc.Col(width=6, #style=dict(backgroundColor='blue'),
                children=[
                    dcc.Graph(id='marketing-time', figure=small_chart,
                          style=dict(height='60vh')),
                          ])
            ])
])

# channel by Tribe callback
@app.callback(
    Output('marketing-tribe', 'figure'),
    Input('tribes-m', 'value')
)
def update_bar(value):
    if value is None or len(value) == 0:
        return update_bar_chart_layout(small_chart)
    else:
        return plot_small_marketing_barplot(df, value)

# channel by Time callback
@app.callback(
    Output('marketing-time', 'figure'),
    [Input('date-picker-marketing', 'start_date'),
    Input('date-picker-marketing', 'end_date')])
def update_output(start_date, end_date):
    if start_date is None:
        return update_bar_chart_layout(small_chart)
    elif end_date is None:
        return update_bar_chart_layout(small_chart)
    else:
        events = df.iloc[:,:2]
        events['CreatedDate'] = pd.to_datetime(events['CreatedDate']).dt.date
        events = events.set_index('CreatedDate')
        events.index = pd.to_datetime(events.index)
        events = events.loc[start_date:end_date]
        if len(events) == 0:
            return update_bar_chart_layout(small_chart)
        else:
            events = events[events['How_did_you_hear_about_Elite_Meet'].str.len() < 30]
            events.rename(columns={'How_did_you_hear_about_Elite_Meet':'Channel'}, inplace=True)
            values = events['Channel'].value_counts().to_frame().reset_index()
            values.rename(columns={'Channel':'Count', 'index': 'Channels'}, inplace=True)

            barchart = px.bar(values,
                              x='Channels',
                              y='Count',
                              orientation='v',
                              hover_name='Channels',
                              hover_data={'Count': False, 'Channels':False},
                              text='Count'
                              )

            update_bar_chart_layout(barchart, chart_title='Marketing Channels - Time Range', title_size=28)
            barchart.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = []
            )
        )
            return barchart
