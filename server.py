# external imports
import dash
import dash_bootstrap_components as dbc
import os
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv


load_dotenv()


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE],
    prevent_initial_callbacks=False,
)

server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'StudentPlotter3.0'


