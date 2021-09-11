import base64
import io
import pandas as pd
import json

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_table
from dash import no_update

from server import app

def layout():
    return html.Div([
            dcc.Upload(
                id='datatable-upload',
                children=html.Div([
                    'Click here to ',
                    html.A('upload CSV file')
                ]),
                style={
                    'width': '30%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1px', 'borderStyle': 'dashed',
                    'borderRadius': '5px', 'textAlign': 'center', 'margin': 'auto'
                },
            ),
            html.Hr(),
            dash_table.DataTable(id='datatable-upload-container', style_table={'overflowX': 'auto'}),
        ])

@app.callback([Output('datatable-upload-container', 'data'),
               Output('datatable-upload-container', 'columns'),
               Output('session', 'data')],
               [Input('datatable-upload', 'contents')],
               [State('datatable-upload', 'filename'),
                State('session', 'data')])
def update_output(contents, filename, data):
    if contents is None:
        if data:
            data = json.loads(data)
            df = pd.DataFrame.from_dict(data, orient='columns')
            df = df.fillna('None')
        else:
            return [{}], [], no_update
    else:
        print(filename)
        df = parse_contents(contents, filename)
        df = df.fillna('None')
    df_json = df.to_json(orient='columns')
    df_dict = df.to_dict('records')
    return df_dict, [{"name": i, "id": i} for i in df.columns], df_json

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        except UnicodeDecodeError:
            print('unicode decode error')
            df = pd.read_csv(io.StringIO(decoded.decode("ISO-8859-1")))

        return df
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))
        return df


