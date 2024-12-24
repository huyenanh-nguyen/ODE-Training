from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages = True, suppress_callback_exceptions= True, pages_folder= "pages", external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([
    # dcc.Store(id = "storage", storage_type = "session"),  # in case i want to store something temporarily over the web
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug = True, host = "0.0.0.0", port = "8050")