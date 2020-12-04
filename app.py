import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.SLATE]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions = True)
server = app.server
