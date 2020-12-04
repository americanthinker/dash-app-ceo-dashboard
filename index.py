import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import helper_functions
import dash_bootstrap_components as dbc
import dash_daq as daq

# must add this line in order for the app to be deployed successfully on Heroku
from app import app

# noinspection PyUnresolvedReferences
from app import server

# import all pages in the app
from apps import homepage, membership, marketing, growth


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/membership':
        return membership.layout
    elif pathname == '/apps/marketing':
         return marketing.layout
    elif pathname == '/apps/growth':
         return growth.layout
    else:
        return homepage.layout

if __name__ == '__main__':
    app.run_server(debug=True)