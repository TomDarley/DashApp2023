import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sqlalchemy import create_engine
import numpy as np


selected_sur_unit  = '6aSU12'
selected_profile  = '6a01613'
# All shapefile loaded into the database should not be promoted to multi
engine = create_engine("postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB")
# Connect to the database using the engine
conn = engine.connect()

# Load topo data from DB
topo_query = f"SELECT * FROM topo_data WHERE survey_unit = '{selected_sur_unit}' AND profile = '{selected_profile}'"  # Modify this query according to your table
topo_df = pd.read_sql_query(topo_query, conn)
topo_df['date'] = pd.to_datetime(topo_df['date']).dt.strftime('%Y-%m-%d')

unique_dates = list(topo_df['date'].unique())

print(unique_dates)


min_chainage = 194
max_chainage = 409
merge_df = pd.DataFrame()

generated_chainage = list(range(min_chainage, max_chainage, 1))
merge_df['chainage'] = generated_chainage
merge_df['chainage'] = merge_df['chainage'].astype(int)

survey_dfs = []  # Assuming this list is supposed to store the results of the merge

unique_dates = topo_df['date'].unique()  # Assuming unique_dates is derived from topo_df

for date in unique_dates:
    df_filter = topo_df.loc[topo_df['date'] == date].copy()

    # Round the chainage values
    df_filter['chainage'] = df_filter['chainage'].round(0).astype(int)

    df_filter = df_filter[['chainage', 'elevation_od']]

    survey_dfs.append(df_filter)  # Append the merged result to the list

# Print or utilize survey_dfs if required
print(survey_dfs)

count =0
for df in survey_dfs:
    merge_df = pd.merge(merge_df, df[["chainage", "elevation_od"]], on="chainage", how="left")
    merge_df = merge_df.rename(columns={"elevation_od": f"elevation_od_{count}"})
    merge_df[f"elevation_od_{count}"]= merge_df[f"elevation_od_{count}"].interpolate(method='polynomial', order=5,
    limit_area = 'inside', limit = 2)
    count+=1

merge_df = merge_df.set_index('chainage')
#merge_df["Max Elevation"] = merge_df.max(axis=1)
max_ele = merge_df.max(axis=1,skipna=True)
average_ele = merge_df.mean(axis=1, skipna=True)
min_ele = merge_df.min(axis=1, skipna=True)

merge_df['Max Elevation'] = max_ele
merge_df['Min Elevation'] = min_ele
merge_df['Mean Elevation'] = average_ele



merge_df.to_csv(r'C:\Users\darle\Desktop\testing\data.csv')
merge_df = merge_df.reset_index()
print(merge_df)


fig = px.line(
            merge_df,
            x="chainage",
            y=["Min Elevation", 'Max Elevation', 'Mean Elevation'],
            #color="date",
            #color_discrete_map=custom_color_mapping,
            template="seaborn",
            #category_orders={"date": date_order},
            #custom_data=['date', 'chainage', 'elevation_od'],)
)

check_df  = topo_df.loc[topo_df['date'] =='2021-06-24']
#trace = go.Scatter(x=check_df['chainage'], y=check_df['elevation_od'], mode='lines', name='Check Data')
trace = go.Scatter(x=topo_df['chainage'], y=topo_df['elevation_od'], mode='markers', name='Check Data')
fig.add_trace(trace)




fig.show()