# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc


# app pages
from pages import (
    upload,
    numerical,
    categorical,
    bivariate,
    about
)

from server import app, server


header = dbc.Container(
    [
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Upload", href="/")),
                dbc.NavItem(dbc.NavLink("Categorical", href="/categorical")),
                dbc.NavItem(dbc.NavLink("Numerical", href='/numerical')),
                dbc.NavItem(dbc.NavLink('Bivariate', href='/bivariate')),
                dbc.NavItem(dbc.NavLink("About", href="/about"))
            ],
        )
    ]
)

app.layout = html.Div(
    [
        dbc.NavbarSimple([header], className="mb-5", id='nav-bar',
                         brand="StudentPlotter3.0",
                         brand_href="/",
                         color="primary",
                         dark=True,
                         ),
        html.Div(id='alert'),
        dbc.Container(
            id='page-content'
        ),
        # create the session store
        dcc.Store(id='session', storage_type='session'),
        dcc.Location(id='base-url', refresh=True)
    ]
)

@app.callback(
    [Output('page-content', 'children'),
     Output('alert', 'children')],
    [Input('base-url', 'pathname')])
def router(pathname):
    page_content = None
    alert = None
    if pathname == '/':
        page_content = upload.layout()
    elif pathname == '/categorical':
        page_content = categorical.layout()
    elif pathname == '/numerical':
        page_content = numerical.layout()
    elif pathname == '/bivariate':
        page_content = bivariate.layout()
    elif pathname == '/about':
        page_content = about.layout()
    return page_content, alert

if __name__ == '__main__':
    app.run_server(debug=False)
