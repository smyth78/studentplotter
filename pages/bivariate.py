import json
import pandas as pd

import dash_table
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash import no_update

import plotly.graph_objs as go
import dash._callback_context as cb_ctx

from server import app
from constants import *
from dictionaries import *
from helper_modules.general_helpers import *
from helper_modules.bivariate_helpers import *
from helper_modules.alerts import *


def layout():
    return html.Div([
        # create the session store
        dcc.Store(id='store-points', storage_type='memory'),
        dcc.Store(id='session-num-data', storage_type='session'),
        html.Div(id='alert-bi-1'),

        # hidden div to store the ind and dep vars
        html.Div([
            dcc.Input(id='chosen-ind-var',
                      type='text',
                      style={'width': '100%'}),
            dcc.Input(id='chosen-dep-var',
                      type='text',
                      style={'width': '100%'}),
        ], style={'display': 'none'}),

        ## hidden drop down menus to store stored variables
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ind-var',
                    placeholder='Dep variable...',
                    style={'width': '35%', 'display': 'none', 'padding-left': '10px'}
                ),
                dcc.Dropdown(
                    id='dep-var',
                    placeholder='Independent variable...',
                    style={'width': '35%', 'display': 'none', 'padding-left': '10px'}
                ),
            ], style={'width': '100%'}),
        ]),

        html.Div([
            dbc.Row(dbc.Col(html.H1(['Bivariate']))),
            dbc.Row([
                dbc.Col([dcc.Graph(id='heatmap')], width={"size": 9, "offset": 1})
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Div([dbc.Input(id='title',
                                                type='text',
                                                placeholder='Add graph title...')
                                      ]),
                            html.Div([], style={'padding-top': '10px'}),
                        ]),
                        dbc.Checklist(
                            id='chart-ops',
                            options=[
                                {'label': 'Flip variables', 'value': 'flip'},
                                {'label': 'Show trend line', 'value': 'trend'},
                            ],
                            inline=True,
                            value=[]
                        ),
                        html.Div([], style={'padding-top': '10px'}),
                        html.Div([
                            html.Div([
                                html.P('Rescale dimensions...'),
                                dcc.Slider(
                                    id='chart-width',
                                    min=0.1,
                                    max=2.1,
                                    step=.1,
                                    value=1,
                                ),
                                dcc.Slider(
                                    id='chart-height',
                                    min=0.1,
                                    max=2.1,
                                    step=.1,
                                    value=1,
                                ),

                            ], id='rescale-div', style={'display': 'block'}),

                        ]),
                        html.Div([
                            dbc.Row([
                                dbc.Col(['Split by category?'], width=3),
                                dbc.Col([dcc.Dropdown(id='sec-feature-bi')], width=9),
                            ]),
                        ], id='sec-feature-bi-div'),
                        html.Div([dash_table.DataTable(
                            style_cell={
                                'textAlign': 'center',
                                # all three widths are needed
                                'minWidth': '50px', 'width': '50px', 'maxWidth': '50px',

                            },
                            style_cell_conditional=[
                                {'if': {'column_id': 'Category'},
                                 'width': '30%'},
                                {'if': {'column_id': 'Trendline'},
                                 'width': '45%'},
                                {'if': {'column_id': 'R-valued'},
                                 'width': '15%'}
                            ],
                            columns=[{'name': 'Category', 'id': 'Category'}, {'name': 'Trendline', 'id': 'Trendline'},
                                     {'name': 'R-value', 'id': 'R-value'}],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            id='bivar-summary-table',
                            export_format="csv",
                        )], id='summary-table-div'),
                        dbc.Row([dbc.Button("Reset", color="danger", className="mr-1", id='reset-outliers')],
                                id='removed-points-div', style={'visibility': 'hidden'})
                    ], style={'margin-top': '30px'})], width=5),
                dbc.Col([
                    html.Div([dcc.Graph(id='scatter')], id='chart-div'),
                ], width=7)
            ]),
        ]),
        html.Div([], style={'padding-bottom': '300px'})
    ])


# Call the Store and find the session data, output to heatmap
@app.callback([Output('session-num-data', 'value'),
               Output('heatmap', 'figure'),
               Output('sec-feature-bi', 'options')],
              [Input('session', 'modified_timestamp')],
              [State('session', 'data')])
def on_data(ts, data):
    try:
        data = json.loads(data)
    except:
        return no_update, no_update, no_update

    df = pd.DataFrame.from_dict(data, orient='columns')

    # get numerical data
    df_num = df.select_dtypes(include=['number'])

    # find the cols not in numerical data
    cat_cols = [c for c in df.columns if c not in df_num.columns]

    # # define categorical DF
    # df_cat = df[cat_cols]

    options = [{'label': i, 'value': i} for i in cat_cols]

    # drop catergorical
    df_num = df.select_dtypes(['number'])

    try:
        figure = {
            'data': [go.Heatmap(
                x=df_num.columns.values.tolist(),
                y=df_num.columns.values.tolist(),
                z=get_corr_matrix(df_num).tolist(),
                xgap=3,
                ygap=3
            )],
            'layout': go.Layout(
                paper_bgcolor='white',
                margin={'l': 250, 'b': 250, 'r': 50, 't': 70},
                plot_bgcolor='black',
                height=800,
                width=800
            )
        }

    except ValueError:
        print('not all numeric data are numbers')
        figure = None

    return data, figure, options


