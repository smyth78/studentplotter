import json
import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State, MATCH, ALL
from dash import no_update
import plotly.express as px
import dash._callback_context as cb_ctx
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go


from helper_modules.alerts import *
from helper_modules.numerical_helpers import *
from constants import *
from dictionaries import *
from helper_modules.general_helpers import *
from helper_modules.categorical_helpers import *

from server import app


def layout():
    return html.Div([
            html.Div(id='alert-num-1'),
            html.Div(id='alert-num-2'),
            # this store is for the combined feature list
            dcc.Store(id='comb-feature-list-store', storage_type='session'),
            dcc.Store(id='comb-feat-index', storage_type='session', data='0'),
                html.Div([
                        dbc.Row(
                            dbc.Col(html.H1(['Numerical']))),
                    ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Tabs([
                            dbc.Tab(label='Main', children=[
                                main_children()
                            ]),
                            dbc.Tab(label='Combine', children=[
                                dbc.Row(dbc.Col([dcc.Markdown('##### Combine only **continuous** features')]),
                                        style={'padding-top': ROW_MARGIN}),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("Add feature", color="primary", id='combine-add', n_clicks=0)
                                    ], width=1),
                                    dbc.Col([
                                        dbc.Button("Delete feature", color="danger", id='combine-delete', n_clicks=0)
                                    ], width=1),
                                    dbc.Col([
                                        dbc.Button("Draw features", color="success", id='num-draw', n_clicks=0)
                                    ], width={'size': 1,  'offset': 1}),

                                ], style={'padding-top': ROW_MARGIN}),
                                dbc.Row([dbc.Col(width=12, id='comb-feat-rows')]),

                                dbc.Row([
                                        dbc.Col([
                                            html.Div([dbc.Input(id='comb-title',
                                                                type='text',
                                                                placeholder='Add graph title...')
                                                      ], style={'margin-bottom': ROW_MARGIN,
                                                                'margin-top': ROW_MARGIN}),
                                            html.Div([dbc.Input(id='comb-x-axis-title',
                                                                type='text',
                                                                placeholder='Add x-axis label...')
                                                      ], style={'margin-bottom': ROW_MARGIN,
                                                                'margin-top': ROW_MARGIN}),
                                            html.Div([
                                                dcc.Dropdown(
                                                    placeholder='Choose scheme...',
                                                    options=[{'label': i, 'value': i} for i in COLOUR_SCHEME],
                                                    value='Light',
                                                    id='comb-colour-scheme')
                                            ], style={'margin-bottom': ROW_MARGIN}),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.RadioItems(
                                                        id='comb-chart-custom-choice',
                                                        inline=True,
                                                        options=[
                                                            {'label': 'Table', 'value': 'table'},
                                                            {'label': 'Rescale', 'value': 'rescale'},
                                                        ],
                                                        value='',
                                                        style={'margin-bottom': ROW_MARGIN}
                                                    ),
                                                ], width=5),
                                                dbc.Col([
                                                    dbc.Checklist(
                                                        options=[
                                                            {"label": "Show stats", "value": 1},
                                                        ],
                                                        value=[],
                                                        id="comb-show_summary-stats",
                                                        switch=True,
                                                    ),
                                                    get_average_switches(True)
                                                ], width=7),
                                            ]),
                                            html.Div([
                                                html.Div([html.Div([no_table])], id='comb-table-alert'),
                                                html.Div([], id='comb-chart-table-title'),
                                                dash_table.DataTable(
                                                    style_cell={
                                                        'height': 'auto',
                                                        # all three widths are needed
                                                        'minWidth': '20px', 'width': '25px', 'maxWidth': '30px',
                                                        'whiteSpace': 'normal'
                                                    },
                                                    columns=[],
                                                    data=[],
                                                    id='comb-main-freq-table',
                                                    export_format="csv",
                                                ),
                                                dbc.Row([
                                                    dbc.Col([
                                                        dbc.Label("Min value"),
                                                        dbc.Input(type="number", id='comb-min'),
                                                    ], width=4),
                                                    dbc.Col([
                                                        dbc.Label("Group width"),
                                                        dbc.Input(type="number", id='comb-bin-width'),
                                                    ], width=4),
                                                ], style={'padding-top': ROW_MARGIN}),

                                            ], id='comb-table-div', style={'display': 'none'}),
                                            html.Div([
                                                html.P('Rescale dimensions...'),
                                                dcc.Slider(
                                                    id='comb-chart-width',
                                                    min=0.1,
                                                    max=2.1,
                                                    step=.1,
                                                    value=1.4,
                                                ),
                                                dcc.Slider(
                                                    id='comb-chart-height',
                                                    min=0.1,
                                                    max=2.1,
                                                    step=.1,
                                                    value=1.4,
                                                ),

                                            ], id='comb-rescale-div', style={'display': 'none'}),

                                        ], width=4),
                                        dbc.Col(dcc.Graph(id='comb-num-chart'), width=8)]),
                                dbc.Row([
                                    dbc.Col([], id='comb-freq-table-div', width={'size': 4, 'offset': 1}),
                                    dbc.Col([], id='comb-stats-summary-div', width={'size': 4, 'offset': 1}),
                                ], style={'padding-bottom': BIG_MARGIN})
                            ]),
                        ])
                    ])
                ]),

            ])

