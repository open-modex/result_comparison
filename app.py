import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import urllib3
from dash.exceptions import PreventUpdate
import os
import ast

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

YEARS = [2020,2030,2050]

null=0
nan=0

DEFAULT_COLORSCALE = ["#f2fffb","#bbffeb","#98ffe0","#79ffd6","#6df0c8","#69e7c0","#59dab2","#45d0a5",
                      "#31c194","#2bb489","#25a27b","#1e906d","#188463","#157658","#11684d","#10523e"]
DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)






#x=df.to_dict('records')


from assets.data.ergebnisse import scalars as honeychu
scalars_in=honeychu
scalars=honeychu
scalar=honeychu
from timeseries import timeseries
'''scalars_in=[]
for i in honeychu:
    if i['region'][0] == 'BB':
        scalars_in.append(i)
qw=pd.DataFrame(scalars_in)
qw=qw[qw['parameter_name']=='electricity generation']
qw=qw['technology'].unique()

from timeseries import timeseries'''




#available_parameter=df['parameter_name'].unique()
#available_energy=df['input_energy_vector'].unique()
#options=[{'label':i, 'value': i} for i in available_energy]'''
from assets.data.data_karte import features
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"
map=pd.read_csv("assets/states_list.csv", engine="python", index_col=False, delimiter='\;', dtype={"abbrev": str})

