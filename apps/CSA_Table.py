from dash import Output, Input, html, callback, dcc,State
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import dcc,dash_table,Dash



style_data_conditional = [
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} <= -30',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'rgb(255, 0, 0)',
        'color': 'white'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= -30 && {Spring to Spring Diff (m2)} <= -15',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(255, 102, 102)',
        'color': 'white'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= -15 && {Spring to Spring Diff (m2)} <= -5',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(255, 153, 153)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= -5 && {Spring to Spring Diff (m2)} <= 5',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'grey',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= 5 && {Spring to Spring Diff (m2)} <= 15',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(204, 224, 255)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= 15 && {Spring to Spring Diff (m2)} <= 30',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(128, 179, 255)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Spring to Spring Diff (m2)} >= 30',
            'column_id': 'Spring to Spring Diff (m2)'
        },
        'backgroundColor': ' RGB(6, 117, 255)',
        'color': 'black'
    },
    ################################################################## Baseline to Spring Diff (m2)
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} <= -30',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'rgb(255, 0, 0)',
        'color': 'white'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= -30 && {Baseline to Spring Diff (m2)} <= -15',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(255, 102, 102)',
        'color': 'white'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= -15 && {Baseline to Spring Diff (m2)} <= -5',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(255, 153, 153)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= -5 && {Baseline to Spring Diff (m2)} <= 5',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'grey',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= 5 && {Baseline to Spring Diff (m2)} <= 15',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(204, 224, 255)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= 15 && {Baseline to Spring Diff (m2)} <= 30',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': 'RGB(128, 179, 255)',
        'color': 'black'
    },
    {
        'if': {
            'filter_query': '{Baseline to Spring Diff (m2)} >= 30',
            'column_id': 'Baseline to Spring Diff (m2)'
        },
        'backgroundColor': ' RGB(6, 117, 255)',
        'color': 'black'
    },


]


layout = html.Div(
    [

                    dash_table.DataTable(id = 'CSA_table', sort_action='native',sort_mode='single', style_cell={'textAlign': 'center'},style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white','font-size':20

    },columns=[{'name': 'Profile', 'id': 'Profile'}, {'name': 'Spring to Spring Diff (m2)', 'id': 'Spring to Spring Diff (m2)'}, {'name': 'Spring to Spring % Change', 'id': 'Spring to Spring % Change'}, {'name': 'Baseline to Spring Diff (m2)', 'id': 'Baseline to Spring Diff (m2)'}, {'name': 'Baseline to Spring % Change', 'id': 'Baseline to Spring % Change'}],
    style_data_conditional=style_data_conditional,




        ),

                ], style ={'margin-left':'0px', "margin-right": "20px","margin-bottom":"50px","margin-top":"30px"  })
@callback(
    (Output("CSA_table", "data"),Output("CSA_table", "columns")),
    [Input("selected-df-storage", "data")],
)

def make_csa_table(selected_csa_data):

    # load in the csa table from the store, set in the scatter plot app
    df = pd.read_json(selected_csa_data)
    df= df.drop(df.index[-1])


    # ranges used to decide the survey type
    spring_range = [1, 2, 3, 4]
    summer_range = [5, 6, 7, 8]
    autumn_range = [9, 10, 11, 12]
    all_dates = []



    classify_dates ={'Spring':[], 'Summer':[], 'Autumn': []}
    for x in df.columns:

        to_date = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date()

        all_dates.append(to_date)
        if to_date.month in spring_range:
            classify_dates['Spring'].append(to_date)
        elif to_date.month in summer_range:
            classify_dates['Summer'].append(to_date)
        elif to_date.month in autumn_range:
            classify_dates['Autumn'].append(to_date)

    print(all_dates)

    # get the target columns using dates
    latest_survey = max(all_dates)
    first_survey = min(all_dates)

    latest_spring = sorted(classify_dates.get('Spring'), reverse=False)[-1]
    last_years_spring = sorted(classify_dates.get('Spring'), reverse=False)[-2]

    cols = list(df.columns.astype(str))
    df = df.set_axis(cols, axis=1)
    df= df.reset_index()

    # get the target date columns only
    df = df[['index',str(first_survey),str(last_years_spring),str(latest_spring)]]

    spr_dif_name =f'Spring to Spring Diff (m2)'
    spr_per_name = f'Spring to Spring % Change'
    base_dif_name = f'Baseline to Spring Diff (m2)'
    base_per_name = f'Baseline to Spring % Change'


    ## calculate the change add as columns
    #df[spr_dif_name] = ((df[str(last_years_spring)] - df[str(latest_spring)])).round(2)
    #df[spr_per_name] = (((df[str(last_years_spring)] - df[str(latest_spring)]) / df[
    #    str(latest_spring)]) * 100).round(2)
    #df[base_dif_name] = ((df[str(first_survey)] - df[str(latest_spring)])).round(2)
    #df[base_per_name] = (((df[str(first_survey)] - df[str(latest_spring)]) / df[
    #    str(latest_spring)]) * 100).round(2)

    # calculate the change add as columns
    df[spr_dif_name] = ((df[str(latest_spring)] - df[str(last_years_spring)])).round(2)
    df[spr_per_name] = (((df[str(latest_spring)] - df[str(last_years_spring)]) / df[
        str(last_years_spring)]) * 100).round(2)
    df[base_dif_name] = ((df[str(latest_spring)] - df[str(first_survey)])).round(2)
    df[base_per_name] = (((df[str(latest_spring)] - df[str(first_survey)]) / df[
        str(first_survey)]) * 100).round(2)

    # select only the columns we want from the df
    df= df[['index',spr_dif_name, spr_per_name,base_dif_name,base_per_name]]

    df= df.rename(columns ={'index': 'Profile'})

    # convert to records format required by dash table
    df1 = df.to_dict('records')

    # Define the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]

    print(columns)



    return  df1, columns
