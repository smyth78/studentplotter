import json, sigfig, decimal
import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input,State
from dash import no_update
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from constants import *
from dictionaries import *
from helper_modules.categorical_helpers import get_unique_colours
from helper_modules.general_helpers import get_colour_scheme, make_ss_freq_table, make_ss_dash_table, get_mean_median
from helper_modules.alerts import *


def main_children():
    div = html.Div([
                main_feature_row(),
          dbc.Row([
              dbc.Col([
                  html.Div([dbc.Input(id='main-title',
                                      type='text',
                                      placeholder='Add graph title...')
                            ], style={'margin-bottom': ROW_MARGIN}),
                  html.Div([
                  ], style={'margin-bottom': ROW_MARGIN}, id='colour-scheme-num-main'),
                  dbc.Row([
                      dbc.Col([dbc.RadioItems(
                          id='main-chart-custom-choice',
                          inline=True,
                          options=[
                              {'label': 'Table', 'value': 'table'},
                              {'label': 'Rescale', 'value': 'rescale'},
                          ],
                          value='',
                      )], width=8),
                      dbc.Col([dbc.Checklist(
                          options=[
                              {"label": "Show stats", "value": 1},
                          ],
                          value=[],
                          id="main-show-summary-stats",
                          switch=True,
                      )], width=4),
                  ], style={'margin-bottom': ROW_MARGIN}),
                  html.Div([
                      html.Div([html.Div([no_table])], id='main-table-alert'),
                      dbc.Row([
                          dbc.Col([
                              dbc.Label("Min value"),
                              dbc.Input(type="number", id='main-min'),
                          ], width=4),
                          dbc.Col([
                              dbc.Label("Group width"),
                              dbc.Input(type="number", id='main-bin-width'),
                          ], width=4),
                      ], style={'padding-top': ROW_MARGIN}),

                  ], id='main-table-options-div', style={'display': 'none'}),
                  html.Div([
                      html.P('Rescale dimensions...'),
                      dcc.Slider(
                          id='main-chart-width',
                          min=0.1,
                          max=2.1,
                          step=.1,
                          value=1,
                      ),
                      dcc.Slider(
                          id='main-chart-height',
                          min=0.1,
                          max=2.1,
                          step=.1,
                          value=1,
                      ),

                  ], id='main-rescale-div', style={'display': 'none'}),

              ], width=4),
              dbc.Col([dcc.Graph(id='main-chart')], width=8)
            ]),
        dbc.Row([
            dbc.Col([], id='main-freq-table-div', width={'size': 4,  'offset': 1}),
            dbc.Col(['stats'], id='main-stats-summary-div', width={'size': 4,  'offset': 1}),
        ], style={'padding-bottom': BIG_MARGIN})
        ])
    return div

def combine_children(index):
    div = html.Div([
        dbc.Row([dbc.Col([
            dyanmic_feature_row(index)
        ], width=12, id='comb-feat-rows')])
    ])
    return div

def chart_choice():
    div = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.RadioItems(
                    id='main-chart-type',
                    options=[
                        {'label': 'Histogram/Bar', 'value': 'hist'},
                        {'label': 'Box', 'value': 'box'},
                    ],
                    value='hist',
                    inline=True
                ),
            ], width=6),
            dbc.Col([
                dbc.Col([dbc.Row([dbc.Checklist(
                options=[
                ],
                value=[],
                id="main-show-cum-f",
                switch=True)])]),
                get_average_switches(False)
            ], width=4),
        ])]
    )
    return div

def data_type():
    div = html.Div([
                    dbc.RadioItems(
                        id='main-data-type',
                        options=[
                            {'label': 'Continuous', 'value': 'cont'},
                            {'label': 'Discrete', 'value': 'disc'},
                        ],
                        value='disc',
                        inline=False
                    ),
                    ]
    )
    return div

def grouping_type():
    div = html.Div([
                    dbc.RadioItems(
                        id='main-grouping-type',
                        options=[
                            {'label': 'Grouped', 'value': 'grouped'},
                            {'label': 'Ungrouped', 'value': 'ungrouped'},
                        ],
                        value='ungrouped',
                        inline=False
                    ),
                    ]
    )
    return div