region_options = [{"label": str(region), "value": str(region)}
                    for region in map['abbrev']]



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
                dcc.Tabs(id="scenario", value='base', children=[
                    dcc.Tab(label='Base-Scenario', value='base', style={'background-color':"#FFFFFF"}),
                    dcc.Tab(label='Pathway', value='var1',style={'background-color':"#1B2129"}),
                    dcc.Tab(label='Pathway + Heat', value='var2',style={'background-color':"#1B2129"})])]),#STANDARD
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
                                html.P(id="slider-text", children="Select Year:"),
                                dcc.Slider(id="years-slider", min=2016, max=2050, step=None, value=2016,
                                            marks={2016: {"label": '2016', "style": {"color": "#7fafdf"}},
                                                   2030: {"label": '2030', "style": {"color": "#7fafdf"}},
                                                   2050: {"label": '2050', "style": {"color": "#7fafdf"}}})]),#STANDARD
                        html.Br(id='filler_1',children=[]),
                        html.Div(
                            id="selection",
                            children=[
                                    html.P(id="utility_text", children='Select Utility:'),
                                    dcc.Dropdown(options=[{'label': 'generation', 'value': 'generation'},
                                                          {'label': 'storage', 'value': 'storage'},
                                                          {'label': 'transmission', 'value': 'transmission'},
                                                          {'label': 'ALL', 'value': 'ALL'}],
                                                 value='generation',searchable=False,
                                                 multi=False, id="dd1",clearable=False),
                                    html.P(id="field_text", children='Select Parameter:'),
                                    dcc.Dropdown(id="dd2",clearable=False, searchable=False),
                                    html.P(id="timeseries_check", children='Timeseries:'),
                                    html.Br(id='filler_4', children=[]),
                                    html.Div(id="regions",
                                             children=[
                                                 html.P(id="region_text",children='Select Region:'),
                                                 dcc.RadioItems(options=[{'label': 'All', 'value': 'All'},
                                                                         {'label': 'choose', 'value': 'choose'}],
                                                   value='choose',labelStyle={'display': 'inline-block'},id='radio3')]),
                                    dcc.Dropdown(options= region_options,
                                                value = ['BB'],multi=True, id="dd3",clearable=False),#STANDARD
                                    html.Br(id='filler_3', children=[]),
                                    dcc.Graph(id="deutschland",
                                          figure={},config = dict({'scrollZoom': False}))]),
                ]),
                #das ist die komplette rechte Seite
                html.Div(
                    id="right-column",
                    children=[
                        html.Div(
                            id="up",
                            children=[
                            html.Div(
                                id="right-left",
                                children=[
                                    html.Div(id="technology",
                                             children=[
                                                 html.P(id="technology_text", children='Select Technology:'),
                                                 dcc.RadioItems(options=[{'label': 'All', 'value': 'All'},
                                                                         {'label': 'choose', 'value': 'choose'}],
                                                                value='choose', labelStyle={'display': 'inline-block'},
                                                                id='radio4')]),
                                    dcc.Dropdown(id="dd4", multi=True),  # 1.Filter TECHNOLOGY
                                    html.Div(id="input",
                                             children=[
                                                 html.P(id="input_text", children='Select Input:'),
                                                 dcc.RadioItems(options=[{'label': 'All', 'value': 'All'},
                                                                         {'label': 'choose', 'value': 'choose'}],
                                                                value='choose', labelStyle={'display': 'inline-block'},
                                                                id='radio5')]),
                                    dcc.Dropdown(multi=True, id="dd5", clearable=False), #2.Filter INPUT
                                    html.Div(id="type",
                                             children=[
                                                 html.P(id="type_text", children='Select Type:'),
                                                 dcc.RadioItems(options=[{'label': 'All', 'value': 'All'},
                                                                         {'label': 'choose', 'value': 'choose'}],
                                                                value='choose', labelStyle={'display': 'inline-block'},
                                                                id='radio6')]),
                                    dcc.Dropdown(multi=True, id="dd6", clearable=False),  # 3.Filter TYPE

                                ]),
                            html.Div(
                                id="arbitrary",
                                children=[

                                    html.Div(id="extra",children=[
                                        dcc.Checklist(
                                        options=[{'label':'Urbs','value':'Urbs'},{'label':'Oemof','value':'Oemof'},
                                                 {'label':'GENESYS-2','value':'GENESYS-2'},{'label':'Balmorel','value':'Balmorel'},
                                                 {'label':'Genesys-mod','value':'Genesys-mod'}],
                                        value=['Balmorel'],
                                        id='source',labelStyle={'display': 'inline-block','size':'50px'}),
                                        html.P(id="description_1", children='html color code'),
                                        dcc.Input(id="background", type='text',
                                              pattern=u"^#[A-Fa-f0-9]{6}$",value="#1f2630",
                                              size="30", minLength="7", maxLength="7",style={'width' : '120px'})]),
                                    html.Br(id='filler_2j2', children=[]),
                                    dcc.Graph(id="scalar", figure={}, style={}),

                                    ]),
                            ]
                        ),
                        html.Br(id='filler_2', children=[]),
                        html.Div(
                            id="down",
                            children=[
                                dcc.Graph(id="timeseries",figure={},style={})
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)])


@app.callback(
    [Output(component_id='dd2', component_property='options'),
     Output(component_id='dd2', component_property='value'),
     Output(component_id='dd2', component_property='multi')],
    [Input(component_id='dd1', component_property='value')])
def start(dd1):
    option=[]
    value=[]


    if dd1=='ALL':
        option=[{'label':'cost system','value':'cost system'},
                {'label':'slack','value':'slack','disabled':True},
                {'label':'renewable generation','value':'renewable generation'},
                {'label':'emissions','value':'emissions'},
                {'label':'variable cost','value':'variable cost'},
                {'label':'fixed cost','value':'fixed cost'}]
        value=['emissions']
        multi=True
    elif dd1=='generation':
        option=[{'label':'electricity generation','value':'electricity generation'},
                {'label':'fixed cost','value':'fixed cost'},
                {'label':'variable cost','value':'variable cost'}]
        value='electricity generation'
        multi=False
    elif dd1=='transmission':
        option=[{'label':'energy flow','value':'energy flow'},
                {'label':'losses','value':'losses'},
                {'label':'added capacity','value':'added capacity','disabled':True}]
        value=['energy flow']
        multi=True
        #if multi is True then value has to be a list, if false, value is only string
    elif dd1=='storage':
        option=[{'label':'storage level','value':'storage level'},
                {'label':'input energy','value':'input energy'},
                {'label':'output energy','value':'output energy'},
                {'label':'losses','value':'losses'}]
        value='input energy'
        multi=False

    return option, value, multi




@app.callback(
    [Output(component_id='timeseries_check', component_property='children'),
     Output(component_id='timeseries_check', component_property='style')],
    [Input(component_id='dd1', component_property='value'),
    Input(component_id='dd2', component_property='value')])
def time(dd1,dd2):
    children=[]
    style = {"color": "red"}
    timeseries=['electricity generation', 'input energy', 'output energy','energy flow']

    if type(dd2) is not None:
        if type(dd2) is list and dd2[0] in timeseries or type(dd2) is str and dd2 in timeseries:
            children = 'Timeseries: YES'
            style = {"color": "green"}
        elif dd2=='storage level':
            children= 'Timeseries ONLY'
            style = {"color": "green"}
        else:
            children = 'Timeseries: NO'
            style = {"color": "red"}
        return children,style

    else:
        raise PreventUpdate



#dropdown 4 TECHNOLOGY
@app.callback(
    [Output(component_id='dd4', component_property='options'),
     Output(component_id='dd4', component_property='value')],
    [Input(component_id='dd1', component_property='value'),
     Input(component_id='radio4', component_property='value'),
     Input(component_id='dd2', component_property='value'),
     ])
def technology_filter(dd1,selector,dd2):
    option=[]
    value=[]
    available = []
    available_2 = []
    '''scalars_in = []
    for i in honeychu:
        for j in range(len(dd3)):
            if len(dd3) > j and i['region'][0] == dd3[j]:
                scalars_in.append(i)'''
    if dd1=='ALL':
        option=[{'label':'ALL','value':'ALL'}]
        value=['ALL']


    if dd1=='generation':

        df=pd.DataFrame(scalars_in)
        #hier muss geändert werden
        df=df[df['technology']!='storage']
        df = df[df['technology'] != 'transmission']
        df = df[df['technology'] != 'ALL']
        dff=pd.DataFrame(timeseries)
        dff = dff[dff['technology'] != 'storage']
        dff = dff[dff['technology'] != 'storage']
        dff = dff[dff['technology'] != 'ALL']

        if type(dd2) is list:
            df = df[df['parameter_name']==dd2[0]]
            dff = dff[dff['parameter_name'] == dd2[0]]
        else:
            df = df[df['parameter_name'] == dd2]
            dff = dff[dff['parameter_name'] == dd2]

        available=df['technology'].unique()
        available_2 = dff['technology'].unique()
        option_1=[{'label':str(technology),'value':str(technology)}
                for technology in available]
        option_2=[{'label':str(technology),'value':str(technology)}
                for technology in available_2]
        for i in range(len(option_2)):
            option_1.append(option_2[i])
        option=[]
        for i in option_1:
            if i not in option:
                option.append(i)

        if len(option)>0:
            option=option
            value = [option[0]["value"]]

        if selector == 'choose':
            option=option
            value = value

        else:
            option=option
            value=[]

            for i in range(len(option)):
                value.append(option[i]["value"])

        return option,value
    elif dd1=="transmission":
        option=[{'label':'transmission','value':'transmission'}]
        value=['transmission']

#HIER MUSS AUCH GEÄNDERT WERDEN
    elif dd1=="storage":
        option=[{'label':'storage','value':'storage'}]
        value=['storage']

    return option,value


#Dropdown 5 Input
@app.callback(
    [Output(component_id='dd5', component_property='options'),
     Output(component_id='dd5', component_property='value')],
    [Input(component_id='dd4', component_property='value'),
     Input(component_id='radio5', component_property='value'),
     ])
def input_filter(dd4,selector):
    option=[]
    value=[]
    available = []
    available_2 = []
    '''scalars_in = []
    for i in honeychu:
        for j in range(len(dd3)):
            if len(dd3) > j and i['region'][0] == dd3[j]:
                scalars_in.append(i)'''
    if dd4=='ALL':
        option=[{'label':'ALL','value':'ALL'}]
        value='ALL'


    if type(dd4) is list:
        if len(dd4)>0:
            x,y=[],[]
            #available = []
            for i in range(len(scalars_in)):
                for j in range(len(dd4)):
                    if scalars_in[i]['technology'] == dd4[j]:
                        x.append(scalars_in[i])
                        df = pd.DataFrame(x, columns=['technology', 'technology_type', 'input_energy_vector'])
                        available = df['input_energy_vector'].unique()
            for i in range(len(timeseries)):
                for j in range(len(dd4)):
                    if timeseries[i]['technology'] == dd4[j]:
                        y.append(timeseries[i])
                        df = pd.DataFrame(y, columns=['technology', 'technology_type', 'input_energy_vector'])
                        available_2 = df['input_energy_vector'].unique()

            '''option = [{'label': str(energy_input), 'value': str(energy_input)}
                      for energy_input in availablee]'''

            option_1 = [{'label': str(energy_input),'value': str(energy_input)}
                        for energy_input in available]
            option_2 = [{'label': str(energy_input),'value': str(energy_input)}
                        for energy_input in available_2]
            for i in range(len(option_2)):
                option_1.append(option_2[i])
            option = []
            for i in option_1:
                if i not in option:
                    option.append(i)
            value = [option[0]["value"]]

            if selector == 'choose':
                option=option
                value = value
            else:
                option=option
                value=[]
                for i in range(len(option)):
                    value.append(option[i]["value"])
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    return option,value

#Dropdown 6 Type
@app.callback(
    [Output(component_id='dd6', component_property='options'),
     Output(component_id='dd6', component_property='value')],
    [Input(component_id='dd5', component_property='value'),
     Input(component_id='dd4', component_property='value'),
     Input(component_id='radio6', component_property='value'),
     ])
def input_filter(dd5,dd4,selector):
    option=[]
    value=[]
    available=[]
    available_2 = []
    '''scalars_in = []
    for i in honeychu:
        for j in range(len(dd3)):
            if len(dd3) > j and i['region'][0] == dd3[j]:
                scalars_in.append(i)'''
    if dd5=='ALL':
        option=[{'label':'ALL','value':'ALL'}]
        value='ALL'

    if type(dd5) is list and type(dd4) is list:
        if len(dd5)>0 and len(dd4)>0:
            x,y=[],[]
            for i in range(len(scalars_in)):
                for j in range(len(dd5)):
                    for k in range(len(dd4)):
                        if scalars_in[i]['input_energy_vector'] == dd5[j] and scalars_in[i]['technology']==dd4[k]:
                            x.append(scalars_in[i])
                            df = pd.DataFrame(x, columns=['technology', 'technology_type', 'input_energy_vector'])
                            available = df['technology_type'].unique()
            for i in range(len(timeseries)):
                for j in range(len(dd5)):
                    for k in range(len(dd4)):
                        if timeseries[i]['input_energy_vector'] == dd5[j] and timeseries[i]['technology']==dd4[k]:
                            y.append(timeseries[i])
                            df = pd.DataFrame(y, columns=['technology', 'technology_type', 'input_energy_vector'])
                            available_2 = df['technology_type'].unique()

            '''option = [{'label': str(type), 'value': str(type)}
                      for type in available]'''
            option_1 = [{'label': str(type),'value': str(type)}
                        for type in available]
            option_2 = [{'label': str(type),'value': str(type)}
                        for type in available_2]
            for i in range(len(option_2)):
                option_1.append(option_2[i])
            option = []
            for i in option_1:
                if i not in option:
                    option.append(i)
            if len(option)>0:
                value = [option[0]["value"]]

            if selector == 'choose':
                option=option
                value = value
            else:
                option=option
                value=[]
                for i in range(len(option)):
                    value.append(option[i]["value"])
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    return option,value

@app.callback(
    [Output(component_id='radio3', component_property='options'),
     Output(component_id='radio3', component_property='value')],
     [Input(component_id='dd1', component_property='value')])
def abc(all):
    option=[]
    value=[]
    if all=='ALL':
        option = [{'label': 'All', 'value': 'ALL'},
                  {'label': 'choose', 'value': 'choose'}]
        value = 'ALL'
    else:
        option = [{'label': 'All', 'value': 'ALL'},
                  {'label': 'choose', 'value': 'choose'}]
        value = 'choose'
    return option, value

#Dropdown 3 regions
@app.callback(
    Output(component_id='dd3', component_property='value'),
    [Input(component_id='radio3', component_property='value')])
def regions(selector):
    value=[]
    if selector == 'choose':
        value = ['BB']

    elif selector == 'ALL':
        for i in range(len(region_options)):
            value.append(region_options[i]["value"])

    return value



#interaktive Karte
@app.callback(
    Output(component_id='deutschland', component_property='figure'),
    [Input(component_id='dd3', component_property='value')])
def karte(region):
    liste=[]
    if len(region)>0:
        for i in features:
            for k in range(len(region)):
                if i['id'] == region[k]:
                    liste.append(i)

        card= json.load(open("assets/card.geojson", "r"))
        card["features"]=liste
        fig = px.choropleth_mapbox(map, geojson=card, locations='abbrev',
                                   mapbox_style="carto-darkmatter", hover_name='Bundesland', color='abbrev',
                                   hover_data=['Population'],
                                   zoom=3.8, center={"lat": 51.3, "lon": 10.3}, opacity=0.7,
                                   color_discrete_map={'BB':'blue','SN':'orange','MV':'red','BY':'yellow',
                                                       'NI':'green','HB':'yellow','HH':'red'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
        return fig

    else:
        raise PreventUpdate
    return fig


@app.callback(
    Output(component_id='scalar', component_property='figure'),
    [Input(component_id='dd1', component_property='value'),
     Input(component_id='dd2', component_property='value'),
     Input(component_id='dd3', component_property='value'),
     Input(component_id='dd4', component_property='value'),
     Input(component_id='dd5', component_property='value'),
     Input(component_id='dd6', component_property='value'),
     Input(component_id='source', component_property='value'),
     Input(component_id='background', component_property='value')])
def masterclass_1 (dd1,parameter,region,technology,input,tech_type,source,background):
    #print(dd1,parameter,region,technology,input,tech_type,source)

    if type(region) is list and type(technology) is list and type(input) is list and type(tech_type) is list:
        if len(technology) >0 and len(region)>0 and len(input)>0 and len(tech_type)>0:
            liste=[]
            for i in honeychu:
                for j in range(len(region)):
                    for s in range(len(i['region'])): # neu
                        if len(region) > j and i['region'][s] == region[j]:

                            for k in range(len(technology)):
                                if len(technology) > k and i['technology'] == technology[k]:

                                    for o in range(len(input)):
                                        if len(input) > o and i['input_energy_vector'] == input[o]:

                                            for h in range(len(tech_type)):
                                                if len(tech_type) > h and i['technology_type'] == tech_type[h]:

                                                    for a in range(len(source)):
                                                        if len(source) > a and i['source'] == source[a] and type(parameter) is list:

                                                            for l in range(len(parameter)):
                                                                if len(parameter) > l and i['parameter_name'] == parameter[l]:
                                                                    liste.append(i)

                                                        elif len(source) > a and i['source'] == source[a] and type(parameter) is str:
                                                                if i['parameter_name'] == parameter:
                                                                    liste.append(i)
            #cutting out possible duplicates
            final_list=[]

            for i in liste:
                if i not in final_list:
                    final_list.append(i)

            Land = ['BW', 'BY', 'BE', 'BB', 'HB', 'HH', 'HE', 'NI', 'MV', 'NW', 'RP', 'SL', 'SN', 'ST', 'SH', 'TH']
            Ersatz = ['Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',
                      'Niedersachsen', 'Meckelnburg-Vorpommern', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
                      'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']
            for l in range(len(final_list)):
                final_list[l]['region_2'] = final_list[l]['region'][0]
                for i in range(len(Land)):
                    if final_list[l]['region'][0]== Land[i]:
                        final_list[l]['region_3'] = Ersatz[i]






            df = pd.DataFrame(final_list, columns=['scenario_id','region', 'parameter_name', 'technology',
                                          'value','unit','source', 'input_energy_vector', 'technology_type'])

            dff = pd.DataFrame(final_list, columns=['scenario_id', 'region','region_2','region_3', 'parameter_name',
                                                    'technology','value', 'unit', 'source', 'input_energy_vector',
                                                    'technology_type'])
            unit = df["unit"].tolist()
            values=[]
            values_2=[]
            for i in range(len(final_list)):
                if final_list[i]['source']=='Balmorel':
                    values.append(final_list[i]['value'])
            for i in range(len(final_list)):
                if final_list[i]['source']=='GENESYS-2':
                    values_2.append(final_list[i]['value'])

            '''for i in range(len(parameter)):
                print('Unit is',unit[i])'''
            if len(unit)>0:
                if parameter[0]=='emissions':
                    total=round(int(sum(values))/1000,1)
                    total_2 = round(int(sum(values_2))/1000,1)
                else:
                    total = int(sum(values))
                    total_2 = int(sum(values_2))
                if parameter[0] == 'emissions':
                    total = str(total).replace('.',',') + '\n' + 'MT'
                    total_2=str(total_2).replace('.',',') + '\n' + 'MT'
                elif parameter[0] == 'renewable generation':
                    total = str(total).replace('.',',') + '\n' + 'TWh'
                    total_2=str(total_2).replace('.',',') + '\n' + 'TWh'
                elif parameter[0] == 'variable cost' or parameter[0]=='fixed cost':
                    total = str(round(int(sum(values)) / 1000000000, 2)).replace('.',',')+ 'Mrd.' + unit[0].replace('€/a','€')
                    total_2 = str(round(int(sum(values_2)) / 1000000000, 2)).replace('.',',')+ 'Mrd.'  + unit[0].replace('€/a','€')
                else:
                    total_2 = str(total_2).replace('.',',') + '\n' + unit[0].replace('€/a','€')
                    total=str(total).replace('.',',') +'\n'+unit[0].replace('€/a','€')

                if type(parameter) is list and len(parameter)>1:
                    farbe = "parameter_name"
                    text=None


                elif len(parameter)==1 or type(parameter) is str:
                    if len(tech_type)>1:
                        farbe='technology_type'
                        text='region'
                    else:
                        farbe = "region_2"
                        text='region'
                        if len(final_list[0]['region'])>1:
                            text='region'
                            farbe='parameter_name'
                        elif len(final_list[0]['region'])==1:
                            text='region'
                            farbe=farbe
                            if len(region)<5:
                                text='region_3'



                fig = px.bar(
                    dff,
                    orientation='h',
                    x="value",
                    y="source",
                    color=farbe,
                    text=text,
                     color_discrete_map={'BB':'#5E5D5F','BE':'#5E5D5F','BW':'#5E5D5F','BY':'#5E5D5F',
                                        'HB':'#5E5D5F','HE':'#5E5D5F','HH':'#5E5D5F','MV':'#5E5D5F',
                                        'NI':'#00549F','NW':'#5E5D5F','RP':'#5E5D5F','SH':'#5E5D5F',
                                        'SL':'#5E5D5F','SN':'#5E5D5F','ST':'#5E5D5F','TH':'#5E5D5F',
                                        'variable cost':'#407FB7','fixed cost':'#00549F',
                                         'renewable generation':'#00549F'},
                    hover_name="region",
                    hover_data=["technology","parameter_name","unit"],
                    labels={"source": "Simulation Framework"},


                )

                fig_layout = fig["layout"]
                fig_layout["paper_bgcolor"] = "#1f2630"
                #fig_layout["plot_bgcolor"] = "#1f2630"
                fig_layout["font"]["color"] = "#ffffff"
                fig_layout["legend_bgcolor"] = "#1f2630"
                fig_layout["title"]["font"]["color"] = "#3391CF"
                fig_layout["xaxis"]["tickfont"]["color"] = "#ffffff"
                fig_layout["yaxis"]["tickfont"]["color"] = "#ffffff"
                fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
                fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
                fig_layout["margin"]["t"] = 50
                fig_layout["margin"]["r"] = 50
                fig_layout["margin"]["b"] = 50
                fig_layout["margin"]["l"] = 50
                fig.add_annotation(xref='paper',yref='paper',x=0.9,y=0.1,text=total,
                                   showarrow=False, bordercolor="#c7c7c7",borderwidth=2,borderpad=4,
                                   bgcolor="#000000",font=dict(color="#ffffff"))
                if len(source)>1:
                    fig.add_annotation(xref='paper', yref='paper', x=0.9, y=0.6, text=total_2,
                                       showarrow=False, bordercolor="#c7c7c7", borderwidth=2, borderpad=4,
                                       bgcolor="#000000", font=dict(color="#ffffff"))
                default_background = "#1f2630"
                if len(background) == 7 and background.startswith("#"):
                    try:
                        int(background[1:], 16)
                        fig_layout["plot_bgcolor"] = background
                    except:
                        fig_layout["plot_bgcolor"] = default_background
                else:
                    fig_layout["plot_bgcolor"] = default_background

                fig.update_layout(transition_duration=500, legend=dict(orientation="h",
                                                                       yanchor="bottom", y=1.02, xanchor="right",
                                                                       x=0.3))
                if text=='region':
                    fig.update_layout(showlegend=False)
                else:
                    fig.update_layout(showlegend=True)
                #fig.update_traces(marker_color="#3391CF")

                if type(parameter) is str:
                    fig.update_xaxes(title=parameter + "\n in \n" + '[' + unit[0].replace('€/a','€') + ']',nticks=20)
                if len(parameter)==1:
                    fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('€/a','€') + ']',nticks=20)
                    if parameter[0]=='emissions':
                        fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + 'kT' + ']',
                                         nticks=20)
                    if parameter[0]=='renewable generation':
                        fig.update_xaxes(title=parameter[0] + "\n in \n" + '[TWh]',
                                         nticks=20)
                if len(parameter)==2:
                    fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('€/a','€') + ']' + "\n & \n" +
                                           parameter[1] + "\n in \n" + '[' + unit[1].replace('€/a','€') + ']',nticks=20)
                if len(parameter)==3:
                    fig.update_xaxes(title=parameter[0] + "\n in \n" + '[' + unit[0].replace('â‚¬/a', '€/a') + ']' + "\n & \n" +
                                           parameter[1] + "\n in \n" + '[' + unit[1].replace('â‚¬/a', '€/a') + ']' + "\n & \n" +
                                           parameter[2] + "\n in \n" + '[' + unit[2].replace('â‚¬/a', '€/a') + ']',nticks=20)


                return fig
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='dd2', component_property='value'),
     Input(component_id='dd3', component_property='value'),
     Input(component_id='dd4', component_property='value'),
     Input(component_id='dd5', component_property='value'),
     Input(component_id='dd6', component_property='value'),
     Input(component_id='source', component_property='value'),
     Input(component_id='background', component_property='value')])
