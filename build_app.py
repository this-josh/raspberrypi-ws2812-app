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

from methods import (
    clear_strip,
    setup_strip,
    block_wave,
    pulse,
    meet_in_the_middle,
    which_method,
    theater_chase,
    theater_chase_rainbow,
    rainbow_cycle,
    rainbow,
    colour_wipe
)

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
                        {"label": "Colour wipe", "value": "colour_wipe"},
                        {"label": "Chase", "value": "theater_chase"},
                        {"label": "Rainbow", "value": "rainbow"},
                        {"label": "Rainbow cycle", "value": "rainbow_cycle"},
                        {
                            "label": "Chase the rainbow",
                            "value": "theater_chase_rainbow",
                        },
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
    clear_strip(strip)

    if mode_of_operation == "colour_wave":
        logger.debug("block wave")
        block_wave(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "pulse":
        logger.debug("pulse")
        pulse(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "meet_in_middle":
        logger.debug("meet in middle")
        meet_in_the_middle(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "colour_wipe":
        logger.debug("colour_wipe")
        colour_wipe(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "theater_chase":
        logger.debug("theater_chase")
        theater_chase(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "rainbow":
        logger.debug("rainbow")
        rainbow(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "rainbow_cycle":
        logger.debug("rainbow_cycle)
        rainbow_cycle(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "theater_chase_rainbow":
        logger.debug("theater_chase_rainbow")
        theater_chase_rainbow(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "clear_strip":
        clear_strip(strip)
    return mode_of_operation


@app.callback(
    Output(component_id="selected-brightness", component_property="children"),
    Input(component_id="chosen-brightness", component_property="value"),
)
def change_brightness(chosen_brightness):
    clear_strip(strip)
    strip.setBrightness(chosen_brightness)
    return strip.getBrightness()


application = app.server
serve(application)