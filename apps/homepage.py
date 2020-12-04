import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
external_stylesheets = [dbc.themes.SLATE]
from app import app

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div(id='container', style=dict(backgroundColor='black',
                                                 fontFamily='Balto',
                                                 height='100vh'),
            children=[
                dbc.Container([

# Title
                    dbc.Row([
                        dbc.Col(html.H1("Elite Meet Analytics Dashboard",
                                        style=dict(fontSize=60,
                                                   color='red'),
                                        className="text-center"),
                                className="mb-5 mt-5")
                    ]),

# Elite Meet Logo
                    dbc.Row([
                        dbc.Col(html.A([
                                    html.Img(id='em-logo', src=app.get_asset_url('EM-logo.svg'))
                                       ], href='https://elitemeetus.org/'),
                            style=dict(backgroundColor='slategrey',
                                       marginBottom='25px'),
                            width=dict(size=4, offset=4))
                    ], style={'textAlign': 'center'}),

# spacer row
                    dbc.Row([
                        dbc.Col(html.H5(), className="mb-5")
                            ]),

# Navigation buttons
                    dbc.Row([
                        dbc.Col(dbc.Card(children=[html.H3(children='Geographic distribution',
                                                           className="text-center"),
                                                   dbc.Button("Membership",
                                                              href="/apps/membership",
                                                              color="primary",
                                                              size='lg',
                                                              className="mt-3"),
                                                   ],
                                         body=True, color="dark", outline=True)
                                , width=4, className="mb-4"),

                        dbc.Col(dbc.Card(children=[html.H3(children='View growth trends',
                                                           className="text-center"),
                                                   dbc.Button("Growth",
                                                              href="/apps/growth",
                                                              color="primary",
                                                              size='lg',
                                                              className="mt-3"),
                                                   ],
                                         body=True, color="dark", outline=True)
                                , width=4, className="mb-4"),

                        dbc.Col(dbc.Card(children=[html.H3('View marketing channels',
                                                           className="text-center"),
                                                   dbc.Button("Marketing",
                                                              href="/apps/marketing",
                                                              color="primary",
                                                              size='lg',
                                                              className="mt-3"),

                                                   ],
                                         body=True, color="dark", outline=True)
                                , width=4, className="mb-4")
                    ], className="mb-5"),

# SOF logos
                    dbc.Row(#style=dict(backgroundColor='yellow'),
                        children=
                            dbc.Col(children=[
                                html.A(html.Img(id='arsoc-logo', src=app.get_asset_url('arsoc-logo.png'),
                                                style=dict(height='15vh',
                                                           marginLeft='10px',
                                                           marginRight='10px')),
                                            href="https://www.soc.mil/"),
                                html.A(html.Img(id='navsoc-logo', src=app.get_asset_url('nswc.png'),
                                                style=dict(height='15vh',
                                                            marginLeft='10px',
                                                            marginRight='10px')),
                                            href="https://www.nsw.navy.mil/"),
                                html.A(html.Img(id='socom-logo', src=app.get_asset_url('socom.png'),
                                                style=dict(height='20vh',
                                                            marginLeft='10px',
                                                            marginRight='10px')),
                                            href="https://www.socom.mil"),
                                html.A(html.Img(id='afsoc-logo', src=app.get_asset_url('afsoc.png'),
                                                style=dict(height='13vh',
                                                            marginLeft='10px',
                                                            marginRight='10px')),
                                            href="https://www.afsoc.af.mil/"),
                                html.A(html.Img(id='marsoc-logo', src=app.get_asset_url('marsoc.png'),
                                                style=dict(height='15vh',
                                                            marginLeft='10px',
                                                            marginRight='10px')),
                                            href="https://www.marsoc.marines.mil/"),

                            ], style=dict(textAlign='center')))

    ])

])

# needed only if running this as a single page app
#if __name__ == '__main__':
 #   app.run_server(debug=True)