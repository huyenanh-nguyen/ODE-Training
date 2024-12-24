from dash import Dash, html, dcc, callback
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from PIL import Image
from ODE import Duffing
from pathlib import Path
import plotly.graph_objects as go

# [Design]____________________________________________________________________________________________________________________________________________________________

logo = Path(str(Path.cwd()) + "/dashapp/templates/logo.png")
pil_img = Image.open(logo)

external_stylesheets = dbc.themes.JOURNAL

dash.register_page(
    __name__, 
    path = "/implementing",
    title = "Implementing",
    name = "implementing",
    theme = external_stylesheets
)

# [Page_Layout]_______________________________________________________________________________________________________________________________________________________

layout = dbc.Container(fluid = True, children = [
    # [header]
    dbc.NavbarSimple(
        brand = "Implementing",
        color = "#F0D6C7",
        dark = True
    ),
    html.Div(style = {"padding" : 20}),

    dbc.Row(
        dbc.Col(
            html.Div([
                html.P(),
                html.Img(
                    src = pil_img,
                    style= {"height" : "6%", "width" : "6%", "textAlign" : "center"}
                    )
                ],
            style= {"textAlign" : "center"}
            )
        )

    ),

    html.Div(style = {"padding" : 40}),

    dbc.Row(
        children = [
            dbc.Accordion([
                dbc.AccordionItem([
                    dbc.Row(
                        children = [
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "u value",
                                    id = "u_value",
                                ), width= {"size" : 2}
                            ),
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "v value",
                                    id = "v_value",
                                ), width= {"size" : 2}
                            ),
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "w value",
                                    id = "w_value",
                                ), width= {"size" : 2}
                            ),
                        ], justify= "center"
                    ),

                    html.P(),

                    dbc.Row(
                        children = [
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "Gamma Value",
                                    id = "gamma",
                                ), width= {"size" : 2}
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "alpha Value",
                                    id = "alpha",
                                ), width= {"size" : 2}
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "omega Value",
                                    id = "omega",
                                ), width= {"size" : 2}
                            ),
                        ], justify= "center"
                    )
                ], title = "D U F F I N G")
            ], start_collapsed= False, id = "duffing")
        ]
    )

])