# Call the Store and find the session data, output to MAIN option dropdown
@app.callback(Output('main-grouping-div', 'style'),
              [Input('main-data-type', 'value')])
def get_data(d_type):
    style = {'display': 'none' if 'cont' in d_type else 'block'}
    return style

# Call the Store and find the session data, output to MAIN option dropdown
@app.callback([Output('pri-num-feature', 'options'),
               Output('sec-num-cat-feature', 'options'),
               Output('alert-num-1', 'children')],
              [Input('session', 'modified_timestamp')],
              [State('session', 'data')])
def get_data(analyse_link, data):
    # add alerts
    if data is None or data == '' or data == []:
        alert = html.Div([no_data])
    else:
        alert = no_update
    # get the data from the store (could change this to a DB call? but not need as data is immuatbel)
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data, orient='columns')

    # get numerical data
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    df_num = df.select_dtypes(include=numerics)

    # find the num cols
    num_cols = [c for c in df.columns if c in df_num.columns]

    # find the cols not in numerical data
    cat_cols = [c for c in df.columns if c not in df_num.columns]

    num_options = [{'label': i, 'value': i} for i in num_cols]
    cat_options = [{'label': i, 'value': i} for i in cat_cols]
    return num_options, cat_options, alert

# this callback is for the main tab simple graph
@app.callback(
    [Output('main-chart', 'figure'),
     Output('main-stats-summary-div', 'children'),
     Output('main-table-alert', 'children'),
     Output('main-freq-table-div', 'children'),
     Output("main-show-cum-f", 'options'),
     Output('sec-num-cat-feature-div', 'style')],
    [Input('pri-num-feature', 'value'),
     Input('sec-num-cat-feature', 'value'),
     Input('freq-choice-num', 'value'),
     Input('main-chart-type', 'value'),
     Input('main-title', 'value'),
     Input('main-colour-scheme', 'value'),
     Input('main-chart-width', 'value'),
     Input('main-chart-height', 'value'),
     Input('main-min', 'value'),
     Input('main-bin-width', 'value'),
     Input('main-data-type', 'value'),
     Input('main-grouping-type', 'value'),
     Input("main-show-cum-f", 'value'),
     Input("main-show-mean", 'value'),
     Input("main-show-median", 'value')],
    [State('session', 'data')]
)
def update_main_chart(pri_feat, sec_f, freq_choice, chart_type, title, colour_scheme, width, height, bin_min, bin_width, d_type,
                      grouping, show_cum, show_mean, show_median, data):
    colour_scheme = get_colour_scheme(colour_scheme) if colour_scheme is not None else px.colors.qualitative.G10

    # get the data into a PD
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data, orient='columns')

    table_ss = None
    table_freq = None
    bin_edges = None
    counts = None
    data_f = None
    columns_f = None
    alert = None
    sec_num_cat_feature_div_style = no_update

    fig = no_update

    style_show_cf_switch = [{"label": "Show CF", "value": 'show-cf', 'disabled': False if chart_type == 'hist' else True}]

    # freq-choice ie density or not?
    freq_choice = freq_choice if freq_choice == 'probability density' else None
    y_title = 'Frequency' if freq_choice is None else 'Frequency density'

    is_bins_set = True if (bin_min is not None and bin_width is not None) else False

    if pri_feat is not None:
        # need to check bin_width is 'sensible'!
        x_vals = df[pri_feat].values

        if is_bins_set:
            if (max(x_vals) - min(x_vals)) / bin_width > MAX_BINS:
                alert = html.Div([too_many_groups])
                return no_update, no_update, alert, no_update, no_update

        is_grouped = True if grouping == 'grouped' else False
        is_continuous = True if d_type == 'cont' else False
        is_show_cf = True if 'show-cf' in show_cum else False
        is_split = True if not is_continuous and chart_type == 'hist' and sec_f else False

        sec_num_cat_feature_div_style = {'display': 'block' if not is_continuous and chart_type == 'hist' else 'none'}

        # if the data is grouped
        if is_grouped:
            if not is_bins_set:
                bin_min = min(x_vals)
                bin_width = (max(x_vals) - min(x_vals))/10
            bin_edges = get_bin_edges(is_continuous, x_vals, bin_min, bin_width)
            counts, bin_edges = np.histogram(x_vals, bins=bin_edges)
            # make freq table columns and data
            columns_f, data_f = make_freq_table_cols_data(is_continuous, True, counts, bin_edges, pri_feat)

        # if the data is not grouped
        else:
            # if ungrouped make new df:
            dff = df.groupby(pri_feat).size().reset_index(name='Count').rename(
                columns={'Col1': 'Col_value'})
            dff.reset_index(drop=True, inplace=True)

            # create the table for freq table for DISC - > create a df of the info
            columns_f, data_f = make_freq_table_cols_data(is_continuous, False, dff['Count'].values,
                                                          dff[pri_feat].values, pri_feat)
        table_ss = make_ss_dash_table(df[pri_feat].values, False, None)
        table_freq = make_ss_freq_table(columns_f, data_f, False, None)

        fig = make_subplots(specs=[[{"secondary_y": True}]]) if is_show_cf and chart_type == 'hist' else go.Figure()

        # first look to find the exception when the data is discrete and split
        if is_split:
                # add a warning if they choose box and try to split....
                # ungrouped only
                # need to make a dff for this data
                #     col_names, data_f = split_disc_data_by_sec_f(df, pri_feat, sec_f)
                dff, y_names, list_for_df_freq_table, column_names  = split_cat_data_by_sec_f(df, sec_f, pri_feat)
                # reverse the order of features cuase looks better on eye in table
                dff_for_table, y_names_for_2_way, list_for_df_freq_table_for_2_way, column_names_for_2_way = \
                    split_cat_data_by_sec_f(df, pri_feat, sec_f)
                list_for_df_freq_table_for_2_way[0][0] = pri_feat
                columns_f, data_f = create_freq_table(list_for_df_freq_table_for_2_way, column_names_for_2_way, True)
                table_freq = make_ss_freq_table(columns_f, data_f, False, None)
                list_of_x_vals_inc_pri_f = []
                for sec_name in y_names:
                    list_of_x_vals_inc_pri_f.append([dff[sec_name].values, sec_name])
                table_ss = make_comb_ss_table_div(list_of_x_vals_inc_pri_f, y_names, None, False)
        if chart_type == 'hist':
            if is_grouped:
                data_names = None
                if not is_continuous:
                    # histo - is_cont, custom bin
                    data_names = []
                    for dic in data_f:
                        data_names.append(dic[pri_feat])
                fig.add_trace(go.Bar(
                    x=bin_edges.tolist() if is_continuous else data_names,
                    y=counts.tolist(),
                    offset=0 if is_continuous else -0.5,
                    marker={
                        'line': {
                            'width': 1,
                            'color': 'white'},
                        'color': colour_scheme[0]
                    },
                ))
            else:
                if is_split:
                    # fig = px.bar(dff, x=y_names, y=dff, color=sec_f, barmode="group")
                    fig = px.histogram(dff, x=pri_feat, y=y_names, barmode='group', template="simple_white",
                                       width=LARGE_WIDTH * width, height=LARGE_HEIGHT * height, histnorm=freq_choice,
                                       color_discrete_sequence=colour_scheme)
                    fig.update_xaxes(type='category')
                    fig.update_layout(
                        legend_title='',
                        bargroupgap=0.1
                        )
                else:
                    values = dff[pri_feat].tolist()
                    nums_as_cats = [str(x) for x in values]
                    fig.add_trace(go.Bar(
                        x=nums_as_cats,
                        y=dff['Count'].values,
                        offset=-0.4,
                        marker={
                            'line': {
                                'width': 1,
                                'color': 'white'},
                            'color': colour_scheme[0]
                        },
                    ))
                    fig.update_xaxes(type='category')
            fig.update_yaxes(secondary_y=False) if (is_show_cf and is_continuous) else None
            fig.update_layout(bargap=0 if is_continuous else 0.2, showlegend=True if is_split else False,
                              plot_bgcolor='white', width=LARGE_WIDTH * width, height=LARGE_HEIGHT * height)
            fig.update_yaxes(title=y_title, showline=True, linewidth=2, linecolor='black')

        elif chart_type == 'box':
            fig = px.box(df[pri_feat], orientation='h', template="simple_white", x=pri_feat,
                         width=LARGE_WIDTH*width, height=SMALL_HEIGHT*height, color_discrete_sequence=colour_scheme)
            fig.update_yaxes(title=None, showline=False)

        if is_show_cf and is_continuous:
            x_vals = df[pri_feat]

            if not is_bins_set:
                histo_data = np.histogram(x_vals, bins=10)
                bin_edges = histo_data[1].tolist()[1:]
                cum_sum = np.cumsum(histo_data[0])
            else:
                bin_edges = bin_edges.tolist()[1:]
                cum_sum = np.cumsum(counts)
            fig.add_trace(go.Scatter(x=bin_edges, y=cum_sum.tolist(), line=dict(color="black")), secondary_y=True)
            fig.update_layout(yaxis2=dict(
                              title="Cumulative Frequency",
                              overlaying="y",
                              side="right"))

        fig.update_layout(title_text=title, title_x=0.5)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black', title=pri_feat,
                         gridwidth=0.1, gridcolor='lightgrey')
        fig.update_xaxes(showgrid=True if is_continuous else False)

        # add the mean/median line
        mean, median = get_mean_median(x_vals)
        if 'show-mean' in show_mean:
            fig.add_shape(
                go.layout.Shape(type='line', xref='x', yref='paper',
                                x0=mean, y0=0, x1=mean, y1=1.1, line={'dash': 'dash', 'width': 3, 'color': 'green'}),
            )
        if 'show-median' in show_median:
            fig.add_shape(
                go.layout.Shape(type='line', xref='x', yref='paper',
                                x0=median, y0=0, x1=median, y1=1.1, line={'dash': 'dash', 'width': 3, 'color': 'blue'},
                                ))

    return fig, table_ss, alert, table_freq, style_show_cf_switch, sec_num_cat_feature_div_style


