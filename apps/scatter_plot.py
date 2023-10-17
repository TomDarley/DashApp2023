import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objs as go
import sqlalchemy
import base64

# delete this
image_path = r"media/NERD.jpeg"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()


layout = html.Div(
    [
        dcc.Store(
            id="selected-df-storage",
            data={"current": None, "previous": None},
        ),
        # stores for the metrics generated in plot creation
        dcc.Store(id="lowest_recorded_value"),
        dcc.Store(id="lowest_recorded_year"),
        dcc.Store(id="highest_recorded_value"),
        dcc.Store(id="highest_recorded_year"),
        dcc.Store(id="change_rate"),
        dcc.Store(id="scatter_chart"),
        # wrap inside card so it scales correctly .... stupid
        dbc.Card(
            [
                dcc.Graph(
                    id="scatter_plot",
                    style={
                        "width": "100%",
                        "height": "60vh",
                    },
                    config={"responsive": True},
                ),
            ],style={"border-radius": "10px", "overflow": "hidden"}
        ),
        dbc.Button(
            [html.Span(className="bi bi-info-circle-fill")],
            size="md",
            id="scatter_open_info",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "left": "8px","border-radius": "5px"},
        ),
        dbc.Button(
            [html.Span(className="fa-solid fa-expand")],
            size="md",
            id="scatter_open_full",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "right": "8px","border-radius": "5px"},
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("CSA Scatter Plot")),
                dbc.ModalBody(
                    [
                        html.P(
                            "This chart shows the combined cross-sectional area for each profile line. It is nice, I like it a lot.",
                            style={"font-size": 20},
                        ),
                        html.Img(
                            src=f"data:image/jpeg;base64,{encoded_image}",
                            alt="CSA Scatter Plot Image",
                            style={"height": "40vh"},
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="scatter_info_close",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="scatter_info_model",
            is_open=False,
            fullscreen=True,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cross Sectional Line Plot")),
                dbc.ModalBody(
                    dcc.Graph(id="scatter_plot_model", style={"height": "100vh"})
                ),  ## might not work
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="scatter_full_close",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modal_scatter_plot",
            is_open=False,
            fullscreen=True,
        ),
    ],
    style={
        "position": "relative",
        "height": "100%",
        "margin-right": "20px",
    },  # Set the position of the containing div to relative
)


