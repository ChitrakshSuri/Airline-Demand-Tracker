from dash import html, dcc
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc

from src.pages import ApiAnalytics, Analytics
from src.pages.Analytics import flight_scrapper_dash
# from src.components import navbar
from src.utils.gemini import get_flight_insights_from_gemini

# Access dataframe from ApiAnalytics
df = ApiAnalytics.df
# nav = navbar.Navbar()

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.7"}],
                external_stylesheets=[dbc.themes.MINTY],
                suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # nav,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/ApiAnalytics':
        return ApiAnalytics.layout
    elif pathname == '/':
        return ApiAnalytics.layout   # 👈 Set default to ApiAnalytics
    else:
        return html.H1("404 Page Not Found")# You can replace with a landing page if needed

# Analytics figures callback
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
def update_figures(departure_date, return_date):
    return flight_scrapper_dash(departure_date, return_date)

# Gemini Summary Callback
@app.callback(
    Output("gemini-summary", "children"),
    Input("summarize-btn", "n_clicks"),
    prevent_initial_call=True
)
def update_summary(n_clicks):
    return get_flight_insights_from_gemini(df)

if __name__ == '__main__':
    app.run_server(debug=True)
