from dash import Dash, html, dcc, callback
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from PIL import Image
import numpy as np
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
                                    placeholder = "time end",
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
                                children= "For example you only want to see the last 1100 timepoints, enter 1100 in the Input",
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
                                    step = 0.01,
                                    id = "u_value",
                                ), width= {"size" : 2}
                            ),
                            dbc.Popover(
                                children= "enter u. For example 2",
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
                                    step = 0.01,
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter v. For example 2",
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
                                    step = 0.01,
                                ), width= {"size" : 2}
                            ),
                        ], justify= "center"
                    ),

                    dbc.Popover(
                                children= "enter w. For example 2",
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
                                    step = 0.01,
                                    id = "gamma",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03B3. For example 0.2",
                                target = "gamma",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "\u03B1 value",
                                    id = "alpha",
                                    step = 0.01,
                                    type = "number",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03B1. For example 2.5",
                                target = "alpha",
                                body= True,
                                trigger= "hover",
                                placement= "top"
                            ),

                            dbc.Col(
                                dbc.Input(
                                    placeholder = "\u03A9 value",
                                    id = "omega",
                                    step = 0.01,
                                    type = "number",
                                ), width= {"size" : 2}
                            ),

                            dbc.Popover(
                                children= "enter \u03A9. For example 0.61",
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
                                outline= True,
                                n_clicks = 0
                                ),width= {"size" : 1}
                            )
                        ], justify= "center"
                        
                        
                    ),

                        ], justify= "center"
                    )
                ], title = "I N I T I A L - C O N D I T I O N"),

            ], start_collapsed= False, id = "initial_condition", always_open=True,)
        ]
    ),

    html.Div(style = {"padding" : 40}),
        dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row(
                            children = [
                                dbc.Col(dcc.Dropdown(
                                    options = ["u", "v"],
                                    value = "u",
                                    id = "timeseries_ddm",
                                    placeholder = "choose your y-values"
                                ), width = {"size" : 3}),
                            ], justify= "center"
                        ),

                        dbc.Row(
                            children = [

                                

                                dbc.Col(
                                    dcc.Graph(
                                    id = "timeseries",
                                    style = {"width" : "80vh", "height" : "80vh"}
                                    ), width = {"size" : "auto"}
                                )
                            ], justify = "center"
                        )

                    ], title = "T I M E S E R I E S")
                ], start_collapsed= True, always_open=True),

    html.Div(style = {"padding" : 40}),
        dbc.Accordion([
                    dbc.AccordionItem([
                        dbc.Row(
                            children = [
                                dbc.Col(
                                    dcc.Graph(
                                    id = "phaseportraits",
                                    style = {"width" : "80vh", "height" : "80vh"}
                                    ), width = {"size" : "auto"}
                                )
                            ], justify = "center"
                        )

                    ], title = "P H A S E P O R T R A I T S")
                ], start_collapsed= True, always_open=True)

])




# [Callbacks]_________________________________________________________________________________________________________________________________________________________

@callback(
   [ 
       Output("duffing_solution", "data"),
       Output("duffing_u_solution", "data"),
       Output("duffing_v_solution", "data"),
       Output("duffing_w_solution", "data"),
       
    ],
    [
        Input("calculate", "n_clicks"),
        Input("last_timepoint", "value"),
        Input("time_steps", "value"),
        State("observ_timeinterval", "value"),
        Input("u_value", "value"),
        Input("v_value", "value"),
        Input("w_value", "value"),
        Input("gamma", "value"),
        Input("alpha", "value"),
        Input("omega", "value")
    ],
    prevent_initial_call = True
)
def solv_duffing(click, t_end, t_step, keep, u, v, w, gamma, alpha, omega):
    if not click:
        return None
    
    

    par = [u, v, w]
    t = np.arange(0, t_end, t_step)
    
    duff = Duffing(par, t, gamma, alpha, omega)

    sol = duff.duffing_solver()

    x_sol = duff.x_solv(keep)
    y_sol = duff.y_solv(keep)
    z_sol = duff.z_solv(keep)
    
    return [sol, x_sol, y_sol, z_sol]


@callback(
        Output("timeseries", "figure"),
        [
            Input("timeseries_ddm", "value"),
            Input("duffing_u_solution", "data"),
            Input("duffing_v_solution", "data"),
            Input("time_steps", "value"),
            State("observ_timeinterval", "value"),
        ]
)
def duffing_timeseries(dropdown, u_sol, v_sol, t_step, t_last):
    t = np.arange(0, t_last, t_step)
    
    if dropdown == "u":
    
        fig = go.Figure()
        fig.update_xaxes(title_text = " t in h ")
        fig.update_yaxes(title_text = " u conc in a.u. ")
        fig = fig.add_trace(
            go.Scatter(
                x = t,
                y = u_sol,
                mode = "lines"
            )
        )

        return fig
    
    else:
        fig = go.Figure()
        fig.update_xaxes(title_text = " t in h ")
        fig.update_yaxes(title_text = " v conc in a.u. ")
        fig = fig.add_trace(
            go.Scatter(
                x = t,
                y = v_sol,
                mode = "lines"
            )
        )

        return fig



@callback(
    Output("phaseportraits", "figure"),
    [Input("duffing_u_solution", "data"),
    Input("duffing_v_solution", "data")],
    prevent_initial_call = True
)
def duffing_phaseportraits(u_sol, v_sol):
    fig = go.Figure()
    fig.update_xaxes(title_text = " u conc in a.u.")
    fig.update_yaxes(title_text = " v conc in a.u.")
    fig = fig.add_trace(
        go.Scatter(
            x = u_sol,
            y = v_sol,
            mode = "lines"
        )
    )
    return fig
  