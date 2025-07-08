# Import pandas for data manipulation
import pandas as pd

# Import Dash and its components for web app creation
import dash
import dash_html_components as html  # HTML components for Dash (deprecated in newer Dash)
import webbrowser  # To open the app in a web browser
import dash_core_components as dcc  # Core components for Dash (deprecated in newer Dash)

from dash.dependencies import Input, Output  # For callbacks (interactivity)

# Import plotting libraries
import plotly.graph_objects as go
import plotly.express as px

from dash.exceptions import PreventUpdate  # For preventing unnecessary updates in callbacks

# Initialize the Dash app
app = dash.Dash()

# Set up global color scheme for the app
global colors
colors = {'background': '#D3D3D3', 'text': '#111111'}

# Function to load data and initialize global variables
def load_data():
    dataset_name = "global_terror.csv"  # Name of the CSV file containing data
    
    global df
    df = pd.read_csv(dataset_name)  # Read CSV data into DataFrame
    
    # Month mapping for dropdowns
    month = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    global month_list
    month_list = [{"label": key, "value": value} for key, value in month.items()]  # For month dropdown

    global date_list
    date_list = [x for x in range(1, 32)]  # List of dates for date dropdown

    # Create mapping of region to countries for filtering
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

    # Create mapping of country to states for filtering
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

    # Create mapping of state to cities for filtering
    global city_list
    city_list = df.groupby("provstate")["city"].unique().apply(list).to_dict()

    # Create region list for dropdown options
    global region_list
    region_list = [{"label": str(i), "value": str(i)} for i in sorted(df["region_txt"].unique().tolist())]

    # Create attack type list for dropdown
    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)} for i in df["attacktype1_txt"].unique().tolist()]

    # List of years available in the dataset
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())

    # Dictionary for year slider marks
    global year_dict
    year_dict = {str(year): str(year) for year in year_list}

    # Dropdown options for chart filters
    global chart_dropdown_values
    chart_dropdown_values = {
        "Terrorist Organisation": 'gname',
        "Target Natinonality": 'natlty1_txt',
        "Target Type": 'targtype1_txt',
        'Type of Attack': 'attacktype1_txt',
        'Weapon Type': 'weaptype1_txt',
        'Region': 'region_txt',
        'Country Attacked': 'country_txt'
    }
    chart_dropdown_values = [{'label': key, 'value': value} for key, value in chart_dropdown_values.items()]

