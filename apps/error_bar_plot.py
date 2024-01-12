import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from io import StringIO


layout = html.Div(
    [
        dcc.Store(id="error_chart"),


        dcc.Graph(id="error_plot",
                  ),
        # adding info and max view buttons
        dbc.Button(
            [html.Span(className="bi bi-info-circle-fill")],
            size="md",
            id="error_open_info",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "left": "8px","border-radius": "5px"},
        ),
        dbc.Button(
            [html.Span(className="fa-solid fa-expand")],
            size="md",
            id="error_open_full",
            n_clicks=0,
            className="mr-3",
            style={"position": "absolute", "bottom": "1%", "right": "8px","border-radius": "5px"},
        ),
        # adding info and max view modals (the popups)
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Box Plot")),
                dbc.ModalBody("This is a nice chart!"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="error_info_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="error_info_model",
            is_open=False,
            fullscreen=False,
        ),
        dbc.Modal(
            [
                #dbc.ModalHeader(dbc.ModalTitle("Box Plot")),
                dbc.ModalBody(
                    dcc.Graph(id="error_plot_model", style={"height": "90vh"})
                ),  ## might not work
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="error_full_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_error_plot",
            is_open=False,
            fullscreen=True,
        ),
        dcc.Dropdown(
            options=[

                {
                    "label": "Latest",
                    "value": "Latest",
                },

            ],
            value="Latest",
            id="error-bar-dropdown",
            multi=False

        ),


    ],

    id= 'error_bar_plot_div'
)


@callback(
    Output("error_plot", "figure"),
    Output("error_plot_model", "figure"),
    Output("error_chart", "data"),
    Output('error-bar-dropdown', 'options'),
    Output('error-bar-dropdown', 'value'),
    Input("selected-df-storage", "data"),
    State("survey-unit-dropdown", "value"),
    Input('error-bar-dropdown', 'value'),

)
def make_scatter_plot(cpa_df, selected_survey_unit, drop_down_val):

    #  load in the csa table from the store, json to df
    df = pd.read_json(StringIO(cpa_df))
    df = df.drop("Sum", axis=0)

    # Melt the DataFrame to long format
    melted_df = df.melt(
        ignore_index=False, var_name="Date", value_name="Value"
    ).reset_index()

    # Get a list of all unique dates to populate the dropdown
    drop_down_dates = list(melted_df['Date'].unique())

    def make_options_list(date_list):
        options= []
        options.append({"label": 'Latest',"value": 'Latest'})

        for date in date_list:
            option_dict ={}
            option_dict.update({ "label": date.strftime('%Y-%m-%d'),"value": date})
            options.append(option_dict)
        return options

    drop_down_options = make_options_list(drop_down_dates)

    # Calculate min and max values for each profile
    min_values = melted_df.groupby("index")["Value"].min()
    max_values = melted_df.groupby("index")["Value"].max()

    # Creating the box and whisker plot using Plotly Express
    fig = px.box(
        melted_df,
        x="index",
        y="Value",
        title="",
        points=False,
        template="plotly",
        # height=600,
    )
    if drop_down_val == 'Latest' or drop_down_val is None:
        # Calculate the most recent value information
        set_dropdown_val = 'Latest'
        format_legend_title = 'Latest'
        latest_date = df.columns[-1]
        most_recent_values = df[latest_date]
        most_recent_info = pd.DataFrame(
            {"Index": most_recent_values.index, "Value": most_recent_values}
        )
    else:
        set_dropdown_val = drop_down_val
        latest_date = drop_down_val
        format_legend_title = latest_date.split('T')[0]
        most_recent_values = df[latest_date]
        most_recent_info = pd.DataFrame(
            {"Index": most_recent_values.index, "Value": most_recent_values})

    # Add a red scatter point for the most recent values
    for _, row in most_recent_info.iterrows():
        popup_text = f"Survey: {format_legend_title}"
        scatter_trace = go.Scatter(
            x=[row["Index"]],
            y=[row["Value"]],
            mode="markers",
            #text=popup_text,
            marker=dict(color="red", size=10),
            showlegend=False,
            customdata=[[[row["Index"]],[round(row["Value"],2)]]],
        )
        fig.add_trace(scatter_trace)


    # Format the label shown in the hover
    fig.update_traces(
        hovertemplate="<b>Profile ID:</b> %{customdata[0]}<br>" +
                      "<b>CPA:</b> %{customdata[1]}<extra></extra>"  # Include <extra></extra> to remove the legend
    )

    # Modify the box plot traces to show custom error bars
    for profile in df.index:
        fig.update_traces(
            selector=dict(name=profile),
            boxpoints="all",
            lowerfence=min_values[profile],
            uperfence=max_values[profile],
            showlegend=False,
        )

    # Create a custom legend entry with a dummy point and label
    dummy_legend_trace = go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(color="red", size=8),
        name=str(format_legend_title),
    )
    fig.add_trace(dummy_legend_trace)
    fig.update_layout(showlegend=True, legend_title_text="Profile Name")
    # Update x-axis tick labels
    fig.update_layout(
        title={
            "text": f"<b>Box Plot: {selected_survey_unit}</b>",
            "y": 0.96,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        title_font=dict(size=15, family="Helvetica"),
        title_x=0.5,
        yaxis_title={"text": "Cross Sectional Profile Area (m²)", "font": {"size": 15}},
        xaxis_title=None,
        legend_title="",
        font=dict(size=15, color="blue", family="Helvetica"),
        xaxis=dict(
            tickmode="array",
            tickangle=45,
            tickfont=dict(
                size=12,  # Set the font size
                color="blue",  # Set the font color
                family="Helvetica",  # Set the font family
            ),
        ),
    )

    # Customize the legend font and size
    fig.update_layout(
        legend=dict(
            title_font=dict(
                size=12, family="Helvetica"
            ),  # Customize font size and family
            title_text="",  # Remove legend title
            font=dict(
                size=12, family="Helvetica"
            ),  # Customize font size and family for legend labels
        ),
        legend_traceorder="reversed",
        legend_title_text=f"",
    )

    fig.update_layout(
        xaxis=dict(tickfont=dict(size=15)),  # Adjust the size as needed
        yaxis=dict(tickfont=dict(size=15)),  # Adjust the size as needed
    )


    # Serialize the figure to JSON
    serialized_fig = fig.to_json()

    # Update the 'cpa' key in the store's data with the serialized figure
    chart_data = {"error_plot": serialized_fig}

    return fig, fig, chart_data, drop_down_options, set_dropdown_val


# adding the callbacks that control the modal buttons display logic
@callback(
    Output("error_info_model", "is_open"),
    [Input("error_open_info", "n_clicks"), Input("error_info_close", "n_clicks")],
    [State("error_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("modal_error_plot", "is_open"),
    Output("error_open_full", "n_clicks"),
    Input("error_open_full", "n_clicks"),
    Input("error_full_close", "n_clicks"),
    Input("error_plot", "relayoutData"),
)
def toggle_modal_chart(n1, n2, relayoutData):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "open" in changed_id:
        return True, 0
    elif "close" in changed_id:
        return False, 0
    return False, 0
