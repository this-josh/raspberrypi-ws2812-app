import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
from waitress import serve

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

application = app.server