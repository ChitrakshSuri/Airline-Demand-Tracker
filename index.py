from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd

# Connect to your app pages and components
from src.pages import ApiAnalytics
from src.pages import Analytics
from src.pages.Analytics import flight_scrapper_dash
from src.components import navbar
from src.utils.gemini import get_flight_insights_from_gemini

# Reuse dataframe from ApiAnalytics
df = ApiAnalytics.df

# Define navbar
nav = navbar.Navbar()

# Initialize app
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.7"}],
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

# Define the index layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

# Handle page routing
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ApiAnalytics':
        return html.Div([
            ApiAnalytics.layout,
            html.Hr(),
            dbc.Button("🧠 Get AI Summary", id="summarize-btn", color="primary", n_clicks=0),
            dbc.Spinner(html.Div(id="gemini-summary"), size="md", color="info", type="border", fullscreen=False, delay_hide=500)
        ])
    return ApiAnalytics.layout

# Callback for flight scrapper plots
@app.callback(
    [Output("indicators_flights", "figure"),
     Output("fig1", "figure"),
     Output("fig2", "figure"),
     Output("fig3", "figure"),
     Output("fig4", "figure"),
     Output("fig5", "figure")],
    [Input("departure_date", "value"),
     Input("return_date", "value")]
)
def callback_function(departure_date, return_date):
    indicators_flights, fig1, fig2, fig3, fig4, fig5 = flight_scrapper_dash(departure_date, return_date)
    return indicators_flights, fig1, fig2, fig3, fig4, fig5

# Callback for Gemini summary
@app.callback(
    Output("gemini-summary", "children"),
    Input("summarize-btn", "n_clicks"),
    prevent_initial_call=True
)
def update_summary(n_clicks):
    return get_flight_insights_from_gemini(df)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