def dynamic_chart_choice(index):
    div = html.Div([
                    dbc.RadioItems(
                        id={'type': 'comb-chart-type', 'index': index},
                        options=[
                            {'label': 'Histogram', 'value': 'hist'},
                            {'label': 'Box', 'value': 'box'},
                        ],
                        value='box',
                        inline=True
                    ),
                    ]
    )
    return div


def main_feature_row():
    div = html.Div([
        dbc.Row(dbc.Col([dcc.Markdown('##### Single feature analysis')]),
                style={'padding-top': ROW_MARGIN}),
        dbc.Row([
        dbc.Col([
                dcc.Dropdown(
                    placeholder='Choose the primary feature...',
                    id='pri-num-feature',
                    style={'display': 'block'}),
                html.Div([
                    dcc.Dropdown(
                        placeholder='Split by cat...',
                        id='sec-num-cat-feature'),
                    dbc.RadioItems(
                        id='freq-choice-num',
                        inline=True,
                        options=[
                            {'label': 'Frequency', 'value': 'freq'},
                            {'label': 'Frequency density', 'value': 'probability density'},

                        ],
                        value='freq',
                        style={'padding-top':'5px'}
                    ),
                ], id='sec-num-cat-feature-div', style={'display': 'none'})
            ], width=4),
        dbc.Col([chart_choice()], width=5),
        dbc.Col([data_type()], width=2),
        dbc.Col([grouping_type()], width=1, id='main-grouping-div'),
    ], style={'margin-top': ROW_MARGIN, 'margin-bottom': BIG_MARGIN}),
    ])
    return div

def dyanmic_feature_row(index, pri_options, sec_options, is_pri_only):

    div = html.Div([dbc.Row([
        dbc.Col(
            html.Div(dynamic_dropdown(index, pri_options, 'pri-num-feature', 'Choose the primary feature...'),
                    ), width=4),
        dbc.Col(
            html.Div(dynamic_dropdown(index, sec_options, 'sec-num-feature', 'Split by category?'),
            ), width=4, id={'type': 'sec-f-div', 'index': index}, style={'display': 'none' if is_pri_only else 'block'}),
        dbc.Col(dynamic_chart_choice(index), width=3),
    ], style={'margin-top': ROW_MARGIN, 'margin-bottom': ROW_MARGIN}),
    ])
    return div

def dynamic_dropdown(index, option_list, name, placeholder):
    drop_down = dcc.Dropdown(
                    placeholder=placeholder,
                    id={'type': name, 'index': index},
                    style={'display': 'block'},
                    options=option_list,
                    value=''
    ),
    return drop_down

def split_df_by_sec_f(df, sec_f):
    new_dfs = []
    sec_f_titles = []
    dff = df.copy()
    # get number of discrete labels in secondary data columns
    sec_f_options = df.groupby(sec_f).size().reset_index(name='Count').rename(columns={'Col1': 'Col_value'})
    sec_f_options.reset_index(drop=True, inplace=True)

    distinct_sec_f_options = sec_f_options.iloc[:, 0]

    for i, sec_f_option in enumerate(distinct_sec_f_options):
        new_df = dff[dff[sec_f] == sec_f_option]
        new_dfs.append(new_df)
        sec_f_titles.append(sec_f_option)
    return new_dfs, sec_f_titles

def parse_context_state(ctx):
    parsed_inputs = []
    for comp_states in ctx.callback_context.states_list:
        try:
            input_context = []
            for comp_dy_id in comp_states:
                this_index = comp_dy_id['id']['index']

                if this_index > 0:
                    if comp_dy_id['id']['type'] == 'pri-num-feature':
                        val = comp_dy_id['value']
                        input_context.append(val)
                    elif comp_dy_id['id']['type'] == 'sec-num-feature':
                        input_context.append(comp_dy_id['value'])
                    elif comp_dy_id['id']['type'] == 'comb-chart-type':
                        input_context.append(comp_dy_id['value'])
            parsed_inputs.append(input_context)
        except:
            print('not of right form')
    return parsed_inputs


