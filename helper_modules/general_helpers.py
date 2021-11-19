import decimal

import numpy as np
import pandas as pd
import sigfig
import random

import plotly.express as px
import dash_table
import dash_html_components as html
import dash_core_components as dcc

from dictionaries import *

def shuffle_and_return(x):
  random.shuffle(x)
  return x

def get_random_colour_stuff(id):
    colour_options = shuffle_and_return([{'label': i, 'value': i} for i in COLOUR_SCHEME])
    starting_colour = random.choice(colour_options)

    colour_div = dcc.Dropdown(
        placeholder='Choose scheme...',
        options=colour_options,
        value=starting_colour,
        id=id)
    return colour_div

def get_colour_scheme(colour_scheme):
    colour_scheme = colour_scheme['value'] if type(colour_scheme) == dict else colour_scheme
    if colour_scheme == 'Light':
        return px.colors.qualitative.Light24
    elif colour_scheme == 'Dark':
        return px.colors.qualitative.Dark24
    elif colour_scheme == 'Pastel':
        return px.colors.qualitative.Pastel1
    elif colour_scheme == 'Antique':
        return px.colors.qualitative.Antique
    elif colour_scheme == 'Bold':
        return px.colors.qualitative.Bold
    elif colour_scheme == 'Safe':
        return px.colors.qualitative.Safe
    elif colour_scheme == 'Vivid':
        return px.colors.qualitative.Vivid

def get_summary_stats(list_values):
    values = np.asarray(list_values)
    number = len(list_values)
    q_0 = np.quantile(values, 0)
    q_1 = np.quantile(values, 0.25)
    q_2 = np.quantile(values, 0.5)
    q_3 = np.quantile(values, 0.75)
    q_4 = np.quantile(values, 1)
    mean = sigfig.round(float(np.mean(values)), 3)
    std = sigfig.round(float(np.std(values)), 3)
    summary_stats = [number, mean, std, q_0, q_1, q_2, q_3, q_4]
    return summary_stats


def make_ss_dash_table(values, is_comb, title):
    ss = get_summary_stats(values)
    ss_df = create_summary_stats_table(ss)
    ss_df_dict = ss_df.to_dict('records')
    columns_ss = [{"name": i, "id": i} for i in ss_df.columns]
    data_ss = ss_df_dict
    table = dash_table.DataTable(
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '10px', 'width': '20px', 'maxWidth': '30px',
            'whiteSpace': 'normal'
        },
        columns=columns_ss,
        data=data_ss,
        id='num-main-ss-table',
        export_format="csv",
    ),
    return table


def make_ss_freq_table(cols_f, data_f, is_comb, title):
    table = dash_table.DataTable(
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '10px', 'width': '20px', 'maxWidth': '30px',
            'whiteSpace': 'normal'
        },
        columns=cols_f,
        data=data_f,
        id='comb-chart-freq-table' if is_comb else 'main-chart-freq-table',
        export_format="csv",
    ),

    return table


def create_summary_stats_table(summary_stats):
    ss = summary_stats
    table = []
    headings = ['Statistic', 'Value']
    row_titles = ['Number', 'Mean', 'Stand Dev', 'Minimum (q0)',
                  'Lower Quart (q1)', 'Median (q2)',
                  'Upper Quart (q3)', 'Maximum (q4)']
    for i, value in enumerate(ss):
        row_title = row_titles[i]
        row_value = value
        row = [row_title, row_value]
        table.append(row)
    ss_table = pd.DataFrame(table, columns=headings)
    return ss_table



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


def get_mean_median(x_vals):
    return np.mean(x_vals), np.median(x_vals)