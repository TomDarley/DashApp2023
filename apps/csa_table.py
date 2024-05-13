from dash import Output, Input, html, callback, dash_table,dcc
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
from io import StringIO

"""App for creating the CSA table. As well as making the table there is a section which creates a table saved to 
   a store that is read by the map, to color the profile lines. It is convenient to do this from here as this 
   is where the cpa for the profile lines is processed. 
   
   Note the CPA table layout is actually two tables, spr -spr and baseline-spring."""


def handle_survey_dates(df):
    """
        Function used to determine the appropriate survey dates to display in the CSA table. The isles of Scilly
        cause a unique headache as they are surveyed in the Autumn. Therefore, logic is needed to switch the dates
        to extract data from and change table column names etc.

        Parameters:
            df (DataFrame): A pandas DataFrame containing survey dates as column names.

        Returns:
            Tuple: A tuple containing information about the survey dates.
                - is_scilly_unit (bool): True number of Autumns is > number of Other Seasons, True False otherwise.
                - latest_survey (date): The date of the latest survey recorded in the dataset.
                - first_survey (date): The date of the earliest survey recorded in the dataset.
                - next_spr_or_baseline (date): The next spring or baseline survey date after removing autumn surveys.

        Details:
            This function processes survey dates to determine the appropriate dates to display in the Coastal
            State Assessment (CSA) table. It evaluates whether the survey data pertains to the Scilly unit based
            on the prevalence of autumn surveys. If the majority of surveys occur during autumn months, it considers
            the data as being from a Scilly unit. Otherwise, it assumes data is from other units.

            For non-Scilly units:
            - It removes autumn surveys to prioritize spring or baseline surveys.
            - It identifies the latest survey date, earliest survey date, and the next spring or baseline survey date
              following the removal of autumn surveys.

            For Scilly units:
            - It identifies the next spring or baseline survey date without removing any autumn surveys.

            If any errors occur during the processing, the function returns None for all outputs.

        Note:
            This function assumes the DataFrame columns contain datetime information, formatted as "%Y-%m-%d %H:%M:%S".
        """

    # ranges used to decide the survey type
    spring_range = [1, 2, 3, 4]
    summer_range = [5, 6, 7, 8]
    autumn_range = [9, 10, 11, 12]

    all_dates = []
    for date in df.columns:
        to_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").date()
        all_dates.append(to_date)

    latest_survey = max(all_dates)
    first_survey = min(all_dates)

    # logic to work out if the data is from the Scilly
    autumn_count = 0
    other_count = 0
    for date in all_dates:
        if date.month in autumn_range:
            autumn_count += 1
        else:
            other_count += 1

    is_scilly_unit = False
    if autumn_count > other_count:
        is_scilly_unit = True

    if not is_scilly_unit:

        # Logic to check if the first survey is an Autumn if it is keep removing dates until the next date is not an autumn
        while latest_survey.month in autumn_range:
            try:
                all_dates.remove(latest_survey)
                latest_survey = max(all_dates)
            except Exception as e:
                print(e)

        all_dates_most_recent_removed = all_dates[:-1]
        next_spr_or_baseline = all_dates_most_recent_removed[-1]

        while next_spr_or_baseline.month in autumn_range:
            try:
                all_dates_most_recent_removed.remove(next_spr_or_baseline)
                next_spr_or_baseline = all_dates_most_recent_removed[-1]
            except Exception as e:
                print(e)


    elif is_scilly_unit:
        next_spr_or_baseline = all_dates[-2]

    else:
        print("Something has gone very wrong!")
        return None, None, None, None

    return is_scilly_unit, latest_survey, first_survey, next_spr_or_baseline,


