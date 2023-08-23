import dash_bootstrap_components as dbc
from dash import html, dcc,callback, Input, Output
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


MLSW = -1.2
UPPER_CHAINAGE_LIMIT = 0

layout = html.Div([
    dbc.Container(dbc.Row(
        [
            dbc.Col(dcc.Graph(id="scatter_plot",
                              ),

                    width={"size": 6, 'offset': 0, "order": 2},
                    style={"margin-left": 0, "margin-top": 10, 'background-colour':'white' },

                    )
        ]
    ),
    style={'background-color': '#1b1c1c',
           "margin": 0,       # Remove container margin
            "padding": 0 }      # Remove container padding

    )
])

@callback(
    (Output("scatter_plot", "figure")),
    [
        Input('survey-unit-dropdown', 'value'),

    ],
)

def make_scatter_plot(selected_survey_unit):

    current_year = datetime.now().year
    survey_unit = selected_survey_unit

    def get_data():

        """ Establish database connection and get data and return df """
        conn = psycopg2.connect(
            database="Dash_DB",
            user="postgres",
            password="Plymouth_C0",
            host="localhost",
            port="5432"
        )

        # Import spatial data as GeoDataFrame
        query = f"SELECT * FROM topo_data WHERE survey_unit = '{survey_unit}'"  # Modify this query according to your table
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_survey_unit_profiles(df):
        return df['reg_id'].unique()

    def get_survey_unit_dates(df):
        return df['date'].unique()

    def filter_df_for_master_profile(df):

        """Function filters the target profile df for data within the bounds of the master profile.
           This is achieved by removing all elevation data below MLSW and corresponding chainage. Then removing all
           chainage and corresponding elevation data lower than the upper chainage limit (the master profile start chainage),

           Need to factor in removing elevation values that are above MLSW but after where the elevation has dipped below
           MLSW.

           """

        # Extract Numpy arrays of the chainage and elevation data
        chainage = df['chainage'].values
        elevation = df['elevation_OD'].values

        # Create an interpolation function - interpolate the data to get more points
        interpolation_func = interp1d(chainage, elevation, kind='linear')

        # Create an array of x values for interpolation- get the values of the interpolated data (set to 200 points)
        interpolated_x_values = np.linspace(min(chainage), max(chainage), num=200)

        # Use the interpolation function to get y values
        interpolated_y_values = interpolation_func(interpolated_x_values)

        # filter the interpolation values for the mlsw - elevation on the y-axis:
        filtered_elevation_indices = interpolated_y_values >= MLSW
        filtered_chainage_lower = interpolated_x_values[filtered_elevation_indices]
        filtered_elevation_lower = interpolated_y_values[filtered_elevation_indices]

        # filter for upper chainage limit - chainage on the x-axis
        filtered_chainage_indices = filtered_chainage_lower >= UPPER_CHAINAGE_LIMIT
        filtered_chainage_upper = filtered_chainage_lower[filtered_chainage_indices]
        filtered_elevation_upper = filtered_elevation_lower[filtered_chainage_indices]

        # clean the namespace setting the filtered data to a better name
        filtered_chainage = filtered_chainage_upper
        filtered_elevation = filtered_elevation_upper

        # print(filtered_chainage)
        # print(filtered_elevation)

        # plt.figure(figsize=(10, 6))
        # plt.plot(interpolation_func.x,interpolation_func.y)
        # plt.plot(interpolated_x_values, interpolated_y_values, 'o', label='Data')
        # plt.show()

        return filtered_chainage, filtered_elevation

    def calculate_area(x, y):

        """Calculate the area using the profile data that has been filtered by the master profile bounds"""

        area = np.trapz(y=y, x=x)
        return area

    loaded_data_df = get_data()

    def make_cpa_df(df):

        dfs = []

        for date in get_survey_unit_dates(df):

            df_filter_by_date = df.loc[df['date'] == date]
            profiles_for_date = get_survey_unit_profiles(df_filter_by_date)
            data = []
            for profile in profiles_for_date:
                filter_df_for_profile = df_filter_by_date.loc[df_filter_by_date['reg_id'] == profile]
                filtered_master_profile_data = filter_df_for_master_profile(filter_df_for_profile)
                area = calculate_area(filtered_master_profile_data[0], filtered_master_profile_data[1])
                data.append((date, profile, area))

            for data_set in data:
                df1 = pd.DataFrame([data_set], columns=['Date', 'Profile', 'area'])
                dfs.append(df1)

        master_df = pd.concat(dfs)

        # Pivot the data
        pivot_df = master_df.pivot(index='Profile', columns='Date', values='area')
        pivot_df.loc['total'] = pivot_df.iloc[:, :-1].sum()
        # Pivot the data
        pivot_df = master_df.pivot(index='Profile', columns='Date', values='area')
        pivot_df.loc[:, 'Mean'] = pivot_df.mean(axis=1)

        # Add column with representing the sum of the total number of dates in df
        pivot_df.loc[:, 'countSurveyedDates'] = (len(list(pivot_df)) - 1) / 2

        # Add column representing the sum of the total number NaNs in each row
        pivot_df.loc[:, 'NaNCount'] = pivot_df.isnull().sum(axis=1)

        # Logic for determining if the number of NaNs is more than half the number of total number of dates surveyed
        pivot_df.loc[:, 'DropRow'] = pivot_df['countSurveyedDates'] > pivot_df['NaNCount']


        return pivot_df

    cpa_df = make_cpa_df(loaded_data_df)

    # get the filtered for NaNs as new df for plotting
    cpa_df = cpa_df.loc[cpa_df['DropRow'] == True]

    # remove NaNCount, DropRow columns
    cpa_df = cpa_df.drop(['NaNCount', 'DropRow', 'countSurveyedDates', 'Mean'], axis=1)

    # fill NaN values in each row with Mean
    cpa_df = cpa_df.T.fillna(cpa_df.mean(axis=1)).T

    # add a sum of columns to df
    cpa_df.loc['Sum'] = cpa_df.sum()
    cpa_df = pd.DataFrame(cpa_df)
    cpa_df = cpa_df.transpose()
    cpa_df = cpa_df["Sum"]
    df2 = pd.DataFrame(cpa_df)
    df2['index1'] = df2.index
    chart_ready_df = df2
    chart_ready_df['index1'] = pd.to_datetime(chart_ready_df['index1'], format='%Y-%m-%d')

    # Mapping seasons to each date
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

    # Adding seasons to chart_ready_df as column
    chart_ready_df['season'] = season_list

    # extracting values as lists for the y and x-axis
    x_axis = list(df2['index1'])
    y_axis = list(df2['Sum'])

    # Convert x_axis to number format - needed for correlation calculation
    x_mdates = mdates.date2num(x_axis)

    # Create df3
    chart_ready_df = pd.DataFrame({'Sum': list(df2['Sum'])})

    # Store x-axis data and season_list in df3
    chart_ready_df['season'] = season_list
    chart_ready_df['x'] = x_mdates

    # Define tick positions and tick labels
    x_min = min(x_axis)
    x_max = max(x_axis)
    num_ticks = 10
    tick_dates = pd.date_range(start=x_min, end=x_max, periods=num_ticks)
    tickvals = mdates.date2num(tick_dates)  # Convert tick dates to number format
    ticktext = tick_dates.strftime('%Y-%m')

    # linear regression fit
    regline = sm.OLS(chart_ready_df['Sum'], sm.add_constant(chart_ready_df["x"])).fit().fittedvalues

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
    r_squared = round((correlation_xy ** 2), 3)
    # print("R² Value: " + str(r_squared))

    # obtain the average area for all profiles for all years
    yearly_summed_area = (list(df2['Sum']))

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
    fig = px.scatter(chart_ready_df, x='x', y='Sum', color="season", symbol='season', height=600, template='plotly_dark')

    # Update x-axis tick labels
    fig.update_layout(
        title={'text': f'{state}: {round(accretion_levels, 1)}m² yˉ¹ ',
               'y': 0.95,
               'x': 0.5,
               'xanchor': 'center',
               'yanchor': 'top',


               },
        title_font={'size': 15, 'family': "Helvetica", 'color': "white"},
        xaxis_title="",
        yaxis_title="Combined Profile Area (m²)",
        legend_title="",
        font=dict(
            size=11,
            color="white",
            family= "Helvetica"

        ),
        xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext,
            tickangle= 45,
            tickfont=dict(
                size=12,  # Set the font size
                color='white',  # Set the font color
                family='Helvetica'  # Set the font family
            )

        )
    )

    # increase marker size
    fig.update_traces(marker=dict(size=10,
                                  line=dict(width=0,
                                            )),
                      selector=dict(mode='markers'))

    # add linear regression line for whole sample
    fig.add_traces(go.Scatter(x=x_mdates, y=regline,
                              mode='lines',
                              name='Trend')
                   )

    return fig


