# Function to create the UI layout for the app
def create_app_ui():
    main_layout = html.Div(
        style={'backgroundColor': colors['background']},
        children=[
            html.Br(),
            html.H1(
                "Terrorism Analysis with Insights",
                id="Main_title",
                style={'textAlign': 'center', 'color': '#FF0000'}
            ),
            html.Hr(),

            # Main Tabs: Map Tool and Chart Tool
            dcc.Tabs(
                id="Tabs", value="Map", children=[
                    # Map Tool Tab
                    dcc.Tab(
                        label="Map tool",
                        id="Map tool",
                        value="Map",
                        children=[
                            # Subtabs for World and India Map
                            dcc.Tabs(
                                id="subtabs", value="WorldMap", children=[
                                    dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                                    dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                                ]
                            ),
                            # Dropdowns for all filter options
                            dcc.Dropdown(
                                id='region-dropdown',
                                options=region_list,
                                placeholder="Select Region",
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id="country-dropdown",
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder="Select Country",
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id="state-dropdown",
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder="Select State or Province",
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id="city-dropdown",
                                options=[{'label': 'All', 'value': 'All'}],
                                placeholder="Select City",
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id="attacktype-dropdown",
                                options=attack_type_list,
                                placeholder='Select Attack Type',
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='month',
                                options=month_list,
                                placeholder='Select month',
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='date',
                                placeholder="Select Date",
                                style={'textAlign': 'center'},
                                multi=True
                            ),
                            html.H5(
                                'Select the Year', id='year_title',
                                style={'textAlign': 'center', 'color': '#FF0000'}
                            ),
                            dcc.RangeSlider(
                                id='year-slider',
                                min=min(year_list),
                                max=max(year_list),
                                value=[min(year_list), max(year_list)],
                                marks=year_dict,
                                step=None
                            ),
                            html.Br()
                        ]
                    ),
                    # Chart Tool Tab
                    dcc.Tab(
                        label="Chart Tool",
                        id="chart tool",
                        value="chart",
                        children=[
                            # Subtabs for World and India Charts
                            dcc.Tabs(
                                id="subtabs2",
                                value="WorldChart",
                                children=[
                                    dcc.Tab(label="World Chart Tool", id="WorldC", value="WorldChart"),
                                    dcc.Tab(label="India Chart Tool", id="IndiaC", value="IndiaChart")
                                ]
                            ),
                            dcc.Dropdown(
                                id="Chart_Dropdown",
                                options=chart_dropdown_values,
                                placeholder="Select Option",
                                style={'textAlign': 'center'},
                                value="region_txt"
                            ),
                            html.Br(),
                            html.Br(),
                            html.Hr(),
                            dcc.Input(id="search", placeholder="Search Filter"),
                            html.Hr(),
                            html.Br(),
                            dcc.RangeSlider(
                                id='cyear_slider',
                                min=min(year_list),
                                max=max(year_list),
                                value=[min(year_list), max(year_list)],
                                marks=year_dict,
                                step=None
                            ),
                            html.Br()
                        ]
                    ),
                ]
            ),
            # Div to display graphs
            html.Div(
                id="graph-object",
                children=":::::Graph will be shown here:::::",
                style={'textAlign': 'center', 'color': '#FF0000'}
            )
        ]
    )
    return main_layout

