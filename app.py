import os
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import requests
import pandas
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import urllib3

urllib3.disable_warnings()

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


YEARS = [2020,2030,2050]



DEFAULT_COLORSCALE = ["#f2fffb","#bbffeb","#98ffe0","#79ffd6","#6df0c8","#69e7c0","#59dab2","#45d0a5",
                      "#31c194","#2bb489","#25a27b","#1e906d","#188463","#157658","#11684d","#10523e"]
DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)


#scalar=scalar[1540:1556]
#df=df[df["parameter_name"]!="cost system"]


URL='https://modex.rl-institut.de/scenario/id/3?source=modex_output&mapping=concrete'
response = requests.get(URL, timeout=10000, verify=False)
json_data = json.loads(response.text)
scalar=json_data['oed_scalars']
scalar=scalar[0:1540]
df=pd.DataFrame(scalar)

'''dff = df[df["technology"] == 'battery storage']
dff = df[df["parameter_name"] == 'input energy']

#print(dff)

#available_parameter=df['parameter_name'].unique()
#available_energy=df['input_energy_vector'].unique()
#options=[{'label':i, 'value': i} for i in available_energy]

fig = px.bar(
        dff,
        orientation='h',
        x="value",
        y="source",
        hover_name="region",
        labels={"source": "Simulation Framework"},
    )'''


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
                                dcc.Slider(id="years-slider", min=min(YEARS), max=max(YEARS), value=min(YEARS),
                                           marks={str(year): {"label": str(year), "style": {"color": "#7fafdf"}}
                                                  for year in YEARS})]),
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
                                          figure=dict(
                                            layout=dict(
                                                mapbox=dict(layers=[],accesstoken=mapbox_access_token,
                                                        style=mapbox_style,center=dict(lat=38.72490, lon=-95.61446),
                                                        pitch=0,zoom=3.5),
                                            autosize=True)))]),
                ]),
                #das ist die komplette rechte Seite
                html.Div(
                    id="abc",
                    children=[
                        html.Div(
                            id="headerr",
                            children=[
                                html.H5("Info"),
                                html.P("With renewable energy sources, here you can put in a bunch of text")
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
                                html.Button('Start',id='start',n_clicks=0),
                                dcc.Graph(id="selected-data",figure={},style={})
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)])

'''@app.callback(
    [Output(component_id='tabs', component_property='children'),
     Output(component_id='filler', component_property='children'),
     ],
    [Input(component_id='folder', component_property='value')])
def base(basic):
    child_tab=[]
    child_filler = []


    if basic=='scalars':
        child_tab=[
                    dcc.Tab(label='Generation', value='generation', style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Battery Storage', value='battery storage',style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Transmission', value='transmission',style={'background-color':"#1B2129"})],
        child_filler=[],


    elif basic=='timeseries':
        child_tab=[html.Div(id="ok",children=[
            html.Button('Start', id='sssart', n_clicks=0),
            html.Div(id="dd",children=[
                dcc.Graph(id="tdimes",figure={},style={}),
                dcc.Graph(id="times",figure={},style={})])])]
        child_filler=[]


    return child_tab,child_filler'''




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
    [Input(component_id='tabs_2', component_property='value')])
def two_three(tabs_2):
    opt=[]
    value=[]
    if tabs_2=='energy_transmission':
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
     Output(component_id='state-dropdown', component_property='value')],
    [Input(component_id='tabs_2', component_property='value'),
     Input(component_id='radio', component_property='value')])
def three_four(tabs_2,selector):
    opt=[]
    value=[]

    if tabs_2=='energy_transmission':
        opt = [{'label': 'Brandenburg to Berlin', 'value': 'BB to BE'},
                 {'label': 'Berlin to Brandenburg', 'value': 'BE to BB'},
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


        if selector =='choose':
            opt=opt
            value = ['BB to BE']
        else:
            opt = opt
            value= ['BB to BE']
        return opt, value

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

        if selector =='choose':
            opt=opt
            value = ['BB']
        else:
            opt = opt
            value= ['BB','BE','BW','BY','HB','HE','HH','MV','NI','NW','RP','SH','SL','SN','ST','TH']
        return opt, value

    return opt,value


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
        opt = [{'label': 'energy flow', 'value': 'energy flow'},
                  {'label': 'losses', 'value': 'losses'}]
        value = ['energy flow']
    elif dropdown=='costs_transmission': #costs in transmission
        opt = [{'label': 'deprecated investment costs', 'value': 'deprecated investment cost'},
                  {'label': 'deprecated fixed costs', 'value': 'deprecated fixed cost'}]
        value = ['deprecated investment cost']
    #print('paramter name=', value)
    return opt,value


@app.callback(
    Output(component_id='selected-data', component_property='figure'),
    [Input(component_id='start', component_property='n_clicks')],
     [State(component_id='technology_id', component_property='value'),
     State(component_id='parameter_id', component_property='value')])
def masterclass (n_clicks,technology,parameter):
    if len(technology) >0:
        dff = df[df["technology"] == technology[0]]
        dfff = dff[dff["parameter_name"] == parameter[0]]
        print('')
        print('Technology is',technology[0])
        print('Parameter is',parameter[0])
        print('Button has been clicked',n_clicks)
        print('')

        unit = dfff["unit"].tolist()
        fig = px.bar(
            dfff,
            orientation='h',
            x="value",
            y="source",
            #color="regions[0]",
            hover_name="region",
            hover_data=["technology","input_energy_vector","parameter_name","unit"],
            labels={"source": "Simulation Framework"},

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
        fig.update_layout(transition_duration=500)
        fig.update_traces(marker_color="#3391CF")
        fig.update_xaxes(title=parameter[0] + "\n in \n" + unit[0])

        return fig
    else:
        raise dash.exceptions.PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)
