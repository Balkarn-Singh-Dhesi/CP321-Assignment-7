# FIFA World Cup Dashboard - Balkarn Singh
# Hosted at: [INSERT_YOUR_RENDER_LINK_HERE]
# Password: [INSERT_PASSWORD_IF_ANY]

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data from CSV
df = pd.read_csv("world_cup_finals_data.csv")

# Merge West Germany into Germany
df.replace({"Winner": {"West Germany": "Germany"}, "RunnerUp": {"West Germany": "Germany"}}, inplace=True)

# Count wins
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Initialize app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Final Results Dashboard"),

    html.Label("View World Cup Winning Countries on Map"),
    dcc.Graph(id='world-cup-map'),

    html.Label("Select a Country to See Number of Wins:"),
    dcc.Dropdown(options=[{'label': c, 'value': c} for c in sorted(win_counts['Country'].unique())],
                 id='country-select'),
    html.Div(id='country-output'),

    html.Label("Select a Year to See Final Match Result:"),
    dcc.Dropdown(options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
                 id='year-select'),
    html.Div(id='year-output')
])

@app.callback(
    Output('world-cup-map', 'figure'),
    Input('country-select', 'value')
)
def update_map(_):
    # Clone win_counts and replace 'England' with 'United Kingdom' for map purposes
    map_df = win_counts.copy()
    map_df['MapCountry'] = map_df['Country'].replace({'England': 'United Kingdom'})

    fig = px.choropleth(map_df,
                        locations='MapCountry',
                        locationmode='country names',
                        color='Wins',
                        hover_name='Country',
                        title='Countries That Have Won the FIFA World Cup',
                        color_continuous_scale='Viridis',
                        range_color=(0, map_df['Wins'].max()))
    return fig

@app.callback(
    Output('country-output', 'children'),
    Input('country-select', 'value')
)
def display_wins(country):
    if not country:
        return ""
    wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
    return f"✅ {country} has won the World Cup {wins} time(s)."

@app.callback(
    Output('year-output', 'children'),
    Input('year-select', 'value')
)
def display_year_result(year):
    if not year:
        return ""
    row = df[df['Year'] == year].iloc[0]
    return f"📅 In {year}, 🏆 {row['Winner']} won the World Cup. 🥈 Runner-up: {row['RunnerUp']}."

if __name__ == '__main__':
    app.run(debug=True)
