from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash


app = Dash(__name__, use_pages = True, suppress_callback_exceptions= True, pages_folder= "pages", external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([
    dcc.Store(id = "duffing_solution", storage_type = "session"),  # in case i want to store something temporarily over the web
    dcc.Store(id = "duffing_u_solution", storage_type = "session"),
    dcc.Store(id = "duffing_v_solution", storage_type = "session"),
    dcc.Store(id = "duffing_w_solution", storage_type = "session"),
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug = True, host = "0.0.0.0", port = "8050")

# http://127.0.0.1:8050
# http://192.168.1.4:8050 -> for other devices

