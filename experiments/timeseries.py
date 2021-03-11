import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import urllib3
from assets.data.data_timeseries import timeseries
urllib3.disable_warnings()


# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"}
    ],
)
server = app.server


'''URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
timeseries=json_data['oed_timeseries']'''
timeseries=timeseries

germany = json.load(open("../assets/karte.geojson", "r"))
map=pd.read_csv("../assets/states_list.csv", engine="python", index_col=False, delimiter='\;', dtype={"abbrev": str})


fig = px.choropleth_mapbox(map, geojson=germany, locations='abbrev',
                           mapbox_style="carto-darkmatter",hover_name='Bundesland',color='Area (sq. km)',
                           color_continuous_scale="Viridis", hover_data=['Population','Capital','Area (sq. km)'],
                           zoom=5, center = {"lat": 51.3, "lon": 10},opacity=0.2)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},coloraxis_showscale=False)


# App layout
app.layout = html.Div(
    id="all",children=[
html.Div(
    id="logo_up",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("open_Modex-logo.png"),
                         style={"height": "100px","width": "auto"}),
                html.H4(children="Energy Frameworks to Germany"),
                html.P(id="description",children="How to efficiently sustain Germany's energy "
                                                 "\n usage with efficient parameters based on regions.")]),
        html.Div(
            dcc.Tabs(id="folder", value='timeseries', children=[
                dcc.Tab(label='scalars', value='scalars', style={'background-color': "#1B2129"}),
                dcc.Tab(label='timeseries', value='timeseries', style={'background-color': "#1B2129"})]))
    ]
),
html.Div(
    id="root",
    children=[
        html.Div(id="tab",children=[
                dcc.Tabs(id="tabs", value='photovoltaics', children=[
                    dcc.Tab(label='Photovoltaics', value='photovoltaics', style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Generator', value='generator',style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Battery Storage', value='battery storage',style={'background-color':"#1B2129"}),
                    dcc.Tab(label='All', value='ALL',style={'background-color':"#1B2129"})])]),
        html.Br(id='filler',children=[]),
        html.Div(
            id="app-container",
            children=[
                #das ist die komplette linke Seite
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(id="slider-text", children="Drag the slider to change the scenario:"),
                                dcc.Slider(id="years-slider", min=3, max=5, step=None, value=3,
                                            marks={3: {"label": '2020', "style": {"color": "#7fafdf"}},
                                                   4: {"label": '2030', "style": {"color": "#7fafdf"}},
                                                   5: {"label": '2050', "style": {"color": "#7fafdf"}}})]),
                        html.Div(
                            id="deutschland",
                            children=[
                                html.Div([
                                    html.P("States of Germany",id="titel"),
                                    dcc.RadioItems(options=[],value='',
                                                   labelStyle={'display': 'inline-block'},id='radio')]),
                                    dcc.Dropdown(options=[], value=[],id="state-dropdown"),
                                    dcc.Graph(id="country-choropleth",figure=fig,
                                              config = dict({'scrollZoom': False}))]),
                ]),
                #das ist die komplette rechte Seite
                html.Div(
                    id="abc",
                    children=[
                        html.Div(
                            id="headerr",
                            children=[
                                html.H5("Info"),
                                html.P("You can visualise the timeseries here")
                                ]),
                        html.Div(
                            id="graph-container",
                            children=[
                                html.P(id="chart-selector", children="Select chart:"),
                                #parameter name
                                dcc.Dropdown(
                                    options=[],value=[],
                                    id="parameter_id_2",multi=False,clearable=False),
                                dcc.Checklist(
                                    options=[{'label':'Urbs','value':'Urbs'},{'label':'GENESYS-2','value':'GENESYS-2'},
                                             {'label':'Oemof','value':'Oemof'},{'label':'Genesys-mod','value':'Genesys-mod'},
                                             {'label':'Balmorel','value':'Balmorel'},],value=['Urbs'],
                                    labelStyle={'display': 'inline-block'},id='source'),
                                dcc.Graph(id="selected-data",figure={},style={})
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)])

#selecting technology
@app.callback(
    [Output(component_id='radio', component_property='options'),
     Output(component_id='radio', component_property='value')],
    [Input(component_id='tabs', component_property='value')])
def one_two(tabs):
    opt = []
    value = ''

    if tabs=='ALL':
        opt = [{'label': 'All', 'value': 'ALL'},
               {'label': 'Customize', 'value': 'choose', 'disabled':True}]
        value = 'ALL'

    else:
        opt = [{'label': 'All', 'value': 'ALL'},
               {'label': 'Customize', 'value': 'choose'}]
        value = 'choose'

    return opt, value

#selecting regions
@app.callback(
    [Output(component_id='state-dropdown', component_property='multi'),
     Output(component_id='state-dropdown', component_property='options'),
     Output(component_id='state-dropdown', component_property='value')],
    [Input(component_id='radio', component_property='value')])
def two_three(selector):
    multi=True
    opt = [{'label': 'Brandenburg', 'value': 'BB'}, {'label': 'Berlin', 'value': 'BE'},
           {'label': 'Baden-Württemberg', 'value': 'BW','disabled':True}, {'label': 'Bayern', 'value': 'BY','disabled':True},
           {'label': 'Bremen', 'value': 'HB','disabled':True}, {'label': 'Hessen', 'value': 'HE'},
           {'label': 'Hamburg', 'value': 'HH','disabled':True}, {'label': 'Mecklenburg-Vorpommern', 'value': 'MV','disabled':True},
           {'label': 'Niedersachsen', 'value': 'NI','disabled':True}, {'label': 'Nordrhein-Westfalen', 'value': 'NW','disabled':True},
           {'label': 'Rheinland-Pfalz', 'value': 'RP','disabled':True}, {'label': 'Schleswig-Holstein', 'value': 'SH','disabled':True},
           {'label': 'Saarland', 'value': 'SL','disabled':True}, {'label': 'Sachsen', 'value': 'SN','disabled':True},
           {'label': 'Sachsen-Anhalt', 'value': 'ST','disabled':True}, {'label': 'Thüringen', 'value': 'TH','disabled':True}]
    value=[]
    if selector=='ALL':
        multi=True
        opt=[{'label':'Deutschland','value':'a'}]
        value= 'a'
        if value=='a':
            value=['BB', 'BE', 'BW', 'BY', 'HB', 'HE', 'HH', 'MV', 'NI', 'NW', 'RP', 'SH', 'SL', 'SN', 'ST', 'TH']
        return value
    else:
        multi=False
        opt=opt
        value = 'BB'

    return multi,opt,value

#selecting parameter_name
@app.callback(
    [Output(component_id='parameter_id_2', component_property='options'),
     Output(component_id='parameter_id_2', component_property='value')],
    [Input(component_id='tabs', component_property='value')])
def three_four (dropdown):
    opt = []
    value = ''
    if dropdown=='photovoltaics':
        opt = [{'label': 'generation', 'value': 'generation'}]
        value='generation'

    elif dropdown=='generator':
        opt = [{'label': 'generation', 'value': 'generation'}]
        value = 'generation'

    elif dropdown=='battery storage':
        opt = [{'label': 'electricity', 'value': 'input energy'}]
        value = 'input energy'

    elif dropdown=='ALL':
        opt = [{'label': 'emissions', 'value': 'emissions'},
               {'label': 'cost system', 'value': 'cost system'},
               {'label': 'curtailment', 'value': 'curtailment'},
               {'label': 'slack', 'value': 'slack'}]
        value = 'emissions'

    return opt,value

@app.callback(
    Output(component_id='selected-data', component_property='figure'),
    [Input(component_id='years-slider', component_property='value'),
     Input(component_id='tabs', component_property='value'),
     Input(component_id='parameter_id_2', component_property='value'),
     Input(component_id='state-dropdown', component_property='value'),
     Input(component_id='source', component_property='value')])
def masterclass (year,technology,parameter,region,source):
    liste=[]
    fig={}
    for i in timeseries:
        for j in range(len(region)):
            if len(region) > j \
                    and i['region'][0] == region[j] \
                    and i['technology'] == technology \
                    and i['parameter_name'] == parameter \
                    and i['scenario_id'] == year:
                liste.append(i)
            elif i['region'][0] == region \
                    and i['technology'] == technology \
                    and i['parameter_name'] == parameter \
                    and i['scenario_id'] == year:
                liste.append(i)

    if len(liste)>0 and len(parameter)>0:
        data = {timeseriess["source"]: timeseriess["series"] for timeseriess in liste}
        data["hour"] = range(201)  # hier wird ein neuer key eingefügt
        df=pd.DataFrame(data)
        help=[]

        if len(df)>0:
            print('')
            print('Technology is',technology)
            print('Parameter is',parameter)
            print('Region is',region)
            print('years is',year)
            print("Source/s is/are", source)
            print('')
            y=[]
            for i in range(len(source)):
                y.append(source[i])
                fig = px.line(
                    df,
                    x="hour",
                    y=y
                    #color="parameter_name"
                )
            fig_layout = fig["layout"]
            fig_layout["paper_bgcolor"] = "#1f2630"
            fig_layout["plot_bgcolor"] = "#1f2630"
            fig_layout["font"]["color"] = "#3391CF"
            fig_layout["title"]["font"]["color"] = "#3391CF"
            fig_layout["xaxis"]["tickfont"]["color"] = "#3391CF"
            fig_layout["yaxis"]["tickfont"]["color"] = "#3391CF"
            fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
            fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
            fig_layout["margin"]["t"] = 75
            fig_layout["margin"]["r"] = 50
            fig_layout["margin"]["b"] = 100
            fig_layout["margin"]["l"] = 50
            fig.update_layout(transition_duration=100)
            fig.update_traces(marker_color="#3391CF")
            if parameter==parameter:
                fig.update_yaxes(title= parameter)
            else:
                raise PreventUpdate
            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
