
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load local dataset (Render will use this path)
df = pd.read_csv("global_terror.csv")
# Dropdown options
countries = [{'label': c, 'value': c} for c in sorted(df['country_txt'].dropna().unique())]
years = sorted(df['iyear'].dropna().unique())

# Initialize app
app = dash.Dash(__name__)
server = app.server  # Needed for deployment on Render

# Layout
app.layout = html.Div([
    html.H1("🌍 Global Terrorism Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(id='country-dropdown', options=countries, value='India'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Slider(
            id='year-slider',
            min=min(years),
            max=max(years),
            value=2015,
            marks={str(year): str(year) for year in years[::5]},
            step=1
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '0px 20px 20px 20px'}),

    dcc.Graph(id='attack-map'),
    dcc.Graph(id='attack-trend')
])

# Callback
@app.callback(
    [Output('attack-map', 'figure'),
     Output('attack-trend', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_graph(selected_country, selected_year):
    filtered_df = df[(df['country_txt'] == selected_country) & (df['iyear'] == selected_year)]

    map_fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        hover_data=["attacktype1_txt", "nkill", "nwound"],
        color="attacktype1_txt",
        zoom=3,
        height=500
    )
    map_fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})

    trend_df = df[df['country_txt'] == selected_country].groupby('iyear').size().reset_index(name='attacks')
    trend_fig = px.line(trend_df, x='iyear', y='attacks', title=f'Attacks Over Time in {selected_country}')
    #trend_fig = px.line(trend_df, x='iyear', y='attacks')

    return map_fig, trend_fig

if __name__ == '__main__':
    app.run_server()