# populate the customised div on bar chart
@app.callback(
    [Output('main-table-options-div', 'style'),
     Output('main-rescale-div', 'style'),
     Output('main-stats-summary-div', 'style'),
     Output('main-freq-table-div', 'style')],
    [Input('main-chart-custom-choice', 'value'),
     Input("main-show-summary-stats", 'value'),
     Input('main-min', 'value'),
     Input('main-bin-width', 'value'),
     Input('main-data-type', 'value'),
     Input('main-grouping-type', 'value')
     ]
)
def show_freq_div(choice, show_stats, main_min, main_bin_width, data_t, grouping):
    visible = {'display': 'block'}
    invis = {'display': 'none'}
    stats_div = {'display': 'block'} if 1 in show_stats else {'display': 'none'}
    if choice == 'table':
        if grouping == 'ungrouped':
            return invis, invis, stats_div, visible
        elif main_min is not None and main_bin_width is not None:
            return visible, invis, stats_div, visible
        else:
            return visible, invis, stats_div, invis
    elif choice == 'rescale':
        return invis, visible, stats_div, invis
    else:
        return no_update, no_update, stats_div, invis

# populate the customised div on comb  chart
@app.callback(
    [Output('comb-table-div', 'style'),
     Output('comb-rescale-div', 'style'),
     Output('comb-stats-summary-div', 'style')],
    [Input('comb-chart-custom-choice', 'value'),
     Input("comb-show_summary-stats", 'value')]
)
def show_freq_div(choice, show_ss):
    visible = {'display': 'block'}
    invis = {'display': 'none'}
    show_ss = visible if 1 in show_ss else invis
    if choice == 'table':
        return visible, invis, show_ss
    elif choice == 'rescale':
        return invis, visible, show_ss
    else:
        return no_update, no_update, show_ss


