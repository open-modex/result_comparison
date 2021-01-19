# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import timeseries

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    children=[
        html.Div(
            dcc.Tabs(id="folder", value='timeseries', children=[
                dcc.Tab(label='scalars', value='scalars', style={'background-color': "#1B2129"}),
                dcc.Tab(label='timeseries', value='timeseries', style={'background-color': "#1B2129"})])),
        html.Div(id="page-content")
    ]
)

# Update page
@app.callback(
    [Output(component_id='page-content', component_property='children')],
    [Input(component_id='folder', component_property='value')])
def display_page(value):
    if value=='scalars':
        return scalars.create_layout(app)
    elif value=='timeseries':
        return timeseries.create_layout(app)



if __name__ == "__main__":
    app.run_server(debug=True)