# updates the hidden div with chosen vars
@app.callback(
    [Output('chosen-ind-var', 'value'),
     Output('chosen-dep-var', 'value')],
    [Input('ind-var', 'value'),
     Input('dep-var', 'value'),
     Input('chart-ops', 'value')]
)
def update_hidden_div(ind_var, dep_var, flip):
    if 'flip' in flip:
        return dep_var, ind_var
    else:
        return ind_var, dep_var


# add click to heatmap -> updates the chosen indicators
@app.callback(
    [Output('ind-var', 'value'),
     Output('dep-var', 'value')],
    [Input('heatmap', 'clickData')],
)
def update_textarea(clicked_region):
    if clicked_region:
        return clicked_region['points'][0]['x'], clicked_region['points'][0]['y']
    else:
        return no_update, no_update


# this is for the scatter
@app.callback(
    [Output('chart-div', 'children'),
     Output('alert-bi-1', 'children'),
     Output('bivar-summary-table', 'data'),
     Output('summary-table-div', 'style'),
     Output('removed-points-div', 'children'),
    Output('removed-points-div', 'style'),
     Output('store-points', 'data')],
    [Input('chosen-ind-var', 'value'),
     Input('chosen-dep-var', 'value'),
     Input('title', 'value'),
     Input('chart-height', 'value'),
     Input('chart-width', 'value'),
     Input('sec-feature-bi', 'value'),
     Input('chart-ops', 'value'),
     Input('scatter', 'clickData'),
     Input('reset-outliers', 'n_clicks')],
    [State('session', 'data'),
     State('store-points', 'data')]
)
def plot_scatter(ind_var, dep_var, title, height, width, sec_f, options, clicked_point, reset, data, removed_points):
    alert = click_on_heatmap

    # get the data into a PD convert all numbers to floats
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data)
    orig_df = df.copy()

    ctx = cb_ctx

    trend = 'ols' if 'trend' in options else None
    show_table = {'display': 'block', 'visibility': 'visible' if 'trend' in options else 'hidden'}

    # get numerical data
    df_num = df.select_dtypes(include=['number'])

    # find the cols not in numerical data
    cat_cols = [c for c in df.columns if c not in df_num.columns]

    # # define categorical DF
    # df_cat = df[cat_cols]

    removed_points = removed_points or []

    # need to clear removed points list when sec_f is removed from plot
    if ctx.callback_context.triggered[0]['prop_id'] == 'sec-feature-bi.value':
        if sec_f is None:
            removed_points = []

    # clear outlier list
    if ctx.callback_context.triggered[0]['prop_id'] == 'reset-outliers.n_clicks':
        removed_points = []

    if ctx.callback_context.triggered[0]['prop_id'] == 'scatter.clickData':
        is_in_list = False
        if len(removed_points) != 0:
            for point in removed_points:
                if clicked_point['points'][0]['x'] == point['x'] and clicked_point['points'][0]['y'] == point['y']:
                    is_in_list = True

        removed_points.append(clicked_point['points'][0]) if not is_in_list else None

        df = remove_current_outliers_from_list(ind_var, dep_var, removed_points, df, sec_f)

    # write clicked points in textarea
    point_strings = []
    for point in removed_points:
        if sec_f:
            sec_f_cat = select_sec_f_cat_based_on_row_vals(orig_df, ind_var, dep_var, sec_f, point['x'], point['y'])
            point_string = '(' + str(point['x']) + ', ' + str(point['y']) + ') ' + sec_f_cat
        else:
            point_string = '(' + str(point['x']) + ', ' + str(point['y']) + ')'
        point_strings.append(point_string)

    point_string_visibility = 'visible' if len(point_strings) > 0 else 'hidden'

    chart_div = dcc.Graph(id='scatter')
    table_rows = []
    if ind_var and dep_var:
        fig = px.scatter(df, x=ind_var, y=dep_var, color=sec_f, template="simple_white",
                         height=LARGE_HEIGHT * height, width=LARGE_WIDTH * width, trendline=trend)
        if trend:
            trend_line_stats = []
            category_names = []
            if sec_f:
                dff = df.copy()
                # find the unique categories in the sec_f
                sec_cats = np.unique(dff[sec_f].values)
                for cat in sec_cats:
                    temp_df = dff.loc[dff[sec_f] == cat]
                    slope, intercept, r_value = get_trendline_stats(temp_df, ind_var, dep_var)
                    trend_line_stats.append([slope, intercept, r_value])
                    category_names.append(cat)
            else:
                # pass in data as a list
                slope, intercept, r_value = get_trendline_stats(df, ind_var, dep_var)
                trend_line_stats.append([slope, intercept, r_value])
                category_names.append('Population')
            table_rows = get_table_rows(trend_line_stats, category_names)

        fig.update_layout(title_text=title, title_x=0.5, legend=dict(title=None))
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
        alert = None

        chart_div = dcc.Graph(figure=fig, id='scatter')

    point_strings_div = get_point_strings_div(point_strings)
    point_strings_style = {'visibility': point_string_visibility}

    return chart_div, alert, table_rows, show_table, point_strings_div, point_strings_style, removed_points

