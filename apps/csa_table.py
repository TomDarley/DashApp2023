from dash import Output, Input, html, callback, dash_table,dcc
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
from io import StringIO


def handle_survey_dates(df):
    """Function used to pick the correct dates to show in the CSA table"""

    # ranges used to decide the survey type
    spring_range = [1, 2, 3, 4]
    summer_range = [5, 6, 7, 8]
    autumn_range = [9, 10, 11, 12]

    all_dates = []
    for x in df.columns:
        to_date = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date()
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

    print(f"Is Scilly Unit: {is_scilly_unit}")
    print(f"First Survey: {first_survey}")

    if not is_scilly_unit:
        # Logic to check if the first survey is an Autumn if it is keep removing dates until the next date is not an autumn
        while latest_survey.month in autumn_range:
            try:
                all_dates.remove(latest_survey)
                latest_survey = max(all_dates)
            except Exception as e:
                print(e)

        print(f"Latest Survey: {latest_survey}")
        all_dates_most_recent_removed = all_dates[:-1]
        next_spr_or_baseline = all_dates_most_recent_removed[-1]

        while next_spr_or_baseline.month in autumn_range:
            try:
                all_dates_most_recent_removed.remove(next_spr_or_baseline)
                next_spr_or_baseline = all_dates_most_recent_removed[-1]
            except Exception as e:
                print(e)
        print(f"Next Spring or Baseline: {next_spr_or_baseline}")

    elif is_scilly_unit:
        next_spr_or_baseline = all_dates[-2]

    else:
        print("Something has gone very wrong!")
        return None, None, None, None

    return is_scilly_unit, latest_survey, first_survey, next_spr_or_baseline,

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
    [dcc.Store(
            id="csa_header_store",
            data={"spr_spr": None,"baseline_spr":None},
        ),
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

    #  load in the csa table from the store, json to df
    df = pd.read_json(StringIO(selected_csa_data))
    df = df.drop(df.index[-1])

    is_scilly_unit, latest_survey, first_survey, next_spr_or_baseline = handle_survey_dates(df)

    ## ranges used to decide the survey type
    #spring_range = [1, 2, 3, 4]
    #summer_range = [5, 6, 7, 8]
    #autumn_range = [9, 10, 11, 12]
    #all_dates = []
#
    #classify_dates = {"Spring": [], "Summer": [], "Autumn": []}
    #for x in df.columns:
    #    to_date = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date()
#
    #    all_dates.append(to_date)
    #    if to_date.month in spring_range:
    #        classify_dates["Spring"].append(to_date)
    #    elif to_date.month in summer_range:
    #        classify_dates["Summer"].append(to_date)
    #    elif to_date.month in autumn_range:
    #        classify_dates["Autumn"].append(to_date)
#
    ## get the target columns using dates
    #latest_survey = max(all_dates)
    #first_survey = min(all_dates)
#
    ## bool holds if a second to last spring exists
    #no_second_to_last_spring = False
#
    ## We look for the second to last spring date found, in try as might not be one
    #try:
    #    latest_spring = sorted(classify_dates.get("Spring"), reverse=False)[-1]
    #    no_second_to_last_spring = False
    #except Exception:
    #    no_second_to_last_spring = True
    #    pass
#
    ## Scillies are surveyed in the autumn we handle this here. Swap to look for autumns.
    #not_enough_springs = False
    #try:
    #    last_years_spring = sorted(classify_dates.get("Spring"), reverse=False)[-2]
#
    #except IndexError as ie:
    #    # index error will be thrown as no springs oo look for.
    #    print(ie)
    #    not_enough_springs = True
#
    ## logic to catch if springs exist but not
    #if latest_survey.month in  autumn_range and first_survey.month in autumn_range:
    #    not_enough_springs = True
#
#
    #if not_enough_springs:
    #    last_years_spring = sorted(classify_dates.get("Autumn"), reverse=False)[-2]
    #    latest_spring = sorted(classify_dates.get("Autumn"), reverse=False)[-1]

    cols = list(df.columns.astype(str))
    df = df.set_axis(cols, axis=1)
    df = df.reset_index()

    #df = df[["index", first_survey, next_spr_or_baseline, latest_survey]]

    #is_scilly_unit, latest_survey, first_survey, next_spr_or_baseline

    # get the target date columns only
    #df = df[["index", str(first_survey), str(last_years_spring), str(latest_spring)]]

    df = df[["index", str(first_survey), str(next_spr_or_baseline), str(latest_survey)]]

    # change the table names depending on the season being used
    if is_scilly_unit:
        spr_dif_name = f"Autumn to Autumn Diff (m2)"
        spr_per_name = f"Autumn to Autumn % Change"
        base_dif_name = f"Baseline to Autumn Diff (m2)"
        base_per_name = f"Baseline to Autumn % Change"
    else:
        spr_dif_name = f"Spring to Spring Diff (m2)"
        spr_per_name = f"Spring to Spring % Change"
        base_dif_name = f"Baseline to Spring Diff (m2)"
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

    # Define the functions to map values to colors
    def difference_values_to_color(value):
        # Define your logic to map values to colors here
        # This is just a sample logic, replace it with your actual logic
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

    df_for_map  = df

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

    #df_for_map = df_for_map[['Profile', 'Spring to Spring Diff Color', 'Baseline to Spring Diff Color']]
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
                "Baseline to Autumn Diff (m2)",
                "Baseline to Autumn % Change",
            ]
        ]

    else:
        spr_spr_df = df[
            ["Profile", "Spring to Spring Diff (m2)", "Spring to Spring % Change"]
        ]

        base_spr_df = df[
            [
                "Profile",
                "Baseline to Spring Diff (m2)",
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
