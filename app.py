import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import json
import pandas as pd
from dash.dependencies import Input, Output
import urllib3
from dash.exceptions import PreventUpdate

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

from assets.data.data_scalars import scalars
scalar=scalars[0:1540]


#x=df.to_dict('records')
#print(x==scalar)
#print(scalar)
from assets.data.data_timeseries import timeseries

from assets.data.data_in_scalars import scalars_in






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
                    dcc.Tab(label='Base-Scenario', value='base', style={'background-color':"#1B2129"}),
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
                                                          {'label': 'transmission', 'value': 'transmission'}],
                                                 value='generation',searchable=False,
                                                 multi=False, id="dd1",clearable=False),
                                    html.P(id="field_text", children='Select Field:'),
                                    dcc.Dropdown(options=[{'label':'economic','value':'economic'},
                                                          {'label':'environmental','value':'environmental'},
                                                          {'label':'technical','value':'technical'}],
                                                 value='economic',clearable=False,
                                            multi=False,id="dd2",searchable=False),
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
                                    dcc.Dropdown(multi=True, id="dd4", clearable=False),  # 1.Filter TECHNOLOGY
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
                                        options=[{'label':'urbs','value':'urbs'},{'label':'oemof','value':'oemof'},
                                                 {'label':'GENESYS-2','value':'gen2'},{'label':'BALMOREL','value':'balmorel'},
                                                 {'label':'GENeSYS-mod','value':'gen'}], value=['urbs','oemof','balmorel','gen2','gen'],
                                        id='source',labelStyle={'display': 'inline-block','size':'50px'}),
                                        html.P(id="description_1", children='html color code'),
                                        dcc.Input(id="background", type='text',
                                              placeholder='html color code for background',value="#1f2630",
                                              size="30", minLength="7", maxLength="7",style={'width' : '120px'})]),
                                    html.Br(id='filler_2j2', children=[]),
                                    dcc.Graph(id="scalar", figure={}, style={}),
                                    html.Div(id="parameter",
                                             children=[
                                                 html.P(id="parameter_text", children='Select Parameter:'),
                                                 dcc.Dropdown(options=[{'label': 'fixed costs', 'value': 'fixed'},
                                                                       {'label': 'deceprated investment costs',
                                                                        'value': 'dic'}],
                                                              value=['fixed'],
                                                              multi=True, id="dd7", clearable=False)]),  # 3.Filter]),
                                    dcc.RadioItems(options=[{'label': 'All', 'value': 'All'},
                                                            {'label': 'choose', 'value': 'choose'}],
                                                   value='choose', labelStyle={'display': 'inline-block'},
                                                   id='radio7'),
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


#dropdown 4 TECHNOLOGY
@app.callback(
    [Output(component_id='dd4', component_property='options'),
    Output(component_id='dd4', component_property='value')],
    [Input(component_id='dd1', component_property='value'),
     Input(component_id='radio4', component_property='value')])
def technology_filter(dd1,selector):
    option=[]
    value=[]

    if dd1=='generation':
        df=pd.DataFrame(scalars_in)
        df=df[df['technology']!='storage']
        df = df[df['technology'] != 'transmission']
        available=df['technology'].unique()
        option=[{'label':str(technology),'value':str(technology)}
                for technology in available]
        value=["photovoltaics"]
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
    elif dd1=="storage":
        option=[{'label':'storage','value':'storage'}]
        value=['storage']


    return option,value


#Dropdown 5 Input
@app.callback(
    [Output(component_id='dd5', component_property='options'),
    Output(component_id='dd5', component_property='value')],
    [Input(component_id='dd4', component_property='value'),
     Input(component_id='radio5', component_property='value')])
def input_filter(dd4,selector):
    option=[]
    value=[]
    if type(dd4) is list:
        if len(dd4)>0:
            x=[]
            for i in range(len(scalars_in)):
                for j in range(len(dd4)):
                    if scalars_in[i]['technology'] == dd4[j]:
                        x.append(scalars_in[i])
                        df = pd.DataFrame(x, columns=['technology', 'technology_type', 'input_energy_vector'])
                        available = df['input_energy_vector'].unique()
            option = [{'label': str(energy_input), 'value': str(energy_input)}
                      for energy_input in available]
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
     Input(component_id='radio6', component_property='value')])
def input_filter(dd5,dd4,selector):
    option=[]
    value=[]
    available=[]

    if type(dd5) is list and type(dd4) is list:
        if len(dd5)>0 and len(dd4)>0:
            x=[]
            for i in range(len(scalars_in)):
                for j in range(len(dd5)):
                    for k in range(len(dd4)):
                        if scalars_in[i]['input_energy_vector'] == dd5[j] and scalars_in[i]['technology']==dd4[k]:
                            x.append(scalars_in[i])
                            df = pd.DataFrame(x, columns=['technology', 'technology_type', 'input_energy_vector'])
                            available = df['technology_type'].unique()

            option = [{'label': str(type), 'value': str(type)}
                      for type in available]
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


#Dropdown 3 regions
@app.callback(
    Output(component_id='dd3', component_property='value'),
    [Input(component_id='radio3', component_property='value')])
def regions(selector):
    value=[]
    if selector == 'choose':
        value = ['BB']
    else:
        for i in range(len(region_options)):
            value.append(region_options[i]["value"])

    return value



#background color change
'''@app.callback(
    [Output(component_id='timeseries', component_property='figure'),
    Output(component_id='scalar', component_property='figure')],
    [Input(component_id='background', component_property='value')])
def background_color (background):
    if len(background)==7 and background.startswith('#'):
        figgg_layout["plot_bgcolor"] = background
        figg_layout["plot_bgcolor"] = background
    else:
        raise PreventUpdate
    return figgg,figg'''

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
                                   hover_data=['Population', 'Capital', 'Area (sq. km)'],
                                   zoom=3.8, center={"lat": 51.3, "lon": 10.3}, opacity=0.7,
                                   color_discrete_map={'BB':'blue','SN':'orange','MV':'red','BY':'yellow',
                                                       'NI':'green','HB':'yellow','HH':'red'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)
        return fig

    else:
        raise PreventUpdate
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
