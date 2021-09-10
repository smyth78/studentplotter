import dash_bootstrap_components as dbc
import dash_html_components as html

no_data = dbc.Alert(
    html.H5('You must go to the upload page and upload some data to continue...'),
    color='warning',
    dismissable=True
)

choose_pri = dbc.Alert(
    html.H5('Choose primary feature to continue...'),
    color='info',
    dismissable=True
)

no_pie = dbc.Alert(
    html.H5('A pie chart cannot display split data...'),
    color='warning',
    dismissable=True
)

pie_order = dbc.Alert(
    html.H5('Cannot reorder groups of a pie chart...'),
    color='warning',
    dismissable=True
)

not_split = dbc.Alert(
    html.H5('You must split the data by a category to draw a stacked bar chart...'),
    color='warning',
    dismissable=True
)

invalid_order = dbc.Alert(
    html.H5('You must type category names exactly as presented.\nUse the / to seperate categories.'),
    color='info',
    dismissable=True
)

not_enough_colours = dbc.Alert(
    html.H5('Not enough colours in this scheme to have unique colour...'),
    color='warning',
    dismissable=True
)

pri_different_to_sec = dbc.Alert(
    html.H5('The secondary feature must be different to the primary one...'),
    color='warning',
    dismissable=True
)

add_group_size_collect_small = dbc.Alert(
    html.H5('Add the group size to collect the small categories together...'),
    color='warning',
    dismissable=True
)

error_collect_small = dbc.Alert(
    html.H5('You can only collect small groups when analysing a single feature...'),
    color='warning',
    dismissable=True
)

specify_hist_param= dbc.Alert(
    html.H5('Specify the minimum value and bin width...'),
    color='warning',
    dismissable=True
)
no_table= dbc.Alert(
    html.H5('Complete the following to see a frequency table...'),
    color='warning',
    dismissable=True
)
select_sec_f_or_another_f = dbc.Alert(
    html.H5('You must choose a category to split by or another feature...'),
    color='warning',
    dismissable=True
)
too_many_groups= dbc.Alert(
    html.H5('Error, too many groups, make your bin width larger...'),
    color='warning',
    dismissable=True
)

click_on_heatmap = dbc.Alert(
    html.H5('Click on a square on the heatmap to continue...'),
    color='warning',
    dismissable=True
)