# add a feature to combined charts
@app.callback(
    [Output('comb-feat-rows', 'children'),
     Output('comb-feat-index', 'data'),
     Output({'type': 'sec-f-div', 'index': ALL}, 'style')],
    [Input('combine-add', 'n_clicks'),
     Input('combine-delete', 'n_clicks')],
    [State('comb-feat-rows', 'children'),
     State('comb-feat-index', 'data'),
     State({'type': 'sec-f-div', 'index': ALL}, 'style'),
     State('session', 'data')]
)
def add_sub_comb_feats(add, delete, existing_rows, index, sec_f_divs, data):
    ctx = cb_ctx

    existing_rows = existing_rows if existing_rows is not None else []

    is_pri_only = True if len(existing_rows) > 0 else False

    index = int(index) + 1

    # get the data from the store
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data, orient='columns')

    # get numerical data
    df_num = df.select_dtypes(include=['number'])

    # find the num cols
    num_cols = [c for c in df.columns if c in df_num.columns]

    # find the cat cols
    cat_cols = [c for c in df.columns if c not in df_num.columns]
    cat_cols.insert(0, 'None')

    num_options = [{'label': i, 'value': i} for i in num_cols]
    cat_options = [{'label': i, 'value': i} for i in cat_cols]

    is_delete = False
    if ctx.callback_context.triggered[0]['prop_id'] == 'combine-add.n_clicks':
        try:
            existing_rows.append(dyanmic_feature_row(index, num_options, cat_options, is_pri_only))
        except:
            print('no existing rows')

    elif ctx.callback_context.triggered[0]['prop_id'] == 'combine-delete.n_clicks':
        try:
            is_delete = True
            existing_rows = existing_rows[:-1]
        except:
            print('no existing rows')

    rows_in_state = len(ctx.callback_context.states_list[2])

    if rows_in_state >= 1:
        if is_delete and rows_in_state == 2:
            styles = [{'display': 'block'}] * rows_in_state
        else:
            styles = [{'display': 'none'}] * rows_in_state
    else:
        styles = [{'display': 'block'}] * rows_in_state

    return existing_rows, index, styles