# This is style conditional passed to the dcc.table to style the colors of each cell.
style_data_conditional = [
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} <= -30",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= -30 && {Spring to Spring Diff (m2)} <= -15",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= -15 && {Spring to Spring Diff (m2)} <= -5",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= -5 && {Spring to Spring Diff (m2)} <= 5",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= 5 && {Spring to Spring Diff (m2)} <= 15",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= 15 && {Spring to Spring Diff (m2)} <= 30",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring Diff (m2)} >= 30",
            "column_id": "Spring to Spring Diff (m2)",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },
    ################################################################## Baseline to Spring Diff (m2)
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} <= -30",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= -30 && {Baseline to Spring Diff (m2)} <= -15",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= -15 && {Baseline to Spring Diff (m2)} <= -5",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= -5 && {Baseline to Spring Diff (m2)} <= 5",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= 5 && {Baseline to Spring Diff (m2)} <= 15",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= 15 && {Baseline to Spring Diff (m2)} <= 30",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring Diff (m2)} >= 30",
            "column_id": "Baseline to Spring Diff (m2)",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },
    ############################
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} <= -30",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= -30 && {Baseline to Spring % Change} <= -15",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= -15 && {Baseline to Spring % Change} <= -5",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= -5 && {Baseline to Spring % Change} <= 5",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= 5 && {Baseline to Spring % Change} <= 15",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= 15 && {Baseline to Spring % Change} <= 30",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Spring % Change} >= 30",
            "column_id": "Baseline to Spring % Change",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },########

    {
        "if": {
            "filter_query": "{Spring to Spring % Change} <= -30",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= -30 && {Spring to Spring % Change} <= -15",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= -15 && {Spring to Spring % Change} <= -5",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= -5 && {Spring to Spring % Change} <= 5",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= 5 && {Spring to Spring % Change} <= 15",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= 15 && {Spring to Spring % Change} <= 30",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Spring to Spring % Change} >= 30",
            "column_id": "Spring to Spring % Change",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },{
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} <= -30",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= -30 && {Autumn to Autumn Diff (m2)} <= -15",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= -15 && {Autumn to Autumn Diff (m2)} <= -5",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= -5 && {Autumn to Autumn Diff (m2)} <= 5",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= 5 && {Autumn to Autumn Diff (m2)} <= 15",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= 15 && {Autumn to Autumn Diff (m2)} <= 30",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn Diff (m2)} >= 30",
            "column_id": "Autumn to Autumn Diff (m2)",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },
    ################################################################## Baseline to Autumn Diff (m2)
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} <= -30",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= -30 && {Baseline to Autumn Diff (m2)} <= -15",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= -15 && {Baseline to Autumn Diff (m2)} <= -5",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= -5 && {Baseline to Autumn Diff (m2)} <= 5",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= 5 && {Baseline to Autumn Diff (m2)} <= 15",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= 15 && {Baseline to Autumn Diff (m2)} <= 30",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn Diff (m2)} >= 30",
            "column_id": "Baseline to Autumn Diff (m2)",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },
    ############################
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} <= -30",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= -30 && {Baseline to Autumn % Change} <= -15",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= -15 && {Baseline to Autumn % Change} <= -5",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= -5 && {Baseline to Autumn % Change} <= 5",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= 5 && {Baseline to Autumn % Change} <= 15",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= 15 && {Baseline to Autumn % Change} <= 30",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Baseline to Autumn % Change} >= 30",
            "column_id": "Baseline to Autumn % Change",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },########

    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} <= -30",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "#ff0000",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= -30 && {Autumn to Autumn % Change} <= -15",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "#ff6666",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= -15 && {Autumn to Autumn % Change} <= -5",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "#ff9999",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= -5 && {Autumn to Autumn % Change} <= 5",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "grey",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= 5 && {Autumn to Autumn % Change} <= 15",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "#00ace6",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= 15 && {Autumn to Autumn % Change} <= 30",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "rgb(0, 103, 230)",
        "color": "white",
    },
    {
        "if": {
            "filter_query": "{Autumn to Autumn % Change} >= 30",
            "column_id": "Autumn to Autumn % Change",
        },
        "backgroundColor": "rgb(0, 57, 128)",
        "color": "white",
    },

]


