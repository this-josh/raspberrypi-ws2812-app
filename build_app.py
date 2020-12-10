import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from waitress import serve
import flask

from methods import setup_strip, block_wave, pulse, meet_in_the_middle

strip = setup_strip()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.title = "Chrimbo lights"

app.layout = html.Div(
    [
        html.H1(
            children="Chrimbo lights controller",
            style={
                "textAlign": "center",
            },
        ),
        html.Div(
            [
                dcc.Markdown("Choose your pattern"),
                dcc.RadioItems(
                    id="light-mode",
                    options=[
                        {"label": "Two colour wave", "value": "colour_wave"},
                        {"label": "Meet at the middle", "value": "meet_in_middle"},
                        {"label": "Pulse", "value": "pulse"},
                    ],
                    value="colour_wave",
                    labelStyle={"display": "inline-block"},
                ),
            ]
        ),
        html.Div(id="selected-mode"),
        html.Div(
            [
                dcc.Markdown("Choose how bright you would like the lights to be"),
                dcc.Slider(min=0, max=255, step=1, value=0),
            ]
        ),
        html.Div(
            [
                dcc.Markdown("What colours would you like in the pattern?"),
                dcc.Dropdown(
                    options=[
                        {"label": "Red", "value": "Red"},
                        {"label": "Green", "value": "Green"},
                        {"label": "Blue", "value": "Blue"},
                    ],
                    multi=True,
                    value="Red",
                ),
            ]
        ),
    ]
)


@app.callback(
    Output(component_id="selected-mode", component_property="children"),
    Input(component_id="light-mode", component_property="value"),
)
def change_mode(mode_of_operation):
    print(mode_of_operation)
    global pulse_on
    global block_wave_on
    global meet_in_middle_on

    if mode_of_operation == "colour_wave":
        print("block wave")
        block_wave_on = True
        pulse_on = False
        meet_in_middle_on = False
        block_wave(strip)
    elif mode_of_operation == "pulse":
        pulse_on = True
        meet_in_middle_on = False
        block_wave_on = False
        print("pulse")
        pulse(strip)
    elif mode_of_operation == "meet_in_middle":
        meet_in_middle_on = True
        block_wave_on = False
        pulse_on = False
        print("meet in middle")
        meet_in_the_middle(strip)
    return mode_of_operation


application = app.server
serve(application)