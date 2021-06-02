import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import dash_daq as daq

def index_page():
    return html.Div([
        html.H1("Fantasy Football Data", style={'text-align': 'center', 'background-color': 'lightblue'}),

        dcc.Link('Navigate to 2019-2020 season data', href='/ff-2019'),
        html.Br(),
        dcc.Link('Navigate to 2020-2021 season data', href='/ff-2020'),
        html.Br(),
    ])

def test():
    return html.Div([
        html.H1("Fantasy Football Data (test)", style={'text-align': 'center', 'background-color': 'lightblue'}),

    ])

def ff_data():
    return html.Div([
        html.H1("Fantasy Football Data", style={'text-align': 'center', 'background-color': 'lightblue'}),


    ])