def get_comb_figure(df, parsed_inputs, title, colour_scheme, width, height, x_title, bin_min, bin_width, show_mean,
                    show_median):
    is_split = False if len(parsed_inputs[0]) > 1 else True

    pri_f = None
    chart = None
    chart_list = None
    sec_f_titles = None
    mixed_chart_types = False
    includes_cum_f = False
    includes_box  = False
    includes_hist = False
    is_bins_set = True if (bin_min is not None and bin_width is not None) else False
    freq_tables_div = no_update
    ss_tables_div = no_update
    mean, median = None, None


    if is_split:
        # one pri_f only
        pri_f = parsed_inputs[0][0]
        sec_f = parsed_inputs[1][0]
        chart = parsed_inputs[2][0]

        # add the mean/median line
        mean, median = get_mean_median(df[pri_f].values)

        if sec_f == '':
            return no_update, html.Div([select_sec_f_or_another_f]), no_update, no_update

        # pri_f_list is a list of dataframes split by sec_f
        pri_f_list, sec_f_titles = split_df_by_sec_f(df, sec_f)
        unique_colours, alert = get_unique_colours(get_colour_scheme(colour_scheme), len(sec_f_titles))

        list_of_x_vals_inc_pri_f  = [[dff[pri_f].values, pri_f] for dff in pri_f_list]
    else:
        # can be 1 pri_f or mutliple....

        # pri_f_list is a list of pri features names
        pri_f_list = parsed_inputs[0]
        chart_list = parsed_inputs[2]
        list_of_x_vals_inc_pri_f = [[df[pri_f_from_list].values, pri_f_from_list] for pri_f_from_list in pri_f_list]

        unique_colours, alert = get_unique_colours(get_colour_scheme(colour_scheme), len(pri_f_list))

        mixed_chart_types = not all_equal(chart_list)
        includes_cum_f = True if 'cum_f' in chart_list else False
        includes_box = True if 'box' in chart_list else False
        includes_hist = True if 'hist' in chart_list else False

        # get popoulaiton mean/median
        # add the mean/median line
        pop_x_vals = []
        for x_vals in list_of_x_vals_inc_pri_f:
            pop_x_vals.append(x_vals[0])
        mean, median = get_mean_median(pop_x_vals)

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.01,
                        specs=[[{"rowspan": 1, "colspan": 1}], [{"rowspan": 2, "colspan": 1}], [{}]]) if \
        mixed_chart_types else go.Figure()

    pri_f_list_titles = []
    for pri_f_title_extra in list_of_x_vals_inc_pri_f:
        pri_f_list_titles.append(pri_f_title_extra[1])

    ss_tables_div = make_comb_ss_table_div(list_of_x_vals_inc_pri_f, pri_f_list_titles, sec_f_titles, is_split)

    # can only get the freq table if the bins are set
    if is_bins_set:
        # make the freq table divs (only show if bins set) and ss_summary divs
        freq_table_data = []
        for x_vals_pri_f in list_of_x_vals_inc_pri_f:
            bin_edges = get_bin_edges(True, x_vals_pri_f[0], bin_min, bin_width)
            counts, bin_edges = np.histogram(x_vals_pri_f[0], bins=bin_edges)
            # make freq table columns and data
            columns_f, data_f = make_freq_table_cols_data(True, True, counts, bin_edges, x_vals_pri_f[1])
            freq_table_data.append([columns_f, data_f])

        # This is to decide which titles to add to the table
        if is_split:
            titles = sec_f_titles
        elif not is_split and set(pri_f_list) == 1:
            titles = [pri_f] * len(freq_table_data)
        else:
            titles = pri_f_list
        freq_tables_div = make_comb_freq_table_div(freq_table_data, titles)

    if not is_split:
        # need to reverse alpha it so hist is always drawn first
        chart_list.sort(reverse=True)

    # note: for split data DFs are used and iterated through, but when combining featerures we just use a list of pri_f names
    for i, data in enumerate(pri_f_list):

        this_chart_type = chart if is_split else chart_list[i]

        if this_chart_type == 'hist':
            x_vals = data[pri_f] if is_split else df[data]
            hist = go.Histogram(x=x_vals,
                                name=sec_f_titles[i] if is_split else data,
                                marker=dict(
                                    color=unique_colours[i],
                                    line=dict(color='rgba(0, 0, 0, 0.5)', width=1)))
            fig.add_trace(hist, row=2, col=1) if mixed_chart_types else fig.add_trace(hist)

            # need to check bin_width is 'sensible'!
            if is_bins_set:
                if (max(x_vals) - min(x_vals)) / bin_width > MAX_BINS:
                    alert = html.Div([too_many_groups])
                    return no_update, alert, no_update, no_update

            fig.update_traces(opacity=0.75)
            fig.update_traces(xbins=dict(
                start=bin_min,
                size=bin_width
            )) if is_bins_set else None

        elif this_chart_type == 'box':
            box_already_added = True
            name = sec_f_titles[i] if is_split else data
            # name = name if not mixed_chart_types else ''

            box = go.Box(x=data[pri_f] if is_split else df[data],
                         name=name,
                         fillcolor=unique_colours[i])

            fig.add_trace(box, row=1, col=1) if mixed_chart_types else fig.add_trace(box)

    fig.update_layout(barmode='overlay', title_text=title, title_x=0.5, showlegend=True, bargroupgap=0, legend=dict(title=None),
                      plot_bgcolor='white', width=LARGE_WIDTH*width, height=LARGE_HEIGHT*height)

    fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='lightgrey')
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', showticklabels=True,
                     title_text=pri_f if is_split else x_title,
                     row=2 if mixed_chart_types else None,
                     col=1 if mixed_chart_types else None)

    if 'show-mean' in show_mean:
        fig.add_shape(
            go.layout.Shape(type='line', xref='x', yref='paper',
                            x0=mean, y0=0, x1=mean, y1=1.1, line={'dash': 'dash', 'width': 3, 'color': 'green'})
        , row=2 if mixed_chart_types else None, col=1 if mixed_chart_types else None)
    if 'show-median' in show_median:
        fig.add_shape(
            go.layout.Shape(type='line', xref='x', yref='paper',
                            x0=median, y0=0, x1=median, y1=1.1, line={'dash': 'dash', 'width': 3, 'color': 'blue'},
                            ), row=2 if mixed_chart_types else None, col=1 if mixed_chart_types else None)
    if mixed_chart_types:
        for line in fig.layout.shapes:
            line['yref'] = 'paper'

    return fig, alert, freq_tables_div, ss_tables_div


