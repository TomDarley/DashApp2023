import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import numpy as np
import pandas as pd
import psycopg2
import geopandas as gpd
from scipy.interpolate import interp1d
from datetime import datetime
import matplotlib.dates as mdates
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objs as go
import sqlalchemy
from scipy.integrate import quad
import warnings
import time
import matplotlib.pyplot as plt

layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="error_plot",
                        ),
                        width={"size": 12, "offset": 0, "order": 2},
                        style={
                            "margin-left": 0,
                            "margin-top": 10,
                            "background-colour": "white",
                        },
                    ),
                ]
            ),
            style={
                "background-color": "#1b1c1c",
                "margin": 0,  # Remove container margin
                "padding": 0,
            },  # Remove container padding
        )
    ]
)


@callback(
    (Output("error_plot", "figure")),
    [Input("selected-df-storage", "data")],
)
def make_scatter_plot(cpa_df):

    df = pd.read_json(cpa_df)
    df = df.drop("Sum", axis=0)
    # Melt the DataFrame to long format
    melted_df = df.melt(
        ignore_index=False, var_name="Date", value_name="Value"
    ).reset_index()

    # Calculate min and max values for each profile
    min_values = melted_df.groupby("index")["Value"].min()
    max_values = melted_df.groupby("index")["Value"].max()

    # Creating the box and whisker plot using Plotly Express
    fig = px.box(
        melted_df,
        x="index",
        y="Value",
        title="",
        points=False,
        template="plotly_dark",
        height=600,
    )

    # Calculate the most recent value information
    latest_date = df.columns[-1]
    most_recent_values = df[latest_date]
    most_recent_info = pd.DataFrame(
        {"Index": most_recent_values.index, "Value": most_recent_values}
    )

    # Add a red scatter point for the most recent values
    for _, row in most_recent_info.iterrows():
        popup_text = f"Latest Survey: {latest_date}"
        scatter_trace = go.Scatter(
            x=[row["Index"]],
            y=[row["Value"]],
            mode="markers",
            text=popup_text,
            marker=dict(color="red", size=10),
            showlegend=False,
        )

        fig.add_trace(scatter_trace)

    # Modify the box plot traces to show custom error bars
    for profile in df.index:
        fig.update_traces(
            selector=dict(name=profile),
            boxpoints="all",
            lowerfence=min_values[profile],
            uperfence=max_values[profile],
            showlegend=False,
        )

    # Create a custom legend entry with a dummy point and label
    dummy_legend_trace = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Latest Survey",
    )
    fig.add_trace(dummy_legend_trace)
    fig.update_layout(showlegend=True, legend_title_text="Profile Name")
    # Update x-axis tick labels
    fig.update_layout(
        title_font={"size": 15, "family": "Helvetica", "color": "white"},
        yaxis_title="Combined Profile Area (m²)",
        xaxis_title=None,
        legend_title="",
        font=dict(size=15, color="white", family="Helvetica"),
        xaxis=dict(
            tickmode="array",
            tickangle=45,
            tickfont=dict(
                size=12,  # Set the font size
                color="white",  # Set the font color
                family="Helvetica",  # Set the font family
            ),
        ),
    )

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=15)),  # Adjust the size as needed
        yaxis=dict(tickfont=dict(size=15)),  # Adjust the size as needed
    )

    return fig
