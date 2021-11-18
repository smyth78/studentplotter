import json

import dash_table
import dash_core_components as dcc
from dash.dependencies import Output,Input,State
from dash import no_update
import dash._callback_context as cb_ctx

from server import app
from constants import *
from dictionaries import *
from helper_modules.general_helpers import *
from helper_modules.categorical_helpers import *

def layout():
    return html.Div([
            html.Div(id='alert-cat-1'),
            html.Div(id='alert-cat-2'),
            html.Div([
                    dbc.Row(dbc.Col(html.H1(['Categorical']))),
                    dbc.Row([
                        dbc.Col(html.Div([
                            dcc.Dropdown(
                                placeholder='Choose the primary feature...',
                                id='pri-feature',
                                style={'display':'block'}),
                                ]),
                            width=6),
                        dbc.Col(html.Div([
                            dbc.Checklist(
                                id='show-sec-f',
                                options=[
                                    {'label': 'Split by category', 'value': 'sec-f'},
                                    {'label': 'Flip selected features', 'value': 'flip', 'disabled': True},
                                ],
                                value=[]
                                )]),
                            width=2),
                        dbc.Col(html.Div([
                                dcc.Dropdown(id='sec-feature', placeholder='Choose secondary feature...'),
                                ], id='secondary-feature-cat', style={'visibility':'hidden', 'font-size' : '85%'}),
                            width=4),
                        ], style={'margin-top': ROW_MARGIN}),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                    html.Div([
                                        dbc.RadioItems(
                                            id='chart-type',
                                            inline=True,
                                            options=[],
                                            value='group',
                                        )
                                    ], style={'margin-bottom':'10px'}),
                                    html.Div([

                                    html.Div([dbc.Input(id='title',
                                                        type='text',
                                                        placeholder='Add graph title...')
                                              ]),
                                    html.Div([], style={'padding-top': '10px'}),
                                ]),
                                html.Div([dbc.Checklist(
                                        id='hide-legend',
                                        options=[
                                            {'label': 'Display legend', 'value': 'hide'},
                                        ],
                                        inline=True,
                                        value=[]
                                    ),], id='hide-legend-div'),
                                html.Div([
                                    dbc.RadioItems(
                                        id='freq-choice',
                                        inline=True,
                                        options=[
                                            {'label': 'Frequency', 'value': 'freq'},
                                            {'label': 'Frequency density', 'value': 'probability density'},

                                        ],
                                        value='freq',
                                    ),
                                ], id='freq-choice-div'),
                                    html.Div([], style={'padding-bottom':'10px'}),
                                    html.Div([
                                        html.Div([
                                            dcc.Dropdown(
                                                placeholder='Choose scheme...',
                                                options=[{'label': i, 'value': i} for i in COLOUR_SCHEME],
                                                value='Light',
                                                id='colour-scheme')
                                        ], style={'margin-bottom': '10px'}),
                                        dbc.RadioItems(
                                            id='chart-custom-choice',
                                            inline=True,
                                            options=[
                                                {'label': 'Table', 'value': 'table'},
                                                {'label': 'Rescale', 'value': 'rescale'},
                                                {'label': 'Reorder', 'value': 'reorder'},

                                            ],
                                            value='',
                                        )
                                    ], style={'margin-bottom': '10px'}),
                                html.Div([
                                    html.Div([], id='customise-div'),
                                    html.Div([
                                        html.Div([], id='cat-freq-title'),
                                        dash_table.DataTable(
                                            style_cell={
                                                'height': 'auto',
                                                # all three widths are needed
                                                'minWidth': '10px', 'width': '20px', 'maxWidth': '30px',
                                                'whiteSpace': 'normal'
                                            },
                                            columns=[],
                                            data=[],
                                            id='cat-freq-table',
                                            export_format="csv",
                                        )
                                    ], id='table-div', style={'display': 'none'}),
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

                                    ], id='rescale-div', style={'display':'none'}),
                                    html.Div([
                                        html.P('Reorder groups...'),
                                        dbc.RadioItems(
                                            id='order',
                                            options=[
                                                {'label': 'Increasing', 'value': 'total ascending'},
                                                {'label': 'Decreasing', 'value': 'total descending'},
                                                {'label': 'Alphabetical', 'value': 'category ascending'},
                                                {'label': 'Any', 'value': 'trace'},
                                                {'label': 'Custom', 'value': 'array'}
                                            ],
                                            value='trace',
                                            labelStyle={'display': 'block', 'padding': '2px'},
                                        ),
                                        html.Div([
                                            dbc.Input(id='custom-order', type='text',
                                                      placeholder='Type order, seperate by comma...'),
                                        ], style={'visibility': 'hidden'},
                                            id='custom-order-div'),
                                    ], id='reorder-div', style={'display':'none'}),
                                    html.Div([
                                        html.Div([], style={'padding-top': 10}),
                                        dcc.Markdown('###### Collect small groups'),
                                        html.Div([
                                            html.Div([
                                                dbc.Input(id='group-size',
                                                          type='text',
                                                          placeholder='Size'),
                                            ]),
                                            html.Div([
                                                dbc.Input(id='small-name',
                                                          type='text',
                                                          placeholder='Name',
                                                          value='Other'),
                                            ]),
                                            html.Div([
                                                html.Div(id='removed',
                                                         style={'width': '100%', 'padding': '10px',
                                                                })
                                            ], style={'padding-top': '10px'})
                                        ], id='small-groups-div', style={'display': 'block'}),
                                    ], id='collect-div', style={'display':'block'}),

                                ]),
                        ], style={'margin-top': '30px'})], width=4),
                        dbc.Col([
                            html.Div([
                                    dcc.Graph(id='chart'),
                                ]),
                        ], width=8)
                    ]),
                ]),
        ])