# Callback to update the graph based on user selections
@app.callback(
    dash.dependencies.Output('graph-object', 'children'),
    [
        dash.dependencies.Input('Tabs', 'value'),
        dash.dependencies.Input('month', 'value'),
        dash.dependencies.Input('date', 'value'),
        dash.dependencies.Input('region-dropdown', 'value'),
        dash.dependencies.Input('country-dropdown', 'value'),
        dash.dependencies.Input('state-dropdown', 'value'),
        dash.dependencies.Input('city-dropdown', 'value'),
        dash.dependencies.Input('attacktype-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('cyear_slider', 'value'),
        dash.dependencies.Input('Chart_Dropdown', 'value'),
        dash.dependencies.Input('search', 'value'),
        dash.dependencies.Input('subtabs2', 'value')
    ]
)
def update_app_ui(Tabs, month_value, date_value, region_value, country_value, state_value, city_value,
                  attack_value, year_value, chart_year_selector, chart_dp_value, search, subtabs2):
    fig = None  # Initialize figure variable
    
    # If Map tab is selected
    if Tabs == "Map":
        # Print statements for debugging (can be removed)
        print("Data Type of month value = ", str(type(month_value)))
        print("Data of month value = ", month_value)
        print("Data Type of Day value = ", str(type(date_value)))
        print("Data of Day value = ", date_value)
        print("Data Type of region value = ", str(type(region_value)))
        print("Data of region value = ", region_value)
        print("Data Type of country value = ", str(type(country_value)))
        print("Data of country value = ", country_value)
        print("Data Type of state value = ", str(type(state_value)))
        print("Data of state value = ", state_value)
        print("Data Type of city value = ", str(type(city_value)))
        print("Data of city value = ", city_value)
        print("Data Type of Attack value = ", str(type(attack_value)))
        print("Data of Attack value = ", attack_value)
        print("Data Type of year value = ", str(type(year_value)))
        print("Data of year value = ", year_value)

        # Filter the main DataFrame according to user selections
        year_range = range(year_value[0], year_value[1] + 1)
        new_df = df[df["iyear"].isin(year_range)]

        # Filter by month and date if selected
        if month_value == [] or month_value is None:
            pass
        else:
            if date_value == [] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[(new_df["imonth"].isin(month_value)) & (new_df["iday"].isin(date_value))]
        
        # Filter by region, country, state, city if selected
        if region_value == [] or region_value is None:
            pass
        else:
            if country_value == [] or country_value is None:
                new_df = new_df[(new_df["region_txt"].isin(region_value))]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value)) &
                                        (new_df["country_txt"].isin(country_value)) &
                                        (new_df["provstate"].isin(state_value)) &
                                        (new_df["city"].isin(city_value))]
        
        # Filter by attack type if selected
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]

        # If no data after filtering, create an empty DataFrame with required columns
        if not new_df.shape[0]:
            new_df = pd.DataFrame(
                columns=['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                         'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            new_df.loc[0] = [0, 0, 0, None, None, None, None, None, None, None, None]
        
        # Create the map figure using Plotly
        mapFigure = px.scatter_mapbox(
            new_df,
            lat="latitude",
            lon="longitude",
            color="attacktype1_txt",
            hover_name="city",
            hover_data=["region_txt", "country_txt", "provstate", "city", "attacktype1_txt", "nkill", "iyear"],
            zoom=1
        )
        # Update mapbox style and layout
        mapFigure.update_layout(
            mapbox_style="carto-darkmatter",
            autosize=True,
            margin=dict(l=0, r=0, t=25, b=20)
        )

        fig = mapFigure

    # If Chart tab is selected
    elif Tabs == "chart":
        fig = None
        year_range_c = range(chart_year_selector[0], chart_year_selector[1] + 1)
        chart_df = df[df["iyear"].isin(year_range_c)]

        # Filter for India chart if selected
        if subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"] == "South Asia") & (chart_df["country_txt"] == "India")]

        # Filter and group data for charting
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
                chart_df = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")

        # If no data for chart, create placeholder row
        if not chart_df.shape[0]:
            chart_df = pd.DataFrame(columns=['iyear', 'count', chart_dp_value])
            chart_df.loc[0] = [0, 0, "No data"]

        # Create area chart using Plotly
        fig = px.area(chart_df, x="iyear", y="count", color=chart_dp_value)

    # Return the figure to the graph component
    return dcc.Graph(figure=fig)

# Callback to update date dropdown options based on selected months
@app.callback(
    Output("date", "options"),
    [Input("month", "value")]
)
def update_date(month_value):
    date_list = [x for x in range(1, 32)]  # List of days in a month
    option = []
    if month_value:
        option = [{'label': m, 'value': m} for m in date_list]
    return option

# Callback to update region and country dropdowns when switching map subtabs
@app.callback(
    [Output("region-dropdown", "value"),
     Output("region-dropdown", "disabled"),
     Output("country-dropdown", "value"),
     Output("country-dropdown", "disabled")],
    [Input("subtabs", "value")]
)
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

# Callback to update country dropdown options based on selected regions
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')]
)
def set_country_options(region_value):
    option = []
    if region_value is None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label': m, 'value': m} for m in option]

# Callback to update state dropdown options based on selected countries
@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')]
)
def set_state_options(country_value):
    option = []
    if country_value is None:
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label': m, 'value': m} for m in option]

# Callback to update city dropdown options based on selected states
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')]
)
def set_city_options(state_value):
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label': m, 'value': m} for m in option]

# Function to open the app in the default web browser
def open_webbrowser():
    webbrowser.open_new('http://127.0.0.1:8050/')

# Main function to start the app
def main():
    print("Starting the main function.....")
    load_data()  # Load the dataset and initialize global variables
    open_webbrowser()  # Open browser with app

    global app
    app.layout = create_app_ui()  # Set the app layout
    app.title = "Terrorism Analysis with Insights"  # Set the app title

    app.run_server()  # Start the Dash server

    print("This would be executed only after the script is closed")
    df = None
    app = None

    print("Ending the main function......")

# Standard Python entry point
if __name__ == "__main__":
    print("My project is starting.....")
    main()
    print("My project is ending.....")
    
    
    
    
