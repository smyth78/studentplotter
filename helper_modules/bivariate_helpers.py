import numpy as np
from scipy import stats
from sigfig import round
import dash_table

import plotly.express as px
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

def get_corr_matrix(df):
    arrays = df.to_numpy()
    arrays = arrays.T
    return np.corrcoef(arrays)


def get_trendline_stats(df, ind_var, dep_var):
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[ind_var], df[dep_var])
    try:
        slope = round(float(slope), 3)
        intercept = round(float(intercept), 3)
        r_value = round(float(r_value), 3)
    except ValueError:
        pass
    return slope, intercept, r_value

def custom_legend(fig, name_change):
    for i, data in enumerate(fig.data):
        for elem in data:
            if elem == 'name':
                fig.data[i].name = name_change[fig.data[i].name]
    return fig



def add_annotation_stats(fig, slope, intercept, r_value):
    fig.add_annotation(text='y = {}x + {}'.format(slope, intercept) + '\n' + 'r = {}'.format(r_value),
                       xref="paper", yref="paper",
                       x=0.5, y=0.5, showarrow=False)

def get_table_rows(trendline_stats, cat_names):
    rows = []
    for i, stat in enumerate(trendline_stats):
        line = "y = {}x + {}".format(stat[0], stat[1])
        r_val = "r = {}".format(stat[2])
        row = {'Category': cat_names[i], 'Trendline': line, 'R-value': r_val}
        rows.append(row)
    return rows

def remove_current_outliers_from_list(ind_var, dep_var, removed_points, orig_df, sec_f):
    sub_df = orig_df[[ind_var, dep_var, sec_f]] if sec_f is not None else orig_df[[ind_var, dep_var]]

    for index, row in sub_df.iterrows():
        for point in removed_points:
            if point['x'] == row[ind_var] and point['y'] == row[dep_var]:
                sub_df.drop(index, inplace=True, errors='ignore')

    return sub_df

def select_sec_f_cat_based_on_row_vals(df, ind_var, dep_var, sec_f, x_val, y_val):
    updated_df = df.loc[(df[ind_var] == x_val)]
    updated_df = updated_df.loc[(df[dep_var] == y_val)]
    new_list = updated_df[sec_f].tolist()
    return new_list[0]


def get_point_strings_div(point_strings):
    text_inner_div = []
    for point in point_strings:
        text_inner_div.append(html.Div([point]))
    text_inner_div = html.Div(text_inner_div)
    div = html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([

                    dcc.Markdown('#### _Removed points_'),
                    text_inner_div
                    ], width=8),
                    dbc.Col([dbc.Button("Reset",
                                        color="danger",
                                        className="mr-1",
                                        id='reset-outliers',
                                        n_clicks=0)],
                            width=4)
            ])]),
            ])
        ])

    return div




