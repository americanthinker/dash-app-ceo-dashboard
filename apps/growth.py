import dash
import os
import pandas as pd
from datetime import date, datetime
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

#import time data first
timestamp = datetime.now().strftime('%Y-%m-%d')
filepath = 'data/Lead_' + timestamp
time_df = pd.read_csv(filepath + '.csv', usecols=['ConvertedDate'])
time_df.loc[:, 'ConvertedDate'] = pd.to_datetime(time_df.loc[:, 'ConvertedDate'])

#import tribe data and create options
tribe_df = pd.read_csv('data/updated_pilots.csv', usecols=['CreatedDate', 'Branch', 'Tribe'])
tribe_df.loc[:, 'CreatedDate'] = pd.to_datetime(tribe_df.loc[:, 'CreatedDate'])
tribes = tribe_df['Tribe'].unique()
tribe_selection = [{'label':val, 'value':val} for val in tribes]

#initiatlize overall bar chart
initial_barchart = go.Figure(go.Bar())
small_chart = go.Figure(go.Bar())

#update_bar_chart_layout(barchart)
update_bar_chart_layout(small_chart)


# LAYOUT #################################################################################################################
layout = html.Div(id='container', children=[
    dbc.Row([
        dbc.Col(children=html.H2(id='title',
                                 children='Elite Meet Growth',
                                 style=dict(
                                     fontSize=40,
                                     fontFamily='Times',
                                     marginLeft='25px',
                                     marginTop='20px'))
                ),
# EM Logo
        dbc.Col(width=2, children=
            html.Img(id='em-logo',
                 style=dict(marginTop=20, height='10vh'),
                 src=app.get_asset_url('EM-logo.svg')))
    ]),

# Large Overall Marketing channel bar graph
    dbc.Row(children = [
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
                          dbc.Row(dbc.Button("Marketing",
                              href="/apps/marketing",
                              color="primary",
                              size='lg',
                              className="mt-3"),
                                  justify='center')
                         ]),
        dbc.Col(width=4,#style=dict(backgroundColor='red'),
                children=[
                            dcc.DatePickerRange(
                                id='date-picker-growth',
                                clearable=True,
                                first_day_of_week=0,
                                number_of_months_shown=3,
                                #persistence=True,
                                show_outside_days=True,
                                min_date_allowed=time_df['ConvertedDate'].min().date(),
                                max_date_allowed=time_df['ConvertedDate'].max().date(),
                                initial_visible_month=date(2020, 9, 18),
                                start_date=time_df['ConvertedDate'].min().date(),
                                end_date=time_df['ConvertedDate'].max().date(),
                                style=dict(marginLeft='20px')),

                            html.Div(style=dict(marginLeft='20px'),
                                 children= dcc.Graph(id='growth-tribe', figure=small_chart,
                                              style=dict(height='40vh')))
                    ]),


        dbc.Col(width=(dict(size=4)),
                children=[
                    dcc.Dropdown(
                        id='tribes-g',
                        options=tribe_selection,
                        value='SEAL',
                        multi=False,
                        clearable=True,
                        placeholder='Select Tribe'),
                        #style=dict(marginLeft='20px')),
                        dcc.Graph(id='growth-time', figure=small_chart,
                                style=dict(height='40vh', marginTop='10px'))
                          ])

                ]),

    dbc.Row(
        dbc.Col(width=8,
                children=[
                    dcc.Graph(id='overall', figure=initial_barchart,
                          style=dict(height='70vh')),
                          html.P()
                          ]
                ))
])

@app.callback(
    Output('growth-tribe', 'figure'),
    [Input('date-picker-growth', 'start_date'),
    Input('date-picker-growth', 'end_date')])
def update_output(start_date, end_date):
    if start_date is None:
        return update_bar_chart_layout(small_chart)
    elif end_date is None:
        return update_bar_chart_layout(small_chart)
    else:
        growth = time_df['ConvertedDate'].value_counts().sort_index()
        growth = growth.loc[start_date:end_date]

        if len(growth) == 0:
            return update_bar_chart_layout(small_chart)

        else:
            events = growth.to_frame().reset_index()
            events.rename(columns={'index':'Date', 'ConvertedDate':'Count'}, inplace=True)

            plot = px.line(events,
                              x='Date',
                              y='Count',
                              hover_name='Count',
                              hover_data={'Count':False},
                              render_mode='svg',
                              )

            plot.update_layout(yaxis=dict(visible=False))
            return plot



def hold_fx(start_date, end_date):
    if start_date is None:
        return update_bar_chart_layout(small_chart)
    elif end_date is None:
        return update_bar_chart_layout(small_chart)
    else:
        time_df.loc[:, 'ConvertedDate'] = pd.to_datetime(time_df.loc[:, 'ConvertedDate'].dt.date)
        growth = time_df.set_index('ConvertedDate')
        growth = growth.loc[start_date:end_date]
        if len(growth) == 0:
            return update_bar_chart_layout(small_chart)

        else:
            grouped_date = growth.groupby(growth.index)['Tribe'].count().cumsum()
            plot = px.line(grouped_date,
                              x=grouped_date.index,
                              y=grouped_date.values,
                              hover_name=grouped_date.values,
                              #hover_data={grouped_date.values:False},
                              #text='Count'
                              )
            plot.update_layout(yaxis=dict(visible=False))
            return plot