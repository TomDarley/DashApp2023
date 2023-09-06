from dash import Output, Input, html, callback, dcc,State
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import dash_bootstrap_components as dbc
from dash import dcc,dash_table,Dash

layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dash_table.DataTable(id = 'CSA_table',  style_cell={'textAlign': 'left'},style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },),

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
    (Output("CSA_table", "data"),Output("CSA_table", "columns")),
    [Input("selected-df-storage", "data")],
)

def make_csa_table(selected_csa_data):

    df = pd.read_json(selected_csa_data)
    df= df.drop(df.index[-1])



    spring_range = [1, 2, 3, 4]
    summer_range = [5, 6, 7, 8]
    autumn_range = [9, 10, 11, 12]
    all_dates = []



    classify_dates ={'Spring':[], 'Summer':[], 'Autumn': []}
    for x in df.columns:

        to_date = datetime.strptime(str(x), "%Y-%m-%d %H:%M:%S").date()


        #to_date  =x


        all_dates.append(to_date)
        if to_date.month in spring_range:
            classify_dates['Spring'].append(to_date)
        elif to_date.month in summer_range:
            classify_dates['Summer'].append(to_date)
        elif to_date.month in autumn_range:
            classify_dates['Autumn'].append(to_date)

    print(all_dates)


    latest_survey = max(all_dates)
    first_survey = min(all_dates)
    print(latest_survey)
    print(first_survey)

    latest_spring = sorted(classify_dates.get('Spring'), reverse=False)[-1]
    last_years_spring = sorted(classify_dates.get('Spring'), reverse=False)[-2]

    print(latest_spring)
    print(last_years_spring)
    #print(classify_dates)

    cols = list(df.columns.astype(str))
    df = df.set_axis(cols, axis=1)
    df= df.reset_index()

    df = df[['index',str(first_survey),str(last_years_spring),str(latest_spring)]]

    df['Spring to Spring Diff (m2)'] = ((df[str(last_years_spring)] - df[str(latest_spring)]))
    df['Spring to Spring % Change'] = ((df[str(last_years_spring)] - df[str(latest_spring)]) / df[
        str(latest_spring)]) * 100

    df['Baseline to Spring Diff (m2)'] = ((df[str(first_survey)] - df[str(latest_spring)]))

    df['Baseline to Spring % Change'] = ((df[str(first_survey)] - df[str(latest_spring)]) / df[
        str(latest_spring)]) * 100


    cols = list(df.columns.astype(str))
    df = df.set_axis(cols, axis=1)
    for x in cols:
        print(type(x))

    df= df[['index','Spring to Spring Diff (m2)','Spring to Spring % Change','Baseline to Spring Diff (m2)','Baseline to Spring % Change']]



    df1 = df.to_dict('records')
    print(df1)


    # Define the columns for the DataTable
    columns = [{"name": i, "id": i} for i in df.columns]
    print(columns)




    return  df1, columns