def all_equal(iterator):
    return len(set(iterator)) <= 1


def get_bin_edges(is_cont, data_values, min_bin, bin_width):
    max_val = float(max(data_values))

    upper_limit = float(min_bin)
    bin_edges = [float(min_bin)]

    # find upper limit as multiple of bin width, equal to if discrete
    if is_cont:
        while upper_limit < max_val:
            upper_limit += float(bin_width)
            bin_edges.append(upper_limit)
    else:
        while upper_limit <= max_val:
            upper_limit += float(bin_width)
            bin_edges.append(upper_limit)
    return bin_edges


def make_freq_table_cols_data(is_cont, is_grouped, counts, bin_edges, pri_f):
    freq_df = create_table_df(is_cont, is_grouped, counts, bin_edges, pri_f)
    freq_df_dict = freq_df.to_dict('records')
    columns_f = [{"name": i, "id": i} for i in freq_df.columns]
    data_f = freq_df_dict

    return columns_f, data_f


def create_table_df(is_cont, is_grouped, counts, bin_edges, pri_f):
    table = []
    headings = [str(pri_f), 'F', 'CF']

    cf = 0
    for i, value in enumerate(bin_edges):
        # dont include last bin if continous...
        # the_range = len(bin_edges) - 1 if is_grouped else len(bin_edges)
        the_range = len(bin_edges) - 1
        if is_grouped:
            if i < the_range:
                if is_cont and is_grouped:
                    try:
                        row_group = str(sigfig.round(float(bin_edges[i]), 3)) + u' \u2264' + ' x < ' \
                                    + str(sigfig.round(float(bin_edges[i + 1]), 3))
                    except (KeyError, ValueError, decimal.InvalidOperation) as e:
                        row_group = str(float(bin_edges[i])) + u' \u2264' + ' x < ' \
                                    + str(float(bin_edges[i + 1]))
                    except IndexError:
                        print('index error')


                elif is_cont is False and is_grouped:
                    try:
                        row_group = str(int(sigfig.round(float(bin_edges[i]), 3))) + u' \u2264' + ' x < ' \
                                    + str(int(sigfig.round(float(bin_edges[i + 1]), 3)))
                    except (KeyError, ValueError) as e:
                        row_group = str(int(float(bin_edges[i]))) + u' \u2264' + ' x < ' \
                                    + str(int(float(bin_edges[i + 1])))
                row_count = counts[i]
                cf += counts[i]
                row_cf = cf
                complete_row = [row_group, row_count, row_cf]
                table.append(complete_row)
        else:
            if i < the_range + 1:
                row_group = str(bin_edges[i])
            row_count = counts[i]
            cf += counts[i]
            row_cf = cf
            complete_row = [row_group, row_count, row_cf]
            table.append(complete_row)

    freq_table = pd.DataFrame(table, columns=headings)

    return freq_table