# simple callback to show sec-f option
@app.callback(Output('secondary-feature-cat', 'style'),
             [Input('show-sec-f', 'value')])
def get_data(sec_f):
    hidden = {'visibility': 'hidden', 'font-size': '85%'}
    visibile = {'visibility': 'visible','font-size': '85%'}
    if sec_f is not None and sec_f != []:
        if 'sec-f' in sec_f:
            return visibile
        else:
            return hidden
    else:
        return hidden

# when sec_chosen the option to flip is enabled
@app.callback(Output('show-sec-f', 'options'),
              Input('show-sec-f', 'value'),
)
def allow_flip_features(show_sec_f_checks):
    show_sec_selected = [
        {'label': 'Split feature by category', 'value': 'sec-f'},
    ]
    show_sec_not_selected = [
        {'label': 'Split feature by category', 'value': 'sec-f'},
        {'label': 'Flip selected features', 'value': 'flip', 'disabled': False},
    ]
    if 'sec-f' not in show_sec_f_checks:
        return show_sec_selected
    else:
        return show_sec_not_selected


# Call the Store and find the session data, output to option dropdown
@app.callback([Output('pri-feature', 'options'),
               Output('sec-feature', 'options'),
               Output('alert-cat-1', 'children')],
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
    df_num = df.select_dtypes(include=['number'])

    # find the cols not in numerical data
    cat_cols = [c for c in df.columns if c not in df_num.columns]

    # define categorical DF
    df = df[cat_cols]

    options = [{'label': i, 'value': i} for i in cat_cols]
    return options, options, alert


# this is for the bar and the textarea
@app.callback(
    [Output('chart', 'figure'),
     Output('removed', 'children'),
     Output('alert-cat-2', 'children'),
     Output('cat-freq-table', 'columns'),
     Output('cat-freq-table', 'data'),
     Output('cat-freq-title', 'children')],
    [Input('pri-feature', 'value'),
     Input('sec-feature', 'value'),
     Input('order', 'value'),
     Input('custom-order', 'value'),
     Input('title', 'value'),
     Input('chart-width', 'value'),
     Input('chart-height', 'value'),
     Input('group-size', 'value'),
     Input('small-name', 'value'),
     Input('chart-type', 'value'),
     Input('hide-legend', 'value'),
     Input('show-sec-f', 'value'),
     Input('colour-scheme', 'value'),
     Input('freq-choice', 'value')],
    [State('session','data'),
     State('show-sec-f', 'value'),
     State('chart-custom-choice', 'value')]
)
def update_histo(pri_feat, sec_feat, order, custom_order, title, width,
                 height, group_size, group_name, chart_type, hide_leg, sec_f_check,
                 colour_scheme, freq_choice, data, is_split, custom_choice):
    colour_scheme = get_colour_scheme(colour_scheme) if colour_scheme is not None else px.colors.qualitative.G10

    call_ct = cb_ctx

    # create vars for the cat-freq-table
    columns_f = no_update
    data_f = no_update
    cat_freq_title = no_update
    removed_strings_div = no_update

    # check if features are flip
    is_flip = True if 'flip' in is_split else False

    # check if the data is split by cat
    is_split = True if 'sec-f' in is_split else False

    # now set the alerts for any erroneous choices
    alert = None
    if chart_type == 'pie' and is_split:
        alert = html.Div([no_pie])
        return no_update, no_update, alert, no_update, no_update, no_update
    if chart_type == 'pie' and custom_choice == 'reorder':
        # don't need to return this
        alert = html.Div([pie_order])
        return no_update, no_update, alert, no_update, no_update, no_update
    if chart_type == 'stack' and sec_feat is None:
        alert = html.Div([not_split])
        return no_update, no_update, alert, no_update, no_update, no_update

    # get the data into a PD
    data = json.loads(data)
    df = pd.DataFrame.from_dict(data, orient='columns')

    # set the legend variable
    show_leg = False if hide_leg else True

    # check to see if bar or pie
    is_bar = True if chart_type == 'stack' or chart_type == 'group' else False

    # set the title of the chart and x-axis
    if title is None:
        title = 'Bar Chart' if is_bar else 'Pie Chart'

    # freq-choice ie density or not?
    freq_choice = freq_choice if freq_choice == 'probability density' else None
    y_title = 'Frequency' if freq_choice is None else 'Frequency density'

    # decide type of chart
    chart = 'none'
    if pri_feat and (sec_f_check == [] or sec_f_check is None):
        chart = 'primary'
    elif pri_feat and not sec_feat:
        chart = 'primary'
    elif pri_feat and sec_feat:
        chart = 'secondary'
    if chart_type == 'pie' and chart == 'primary':
        chart = 'pie'

    # collect small -> only implemented for non-split data ONLY
    if not is_split:
        try:
            df, removed_values = collect_small_groups(df, pri_feat, sec_feat, group_size, group_name)
            # create a list of html - strings of removed values as a div
            removed_strings_div = create_removed_strings_div(removed_values)

        except TypeError:
            print('No size entered')

    fig = no_update

    if chart == 'primary' or chart == 'pie':
        alert = None
        dff = df.groupby(pri_feat).size().reset_index(name='Frequency').rename(columns={'Col1': 'Col_value'})
        dff.reset_index(drop=True, inplace=True)
        column_names = [pri_feat, 'Freq']
        columns_f, data_f = create_freq_table(dff, column_names, False)
        cat_freq_title = 'Frequency table:'

        # create the charts on px
        column_names = list(dff.columns)
        if chart == 'primary':
            # bar chart
            fig = px.histogram(dff, x=column_names[0], y=column_names[1], barmode=chart_type, template="simple_white",
                               width=LARGE_WIDTH * width, height=LARGE_HEIGHT * height, histnorm=freq_choice,
                               color_discrete_sequence=colour_scheme)

        # else must be a pie
        else:
            fig = px.pie(dff, names=column_names[0], values=column_names[1], template="simple_white",
                         width=LARGE_WIDTH*width, height=LARGE_HEIGHT*height, color_discrete_sequence=colour_scheme)

    elif chart == 'secondary':
        columns_f, data_f = no_update, no_update
        # need to remove 'Nones' and check for duplicate features
        if sec_feat != pri_feat and sec_feat is not None:
            # swap features if is_flip
            if is_flip:
                pri_feat, sec_feat = sec_feat, pri_feat
            # get the unique values of the secondary feature
            sec_cats = np.unique(df[sec_feat].values)
            colours, alert = get_unique_colours(colour_scheme, len(sec_cats))

            df, y_names, list_for_df_freq_table, column_names = split_cat_data_by_sec_f(df, pri_feat, sec_feat)

            fig = px.histogram(df, x=sec_feat, y=y_names, barmode='group', template="simple_white",
                               width=LARGE_WIDTH*width, height=LARGE_HEIGHT*height, histnorm=freq_choice,
                               color_discrete_sequence=colour_scheme)

            columns_f, data_f = create_freq_table(list_for_df_freq_table, column_names, True)
            cat_freq_title = '2-way table:'
    if fig != no_update:
        fig.update_layout(title_text=title, title_x=0.5, showlegend=show_leg, bargroupgap=0.1, legend=dict(title=None))
        if custom_order is not None:
            custom_order = custom_order.split(',')
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black', categoryorder=order,
                         categoryarray=custom_order)
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black', title=y_title)

    return fig, removed_strings_div, alert, columns_f, data_f, cat_freq_title

