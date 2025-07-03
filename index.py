from dash import html, dcc
from dash.dependencies import Input, Output
from src.pages import ApiAnalytics
import dash
import dash_bootstrap_components as dbc
from src.pages import Analytics
from src.pages.Analytics import flight_scrapper_dash
from src.components import navbar
from src.utils.gemini import get_flight_insights_from_gemini

# Access the existing dataframe from ApiAnalytics
df = ApiAnalytics.df

# Define the navbar
nav = navbar.Navbar()

# Initialize Dash app
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.7"}],
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

# App layout with dynamic content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])

# Page routing
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ApiAnalytics':
        return html.Div([
            ApiAnalytics.layout,
            html.Hr(),
            html.H5("✈️ AI Summary of Flights (via Gemini)", style={"marginTop": "30px"}),
            html.Div(id="gemini-summary", style={"whiteSpace": "pre-wrap", "fontSize": "16px", "paddingBottom": "50px"})
        ])
    return ApiAnalytics.layout

# Callback for charts
@app.callback([
    Output("indicators_flights", "figure"),
    Output("fig1", "figure"),
    Output("fig2", "figure"),
    Output("fig3", "figure"),
    Output("fig4", "figure"),
    Output("fig5", "figure")
], [
    Input("departure_date", "value"),
    Input("return_date", "value")
])
def callback_function(departure_date, return_date):
    indicators_flights, fig1, fig2, fig3, fig4, fig5 = flight_scrapper_dash(departure_date, return_date)
    return indicators_flights, fig1, fig2, fig3, fig4, fig5

# Callback for Gemini AI summary
@app.callback(
    Output("gemini-summary", "children"),
    Input("url", "pathname")
)
def update_gemini_summary(pathname):
    if pathname == '/ApiAnalytics':
        return get_flight_insights_from_gemini(df)
    return ""

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
