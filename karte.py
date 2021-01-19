import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import flask

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)

germany = json.load(open("assets/karte.geojson","r"))
map=pd.read_csv("assets/states_list.csv",engine="python",index_col=False, delimiter='\;',dtype={"abbrev": str})

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
#mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

fig = px.choropleth_mapbox(map, geojson=germany, locations='abbrev',
                           mapbox_style="carto-darkmatter",hover_name='Bundesland',color='Area (sq. km)',
                           color_continuous_scale="Viridis", hover_data=['Population','Capital','Area (sq. km)'],
                           zoom=5, center = {"lat": 51.3, "lon": 10})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.update_traces(bg_color="#323130")


server = flask.Flask(__name__)
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)


