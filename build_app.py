import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from waitress import serve
import flask
from inputs import colour_options
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from methods import setup_strip, block_wave, pulse, meet_in_the_middle, which_method

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
                        {"label": "Clear strip", "value": "clear_strip"},
                    ],
                    value="clear_strip",
                    labelStyle={"display": "inline-block"},
                ),
            ]
        ),
        html.Div(id="selected-mode"),
        html.Div(
            [
                dcc.Markdown("Choose how bright you would like the lights to be"),
                dcc.Slider(
                    id="chosen-brightness",
                    min=0,
                    max=255,
                    step=1,
                    value=0,
                    persistence=True,
                ),
            ]
        ),
        html.Div(id="selected-brightness"),
        html.Div(
            [
                dcc.Markdown("What colours would you like in the pattern?"),
                dcc.Dropdown(
                    id="colour-1",
                    options=colour_options,
                    value=colour_options[0]["value"],
                ),
                dcc.Dropdown(
                    id="colour-2",
                    options=colour_options,
                    value=colour_options[4]["value"],
                ),
            ]
        ),
    ]
)


@app.callback(
    Output(component_id="selected-mode", component_property="children"),
    Input(component_id="light-mode", component_property="value"),
    Input(component_id="colour-1", component_property="value"),
    Input(component_id="colour-2", component_property="value"),
)
def change_mode(mode_of_operation, colour1, colour2):
    logger.debug(mode_of_operation)
    which_method(mode_of_operation, strip)
    if mode_of_operation == "colour_wave":
        logger.debug("block wave")
        block_wave(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "pulse":
        logger.debug("pulse")
        pulse(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "meet_in_middle":
        logger.debug("meet in middle")
        meet_in_the_middle(strip, colour1=colour1, colour2=colour2)
    return mode_of_operation


@app.callback(
    Output(component_id="selected-brightness", component_property="children"),
    Input(component_id="chosen-brightness", component_property="value"),
)
def change_brightness(chosen_brightness):
    strip.setBrightness(chosen_brightness)
    return strip.getBrightness()


application = app.server
serve(application)