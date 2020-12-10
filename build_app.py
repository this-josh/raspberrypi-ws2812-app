import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
                    id="mode",
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
        # Maybe confirm changes
        # html.Div(
        #     dcc.ConfirmDialog(
        #         id="confirm",
        #         message="Danger danger! Are you sure you want to continue?",
        #     )
        # ),
    ]
)


@app.callback(
    Output(component_id="blank", component_property="blank"),
    [Input(component_id="mode", component_property="value")],
)
def change_mode(mode_of_operation):
    print(mode_of_operation)
    if mode_of_operation == "colour_wave":
        block_wave(strip)
    elif mode_of_operation == "mode_of_operation":
        pulse(strip)
    else:
        meet_in_the_middle(strip)


from waitress import serve

application = app.server
serve(application)