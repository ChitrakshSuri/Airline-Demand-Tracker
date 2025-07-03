import os
import pandas as pd
from dash import html, dcc
import plotly.express as px
import pathlib

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "api_flight_data.csv"))
df = pd.read_csv(DATA_PATH)

df['scheduled_time'] = pd.to_datetime(df['scheduled_time'])

# Bar chart - Number of flights per destination
route_count_fig = px.bar(
    df.groupby('to').size().reset_index(name='Flight Count'),
    x='to', y='Flight Count',
    title='Number of Flights by Destination',
    labels={'to': 'Destination'}
)

# Pie chart - Share by airline
airline_fig = px.pie(
    df,
    names='airline_name',
    title='Airline Share (API Flights)'
)

# Timeline
timeline_fig = px.scatter(
    df,
    x='scheduled_time',
    y='to',
    color='airline_name',
    title='Flight Schedule Timeline',
    hover_data=['from']
)

layout = html.Div([
    html.H3("📊 Live API Flight Insights"),
    dcc.Graph(figure=route_count_fig),
    dcc.Graph(figure=airline_fig),
    dcc.Graph(figure=timeline_fig),
])
