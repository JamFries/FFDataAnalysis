import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_table

def index_page():
    return html.Div([
        html.H1("Fantasy Football Data", style={'text-align': 'center', 'background-color': 'lightblue'}),

        dcc.Link('Navigate to 2019-2020 season data', href='/ff-2019'),
        html.Br(),
        dcc.Link('Navigate to 2020-2021 season data', href='/ff-2020'),
        html.Br(),
        dcc.Link('Sortable Datatable', href='/table'),
        html.Br(),
        dcc.Link('Testing page', href='/test'),
        html.Br(),
    ])

# dataTable_page is the html layout that contains a table for users to sort players by specific stats
def dataTable_page(dataframe):
    return html.Div(children=[
        html.H1("Fantasy Football Data", style={'text-align': 'center', 'background-color': 'lightblue'}),

        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dataframe.columns],
            data=dataframe.to_dict('records'),

            filter_action='native',
            sort_action='native',

            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor='paleturquoise'),
            style_data=dict(backgroundColor='lavender')
        ),

        html.Div(id='table-container')
    ])

def test():
    return html.Div([
        html.H1("Fantasy Football Data (test)", style={'text-align': 'center', 'background-color': 'lightblue'}),


    ])

def ff_data():
    return html.Div([
        html.H1("Fantasy Football Data", style={'text-align': 'center', 'background-color': 'lightblue'}),


    ])
