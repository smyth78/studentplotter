import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Jumbotron(
        [
            html.H1("StudentPlotter3.0", className="display-3"),
            html.P(
                "A simple browser based graphing "
                "tool to help students analyse medium sized datasets.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Contact the admin with any feedback, ideas or general enquires."
            ),
            html.Hr(className="my-2"),
            html.P(dcc.Markdown('#### studentplotter@gmail.com'))

        ]
    )
            ])
        ])
    ])
