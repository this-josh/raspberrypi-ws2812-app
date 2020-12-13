import dash
import dash_core_components as dcc
from dash_core_components.Markdown import Markdown
import dash_html_components as html
from dash.dependencies import Input, Output
from waitress import serve
import flask
import time
from datetime import datetime
from inputs import colour_options
import logging
import os

logger = logging.getLogger(__name__)
format = "%(asctime)-15s %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    filename=f"./logs/{datetime.now().strftime('%Y%m%d-%H%M%S')}.log",
    format=format,
    level=logging.DEBUG,
)
logger.setLevel(logging.DEBUG)

from methods import (
    clear_strip,
    setup_strip,
    solid_colour,
    tricolour,
    block_wave,
    pulse,
    meet_in_the_middle,
    colour_wipe,
    which_method,
    theater_chase,
    theater_chase_rainbow,
    rainbow_cycle,
    rainbow,
    colour_wipe,
)

strip = setup_strip()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.title = "Crimbo lights"

app.layout = html.Div(
    [
        html.H1(
            children="Crimbo lights controller",
            style={
                "textAlign": "center",
            },
        ),
        html.Div(
            [
                dcc.Markdown("Choose your pattern"),
                dcc.Dropdown(
                    id="light-mode",
                    options=[
                        {"label": "Two colour wave", "value": "colour_wave"},
                        {"label": "Solid colour", "value": "solid_colour"},
                        {"label": "Vive la France", "value": "tricolour"},
                        {"label": "Meet at the middle", "value": "meet_in_middle"},
                        {"label": "Colour wipe", "value": "colour_wipe"},
                        {"label": "Pulse", "value": "pulse"},
                        {"label": "Chase", "value": "theater_chase"},
                        {"label": "Rainbow", "value": "rainbow"},
                        {"label": "Rainbow cycle", "value": "rainbow_cycle"},
                        {
                            "label": "Chase the rainbow",
                            "value": "theater_chase_rainbow",
                        },
                        {"label": "Turn off", "value": "clear_strip"},
                    ],
                    value="colour_wave",
                    searchable=False,
                ),
            ]
        ),
        html.Div(id="selected-mode"),
        html.Div(
            [
                dcc.Markdown("Choose how bright you would like the lights to be"),
                dcc.Markdown("Note this does not change pulse"),
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
                dcc.Markdown(
                    "Rainbow and flags have fixed colours, methods which only use one colour use the top one"
                ),
                dcc.Dropdown(
                    id="colour-1",
                    options=colour_options,
                    value=colour_options[0]["value"],
                    searchable=False,
                    persistence=True,
                ),
                dcc.Dropdown(
                    id="colour-2",
                    options=colour_options,
                    value=colour_options[4]["value"],
                    searchable=False,
                    persistence=True,
                ),
            ]
        ),
        dcc.ConfirmDialogProvider(
            children=html.Button(
                "Restart server?",
            ),
            id="restart-server",
            message="Are you sure you want to restart the server? This will take around 90 seconds",
        ),
        html.Div(id="reboot-status"),
    ],
    style={"width": "48%", "display": "inline-block"},
)


@app.callback(
    Output(component_id="selected-mode", component_property="children"),
    Input(component_id="light-mode", component_property="value"),
    Input(component_id="colour-1", component_property="value"),
    Input(component_id="colour-2", component_property="value"),
)
def change_mode(mode_of_operation, colour1, colour2):
    logger.debug(mode_of_operation)
    which_method("clear_strip", strip)
    time.sleep(50 / 1000.0)
    which_method(mode_of_operation, strip)
    clear_strip(strip)

    if mode_of_operation == "colour_wave":
        logger.debug("block wave")
        block_wave(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "solid_colour":
        logger.debug("solid_colour")
        solid_colour(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "tricolour":
        logger.debug("tricolour")
        tricolour(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "pulse":
        logger.debug("pulse")
        pulse(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "meet_in_middle":
        logger.debug("meet in middle")
        meet_in_the_middle(strip, colour1=colour1, colour2=colour2)
    elif mode_of_operation == "colour_wipe":
        logger.debug("colour_wipe")
        colour_wipe(strip, colour1=colour1, colour2=colour2)
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
        logger.debug("rainbow_cycle")
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
    strip.setBrightness(chosen_brightness)
    strip.show()
    return f"Brightness is currently at {strip.getBrightness()} out of 255"


@app.callback(
    Output(component_id="reboot-status", component_property="children"),
    Input(component_id="restart-server", component_property="submit_n_clicks"),
)
def change_brightness(num_confirmed):
    if num_confirmed is not None:
        logger.warning("Rebooting the pi")
        os.system("sudo reboot")
        return f"Rebooting... {num_confirmed}"
    return f"Not rebooting.{num_confirmed}"


try:
    application = app.server
    serve(application)
except Exception as e:
    logger.exception(e)