import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
selected_sur_unit = '6aSU12'
selected_profile = '6a01613'

df= pd.read_csv(r'C:\Users\darle\PycharmProjects\Dash_App_Master\DashApp2023\data.csv')
df= df.set_index('Unnamed: 0')
print(df)


spring_range = [1, 2, 3, 4]
summer_range = [5, 6, 7, 8]
autumn_range = [9, 10, 11, 12]
all_dates =[]
classify_dates ={'Spring':[], 'Summer':[], 'Autumn': []}
for x in df.columns:

    to_date = datetime.strptime(x, "%Y-%m-%d").date()
    all_dates.append(to_date)
    if to_date.month in spring_range:
        classify_dates['Spring'].append(to_date)
    elif to_date.month in summer_range:
        classify_dates['Summer'].append(to_date)
    elif to_date.month in autumn_range:
        classify_dates['Autumn'].append(to_date)

latest_survey = max(all_dates)
first_survey = min(all_dates)
print(latest_survey)
print(first_survey)

latest_spring = sorted(classify_dates.get('Spring'), reverse=False)[-1]
last_years_spring = sorted(classify_dates.get('Spring'), reverse=False)[-2]

print(latest_spring)
print(last_years_spring)
#print(classify_dates)

df = df[[str(first_survey),str(last_years_spring),str(latest_spring)]]
df['Spring_to_Spring % Change'] = ((df[str(last_years_spring)] - df[str(latest_spring)]) / df[str(latest_spring)]) * 100
df['Baseline_to_Spring % Change'] = ((df[str(first_survey)] - df[str(latest_spring)]) / df[str(latest_spring)]) * 100


cols = ['a','b','c','d','f']
df =df.set_axis(cols, axis=1)
print(df)