@callback(
    (
        Output("scatter_plot", "figure"),
        Output("change_rate", "data"),
        Output("selected-df-storage", "data"),
        Output("scatter_plot_model", "figure"),
        Output("lowest_recorded_value", "data"),
        Output("lowest_recorded_year", "data"),
        Output("highest_recorded_value", "data"),
        Output("highest_recorded_year", "data"),
        Output("scatter_chart", "data"),
        Input("survey-unit-dropdown", "value"),
    ),
    allow_duplicate=True,
)
def make_scatter_plot(selected_survey_unit):
    current_year = datetime.now().year
    survey_unit = selected_survey_unit
    # print(survey_unit)

    def get_data(target_survey_unit: str):
        """Establish database connection, make query and return df, both target profile and target date
        are optional as make_csa_df and get_area functions require different queries"""

        engine = sqlalchemy.create_engine(
            "postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB"
        )

        # Import spatial data as GeoDataFrame
        query = f"SELECT * FROM cpa_table WHERE survey_unit = '{target_survey_unit}'"
        df = pd.read_sql_query(query, engine)

        # Close the engine connection
        engine.dispose()
        return df

    # load data directly from the DB
    master_df = get_data(survey_unit)
    master_df = master_df[["date", "profile", "area"]]

    # Pivot the data
    pivot_df = master_df.pivot(index="profile", columns="date", values="area")
    pivot_df.loc[:, "Mean"] = pivot_df.mean(axis=1)
    # Add column with representing the sum of the total number of dates in df
    pivot_df.loc[:, "countSurveyedDates"] = (len(list(pivot_df.columns)) - 1) / 2
    # Add column representing the sum of the total number NaNs in each row
    pivot_df.loc[:, "NaNCount"] = pivot_df.isnull().sum(axis=1)
    # Logic for determining if the number of NaNs is more than half the number of total number of dates surveyed
    pivot_df.loc[:, "DropRow"] = pivot_df["countSurveyedDates"] > pivot_df["NaNCount"]
    # droppedRows = pd.DataFrame((pivot_df.loc[pivot_df['DropRow'] == False]))
    # get the filtered for NaNs as new df for plotting
    df1 = pivot_df.loc[pivot_df["DropRow"] == True]
    # remove NaNCount, DropRow columns
    df1 = df1.drop(["NaNCount", "DropRow", "countSurveyedDates", "Mean"], axis=1)
    # fill NaN values in each row with Mean
    df1 = df1.T.fillna(df1.mean(axis=1)).T

    # add a sum of columns to df
    df1.loc["Sum"] = df1.sum()
    df1 = pd.DataFrame(df1)

    # ADDING DF IN CURRENT FORMAT TO STORE FOR ERROR BAR PLOT
    df_store = df1.to_json()

    df1 = df1.transpose()
    df1 = df1["Sum"]
    df2 = pd.DataFrame(df1)
    df2["index1"] = df2.index
    chart_ready_df = df2

    # Get lowest recorded CPA
    lowest = chart_ready_df["Sum"].idxmin()
    row_with_min_value = list(chart_ready_df.loc[lowest])
    lowest_year = row_with_min_value[0]
    lowest_values = row_with_min_value[1]

    # Get highest recorded CPA
    highest = chart_ready_df["Sum"].idxmax()
    row_with_max_value = list(chart_ready_df.loc[highest])
    highest_year = row_with_max_value[0]
    highest_values = row_with_max_value[1]

    chart_ready_df["index1"] = pd.to_datetime(
        chart_ready_df["index1"], format="%Y-%m-%d"
    )
    month_list = []
    for i in chart_ready_df["index1"]:
        month = i.month
        month_list.append(month)
    season_list = []
    for month in month_list:
        spring_range = [1, 2, 3, 4]
        summer_range = [5, 6, 7, 8]
        autumn_range = [9, 10, 11, 12]
        if month in autumn_range:
            season_list.append("Autumn")
        elif month in spring_range:
            season_list.append("Spring")
        elif month in summer_range:
            season_list.append("Summer")
        else:
            season_list.append("gray")
    chart_ready_df["season"] = season_list

    # extracting values as lists for the y and x-axis
    x_axis = list(df2["index1"])
    y_axis = list(df2["Sum"])

    # Convert x_axis to number format - needed for correlation calculation
    x_mdates = mdates.date2num(x_axis)

    # Create df3
    chart_ready_df = pd.DataFrame({"Sum": list(df2["Sum"])})

    # Store x-axis data and season_list in df3
    chart_ready_df["season"] = season_list
    chart_ready_df["x"] = x_mdates

    # Define tick positions and tick labels
    x_min = min(x_axis)
    x_max = max(x_axis)
    num_ticks = 10
    tick_dates = pd.date_range(start=x_min, end=x_max, periods=num_ticks)
    tickvals = mdates.date2num(tick_dates)  # Convert tick dates to number format
    ticktext = tick_dates.strftime("%Y-%m")

    # linear regression fit
    regline = (
        sm.OLS(chart_ready_df["Sum"], sm.add_constant(chart_ready_df["x"]))
        .fit()
        .fittedvalues
    )

    # calculate stats to show in the title
    z = np.polyfit(x_mdates, y_axis, 1)
    p = np.poly1d(z)

    # calculate accretion values
    pAsString = str(p)
    slope_intercept = pAsString.split("x")[0].replace("\n", "").lstrip()
    slope_intercept = float(slope_intercept)
    accretion_levels = round((slope_intercept * 365), 3)

    # r squared value
    correlation_matrix = np.corrcoef(x_mdates, y_axis)
    correlation_xy = correlation_matrix[0, 1]
    r_squared = round((correlation_xy**2), 3)
    # print("R² Value: " + str(r_squared))

    # obtain the average area for all profiles for all years
    yearly_summed_area = list(df2["Sum"])

    def average(lst):
        return sum(lst) / len(lst)

    average_area = average(yearly_summed_area)

    ## calculate the erosion/accretion as a percentage of the average area
    percentage = abs(accretion_levels) / average_area * 100
    percentage = percentage.__round__(2)
    # print(percentage)

    if accretion_levels <= 0:
        state = "Erosion Rate"
    else:
        state = "Accretion Rate"

    global found_state
    found_state = state

    global found_acreation_levels
    found_acreation_levels = round(accretion_levels, 1)

    global found_percentage
    found_percentage = percentage

    # Create the scatter plot using Plotly Express
    fig = px.scatter(
        chart_ready_df,
        x="x",
        y="Sum",
        color="season",
        symbol="season",
        # height=550,
        template="seaborn",
    )

    # Update x-axis tick labels
    fig.update_layout(
        title={
            "text": f"{selected_survey_unit}",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font={"size": 15, "family": "Helvetica", "color": "blue"},
        xaxis_title="",
        yaxis_title="Combined Profile Area (m²)",
        legend_title="",
        font=dict(size=12, color="blue", family="Helvetica"),
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle=45,
            tickfont=dict(
                size=12,  # Set the font size
                color="blue",  # Set the font color
                family="Helvetica",  # Set the font family
            ),
        ),
        legend_traceorder="reversed",
        legend_title_text=f"",
    )

    # increase marker size
    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(
                width=0,
            ),
        ),
        selector=dict(mode="markers"),
    )

    # add linear regression line for whole sample
    fig.add_traces(go.Scatter(x=x_mdates, y=regline, mode="lines", name="Trend"))

    # Serialize the figure to JSON
    serialized_fig = fig.to_json()

    # Update the 'cpa' key in the store's data with the serialized figure
    chart_data = {"cpa": serialized_fig}

    return (
        fig,
        f"{state}: {round(accretion_levels, 1)}m² yˉ¹ ",
        df_store,
        fig,
        lowest_values,
        lowest_year,
        highest_values,
        highest_year,
        chart_data,
    )


@callback(
    Output("scatter_info_model", "is_open"),
    [Input("scatter_open_info", "n_clicks"), Input("scatter_info_close", "n_clicks")],
    [State("scatter_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("modal_scatter_plot", "is_open"),
    Output("scatter_open_full", "n_clicks"),
    Input("scatter_open_full", "n_clicks"),
    Input("scatter_full_close", "n_clicks"),
    Input("scatter_plot", "relayoutData"),
)
def toggle_modal_chart(n1, n2, relayoutData):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "open" in changed_id:
        return True, 0
    elif "close" in changed_id:
        return False, 0
    return False, 0
