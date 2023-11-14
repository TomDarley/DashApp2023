import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


df= pd.read_csv(r'C:\Users\darle\PycharmProjects\DashAppHome_2023\SS\multi_line.csv')

years = list(df['year'].unique().astype(int))
months =list(df['month'].unique())

latest_year = max(years)
default_month = 'summer'


print(latest_year)
spring_range = [1, 2, 3, 4]

summer_range = [5, 6, 7, 8]

autumn_range = [9, 10, 11, 12]


# Function to determine the season based on the month
def get_season(month):
    if month in spring_range:
        return 'spring'
    elif month in summer_range:
        return 'summer'
    elif month in autumn_range:
        return 'autumn'
    else:
        return 'winter'

df['season'] = df['month'].apply(get_season)
print(years, months)

filtered_df = df[(df['year'] == latest_year ) & (df['season'] == default_month)]
print(filtered_df.columns)

fig = px.line_3d(
                filtered_df,
                x="chainage",
                y="reg_id",
                z="elevation_od",
                color="reg_id",
                custom_data=['date', 'chainage', 'elevation_od', 'reg_id'],
                #category_orders={"date": date_order},
                #color_discrete_map=custom_color_mapping,

            )
# Changing the style of the three profiles initially loaded
# Format the label shown in the hover
fig.update_traces(
    hovertemplate="<b>Profile:</b> %{customdata[3]}<br>"+"<b>Date:</b> %{customdata[0]}<br>" +
                  "<b>Chainage:</b> %{customdata[1]}<br>" +
                  "<b>Elevation OD:</b> %{customdata[2]}<br><b><extra></extra>"
)

# Set custom axis labels
fig.update_layout(
    scene=dict(
        xaxis_title="Chainage (m)",
        yaxis_title="Profile",
        zaxis_title="Elevation (m)",
    ),
    title=f"{latest_year} - {default_month}",
)
fig.show()