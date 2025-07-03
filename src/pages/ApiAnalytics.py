from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.express as px
import pathlib

# Load Data
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "api_flight_data.csv"))
df = pd.read_csv(DATA_PATH)
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])

# Create Figures
route_count_fig = px.bar(
    df.groupby('to').size().reset_index(name='Flight Count'),
    x='to', y='Flight Count',
    title='Number of Flights by Destination',
    labels={'to': 'Destination'}
)

airline_fig = px.pie(
    df,
    names='airline_name',
    title='Airline Share (API Flights)'
)

timeline_fig = px.scatter(
    df,
    x='scheduled_time',
    y='to',
    color='airline_name',
    title='Flight Schedule Timeline',
    hover_data=['from']
)

# ✨ Boostrap Layout (REPLACE this layout block in your file)
layout = html.Div([
    dbc.NavbarSimple(
        brand="Flights Scrapper Dashboard",
        color="blue", dark=True,
        # children=[
        #     dbc.NavItem(dbc.NavLink("Analytics", href="/")),
        #     dbc.NavItem(dbc.NavLink("Live API Insights", href="/ApiAnalytics"))
        # ]
    ),

    html.Br(),

    dbc.Container([

        html.H3("📊 Live API Flight Insights", className="text-primary mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=route_count_fig), md=6),
            dbc.Col(dcc.Graph(figure=airline_fig), md=6)
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=timeline_fig), md=12)
        ], className="mt-4"),

        dbc.Card([
            dbc.CardBody([
                html.H5("🤖 AI Summary of Flights", className="card-title"),
                dbc.Button("Get AI Summary", id="summarize-btn", color="primary", className="mb-3"),
                dcc.Loading(
                    id="loading-summary",
                    type="default",
                    children=html.Div(id="gemini-summary", style={"whiteSpace": "pre-wrap"})
                )
            ])
        ], className="mt-4")
    ])
])

__all__ = ["layout", "df"]
