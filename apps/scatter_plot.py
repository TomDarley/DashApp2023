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

layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dcc.Store(
                        id="selected-df-storage",
                        data={"current": None, "previous": None},
                    ),

                    dbc.Col(
                        dcc.Graph(
                            id="scatter_plot",
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
    (
        Output("scatter_plot", "figure"),
        Output("loading-spinner", "children"),
        Output("selected-df-storage", "data"),
    ),
    [
        Input("survey-unit-dropdown", "value"),
    ],
)
def make_scatter_plot(selected_survey_unit):
    print(selected_survey_unit)

    current_year = datetime.now().year
    survey_unit = selected_survey_unit

    def get_data(target_survey_unit: str):
        """Establish database connection, make query and return df, both target profile and target date
        are optional as make_csa_df and get_area functions require different queries"""

        engine = sqlalchemy.create_engine(
            "postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB"
        )

        # Import spatial data as GeoDataFrame
        query = f"SELECT * FROM topo_data WHERE survey_unit = '{target_survey_unit}'"
        df = pd.read_sql_query(query, engine)

        # Close the engine connection
        engine.dispose()
        return df

    def extract_chainage_elevation(profile_id: str):
        """Function extracts master profile data from SANDS exported csv. This will be refactored to connect to the
        AWS database instead for production"""

        master_profile_df = pd.read_csv(
            r"C:\Users\darle\Desktop\DASH_Data\Master_Profile_Tests.csv"
        )

        chainage_values = []
        elevation_values = []

        filtered_df = master_profile_df.loc[
            master_profile_df["Profile_ID"] == profile_id
        ]
        if len(filtered_df) > 0:
            # Extract the chainage value for each column
            for col in filtered_df.columns[1:]:
                try:
                    chainage = list(filtered_df[col])[0].split(",")[0]
                    elevation = list(filtered_df[col])[0].split(",")[3]
                    chainage_values.append(chainage)
                    elevation_values.append(elevation)

                except AttributeError as ae:
                    pass

            x_values = list(map(float, chainage_values))
            y_values = list(map(float, elevation_values))

            return x_values, y_values

        else:
            print(
                f"No data could be found for the {profile_id}, does the master profile table have this profile in it?"
            )
            return None

    def filter_df_for_master_profile(
        df: object, start_chainage: float, end_chainage: float, section_elevation: float
    ):
        """Function filters the target profile df for data within the bounds of the master profile.
        This is achieved by removing all elevation data below MLSW and corresponding chainage. Then removing all
        chainage and corresponding elevation data lower than the upper chainage limit (the master profile start chainag
        Need to factor in removing elevation values that are above MLSW but after where the elevation has dipped below
        ML

        Returns x: filtered chainage, y: filtered elevation
        """

        # Extract Numpy arrays of the chainage and elevation data
        chainage = df["chainage"].values
        elevation = df["elevation_OD"].values

        # Create an interpolation function - interpolate the data to get more points
        interpolation_func = interp1d(chainage, elevation, kind="linear")

        # Create an array of x values for interpolation- get the values of the interpolated data (set to 200 points)
        global interpolated_x_values
        interpolated_x_values = np.linspace(min(chainage), max(chainage), num=5000)

        # Use the interpolation function to get y values
        global interpolated_y_values
        interpolated_y_values = interpolation_func(interpolated_x_values)

        # filter the interpolation values for the mlsw - elevation on the y-axis:
        filtered_elevation_indices = interpolated_y_values >= section_elevation
        filtered_chainage_lower = interpolated_x_values[filtered_elevation_indices]
        filtered_elevation_lower = interpolated_y_values[filtered_elevation_indices]

        # filter for lower chainage limit - chainage on the x-axis
        filtered_chainage_indices = filtered_chainage_lower >= start_chainage
        filtered_chainage_upper = filtered_chainage_lower[filtered_chainage_indices]
        filtered_elevation_upper = filtered_elevation_lower[filtered_chainage_indices]

        # filter for upper section chainage limit - chainage on the x-axis
        filtered_chainage_indices = filtered_chainage_upper <= end_chainage
        filtered_chainage_upper1 = filtered_chainage_upper[filtered_chainage_indices]
        filtered_elevation_upper1 = filtered_elevation_upper[filtered_chainage_indices]

        # clean the namespace setting the filtered data to a better name
        filtered_chainage = filtered_chainage_upper1
        filtered_elevation = filtered_elevation_upper1

        return filtered_chainage, filtered_elevation

    def calculate_area(
        x_values: object, y_values: object, start_x: float, baseline_y: float
    ):
        """Calculate the area under the curve starting from a specific x-value and using a baseline y-value"""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            def integrand(x):
                return baseline_y - np.interp(x, x_values, y_values)

            area, _ = quad(integrand, start_x, max(x_values))
            return area

    def get_area(df, target_profile, target_date):
        """Function extracts the area for the given input params, also handles the creation of the
        profile sections for each area calculation"""

        total_area = []  # holds the area calculations for each profile section

        # filter the df of all data for survey unit for the specific profile and date
        filter_df_for_profile = df.loc[
            (df["reg_id"] == target_profile) & (df["date"] == target_date)
        ]

        master_profile_xy = extract_chainage_elevation(profile_id=target_profile)
        master_profile_chainage = master_profile_xy[0]
        master_profile_elevation = master_profile_xy[1]
        zipped_master_profile_data = list(
            zip(master_profile_chainage, master_profile_elevation)
        )

        # create the sections to calculate area for
        sections = [
            (zipped_master_profile_data[i], zipped_master_profile_data[i + 1])
            for i in range(len(zipped_master_profile_data) - 1)
        ]

        # zip and iterate over each xy pair for master profile chainage and elevation - the sections to calculate area for.
        for section_data in sections:
            start_chainage = section_data[0][0]
            end_chainage = section_data[1][0]
            section_elevation = section_data[0][1]

            # filter the df for section
            filtered_chainage, filtered_elevation = filter_df_for_master_profile(
                df=filter_df_for_profile,
                start_chainage=start_chainage,
                end_chainage=end_chainage,
                section_elevation=section_elevation,
            )

            # check if any data found in section before calculating area
            if len(filtered_chainage) > 0:
                area = abs(
                    calculate_area(
                        filtered_chainage,
                        filtered_elevation,
                        min(filtered_chainage),
                        section_elevation,
                    )
                )
                total_area.append(area)

        return sum(total_area)

    def get_csa_data(target_survey_unit):
        df = get_data(target_survey_unit=target_survey_unit)
        dates = df["date"].unique()
        dfs = []

        for date in dates:
            df_filter_by_date = df.loc[df["date"] == date]
            profiles_for_date = df_filter_by_date["reg_id"].unique()
            data = []
            for profile in profiles_for_date:
                area = get_area(df=df, target_profile=profile, target_date=date)
                data.append((date, profile, area))

            for data_set in data:
                df1 = pd.DataFrame([data_set], columns=["Date", "Profile", "area"])
                dfs.append(df1)

        master_df = pd.concat(dfs)

        return master_df

    master_df = get_csa_data(survey_unit)

    # Pivot the data
    pivot_df = master_df.pivot(index="Profile", columns="Date", values="area")
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
        height=600,
        template="plotly_dark",
    )

    # Update x-axis tick labels
    fig.update_layout(
        title={
            "text": f"",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font={"size": 15, "family": "Helvetica", "color": "white"},
        xaxis_title="",
        yaxis_title="Combined Profile Area (m²)",
        legend_title="",
        font=dict(size=15, color="white", family="Helvetica"),
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle=45,
            tickfont=dict(
                size=15,  # Set the font size
                color="white",  # Set the font color
                family="Helvetica",  # Set the font family
            ),
        ),
    )

    # increase marker size
    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(
                width=0,
            ),
        ),
        selector=dict(mode="markers"),
    )

    # add linear regression line for whole sample
    fig.add_traces(go.Scatter(x=x_mdates, y=regline, mode="lines", name="Trend"))
    return fig, f"{state}: {round(accretion_levels, 1)}m² yˉ¹ ", df_store