def make_comb_freq_table_div(table_data_list, titles):
    tables_div = []
    sec_titles_added = []
    for i, table_data in enumerate(table_data_list):
        if titles[i] not in sec_titles_added:
            table = make_ss_freq_table(table_data[0], table_data[1], True, titles[i])
            tables_div.append(html.Div([]))
            tables_div.append(html.H5(titles[i]))
            # the table is a tuple, needs to be passed as only a dash table
            tables_div.append(table[0])
            tables_div.append(html.Div([]))
            sec_titles_added.append(titles[i])
    return tables_div

def make_comb_ss_table_div(x_vals_pri_f, pri_titles, sec_f_titles, is_split):
    ss_tables_div = []
    titles_appended = []
    titles = pri_titles if not is_split else sec_f_titles
    for i, x_vals_data in enumerate(x_vals_pri_f):
        if titles[i] not in titles_appended:
            table = make_ss_dash_table(x_vals_data[0], True, x_vals_data[1])[0]
            ss_tables_div.append(html.H5([titles[i]]))
            # the table is a tuple, needs to be passed as only a dash table
            ss_tables_div.append(table)
            ss_tables_div.append(html.Div([]))
            titles_appended.append(titles[i])
    return ss_tables_div

def get_average_switches(is_comb):
    div = dbc.Col([dbc.Row([dbc.Checklist(
        options=[
            {"label": "Show population mean" if is_comb else "Show mean", "value": 'show-mean', }
        ],
        value=[],
        id="comb-show-mean" if is_comb else "main-show-mean",
        style={'color': 'green'},
        switch=True)]),
    dbc.Row([dbc.Checklist(
        options=[
            {"label": "Show population median" if is_comb else "Show median", "value": 'show-median', }
        ],
        value=[],
        id="comb-show-median" if is_comb else "main-show-median",
        style={'color': 'blue'},
        switch=True)]),
    ])
    return div


def split_disc_data_by_sec_f(df, disc_feat, cat_feat):
    dff = df[[disc_feat, cat_feat]]
    print(dff)
    pri_cats = np.unique(df[disc_feat].values)
    sec_cats = np.unique(df[cat_feat].values)
    bar_counts = []
    for sec_cat in sec_cats:
        filtered_df = dff.loc[dff[cat_feat] == sec_cat]
        count_df = filtered_df[filtered_df[cat_feat] == sec_cat].shape[0]
        bar_counts.append(count_df)
    return sec_cats, bar_counts


