import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import time


def generate_color_gradient(start_color, end_color, steps):
    """
    Generate a list of hexadecimal colors representing a color gradient. Used to color the profile lines.

    Parameters:
        start_color (tuple): Tuple containing RGB values of the starting color.
        end_color (tuple): Tuple containing RGB values of the ending color.
        steps (int): Number of steps in the color gradient.

    Returns:
        list: A list of hexadecimal colors representing the color gradient.

    Details:
        This function generates a list of hexadecimal colors representing a color gradient
        between the specified start and end colors. It calculates intermediate colors by
        interpolating RGB values based on the number of steps provided. The result is returned
        as a list of hexadecimal color codes.
    """

    # Extract RGB components from the start and end colors
    start_R, start_G, start_B = start_color
    end_R, end_G, end_B = end_color

    # Calculate the step size for each color channel
    delta_R = (end_R - start_R) / steps
    delta_G = (end_G - start_G) / steps
    delta_B = (end_B - start_B) / steps

    # Generate the color ramp
    colors = []
    for step in range(steps):
        # Interpolate RGB values for each step
        R = int(start_R + (delta_R * step))
        G = int(start_G + (delta_G * step))
        B = int(start_B + (delta_B * step))

        # Convert RGB values to hex and append to the colors list
        color_hex = f"#{R:02x}{G:02x}{B:02x}"
        colors.append(color_hex)

    return colors


def generate_custom_colors(num_colors, dates):
    """
        Generate a list of custom colors based on the number of lines to be plotted.

        Parameters:
            num_colors (int): Number of colors required for plotting lines.
            dates (list): List of dates used to generate the color ramp.

        Returns:
            list: A list of custom colors for plotting lines.

        Details:
            This function dynamically generates a list of custom colors for plotting lines based on the number
            of lines that need to be plotted and the dates provided. It generates a color ramp between two
            predefined colors (light blue to a lighter shade of blue) using the 'generate_color_gradient'
            function and then selects a subset of colors evenly spaced across the ramp to ensure
            color differentiation between lines.
        """

    # Generate a list of color names
    start_color = (191, 0, 255)  # Light blue - RGB values
    end_color = (153, 214, 255)
    color_names = generate_color_gradient(start_color, end_color, len(dates))

    # Calculate the number of elements to be taken from the original list
    first_last = 1  # Number of elements to take from the start and end of the list
    middle_count = len(color_names) - 2  # Number of elements excluding the first and last elements

    # Calculate the number of elements for the new list
    num_elements_new_list = first_last * 2 + min(middle_count, num_colors - 2)

    # Calculate the step size to evenly space the elements from the middle part of the list
    if middle_count > 0:
        step = middle_count // (num_elements_new_list - first_last * 2)
    else:
        step = 1

    # Create a new list based on the criteria
    new_list = color_names[:first_last]  # Take the first element from the original list

    # Calculate elements for the middle part
    for i in range(first_last, num_elements_new_list - first_last):
        new_list.append(color_names[i * step])

    new_list += color_names[-first_last:]  # Take the last element from the original list

    return new_list


def establish_connection(retries=3, delay=5):
    """Function attempts to connect to the database. It will retry 3 times before giving up"""

    attempts = 0
    while attempts < retries:
        try:
            # Attempt to create an engine and connect to the database
            engine = create_engine(
                "postgresql://postgres:Plymouth_C0@swcm-dashboard.crh7kxty9yzh.eu-west-2.rds.amazonaws.com:5432/postgres"
            )
            conn = engine.connect()

            # If the connection is successful, return the connection object
            return conn

        except OperationalError as e:
            # Handle the case where a connection cannot be established
            print(f"Error connecting to the database: {e}")
            attempts += 1

            if attempts < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retry attempts reached. Giving up.")
                # Optionally, you can raise an exception, log the error, or take other appropriate actions

    return None