layout = html.Div(
    [   # store which holds the table header of the dates used, passed to the report generation
        dcc.Store(
            id="csa_header_store",
            data={"spr_spr": None,"baseline_spr":None},
        ),
        # store for the profile colors, passed to the map app to color each profile.
        dcc.Store(
            id="csa_profile_line_colors",
            data=None,
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Survey Unit:",
                                                id="spring_to_spring_header",
                                                className="card-title",
                                                style={
                                                    "color": "white",
                                                    "margin-bottom": "5px",
                                                    "text-align": "center",
                                                    "backgroundColor": "#0d4eb8",
                                                },
                                            ),
                                            dash_table.DataTable(
                                                id="spr_to_spr_table",
                                                sort_action="native",
                                                sort_mode="single",
                                                style_cell={
                                                    "textAlign": "center",


                                                },
                                                style_header={
                                                    "backgroundColor": "#0d4eb8",
                                                    "color": "white",
                                                    "font-size": 12,
                                                },
                                                columns=[
                                                    {
                                                        "name": "Profile",
                                                        "id": "Profile",
                                                    },
                                                    {
                                                        "name": "Spring to Spring Diff (m2)",
                                                        "id": "Spring to Spring Diff (m2)",
                                                    },
                                                    {
                                                        "name": "Spring to Spring % Change",
                                                        "id": "Spring to Spring % Change",
                                                    },
                                                ],
                                                style_data_conditional=style_data_conditional,
                                                style_table={'overflowX': 'auto'},

                                            ),
                                        ],

                                        id = 'spr_spr_card_body'
                                    )
                                ],
                                id='spr_spr_card',

                            ),
                        ]
                    ),
                    id='spr_spr_col',



                ),
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Baseline to Spring:",
                                                id="baseline_to_spring_header",
                                                className="card-title",
                                                style={
                                                    "color": "white",
                                                    "margin-bottom": "5px",
                                                    "text-align": "center",
                                                    "backgroundColor": "#0d4eb8",
                                                },
                                            ),
                                            dash_table.DataTable(
                                                id="spr_to_baseline_table",
                                                sort_action="native",
                                                sort_mode="single",
                                                style_cell={
                                                    "textAlign": "center",
                                                },
                                                style_header={
                                                    "backgroundColor": "#0d4eb8",
                                                    "color": "white",
                                                    "font-size": 12,
                                                },
                                                columns=[
                                                    {
                                                        "name": "Profile",
                                                        "id": "Profile",
                                                    },
                                                    {
                                                        "name": "Baseline to Spring Diff (m2)",
                                                        "id": "Baseline to Spring Diff (m2)",
                                                    },
                                                    {
                                                        "name": "Baseline to Spring % Change",
                                                        "id": "Baseline to Spring % Change",
                                                    },
                                                ],
                                                style_data_conditional=style_data_conditional,
                                                style_table={'overflowX': 'auto'},
                                            ),
                                        ],
                                        id = 'base_spr_card_body',

                                    )
                                ],
                                id='base_spr_card',

                            ),
                        ]
                    ),
                    id='base_spr_col',





                ),
            ],
            id = 'csa_table_row',


        ),

    ]
)


