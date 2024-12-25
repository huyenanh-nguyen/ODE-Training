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
    path = "/Duffing",
    title = "Duffing",
    name = "Duffing",
    theme = external_stylesheets
)

# [Page_Layout]_______________________________________________________________________________________________________________________________________________________

layout = dbc.Container(fluid = True, children = [
    # [header]
    dbc.NavbarSimple(
        brand = "Duffing",
        color = "#FCE1E1",
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
                        dbc.Col(dbc.FormText(
                                "Time Conditions. First timepoint starts with Zero",
                                color="secondary"
                            ), width= {"size" : 4}),justify= "center"
                    ),

                    dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "last timepoint",
                                    type = "number",
                                    step = 0.1,
                                    id = "last_timepoint",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter last Timepoint",
                                target = "last_timepoint",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "Steps",
                                    type = "number",
                                    step = 0.01,
                                    id = "time_steps",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "the steps between the first and last timepoint.",
                                target = "time_steps",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "observal time interval",
                                    type = "number",
                                    step = 0.1,
                                    id = "observ_timeinterval",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "For example you only want to see the last 500 timepoints, enter 500 in the Input",
                                target = "observ_timeinterval",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),
                        ], justify= "center"
                        
                    ),

                    html.Div(style = {"padding" : 10}),



                    dbc.Row(
                        dbc.Col(dbc.FormText(
                                "Initial Value for the 3D autonomous vector field (u, v, w). ",
                                color="secondary"
                            ), width= {"size" : 4}),justify= "center"
                    ),
                    dbc.Row(
                        children = [
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "u value",
                                    type = "number",
                                    step = 0.1,
                                    id = "u_value",
                                ), width= {"size" : 2}
                            ),
                            dbc.Popover(
                                children= "enter u",
                                target = "u_value",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "v value",
                                    type = "number",
                                    id = "v_value",
                                    step = 0.1,
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter v",
                                target = "v_value",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "w value",
                                    type = "number",
                                    id = "w_value",
                                    step = 0.1,
                                ), width= {"size" : 2}
                            ),
                        ], justify= "center"
                    ),

                    dbc.Popover(
                                children= "enter w",
                                target = "w_value",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                    html.Div(style = {"padding" : 10}),

                    dbc.Row(
                        dbc.Col(dbc.FormText(
                                "Initial Value for the constants \u03B3, \u03B1, \u03A9. ",
                                color="secondary"
                            ), width= {"size" : 3}),justify= "center"
                    ),

                    dbc.Row(
                        children = [
                            dbc.Col(
                                dbc.Input(
                                    placeholder = "\u03B3 value",
                                    type = "number",
                                    step = 0.1,
                                    id = "gamma",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03B3",
                                target = "gamma",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "\u03B1 value",
                                    id = "alpha",
                                    step = 0.1,
                                    type = "number",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03B1",
                                target = "alpha",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "\u03A9 value",
                                    id = "omega",
                                    step = 0.1,
                                    type = "number",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03A9",
                                target = "omega",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                    html.Div(style = {"padding" : 20}),

                    dbc.Row(
                        children = [
                            dbc.Col(
                                dbc.Button(
                                "Start",
                                id = "calculate",
                                color= "success",
                                outline= True
                                ),width= {"size" : 1}
                            )
                        ], justify= "center"
                        
                        
                    ),

                        ], justify= "center"
                    )
                ], title = "I N I T I A L - C O N D I T I O N")
            ], start_collapsed= False, id = "initial_condition", always_open=True,)
        ]
    )

])