layout = html.Div(
    [
        # store to save line chart to json, used to in the report generation
        dcc.Store(id="line_chart", ),

        # Error Alerts for where data can not be retrieved from the database
        dbc.Alert('No Master Profile Data Could be Found for the Selected Profile',id='mp-alert', color="danger", is_open=False, style= {'margin-top': '50px'}),
        dbc.Alert('No Topo Data Could be Found for the Selected Profile',id='topo-data-alert', color="danger", is_open=False, style= {'margin-top': '50px'}),

        # loading spinner, starts when chart is updating
        dcc.Loading(
            id="loading-chart",
            type="circle",
            children=[

                dcc.Graph(
                    id="line_plot",
                    config={"responsive": True, 'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoscale', ],
                            'displaylogo': False},
                ),
            ], ),

        # adding buttons for modals, full screen and information
        dbc.Button(
            [html.Span(className="bi bi-info-circle-fill")],
            size="md",
            id="line_open_info",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "left": "8px", "border-radius": "5px"},
        ),
        dbc.Button(
            [html.Span(className="fa-solid fa-expand")],
            size="md",
            id="line_open_full",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "right": "8px", "border-radius": "5px"},
        ),

        # add checklist for showing profile envelope.
        dcc.Checklist(
            id='Range_plot',
            options=[
                {"label": "Profile Envelope", "value": "show_range"},
            ],
            value=['show_range'],  # Default selected option
            inline=True,

            inputStyle={
                'marginRight': '5px',
                 'buffer-bottom':'2px'# Add space between the checkbox and label
            },



        ),

        # adding buttons that allow quick left to right navigation of profile charts
        # adding info button/modal for the map
        dbc.Button(
            [html.Span(className="bi bi-arrow-left-circle-fill")],
            size="sm",
            id="line_chart_navigate_left",
            n_clicks=0,
            className="mr-3",
            style={
                'position': 'absolute',
                'bottom': '5px',  # Adjust as needed
                'left': '60px',  # Adjust as needed
                'zIndex': 100,
                'border-radius': 5,
                "width": '80px',
                "height": "30px",
                "lineHeight": "25px",
                "background-color": "lightblue",
                "color": "black",
                "transition": "transform 0.3s ease-in-out"


                # 'fontSize': 13
            },
        ),

        dbc.Button(
            [html.Span(className="bi bi-arrow-right-circle-fill")],
            size="sm",
            id="line_chart_navigate_right",
            n_clicks=0,
            className="mr-3",
            style={
                'position': 'absolute',
                'bottom': '5px',  # Adjust as needed
                'left': '150px',  # Adjust as needed
                'zIndex': 100,
                'border-radius': 5,
                "width": '80px',
                "height": "30px",
                "lineHeight": "25px",
                "background-color": "lightblue",
                "color": "black",
                "transition": "transform 0.3s ease-in-out"

                # 'fontSize': 13
            },
        ),

        # defining the modals, information and full screen
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Profile Cross-Sectional Area Chart", style={"color": "blue"})),
                dbc.ModalBody(
                    [
                        html.P(
                            """This chart represents a cross-section of each beach profile, allowing for a visual comparison of beach change for a certain area across the length of the beach profile.""",
                            style={"font-size": 20, }, ),
                        html.P(
                            """Any number of surveys can be compared by toggling them on or off using the legend function on the right-hand side of the chart. Each profile is displayed against the master profile shown by the dashed red lines, which denotes the seaward boundary of mean low water springs (MLWS) and the landward boundary.""",

                            style={"font-size": 20},
                        ),

                        html.P(
                            """The profile envelope can be displayed or removed using the profile envelope check box. The mean elevation for all profiles is also shown. """,

                            style={"font-size": 20},
                        ),

                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="line_info_close",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="line_info_model",
            is_open=False,
            fullscreen=False,
        ),

        dbc.Modal(
            [
                # dbc.ModalHeader(dbc.ModalTitle("Cross Sectional Line Plot")),
                dbc.ModalBody(
                    dcc.Graph(id="line_plot_model", style={"height": "100vh"},
                              config={"responsive": True,
                                      'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoscale'],
                                      'displaylogo': False},)
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="line_full_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_line_plot",
            is_open=False,
            fullscreen=True,
        ),
    ],
    id='line_plot_div'
)