@callback(
    (
        Output("spr_to_spr_table", "data"),
        Output("spr_to_spr_table", "columns"),
        Output("spring_to_spring_header", "children"),
        Output("spr_to_baseline_table", "data"),
        Output("spr_to_baseline_table", "columns"),
        Output("baseline_to_spring_header", "children"),
        Output("csa_header_store","data"),
        Output("csa_profile_line_colors", 'data')
    ),
    [Input("selected-df-storage", "data"),
    ]
)
def make_csa_table(selected_csa_data):
    """
      Callback function to generate data and formatting for Coastal State Assessment (CSA) tables. Note that
      the logic for abating the CSA data sent to the store is all controlled in the scatter app reducing repeat
      logic for this app.

      Parameters:
          selected_csa_data (str): JSON string containing CSA data.

      Returns:
          Tuple: A tuple containing the data, columns, and other information for displaying CSA tables.
              - spr_to_spr_table_data (list): Data for the "Spring to Spring" CSA table.
              - spr_to_spr_table_columns (list): Columns for the "Spring to Spring" CSA table.
              - spring_to_spring_header (str): Header text for the "Spring to Spring" CSA table.
              - spr_to_baseline_table_data (list): Data for the "Spring to Baseline" CSA table.
              - spr_to_baseline_table_columns (list): Columns for the "Spring to Baseline" CSA table.
              - baseline_to_spring_header (str): Header text for the "Baseline to Spring" CSA table.
              - csa_header_store_data (dict): Data for storing CSA table header information.
              - csa_profile_line_colors (dict): Data for styling CSA profile lines on the map.

      Details:
          This callback function reads JSON data containing Coastal State Assessment (CSA) information,which comes
          from a store created in the scatter plot app. It generates tables for displaying CSA data, and formats the
          tables for presentation. It calculates differences and percentages for various survey intervals, determines
          header text for the tables, and generates color data for styling CSA profile lines on the map.
      """

    #  load in the csa table from the store, json to df
    df = pd.read_json(StringIO(selected_csa_data))
    df = df.drop(df.index[-1])

    is_scilly_unit, latest_survey, first_survey, next_spr_or_baseline = handle_survey_dates(df)

    cols = list(df.columns.astype(str))
    df = df.set_axis(cols, axis=1)
    df = df.reset_index()

    df = df[["index", str(first_survey), str(next_spr_or_baseline), str(latest_survey)]]

    # change the table names depending on the season being used
    if is_scilly_unit:
        spr_dif_name = f"Autumn to Autumn Diff (m²)"
        spr_per_name = f"Autumn to Autumn % Change"
        base_dif_name = f"Baseline to Autumn Diff (m²)"
        base_per_name = f"Baseline to Autumn % Change"
    else:
        spr_dif_name = f"Spring to Spring Diff (m²)"
        spr_per_name = f"Spring to Spring % Change"
        base_dif_name = f"Baseline to Spring Diff (m²)"
        base_per_name = f"Baseline to Spring % Change"

    # calculate the change add as columns
    df[spr_dif_name] = ((df[str(latest_survey)] - df[str(next_spr_or_baseline)])).round(2)
    df[spr_per_name] = (
        (
            (df[str(latest_survey)] - df[str(next_spr_or_baseline)])
            / df[str(next_spr_or_baseline)]
        )
        * 100
    ).round(2)
    df[base_dif_name] = ((df[str(latest_survey)] - df[str(first_survey)])).round(2)
    df[base_per_name] = (
        ((df[str(latest_survey)] - df[str(first_survey)]) / df[str(first_survey)]) * 100
    ).round(2)

    # select only the columns we want from the df
    df = df[["index", spr_dif_name, spr_per_name, base_dif_name, base_per_name]]

    df = df.rename(columns={"index": "Profile"})

    #####################################################################################################
    # SAVING THE CSA TABLE TO STORE TO BE USED IN THE MAP TO STYLE THE LINES, NOTE THIS HAS NOTHING TO DO WITH
    # THE CPA TABLE. IT IS A CONVENIENT PLACE TO EXTRACT THE DATA NEEDED TO COLOR THE MAP LINES.
    def difference_values_to_color(value):
        """
           Function to map difference values to colors.

           Parameters:
               value (float): The difference value to be mapped to a color.

           Returns:
               str: A hexadecimal color code or RGB color representation based on the input value.

           Details:
               This function defines a mapping from difference values to colors. It is used to assign colors
               to cells in Coastal State Assessment (CSA) tables based on the magnitude of difference values.

           """
        if value <= -30:
            return '#ff0000'  # Example color for values less than 20
        elif value >= -30 and value <=-15:
            return '#ff6666'

        elif value >= -15 and value <= -5:
            return '#ff9999'
        elif value >= -5 and value <= 5:
            return '#4f4f54'
        elif value >= 5 and value <= 15:
            return '#00ace6'
        elif value >= 15 and value <= 30:
            return "rgb(0, 103, 230)"
        elif value > 30:
            return "rgb(0, 57, 128)"
        else:
            return 'black'  # Example color for values greater than or equal to 40

    # create a separate df for the map
    df_for_map = df

    if is_scilly_unit:
        df_for_map['Spring to Spring PCT Color'] = df_for_map['Autumn to Autumn % Change'].apply(
            difference_values_to_color)
        df_for_map['Baseline to Spring PCT Color'] = df_for_map['Baseline to Autumn % Change'].apply(
            difference_values_to_color)
    else:
        df_for_map['Spring to Spring PCT Color'] = df_for_map['Spring to Spring % Change'].apply(
            difference_values_to_color)
        df_for_map['Baseline to Spring PCT Color'] = df_for_map['Baseline to Spring % Change'].apply(
            difference_values_to_color)

    df_for_map = df_for_map.to_dict()
    #############################################################################################################

    # split df into two dfs, each representing the table for each card
    if is_scilly_unit:

        spr_spr_df = df[
            ["Profile", "Autumn to Autumn Diff (m2)", "Autumn to Autumn % Change"]
        ]

        base_spr_df = df[
            [
                "Profile",
                "Baseline to Autumn Diff (m²)",
                "Baseline to Autumn % Change",
            ]
        ]

    else:
        spr_spr_df = df[
            ["Profile", "Spring to Spring Diff (m²)", "Spring to Spring % Change"]
        ]

        base_spr_df = df[
            [
                "Profile",
                "Baseline to Spring Diff (m²)",
                "Baseline to Spring % Change",
            ]
        ]

    # convert to records format required by dash table
    spr_spr_df_to_records = spr_spr_df.to_dict("records")
    base_spr_df_to_records = base_spr_df.to_dict("records")

    # Define the columns for the DataTableS
    spr_spr_columns = [{"name": i, "id": i} for i in spr_spr_df.columns]
    base_spr_columns = [{"name": i, "id": i} for i in base_spr_df.columns]

    # Generate the dates as text for the card titles holding each table
    spr_spr_title = f"{next_spr_or_baseline} - {latest_survey}"
    base_spr_title = f"{first_survey} - {latest_survey}"

    # This is passed/used in the report generation to get the dates used
    table_header_data = {'spr_spr':spr_spr_title, 'baseline_spr': base_spr_title}

    return (
        spr_spr_df_to_records,
        spr_spr_columns,
        spr_spr_title,
        base_spr_df_to_records,
        base_spr_columns,
        base_spr_title,
        table_header_data,
        df_for_map
    )
