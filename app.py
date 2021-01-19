import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import requests
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import urllib3
from dash.exceptions import PreventUpdate
from urllib.request import urlopen

urllib3.disable_warnings()

print('Hello World')

# Initialize app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=4.0"}
    ],
)
server = app.server

# Load data

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

from data_scalars import scalars
scalar=scalars[0:1540]
from data_timeseries import timeseries

YEARS = [2020,2030,2050]


DEFAULT_COLORSCALE = ["#f2fffb","#bbffeb","#98ffe0","#79ffd6","#6df0c8","#69e7c0","#59dab2","#45d0a5",
                      "#31c194","#2bb489","#25a27b","#1e906d","#188463","#157658","#11684d","#10523e"]
DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


'''URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
scalar=json_data['oed_scalars']
scalar=scalar[0:1540]
timeseries=json_data['oed_timeseries']'''


#available_parameter=df['parameter_name'].unique()
#available_energy=df['input_energy_vector'].unique()
#options=[{'label':i, 'value': i} for i in available_energy]'''


map=pd.read_csv("assets/states_list.csv", engine="python", index_col=False, delimiter='\;', dtype={"abbrev": str})

'''germany = json.load(open("assets/alles.geojson", "r"))
fig = px.choropleth_mapbox(map, geojson=germany, locations='abbrev',
                           mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                           color_continuous_scale="Viridis", hover_data=['Population', 'Capital', 'Area (sq. km)'],
                           zoom=5, center={"lat": 51.3, "lon": 10}, opacity=0.2)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)'''






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

    ]
),
html.Div(
    id="root",
    children=[
        html.Div(id="tab",children=[
                dcc.Tabs(id="tabs", value='generation', children=[
                    dcc.Tab(label='Generation', value='generation', style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Battery Storage', value='battery storage',style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Transmission', value='transmission',style={'background-color':"#1B2129"})])]),
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
                                dcc.Slider(id="years-slider", min=3, max=5, step=None, value=3,disabled=True,
                                            marks={3: {"label": '2020', "style": {"color": "#7fafdf"}},
                                                   4: {"label": '2030', "style": {"color": "#7fafdf"}},
                                                   5: {"label": '2050', "style": {"color": "#7fafdf"}}})]),
                        html.Div(
                            id="deutschland",
                            children=[
                                html.Div([
                                    html.P("States of Germany",id="titel"),
                                    dcc.Tabs(id='tabs_2',value='',children=[]),
                                    dcc.RadioItems(options=[],value='',
                                                   labelStyle={'display': 'inline-block'},id='radio')]),
                                    dcc.Dropdown(options=[], value=[],
                                            multi=True,id="state-dropdown"),
                                    dcc.Graph(id="country-choropleth",
                                          figure={})]),
                ]),
                #das ist die komplette rechte Seite
                html.Div(
                    id="abc",
                    children=[
                        html.Div(
                            id="headerr",
                            children=[
                                html.H5("Scalars"),
                                html.P("With renewable energy sources, here you can put in a bunch of text \n"
                                       "links kann man kein Szenario auswählen, da im dummy dataset es nur \n"
                                       "Daten mit Basisszenario 1 gibt")
                                ]),
                        html.Div(
                            id="graph-container",
                            children=[
                                html.P(id="chart-selector", children="Select chart:"),
                                #html.Div(id='solo',children=[
                                #        html.P(id="chart_check", children="input energy vector:" ),
                                #        dcc.Checklist(
                                #            options=[], value=[],
                                #            labelStyle={'display': 'inline-block'}, id='technology_id')])
                                dcc.Checklist(
                                    options=[], value=[],
                                    labelStyle={'display': 'inline-block'}, id='technology_id'),
                                #parameter name
                                dcc.Dropdown(
                                    options=[],value=[],
                                    id="chart-dropdown"),
                                #input energy vector
                                dcc.Checklist(
                                    options=[],value=[],
                                    labelStyle={'display': 'inline-block'},id='parameter_id'),
                                dcc.RadioItems(id='experiment',options=[],value=''),
                                dcc.Graph(id="selected-data",figure={},style={})
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id="root_2",
            children=[
                html.Div(id="tab_2", children=[
                    dcc.Tabs(id="tabs_3", value='photovoltaics', children=[
                        dcc.Tab(label='Photovoltaics', value='photovoltaics', style={'background-color': "#1B2129"}),
                        dcc.Tab(label='Generator', value='generator', style={'background-color': "#1B2129"}),
                        dcc.Tab(label='Battery Storage', value='battery storage',
                                style={'background-color': "#1B2129"}),
                        dcc.Tab(label='All', value='ALL', style={'background-color': "#1B2129"})])]),
                html.Br(id='filler_2', children=[]),
                html.Div(
                    id="app-container_2",
                    children=[
                        html.Div(
                            id="abc_2",
                            children=[
                                html.Div(
                                    id="headerr_2",
                                    children=[
                                        html.H5("Timeseries"),
                                        html.P("You can visualise the timeseries here \n"
                                               "es gibt Überschneidungen der Daten mit Regions mit den Skalaren \n"
                                               "daher funktionieren nur Regionen BE/Berlin, BB/Brandenburg & HE/Hessen. \n"
                                               "Außerdem kann man nur eine Einzige Region auswählen. \n"
                                               "Des Weiteren, wenn der tab ALL ausgewählt ist, müssen alle \n"
                                               "Regionen gewählt werden \n"
                                               "Letzlich, sind automatisch ALLE Regionen gewählt, wenn der tab \n"
                                               "ALL gewählt wurde")
                                    ]),
                                html.Div(
                                    id="graph-container_2",
                                    children=[
                                        # parameter name
                                        dcc.Dropdown(
                                            options=[], value=[],
                                            id="parameter_id_2", multi=False, clearable=False),
                                        dcc.Checklist(
                                            options=[{'label': 'Urbs', 'value': 'Urbs'},
                                                     {'label': 'GENESYS-2', 'value': 'GENESYS-2'},
                                                     {'label': 'Oemof', 'value': 'Oemof'},
                                                     {'label': 'Genesys-mod', 'value': 'Genesys-mod'},
                                                     {'label': 'Balmorel', 'value': 'Balmorel'}, ], value=['Urbs'],
                                            labelStyle={'display': 'inline-block'}, id='source'),
                                        dcc.Graph(id="selected-data_2", figure={}, style={})
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)])


#von 1 auf 2
@app.callback(
    [Output(component_id='tabs_2', component_property='children'),
     Output(component_id='tabs_2', component_property='value')],
    [Input(component_id='tabs', component_property='value')])
def one_two(tabs):
    child = []
    value = ''

    if tabs=='transmission':
        child = [dcc.Tab(label='Energy', value='energy_transmission', style={'background-color': "#1B2129"}),
                 dcc.Tab(label='Costs', value='costs_transmission', style={'background-color': "#1B2129"})]
        value = 'energy_transmission'

    elif tabs=='generation':
        child=[]
        value='filler_1'

    elif tabs=='battery storage':
        child=[]
        value='filler_2'

    return child,value

@app.callback(
    [Output(component_id='radio', component_property='options'),
     Output(component_id='radio', component_property='value')],
    [Input(component_id='tabs_2', component_property='value'),
     Input(component_id='tabs_3', component_property='value')])
def two_three(tabs_2,tabs_3):
    opt=[]
    value=[]
    if tabs_3=='ALL':
        opt = [{'label': 'All', 'value': 'ALL'},
               {'label': 'Customize', 'value': 'choose', 'disabled':True}]
        value = 'ALL'

    elif tabs_2=='energy_transmission':
        opt=[{'label': 'All', 'value': 'All','disabled':True},
              {'label': 'Customize', 'value': 'choose'}]
        value='choose'

    else:
        opt = [{'label': 'All', 'value': 'All'},
               {'label': 'Customize', 'value': 'choose'}]
        value = 'choose'

    return opt, value



#callback for selecting regions
#REGIONS_FOUR
@app.callback(
    [Output(component_id='state-dropdown', component_property='options'),
     Output(component_id='state-dropdown', component_property='value'),
     Output(component_id='state-dropdown', component_property='multi')],
    [Input(component_id='tabs_2', component_property='value'),
     Input(component_id='radio', component_property='value')])
def three_four(tabs_2,selector):
    opt=[]
    value=[]
    multi=True

    if tabs_2=='energy_transmission':
        '''opt = [{'label': 'Brandenburg to Berlin', 'value': 'a'},
                 {'label': 'Berlin to Brandenburg', 'value': 'b'},
                 {'label': 'Brandenburg to Mecklenburg-Vorpommern', 'value': 'BB to MV'},
                 {'label': 'Mecklenburg-Vorpommern to Brandenburg', 'value': 'MV to BB'},
                 {'label': 'Brandenburg to Thüringen', 'value': 'BB to TH'},
                 {'label': 'Thüringen to Brandenburg', 'value': 'TH to BB'},
                 {'label': 'Mecklenburg-Vorpommern to Schleswig-Holstein', 'value': 'MV to SH'},
                 {'label': 'Schleswig-Holstein to Mecklenburg-Vorpommern', 'value': 'SH to MV'},
                 {'label': 'Schleswig-Holstein to Hamburg', 'value': 'SH to HH'},
                 {'label': 'Hamburg to Schleswig-Holstein', 'value': 'HH to SH'},
                 {'label': 'Schleswig-Holstein to Nordrhein-Westfalen', 'value': 'SH to NW'},
                 {'label': 'Nordrhein-Westfalen to Schleswig-Holstein', 'value': 'NW to SH'},
                 {'label': 'Nordrhein-Westfalen to Hessen', 'value': 'NW to HE'},
                 {'label': 'Hessen to Nordrhein-Westfalen', 'value': 'HE to NW'},
                 {'label': 'Hessen to Baden-Württemberg', 'value': 'HE to BW'},
                 {'label': 'Baden-Württemberg to Hessen', 'value': 'BW to HE'},
                 {'label': 'Baden-Württemberg to Bayern', 'value': 'BW to BY'},
                 {'label': 'Bayern to Baden-Württemberg', 'value': 'BY to BW'}]
        value='b'
        multi=False
        if value[0]=='a':
            opt=opt
            value=['BB','BE']
            multi = False
        elif value[0]=='b':
            opt=opt
            value=['BE','BB']
            multi= False
        return opt,value,multi'''
        opt = [{'label': 'Brandenburg', 'value': 'BB'}, {'label': 'Berlin', 'value': 'BE'},
               {'label': 'Baden-Württemberg', 'value': 'BW'}, {'label': 'Bayern', 'value': 'BY'},
               {'label': 'Bremen', 'value': 'HB','disabled':True}, {'label': 'Hessen', 'value': 'HE'},
               {'label': 'Hamburg', 'value': 'HH'}, {'label': 'Mecklenburg-Vorpommern', 'value': 'MV'},
               {'label': 'Niedersachsen', 'value': 'NI','disabled':True}, {'label': 'Nordrhein-Westfalen', 'value': 'NW'},
               {'label': 'Rheinland-Pfalz', 'value': 'RP','disabled':True}, {'label': 'Schleswig-Holstein', 'value': 'SH'},
               {'label': 'Saarland', 'value': 'SL','disabled':True}, {'label': 'Sachsen', 'value': 'SN','disabled':True},
               {'label': 'Sachsen-Anhalt', 'value': 'ST','disabled':True}, {'label': 'Thüringen', 'value': 'TH'}]
        value = ['BB']
        multi=True

    else:
        opt = [{'label': 'Brandenburg', 'value': 'BB'}, {'label': 'Berlin', 'value': 'BE'},
               {'label': 'Baden-Württemberg', 'value': 'BW'}, {'label': 'Bayern', 'value': 'BY'},
               {'label': 'Bremen', 'value': 'HB'}, {'label': 'Hessen', 'value': 'HE'},
               {'label': 'Hamburg', 'value': 'HH'}, {'label': 'Mecklenburg-Vorpommern', 'value': 'MV'},
               {'label': 'Niedersachsen', 'value': 'NI'}, {'label': 'Nordrhein-Westfalen', 'value': 'NW'},
               {'label': 'Rheinland-Pfalz', 'value': 'RP'}, {'label': 'Schleswig-Holstein', 'value': 'SH'},
               {'label': 'Saarland', 'value': 'SL'}, {'label': 'Sachsen', 'value': 'SN'},
               {'label': 'Sachsen-Anhalt', 'value': 'ST'}, {'label': 'Thüringen', 'value': 'TH'}]
        value = ['BB']
        multi = True

        if selector =='choose':
            opt=opt
            value = ['BB']
            multi = True
        else:
            opt = opt
            value= ['BB','BE','BW','BY','HB','HE','HH','MV','NI','NW','RP','SH','SL','SN','ST','TH']
            multi = True
        return opt, value,multi

    return opt,value,multi

#interaktive Karte
@app.callback(
    [Output(component_id='country-choropleth', component_property='figure'),
    Output(component_id='country-choropleth', component_property='config')],
    [Input(component_id='state-dropdown', component_property='value')])
def finale(region):
    germany = json.load(open("assets/Karte.geojson", "r"))
    fig = px.choropleth_mapbox(map, geojson=germany, locations='abbrev',
                               mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                               color_continuous_scale="Viridis", hover_data=['Population', 'Capital', 'Area (sq. km)'],
                               zoom=5, center={"lat": 51.3, "lon": 10}, opacity=0.1)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
    config = dict({'scrollZoom': False})
    if len(region)>0:

        if len(region)==16:
            alles = json.load(open("assets/karte.geojson", "r"))
            fig = px.choropleth_mapbox(map, geojson=alles, locations='abbrev',
                                       mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                                       color_continuous_scale="Viridis",
                                       hover_data=['Population', 'Capital', 'Area (sq. km)'],
                                       zoom=5, center={"lat": 51.3, "lon": 10}, opacity=1)
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
        elif region[0]=='BW':
            Baden_Württemberg = json.load(open("assets/Badenwürttemberg.geojson", "r"))
            fig = px.choropleth_mapbox(map, geojson=Baden_Württemberg, locations='abbrev',
                                       mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                                       color_continuous_scale="Viridis",
                                       hover_data=['Population', 'Capital', 'Area (sq. km)'],
                                       zoom=5, center={"lat": 51.3, "lon": 10}, opacity=1)
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
        elif region[0]=='BB':
            Brandenburg = json.load(open("assets/Brandenburg.geojson", "r"))
            fig = px.choropleth_mapbox(map, geojson=Brandenburg, locations='abbrev',
                                       mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                                       color_continuous_scale="Viridis",
                                       hover_data=['Population', 'Capital', 'Area (sq. km)'],
                                       zoom=5, center={"lat": 51.3, "lon": 10}, opacity=1)
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
        elif region[0] == 'BE':
            Berlin = json.load(open("assets/Berlin.geojson", "r"))
            fig = px.choropleth_mapbox(map, geojson=Berlin, locations='abbrev',
                                       mapbox_style="carto-darkmatter", hover_name='Bundesland', color='Area (sq. km)',
                                       color_continuous_scale="Viridis",
                                       hover_data=['Population', 'Capital', 'Area (sq. km)'],
                                       zoom=5, center={"lat": 51.3, "lon": 10}, opacity=1)
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
            return fig
    else:
        raise PreventUpdate


    return fig,config


#von regions auf checkboxes
#TECHNOLOGY ID_FIVE
@app.callback(
    [Output(component_id='technology_id', component_property='options'),
     Output(component_id='technology_id', component_property='value')],
    [Input(component_id='tabs_2', component_property='value')])
def two_five_and_six (tabs_2):
    opt_1=[]
    value_1=[]

    if tabs_2=='energy_transmission':
        opt_1=[{'label':'electricity','value':'transmission','disabled':True}]
        value_1=['transmission'] #transmission

    elif tabs_2=='costs_transmission':
        opt_1=[{'label':'electricity','value':'transmission','disabled':True}]
        value_1=['transmission'] #transmission

    elif tabs_2=='filler_1': #generation
        opt_1 = [{'label': 'solar radiation', 'value': 'photovoltaics'},
                {'label': 'lignite', 'value': 'generator'}]
        value_1 = ['photovoltaics'] #generation

    elif tabs_2=='filler_2': #battery storage
        opt_1=[{'label':'electricity','value':'battery storage','disabled':True}]
        value_1=['battery storage'] #battery storage

    return opt_1,value_1


@app.callback(
    [Output(component_id='chart-dropdown', component_property='options'),
     Output(component_id='chart-dropdown', component_property='value')],
    [Input(component_id='technology_id', component_property='value'),
     Input(component_id='tabs_2', component_property='value')])
def five_six(technology,tabs_2):
    opt=[]
    value=[]
    if technology==['transmission']:
        opt = []
        value = ''
        if tabs_2=='energy_transmission':
            opt = [{'label': 'energy', 'value': 'energy_transmission','disabled':True}]
            value='energy_transmission'
        elif tabs_2=='costs_transmission':
            opt=[{'label': 'costs', 'value': 'costs_transmission','disabled':True}]
            value='costs_transmission'
        return opt,value

    elif technology==['photovoltaics']:
        opt = [{'label': 'generation', 'value': 'generation'},
                 {'label': 'costs', 'value': 'costs_photo'}]
        value = 'generation'
    elif technology==['generator']:
        opt = [{'label': 'generation', 'value': 'generation'},
                 {'label': 'emissions', 'value': 'emissions'},
                 {'label': 'costs', 'value': 'costs_lignite'}]
        value = 'generation'
    elif technology==['battery storage']:
        opt = [{'label': 'energy', 'value': 'energy'},
                 {'label': 'costs', 'value': 'costs'}]
        value = 'energy'
    elif technology==['photovoltaics','generator']:
        opt = [{'label': 'generation', 'value': 'generation'},
               {'label': 'costs', 'value': 'costs_combo'}]
        value = 'generation'

    return opt,value


#this gives the options outgoing from dropdowns
#PARAMETER NAMES_SEVEN
@app.callback(
    [Output(component_id='parameter_id', component_property='options'),
     Output(component_id='parameter_id', component_property='value')],
    [Input(component_id='chart-dropdown', component_property='value')])
def six_seven (dropdown):
    opt = []
    value = []
    if dropdown=='energy':
        opt = [{'label': 'input energy vector', 'value': 'input energy'},
               {'label': 'output energy vector', 'value': 'output energy'},
               {'label': 'losses', 'value': 'losses'}]
        value=['input energy']

    elif dropdown=='costs_photo':
        opt = [{'label': 'deprecated investment costs', 'value': 'deprecated investment cost'},
               {'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'},
               {'label': 'variable costs', 'value': 'variable cost'}]
        value = ['deprecated investment cost']

    elif dropdown=='costs_lignite':
        opt = [{'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'},
               {'label': 'variable costs', 'value': 'variable cost'}]
        value = ['deprecated fixed cost']

    elif dropdown=='costs_combo':
        opt = [{'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'},
               {'label': 'variable costs', 'value': 'variable cost'}]
        value = ['deprecated fixed cost']

    elif dropdown=='costs':
        opt = [{'label': 'deprecated investment costs', 'value': 'deprecated investment cost'},
               {'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'},
               {'label': 'variable costs', 'value': 'variable cost'}]
        value = ['deprecated investment cost']

    elif dropdown=='generation':
        opt = [{'label': 'generation', 'value': 'generation', 'disabled': True}]
        value = ['generation']

    elif dropdown=='emissions':
        opt = [{'label': 'emissions', 'value': 'emissions'},
               {'label': 'primary energy consumption', 'value': 'primary energy consumption'}]
        value = ['emissions']

    elif dropdown=='energy_transmission': #energy in transmission
        opt = [{'label': 'outgoing energy flow', 'value': 'energy flow'},
                  {'label': 'losses', 'value': 'losses'}]
        value = ['energy flow']

    elif dropdown=='costs_transmission': #costs in transmission
        opt = [{'label': 'deprecated investment costs', 'value': 'deprecated investment cost'},
                  {'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'}]
        value = ['deprecated investment cost']

    return opt,value



@app.callback(
    Output(component_id='selected-data', component_property='figure'),
    [Input(component_id='years-slider', component_property='value'),
     Input(component_id='technology_id', component_property='value'),
     Input(component_id='parameter_id', component_property='value'),
     Input(component_id='state-dropdown', component_property='value')])
def masterclass (year,technology,parameter,region):
    if len(technology) >0 and len(region)>0 and len(parameter)>0:
        liste=[]
        for i in scalar:
            for j in range(len(region)):
                if len(region) > j and i['region'][0] == region[j]:

                    for k in range(len(technology)):
                        if len(technology) > k and i['technology'] == technology[k]:

                            for l in range(len(parameter)):
                                if len(parameter) > l and i['parameter_name'] == parameter[l]:
                                    liste.append(i)

        df = pd.DataFrame(liste, columns=['scenario_id','region', 'parameter_name', 'technology', 'value','unit','source'])
        df = df[df["scenario_id"] == year]
        print('')
        print('Technology is',technology)
        print('Parameter is',parameter)
        print('Region is',region)
        print('years is',year)
        print('')
        #print(df)
        print(len(technology))


        unit = df["unit"].tolist()
        '''for i in range(len(parameter)):
            print('Unit is',unit[i])'''
        if len(unit)>0:

            if len(technology)==1:
                farbe = "parameter_name"
            elif len(technology)==2:
                farbe = "technology"

            print(farbe)
            fig = px.bar(
                df,
                orientation='h',
                x="value",
                y="source",
                color=farbe,
                hover_name="region",
                hover_data=["region","technology","parameter_name","unit"],
                labels={"source": "Simulation Framework"},
                color_discrete_map={'generation': "#3391CF",
                                    'emissions': "#3391CF",
                                    'deprecated investment cost': "#3391CF",
                                    'input energy': "#3391CF",
                                    'energy flow': "#3391CF",
                                    'photovoltaics': "#3391CF",}

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
            fig_layout["margin"]["t"] = 50
            fig_layout["margin"]["r"] = 50
            fig_layout["margin"]["b"] = 50
            fig_layout["margin"]["l"] = 50

            fig.update_layout(transition_duration=500,legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ))
            #fig.update_traces(marker_color="#3391CF")

            if len(parameter)==1:
                fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('â‚¬/a', '€/a') + ']',nticks=20)
            if len(parameter)==2:
                fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('â‚¬/a', '€/a') + ']' + "\n & \n" +
                                       parameter[1] + "\n in \n" + '[' + unit[1].replace('â‚¬/a', '€/a') + ']',nticks=20)
            if len(parameter)==3:
                fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('â‚¬/a', '€/a') + ']' + "\n & \n" +
                                       parameter[1] + "\n in \n" + '[' + unit[1].replace('â‚¬/a', '€/a') + ']' + "\n & \n" +
                                       parameter[2] + "\n in \n" + '[' + unit[2].replace('â‚¬/a', '€/a') + ']',nticks=20)


            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

#selecting parameter_name
@app.callback(
    [Output(component_id='parameter_id_2', component_property='options'),
     Output(component_id='parameter_id_2', component_property='value')],
    [Input(component_id='tabs_3', component_property='value')])
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
    Output(component_id='selected-data_2', component_property='figure'),
    [Input(component_id='years-slider', component_property='value'),
     Input(component_id='tabs_3', component_property='value'),
     Input(component_id='parameter_id_2', component_property='value'),
     Input(component_id='state-dropdown', component_property='value'),
     Input(component_id='source', component_property='value')])
def masterclasss (year,technology,parameter,region,source):
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
                    y=y,
                    color_discrete_map={'Urbs': "#3391CF",
                                        'Balmorel':"red"}
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
            fig_layout["margin"]["t"] = 20
            fig_layout["margin"]["r"] = 50
            fig_layout["margin"]["b"] = 50
            fig_layout["margin"]["l"] = 50
            fig.update_layout(transition_duration=100)
            #fig.update_traces(line_color="#3391CF")
            fig.update_xaxes( nticks=40)
            if parameter==parameter:
                fig.update_yaxes(title= parameter,nticks=20)
            else:
                raise PreventUpdate
            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)