# dynamically draw num graphs using drop downs
@app.callback(
    [Output('comb-num-chart', 'figure'),
     Output('comb-table-alert', 'figure'),
     Output('comb-freq-table-div', 'children'),
     Output('comb-stats-summary-div', 'children')],
    [Input('num-draw', 'n_clicks'),
     Input('comb-title', 'value'),
     Input('comb-colour-scheme', 'value'),
     Input('comb-chart-width', 'value'),
     Input('comb-chart-height', 'value'),
     Input('comb-x-axis-title', 'value'),
     Input('comb-min', 'value'),
     Input('comb-bin-width', 'value'),
     Input('comb-show-mean', 'value'),
     Input('comb-show-median', 'value')],
    [State({'type': 'pri-num-feature', 'index': ALL}, 'value'),
     State({'type': 'sec-num-feature', 'index': ALL}, 'value'),
     State({'type': 'comb-chart-type', 'index': ALL}, 'value'),
     State('comb-num-chart', 'figure'),
     State('session', 'data')]
)
def dynamically_draw_comb_chart(draw_click, title, colour_scheme, width, height, x_title, bin_min, bin_width, show_mean,
                                show_median, pri_f, sec_f, chart_type, comb_figure, data):
    ctx = cb_ctx

    # get the data from the store
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data, orient='columns')

    fig = no_update
    alert = None
    freq_tables_div = no_update
    ss_tables_div = no_update

    try:
        # # get list of drop down vals type...
        parsed_inputs = parse_context_state(ctx)

        fig, alert, freq_tables_div, ss_tables_div = get_comb_figure(df, parsed_inputs, title, colour_scheme, width,
                                                                     height, x_title, bin_min, bin_width, show_mean,
                                                                     show_median)

    except IndexError:
        print('error creating combined charts')

    return fig, alert, freq_tables_div, ss_tables_div