# show the custom order div
@app.callback(
    Output('custom-order-div', 'style'),
    [Input('order', 'value'),
     ]
)
def show_custom_div(show_div):
    return {'display': 'inline-block', 'visibility': 'visible' if show_div == 'array' else 'hidden', 'width': '49%'}


# show the small groups div
@app.callback(
    Output('collect-div', 'style'),
    [Input('show-sec-f', 'value')]
)
def show_small_div(sec_f):
    return {'display': 'block' if sec_f == [] else 'none'}


# show freq table
@app.callback(
    Output('cat-freq-div', 'style'),
    [Input('show-freq-table', 'value')]
)
def show_freq_div(show_div):
    return {'display': 'block' if show_div == ['show-tab'] else 'none'}


# disable legend button when approp
@app.callback(
    [Output('freq-choice-div', 'style'),
     Output('hide-legend', 'options'),
     Output('hide-legend', 'value')],
    [Input('show-sec-f', 'value'),
     Input('chart-type', 'value')]
)
def show_freq_div(show_sec_f, chart_type):
    options = [{'label': 'Hide legend', 'value': 'hide'}]
    options_dis = [{'label': 'Show legend', 'value': 'hide', 'disabled': True}]
    visible = {'display': 'block'}
    invisible = {'display': 'none'}

    if chart_type == 'pie':
        if 'sec-f' not in show_sec_f:
            return invisible, options, []
        else:
            return invisible, options_dis, ['hide']
    else:
        return visible, [], []