def masterclass_2 (parameter,region,technology,input,tech_type,source,background):
    from timeseries import timeseries
    from assets.data.ergebnisse import SH_wind_onshore,BB_chp_steam,HE_PV_R,BE_chp_CC,\
        BB_storage,BE_chp_waste,HE_chp_gas,BY_PV_rooftop,BY_chp_gas_cc,BE_chp_gas_gas
    timeseries.append(SH_wind_onshore)
    timeseries.append(BB_chp_steam)
    timeseries.append(HE_PV_R)
    timeseries.append(BE_chp_CC)
    timeseries.append(BB_storage)
    timeseries.append(BE_chp_waste)
    timeseries.append(HE_chp_gas)
    timeseries.append(BY_PV_rooftop)
    timeseries.append(BY_chp_gas_cc)
    timeseries.append(BE_chp_gas_gas)
    #print(parameter,region,technology,input,tech_type,source)
    for i in range(len(timeseries)):
        if timeseries[i]['parameter_name'] == 'generation':
            timeseries[i]['parameter_name'] = 'electricity generation'
    #print(parameter,region,technology,input,tech_type,source)
    if type(region) is list and type(technology) is list and type(input) is list and type(tech_type) is list:
        if len(technology) >0 and len(region)>0 and len(input)>0 and len(tech_type)>0:
            liste=[]
            for i in timeseries:
                for j in range(len(region)):
                    for s in range(len(i['region'])):  # neu
                        if len(region) > j and i['region'][s] == region[j]:

                            for k in range(len(technology)):
                                if len(technology) > k and i['technology'] == technology[k]:

                                    for o in range(len(input)):
                                        if len(input) > o and i['input_energy_vector'] == input[o]:

                                            for h in range(len(tech_type)):
                                                if len(tech_type) > h and i['technology_type'] == tech_type[h]:

                                                    for a in range(len(source)):
                                                        if len(source) > a and i['source'] == source[a] and type(parameter) is list:

                                                            for l in range(len(parameter)):
                                                                if len(parameter) > l and i['parameter_name'] == parameter[l]:
                                                                    liste.append(i)

                                                        elif len(source) > a and i['source'] == source[a] and type(parameter) is str:
                                                                if i['parameter_name'] == parameter:
                                                                    liste.append(i)


            final_list = []
            for i in liste:
                if i not in final_list:
                    final_list.append(i)


            '''if len(final_list)>0 and len(parameter)>0:
                urbs = []
                oemof = []
                gen = []
                gen2 = []
                balmorel = []

                photo=[]
                lignite=[]

                p_help=[photo,lignite]
                pp_help=['photovoltaics','generator']

                x_help = [urbs, oemof, gen2, gen, balmorel]
                xx_help = ['Urbs', 'Oemof', 'GENESYS-2', 'Genesys-mod', 'Balmorel']

                #auf gleiches sources überprüft
                for i in range(len(final_list)):
                    for j in range(len(x_help)):
                        if final_list[i]["source"] == xx_help[j]:
                            x_help[j].append(final_list[i])  # balmorel

                #auf gleiches technology überprüft
                for i in range(len(final_list)):
                    for j in range(len(p_help)):
                        if final_list[i]["technology"] == pp_help[j]:
                            p_help[j].append(final_list[i])  # photovoltaics


                f,g= [],[]
                fg=[f,g]
                fg_2=[photo,lignite]

                a,b,c,d,e = [],[],[],[],[]
                help_1 = [a, b, c, d, e]
                help_2 = [balmorel, urbs, gen, gen2, oemof]
                #arrays gemacht und eine Liste mit gleichen FW gemacht
                for i in range(len(help_2)):
                    for j in range(len(help_2[i])):
                        x = np.array(help_2[i][j]["series"])
                        help_1[i].append(x)  # balmorel

                for i in range(len(fg_2)):
                    for j in range(len(fg_2[i])):
                        x = np.array(fg_2[i][j]["series"])
                        fg[i].append(x)  # balmorel

                liste_2=[f,g]

                liste = [a, b, c, d, e]


                #Summieren der Timeseries-Elemente
                for i in range(len(liste)):
                    if len(liste[i]) == 0:
                        liste[i] = range(201)
                    elif len(liste[i]) > 0:
                        liste[i] = list(sum(liste[i]))  # balmorel

                # Summieren der Timeseries-Elemente
                for i in range(len(liste_2)):
                    if len(liste_2[i]) == 0:
                        liste_2[i] = range(201)
                    elif len(liste_2[i]) > 0:
                        liste_2[i] = list(sum(liste_2[i]))  # balmorel

                #neue Dictionary für die Timeseries
                new = [{'source': 'Balmorel', 'series': liste[0]},
                       {'source': 'Urbs', 'series': liste[1]},
                       {'source': 'Genesys-mod', 'series': liste[2]},
                       {'source': 'GENESYS-2', 'series': liste[3]},
                       {'source': 'Oemof', 'series': liste[4]}]

                final = {x['source']: x["series"] for x in new}
                #hier muss die Range für ein ganzes Jahr geändert werden
                final["hour"] = range(201)
                df = pd.DataFrame(final)

                #neue Dictionary für die Timeseries
                new_2 = [{'technology': 'photovoltaics', 'series': liste_2[0]},
                         {'technology': 'generator', 'series': liste_2[1]}]

                final_2 = {xi['technology']: xi["series"] for xi in new_2}
                #hier muss die Range für ein ganzes Jahr geändert werden
                final_2["hour"] = range(201)
                dff = pd.DataFrame(final_2)'''

            if len(final_list) > 0 and len(parameter) > 0:
                data = {timeseriess["source"]: timeseriess["series"] for timeseriess in final_list}
                data["hour"] = range(8736)  # hier wird ein neuer key eingefügt
                data_2={timeseriess["technology"]: timeseriess["series"] for timeseriess in final_list}
                data_2["hour"]=range(8736)
                df = pd.DataFrame(data)
                dff=pd.DataFrame(data_2)


                #if len(df)>0 and len(source)>1:
                y=[]
                for i in range(len(source)):
                    y.append(source[i])
                    fig = px.line(
                        df,
                        x='hour',
                        y=y,

                        #line_dash='Balmorel',
                        color_discrete_map={'Balmorel':'orange',
                                            'GENESYS-2':'#00549F'},
                                            #{'Balmorel':'#00549F'
                                            #'GENESYS-2':'#8EBAE5',
                                            #'Oemof':'orange'}
                    )
                    print(i,y[i],y)



                    #hier kann noch die summe der regional aggregations her
                '''if len(dff)>0 and len(source)==1:
                    tech = []
                    for i in range(len(technology)):
                        #print('technology selected are',tech)
                        tech.append(technology[i])
                        fig = px.line(
                            dff,
                            x="hour",
                            y=tech)'''

                fig_layout = fig["layout"]
                fig_layout["paper_bgcolor"] = "#1f2630"
                fig_layout["legend_bgcolor"] = "#1f2630"
                fig_layout["font"]["color"] = "#ffffff"
                fig_layout["title"]["font"]["color"] = "#3391CF"
                fig_layout["xaxis"]["tickfont"]["color"] = "#ffffff"
                fig_layout["yaxis"]["tickfont"]["color"] = "#ffffff"
                fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
                fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
                fig_layout["margin"]["t"] = 20
                fig_layout["margin"]["r"] = 50
                fig_layout["margin"]["b"] = 50
                fig_layout["margin"]["l"] = 50
                fig.update_layout(transition_duration=100)
                fig.update_xaxes( tick0=0, dtick=24)
                fig.update_layout(transition_duration=500, legend=dict(orientation="h",
                    yanchor="bottom",y=1.02,xanchor="right",x=0.8))

                #fig.update_traces({"line": {"dash": "solid",'width':4}})
                fig.update_traces(patch={"line": {"dash": "dash"}},selector={"legendgroup": "GENESYS-2"})

                default_background = "#1f2630"


                if len(background) == 7 and background.startswith("#"):
                    try:
                        int(background[1:], 16)
                        fig_layout["plot_bgcolor"] = background
                    except:
                        fig_layout["plot_bgcolor"] = default_background
                else:
                    fig_layout["plot_bgcolor"] = default_background

                if parameter==parameter:
                    fig.update_yaxes(title=parameter + "\n in \n"  + 'GW')#final_list[0]['unit']
                
                else:
                    raise PreventUpdate
                return fig
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
