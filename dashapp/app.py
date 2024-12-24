from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages = True, suppress_callback_exceptions= True, pages_folder= "pages", external_stylesheets=[dbc.themes.JOURNAL])