# disable stacked button and reorder when approp
@app.callback(
    [Output('chart-type', 'options'),
     Output('chart-custom-choice', 'options')],
    [Input('show-sec-f', 'value'),
     Input('chart-type', 'value')],
    State('sec-feature', 'value')
)
def disable_stacked_button(show_check, chart_type, sec_value):
    # cannot choose stacked if not split and cannot reorder a pie chart
    is_pie = True if chart_type == 'pie' else False
    is_sec = True if 'sec-f' in show_check else False

    custom_options = [
          {'label': 'Table', 'value': 'table'},
          {'label': 'Rescale', 'value': 'rescale'},
          {'label': 'Reorder', 'value': 'reorder', 'disabled': True if is_pie else False},
    ]
    options_single = [{'label': 'Bar', 'value': 'group'}, {'label': 'Stacked', 'value': 'stack', 'disabled': True}, {'label': 'Pie', 'value': 'pie'}]
    options_split = [{'label': 'Bar', 'value': 'group'}, {'label': 'Stacked', 'value': 'stack'}, {'label': 'Pie', 'value': 'pie', 'disabled': True}]

    if is_sec:
        return options_split, custom_options
    else:
        return options_single, custom_options

# populate the customised div on bar chart
@app.callback(
    [Output('table-div', 'style'),
     Output('rescale-div', 'style'),
     Output('reorder-div', 'style')],
    [Input('chart-custom-choice', 'value')]
)
def show_freq_div(choice):
    visible = {'display': 'block'}
    invis = {'display': 'none'}
    if choice == 'table':
        return visible, invis, invis
    elif choice == 'rescale':
        return invis, visible, invis
    elif choice == 'reorder':
        return invis, invis, visible
    else:
        return no_update, no_update, no_update