@callback(
    Output("line_plot", "figure"),
    Output("line_plot_model", "figure"),
    Output("line_chart", "data"),
    Output('mp-alert', 'is_open'),
    Output('topo-data-alert', 'is_open'),

    Input("survey-unit-dropdown", "value"),
    Input("survey-line-dropdown", "value"),

    Input("Range_plot", "value"),
    Input('selected-value-storage', 'data'),
    Input('survey_unit_card', 'children'),

    prevent_initial_call=False,
    allow_duplicate=True,
)
def make_line_plot(selected_sur_unit, selected_profile, radio_selection_range_plot_value, selected_val_storage,
                   survey_unit_card
                   ):
    """
        Create a line plot visualization for the selected survey unit and profile.

        Parameters:
            selected_sur_unit (str): Selected survey unit.
            selected_profile (str): Selected profile.
            radio_selection_range_plot_value (str): Value indicating the selected range for plotting.
            selected_val_storage (list or dict): Selected value storage data.
            survey_unit_card (str): Used for local naming.

        Returns:
            None: If the master profile data has less than three columns, a warning is displayed and no plot is generated.
            Otherwise, the function proceeds to create the line plot visualization.

        Details:
            This function generates a line plot visualization for the selected survey unit and profile.
            It retrieves topographic and master profile data from the database and filters the master profile data
            to ensure it has at least three columns (one column for profile names and two or more columns for profile data points).
            If the master profile data does not meet this requirement, a warning is displayed, and no plot is generated.
            Otherwise, the function proceeds to create the line plot using the retrieved data.
        """

    # convert to dict from list if a list
    if selected_val_storage:
        # convert to a dict if not:
        if isinstance(selected_val_storage, list):
            fixed_val_storage = selected_val_storage[0]
        else:
            fixed_val_storage = selected_val_storage
    else:
        fixed_val_storage = None



    # Load topo  and master profile data from DB, do this first as missing profile data causes algorithms to fail.
    conn = establish_connection()
    topo_query = f"SELECT * FROM topo_data WHERE survey_unit = '{selected_sur_unit}' AND profile = '{selected_profile}'"  # Modify this query according to your table
    topo_df = pd.read_sql_query(topo_query, conn)

    master_profile_query = (
        f"SELECT * FROM new_master_profiles WHERE profile_id = '{selected_profile}'"
    )


    # get mp data as df from aws database
    mp_df = pd.read_sql_query(master_profile_query, conn)
    conn.close()


    # Drop/filter for any mp_df that has less than three columns. One col is the profile names, all others are profile
    # data points.
    mp_df = mp_df.loc[:, mp_df.notna().all()]

    if topo_df.empty:
        topo_data_failed = True
    else:
        topo_data_failed = False

    if len(mp_df.columns) >= 3:
        valid_master_profile_data = False
    else:
        valid_master_profile_data = True

    # Check to see if the mp_df has more than one data point. If not show a warning and return a blank chart.
    if not valid_master_profile_data and not topo_data_failed:

        valid_master_profile_data = False  # holds the is_open bool for warning message

        # check if multi selection is enabled. Note this has now been disabled.
        if fixed_val_storage is not None and fixed_val_storage['multi'] == False:

            if selected_sur_unit is None or selected_profile is None:
                raise PreventUpdate

            selection = "2D"

            # must sort the data by chainage for it to display correctly
            topo_df = topo_df.sort_values(by=["chainage"])

            # Get unique dates for database data
            dates = np.unique(topo_df["date"])

            # Sort the dates
            date_order = sorted(dates)

            custom_color_mapping = {}

            # map each generated color to each date, used to color each profile
            num_colors = len(date_order)
            custom_color_list = generate_custom_colors(num_colors, dates)
            for i, date in enumerate(date_order):
                color_index = i
                custom_color_mapping.update({date: custom_color_list[color_index]})

            # Initial Display of lines  - find the most recent date, date-1 amd first
            first_trace_date = 0
            newest_trace_date = len(date_order) - 1
            previous_trace_date = len(date_order) - 2

            # the traces of the dates to show initially
            initial_visible_traces = [first_trace_date, newest_trace_date, previous_trace_date]

            # Load master profile data from DB, extract chainage and elevation
            master_profile_chainage = list(mp_df['chainage'])
            master_profile_elevation = list(mp_df['elevation'])

            # isolate the min max chainage for profile
            min_chainage = master_profile_chainage[0]
            max_chainage = master_profile_chainage[-1]

            # Determine min and max chainage for profile
            min_chainage = float(min_chainage) - 5
            max_chainage = float(max_chainage) + 5

            # locate the index position of max an min chainge
            topo_df = topo_df.reset_index()

            max_index = topo_df.index.max()
            min_index = topo_df.index.min()

            # Find the index position of the value closest to 10
            closest_max_chainage_index = (topo_df['chainage'] - max_chainage).abs().idxmin()
            next_max_index = closest_max_chainage_index + 1
            if next_max_index > max_index:
                use_max_plus_1 = False
            else:
                use_max_plus_1 = True

            # Find the index position of the value closest to 10
            closest_min_chainage_index = (topo_df['chainage'] - min_chainage).abs().idxmin()
            next_min_index = closest_min_chainage_index + 1
            if next_min_index < min_index:
                use_min_plus_1 = False
            else:
                use_min_plus_1 = True

            # filter the topo df to the max/ min chainage
            if use_max_plus_1 and use_min_plus_1:
                topo_df = topo_df.loc[(topo_df.index >= next_min_index) & (topo_df.index <= next_max_index)]
            elif not use_min_plus_1 and use_max_plus_1:
                topo_df = topo_df.loc[(topo_df.index >= closest_min_chainage_index) & (topo_df.index <= next_max_index)]
            elif use_min_plus_1 and not use_max_plus_1:
                topo_df = topo_df.loc[(topo_df.index >= next_min_index) & (topo_df.index <= closest_max_chainage_index)]

            # disabled all other options so will always run in 2D
            if selection == '2D':

                # Create a 2D line plot
                fig = px.line(
                    topo_df,
                    x="chainage",
                    y="elevation_od",
                    color="date",
                    color_discrete_map=custom_color_mapping,
                    template="plotly",
                    category_orders={"date": date_order},
                    custom_data=['date', 'chainage', 'elevation_od'],

                )

                # Changing the style of the three profiles initially loaded
                profile_names = [fig.data[0].name, fig.data[-2].name, fig.data[-1].name]
                profile_colors = ['brown', 'green', 'blue']
                for name, color in zip(profile_names, profile_colors):
                    fig.update_traces(selector=dict(name=name), line=dict(color=color, width=2, dash='solid'))

                # Format the label shown in the hover
                fig.update_traces(
                    hovertemplate="<b>Date:</b> %{customdata[0]}<br>" +
                                  "<b>Chainage:</b> %{customdata[1]}<br>" +
                                  "<b>Elevation OD:</b> %{customdata[2]}<br><b><extra></extra>"
                )

                # logic to initially show only the profiles we want
                for i, trace in enumerate(fig.data):
                    trace.visible = "legendonly" if i not in initial_visible_traces else True
                # Set additional traces (range lines) to be at the top of the legend
                fig.update_layout(legend=dict(traceorder="reversed"))

                fig.add_trace(
                    go.Scatter(
                        x=master_profile_chainage,
                        y=master_profile_elevation,
                        line=dict(color="red", width=2, dash="dash"),
                        name="Master Profile",

                    )
                )

                # Adding the Profile Envelope to the 2D chart, previously its own desperate chart id checked
                if len(radio_selection_range_plot_value) >= 1:

                    topo_df['date'] = pd.to_datetime(topo_df['date']).dt.strftime('%Y-%m-%d')
                    min_chainage = master_profile_chainage[0]
                    max_chainage = master_profile_chainage[-1]
                    min_chainage = float(min_chainage) - 5
                    max_chainage = float(max_chainage) + 5

                    min_chainage = int(min_chainage)
                    max_chainage = int(max_chainage)
                    merge_df = pd.DataFrame()

                    generated_chainage = np.arange(min_chainage, max_chainage + 0.25, 0.25).tolist()
                    merge_df['chainage'] = generated_chainage
                    merge_df['chainage'] = merge_df['chainage']

                    survey_dfs = []  # Assuming this list is supposed to store the results of the merge

                    unique_dates = topo_df['date'].unique()  # Assuming unique_dates is derived from topo_df

                    for date in unique_dates:
                        df_filter = topo_df.loc[topo_df['date'] == date].copy()

                        # Round the chainage values
                        #df_filter['chainage'] = df_filter['chainage'].round(0).astype(int)
                        df_filter['chainage'] = (df_filter['chainage'] * 4).round() / 4

                        df_filter1 = df_filter[['chainage', 'elevation_od']].copy()

                        survey_dfs.append(df_filter1)  # Append the merged result to the list

                    count = 0
                    for df in survey_dfs:
                        merge_df = pd.merge(merge_df, df[["chainage", "elevation_od"]], on="chainage", how="left")
                        merge_df = merge_df.drop_duplicates(subset=['chainage'])
                        merge_df = merge_df.rename(columns={"elevation_od": f"elevation_od_{count}"})
                        merge_df[f"elevation_od_{count}"] = merge_df[f"elevation_od_{count}"].interpolate(
                            method='linear',

                            limit_area='inside',
                            limit=1000)
                        count += 1
                    merge_df = merge_df.drop_duplicates(
                        subset=['chainage'])  # bug duplicates are being made for chainage!!!
                    merge_df = merge_df.set_index('chainage')
                    max_ele = merge_df.max(axis=1)
                    average_ele = merge_df.mean(axis=1, skipna=True)
                    min_ele = merge_df.min(axis=1, skipna=True)
                    merge_df['Max Elevation'] = max_ele
                    merge_df['Mean Elevation'] = average_ele
                    merge_df['Min Elevation'] = min_ele
                    merge_df = merge_df.reset_index()

                    num_columns = merge_df.shape[1]

                    # Drop rows where the number of NaNs is greater than the number of columns - 1
                    merge_df = merge_df.loc[~merge_df['Max Elevation'].isna()]

                    #merge_df.dropna(inplace=True)##
                    min_chainage1 = master_profile_chainage[0]

                    merge_df = merge_df.loc[merge_df['chainage'] >= min_chainage1-0.2]

                    fig.add_trace(go.Scatter(x=merge_df['chainage'], y=merge_df['Mean Elevation'],
                                             line=dict(color='rgba(1,1,1,0.5)', dash='dash'), hoverinfo='x+y',
                                             # display only x and y values on hover
                                             hovertemplate='Mean Elevation: %{y}', showlegend=False))

                    fig.add_trace(go.Scatter(x=merge_df['chainage'], y=merge_df['Min Elevation'],
                                             line=dict(color='rgba(0,0,0,0)', dash=None), hoverinfo='none', showlegend=False))
                    fig.add_trace(
                        go.Scatter(x=merge_df['chainage'], y=merge_df['Max Elevation'], mode='none', fill='tonextx',
                                   fillcolor='rgba(235, 164, 52, 0.5)', showlegend=True, name='Profile Envelope' ))

                # Customize x and y axis fonts and sizes
                fig.update_xaxes(
                    title_text="Chainage (m)",
                    title_font=dict(
                        size=15, family="Calibri", color="blue"
                    ),  # Customize font size and family
                    tickfont=dict(
                        size=15, family="Calibri", color="blue"
                    ),  # Customize tick font size and family
                )

                # y axis on the line plot is Elevation 0D
                fig.update_yaxes(
                    title_text="Elevation (m)",
                    title_font=dict(
                        size=15, family="Calibri", color="blue"
                    ),  # Customize font size and family
                    tickfont=dict(
                        size=15, family="Calibri", color="blue"
                    ),  # Customize tick font size and family
                )

                # Update x-axis tick labels
                fig.update_layout(
                    title={
                        "text": f"<b> CSL: {survey_unit_card} ({selected_sur_unit}) - {selected_profile}</b>",
                        "y": 0.95,
                        "x": 0.5,
                        "xanchor": "center",
                        "yanchor": "top",
                    },
                    title_font={"size": 17, "family": "Calibri", "color": "blue"},
                    xaxis_title="Chainage (m)",
                    yaxis_title="Elevation (m)",
                    legend_title="",
                    font=dict(size=12, color="blue", family="Calibri"),

                    # legend_traceorder="reversed",
                    legend_title_text=f"",
                )

            # Serialize the figure to JSON
            serialized_fig = fig.to_json()

            # Update the 'cpa' key in the store's data with the serialized figure
            chart_data = {"line_plot": serialized_fig}




            return fig, fig, chart_data, valid_master_profile_data,topo_data_failed
        else:
            valid_master_profile_data = False
            fig = px.line()
            chart_data = None
            pass

            return fig, fig, chart_data, valid_master_profile_data,topo_data_failed
    else:


        fig = px.line()
        chart_data = None


        return fig, fig, chart_data, valid_master_profile_data,topo_data_failed




@callback(
    Output("line_info_model", "is_open"),
    [Input("line_open_info", "n_clicks"), Input("line_info_close", "n_clicks")],
    [State("line_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("modal_line_plot", "is_open"),
    Output("line_open_full", "n_clicks"),
    Input("line_open_full", "n_clicks"),
    Input("line_full_close", "n_clicks"),
    Input("line_plot", "relayoutData"),
)
def toggle_modal_chart(n1, n2, relayoutData):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "open" in changed_id:
        return True, 0
    elif "close" in changed_id:
        return False, 0
    return False, 0


