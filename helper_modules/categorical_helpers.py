import random
import pandas as pd
import numpy as np

from helper_modules.alerts import *


def collect_small_groups(df, pri_feat, sec_f, group_size, group_name):

    try:
        group_size = int(group_size)
    except ValueError:
        print('group size is not an integer')

    if sec_f:
        dff, _, _, _ = split_cat_data_by_sec_f(df, pri_feat, sec_f)
    else:
        dff = df.groupby(pri_feat).size().reset_index(name='Count').rename(columns={'Col1': 'Col_value'})
        dff.reset_index(drop=True, inplace=True)

    # make the first column the index
    dff.set_index(list(dff)[0], inplace=True)

    # iterate through each cell of df and record index/col names
    removed_values = []
    for row_index, row in dff.iterrows():
        for column_index, value in row.items():
            if value <= group_size:
                removed_values.append([row_index, column_index, value])

    # now find the row/cols in the df and change cell values  to 'other'
    for removed_val in removed_values:
        if sec_f is None:
            df.loc[(df[pri_feat] == removed_val[0]), pri_feat] = group_name
        else:
            # this is NOT implemented....in fact I'm not sure what this should look like!
            df.loc[(df[pri_feat] == removed_val[1]) & (df[sec_f] == removed_val[0]), pri_feat] = group_name

    return df, removed_values

def split_cat_data_by_sec_f(df, pri_feat, sec_feat):
    pri_cats = np.unique(df[pri_feat].values)
    sec_cats = np.unique(df[sec_feat].values)
    column_titles = list(pri_cats)
    column_titles.insert(0, sec_feat)
    list_for_df_freq_table = [column_titles]
    column_names = []
    for sec_cat in sec_cats:
        column_names.append(sec_cat)
        # make an empty array as long as the primary features
        sec_feature_data = [sec_cat]
        chosen_features = df[[pri_feat, sec_feat]]
        for pri_cat in pri_cats:
            filtered_df = chosen_features[(chosen_features[pri_feat] == pri_cat)]
            # get the row count
            count_df = filtered_df[filtered_df[sec_feat] == sec_cat].shape[0]
            sec_feature_data.append(count_df)

        list_for_df_freq_table.append(sec_feature_data)
    df = pd.DataFrame(list_for_df_freq_table)
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    y_names = list(pri_cats)
    return df, y_names, list_for_df_freq_table, column_names


def get_unique_colours(colours, quantity):
    alert = None
    # need to do 2 cases - first - enough colours for uniqueness
    unique_colours = []
    if len(colours) > quantity:
        while len(unique_colours) < quantity:
            for i in range(quantity):
                colour = random.choice(colours)
                if colour not in unique_colours:
                    unique_colours.append(colour)
    # when not enough unique colours
    else:
        alert = not_enough_colours
        for i in range(quantity):
            unique_colours.append(random.choice(colours))
    return unique_colours, alert


def create_freq_table(list_or_df_freq_table, column_names, is_two_way):
    if is_two_way:
        # format the table appropriatly
        df = pd.DataFrame(list_or_df_freq_table)
        df.columns = df.iloc[0]
        df = df[1:]
        # df = df.apply(pd.to_numeric, downcast='integer')
        df['Totals'] = df.sum(numeric_only=True, axis=1)
        # df = df.apply(pd.to_numeric, downcast='integer')
        # df.loc['Totals'] = df.sum(numeric_only=True, axis=0)
        # df.append(df.sum(numeric_only=True), ignore_index=True)

        # add the correct column/row titles
        sec_feat_titles = []
        for sec_feat_title in list_or_df_freq_table:
            sec_feat_titles.append(sec_feat_title[0])
        sec_feat_titles.append('Totals')
        # df.insert(0, sec_feat_titles[0], sec_feat_titles[1:])

    else:
        # a df is passed if not split
        df = list_or_df_freq_table

    freq_df_dict = df.to_dict('records')
    columns_f = [{"name": i, "id": i} for i in df.columns]
    data_f = freq_df_dict
    return columns_f, data_f


def create_removed_strings_div(removed_values):
    final_div = [html.Div(['Removed categories:', ''])]
    for value in removed_values:
        final_div.append(html.Div(value[0] + ' = ' + str(value[2]) + '\n'))
    return final_div


