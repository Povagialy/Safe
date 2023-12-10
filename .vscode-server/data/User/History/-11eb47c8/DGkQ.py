'''
Dash apps for the demonstration of functionality

Copyright (c) 2018 Gibbs Consulting and others - see CONTRIBUTIONS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# pylint: disable=no-member

import uuid
import random

from datetime import datetime

import pandas as pd

from django.core.cache import cache
from django.utils.translation import gettext, gettext_lazy

import dash
from dash import dcc, html
from dash.dependencies import MATCH, ALL

import plotly.graph_objs as go

import dpd_components as dpd

from dash.exceptions import PreventUpdate

from django_plotly_dash import DjangoDash
from django_plotly_dash.consumers import send_to_pipe_channel

import pandas as pd
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
import pandas as pd
from sqlalchemy import create_engine
from contextlib import contextmanager

con = mysql.connector.connect(
        host="31.31.196.203",
        user='u1832524_stas',
        password='bf2-DvB-Ljx-Uxj',
        database="u1832524_Lider",
    )

engine = create_engine('mysql+pymysql://u1832524_stas:bf2-DvB-Ljx-Uxj@31.31.196.203/u1832524_Lider', pool_pre_ping=True,
pool_recycle=2800)
connection = engine.raw_connection()
cursor = connection.cursor()
columns = ['Лидеры', 'Тип', 'Лидеры.1', 'Устойчивыелидеры', 'Лидерыизлидеров', 'численность1',
'численность2', 'численность3', 'численность4', 'численность5']
select = '''SELECT `Лидеры`, `Тип`, `Лидеры.1`, `Устойчивыелидеры`, `Лидерыизлидеров`, `численность1`,
`численность2`, `численность3`, `численность4`, `численность5` FROM `atat`;'''
#columns = ['Лидеры', 'Регистрационныйномер', 'КатегорияМСПна10.01.23', 'Тип', 'Лидеры.1', 'Устойчивыелидеры', 'Лидерыизлидеров', 'численность1',
#'численность2', 'численность3', 'численность4', 'численность5', 'численность2темп', 'численность3темп', 'численность4темп', 'численность5темп']
#select = '''SELECT `Лидеры`, `Регистрационныйномер`, `КатегорияМСПна10.01.23`, `Тип`, `Лидеры.1`, `Устойчивыелидеры`, `Лидерыизлидеров`, `численность1`,
#`численность2`, `численность3`, `численность4`, `численность5`, `численность2темп`, `численность3темп`, `численность4темп`, `численность5темп` FROM `atat`;'''
#with engine.connect() as cursor:
cursor.execute(select)
result = pd.DataFrame(cursor.fetchall(), columns = columns)

#columns = ['Лидеры', 'Тип', 'Лидеры.1', 'Устойчивыелидеры', 'Лидерыизлидеров', 'численность1',
#'численность2', 'численность3', 'численность4', 'численность5']
#select = '''SELECT `Лидеры`, `Тип`, `Лидеры.1`, `Устойчивыелидеры`, `Лидерыизлидеров`, `численность1`,
#`численность2`, `численность3`, `численность4`, `численность5` FROM `atat`;'''
columns = ['Лидеры', 'Тип', 'Лидеры.1', 'Устойчивыелидеры', 'Лидерыизлидеров', 'численность2темп', 'численность3темп', 'численность4темп', 'численность5темп']
select = '''SELECT `Лидеры`, `Тип`, `Лидеры.1`, `Устойчивыелидеры`, `Лидерыизлидеров`, `численность2темп`, `численность3темп`, `численность4темп`, `численность5темп` FROM `atat`;'''
#with engine.connect() as cursor:
cursor.execute(select)
result_temp = pd.DataFrame(cursor.fetchall(), columns = columns)
slicer = ['0 - 5', '51 - 100', '101 - 150', '251 - 500', '201 - 250', '1 001 - 5 000']

def Agplomeration(slicer, liders_type, liders, data_graph, pok):
    if pok == 'численность':
        data_local = pd.DataFrame([[liders_type, liders_type, liders_type, liders_type, liders_type, pok],
                [liders[~liders[pok + '1'].isin(slicer)]['численность1'].astype(float).median(),
                liders[~liders[pok + '2'].isin(slicer)]['численность2'].astype(float).median(),
                liders[~liders[pok + '3'].isin(slicer)]['численность3'].astype(float).median(),
                liders[~liders[pok + '4'].isin(slicer)]['численность4'].astype(float).median(),
                liders[~liders[pok + '5'].isin(slicer)]['численность5'].astype(float).median()],
                ['1 год жизни', '2 год жизни', '3 год жизни', '4 год жизни', '5 год жизни']]).transpose()
        data_local.columns = ['Тип организаций', 'Медиана', 'Год жизни']
    if pok == 'темп':
        data_local = pd.DataFrame([[liders_type, liders_type, liders_type, liders_type],
                [liders[~liders['численность2темп'].isin(slicer)]['численность2темп'].astype(float).median(),
                liders[~liders['численность3темп'].isin(slicer)]['численность3темп'].astype(float).median(),
                liders[~liders['численность4темп'].isin(slicer)]['численность4темп'].astype(float).median(),
                liders[~liders['численность5темп'].isin(slicer)]['численность5темп'].astype(float).median()],
                ['2 год жизни', '3 год жизни', '4 год жизни', '5 год жизни']]).transpose()
        data_local.columns = ['Тип организаций', 'Медиана','Год жизни']
    if len(data_graph) == 0:
        data_graph = data_local
    else:
        data_graph = pd.concat([data_graph, data_local])
    return data_graph
pok = 'численность'
pok1 = 'темп'
data_graph = []
data_graph_temp = []
liders_type = 'Лидеры'
liders = result[result[liders_type]=='да']
liders1 = result_temp[result_temp[liders_type]=='да']
data_graph = Agplomeration(slicer, liders_type, liders, data_graph, pok)
data_graph_temp = Agplomeration(slicer, liders_type, liders1, data_graph_temp, pok1)

liders_type = 'Лидеры из лидеров'
liders = result[result['Лидерыизлидеров']=='да']
liders1 = result_temp[result_temp['Лидерыизлидеров']=='да']
data_graph = Agplomeration(slicer, liders_type, liders, data_graph, pok)
data_graph_temp = Agplomeration(slicer, liders_type, liders1, data_graph_temp, pok1)

liders_type = 'Устойчивые лидеры'
liders = result[result['Устойчивыелидеры']=='да']
liders1 = result_temp[result_temp['Устойчивыелидеры']=='да']
data_graph = Agplomeration(slicer, liders_type, liders, data_graph, pok)
data_graph_temp = Agplomeration(slicer, liders_type, liders1, data_graph_temp, pok1)

liders_type = 'Не лидеры'
liders = result[result['Лидеры']!='да']
#liders1 = result_temp[result_temp['Лидеры']!='да']
data_graph = Agplomeration(slicer, liders_type, liders, data_graph, pok)
#data_graph_temp = Agplomeration(slicer, liders_type, liders1, data_graph_temp, pok1)

liders_type = 'Все МСП'
liders = result
#liders1 = result_temp
data_graph = Agplomeration(slicer, liders_type, liders, data_graph, pok)
#data_graph_temp = Agplomeration(slicer, liders_type, liders1, data_graph_temp, pok1)
#pylint: disable=too-many-arguments, unused-argument, unused-variable
import plotly.express as px

# Incorporate data
df = data_graph
df1 = data_graph_temp
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
# App layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'height': '1080px;'}, children=[
    html.Div(style={'display': 'flex','height': '1080px;'}, children=[
            dcc.Dropdown(options=['Лидеры', 'Лидеры из лидеров', 'Устойчивые лидеры', 'Не лидеры', 'Все МСП'],
                        value=['Лидеры', 'Лидеры из лидеров', 'Все МСП'],
                        multi=True,
                        id='Dropdown',
                        style={'width': '50%', 'flex': '1'}),
            dcc.Dropdown(options=['1 год жизни', '2 год жизни', '3 год жизни', '4 год жизни', '5 год жизни'],
                            value= ['2 год жизни','3 год жизни', '4 год жизни', '5 год жизни'],
                            multi=True,
                            id='myradiofinal',
                            style={'width': '50%', 'flex': '1'})]),
    html.Div(style={'display': 'flex'}, children=
    [
        html.Div(dcc.Graph(figure={}, id='histofinal'), style={'width': '50%', 'flex': '1'}),
        html.Div(dcc.Graph(figure={}, id='chartfinal'), style={'width': '50%', 'flex': '1'})
    ])
])

# Add controls to build the interaction
@app.callback(
    dash.dependencies.Output(component_id='chartfinal', component_property='figure'),
    dash.dependencies.Input(component_id='myradiofinal', component_property='value'),
    dash.dependencies.Input(component_id='Dropdown', component_property='value')
)
def update_graph1(myradiofinal, Dropdown):
    datas2 = df1[df1['Год жизни'].isin(myradiofinal)]
    #datas2 = datas2[datas2['Тип организаций'].isin(Dropdown)]
    fig = px.bar(datas2, x='Год жизни', y="Медиана", barmode='group', color='Тип организаций', title = 'Темп прироста среднесписочной численности, %')
    return fig

@app.callback(
    dash.dependencies.Output(component_id='histofinal', component_property='figure'),
    dash.dependencies.Input(component_id='Dropdown', component_property='value')
)
def update_graph2(Dropdown):
    datas2 = data_graph[data_graph['Тип организаций'].isin(Dropdown)]
    fig = px.line(datas2, x="Год жизни", y="Медиана", color="Тип организаций", title = 'Динамика медианы среднесписочной численности <br> работников в первые 5 лет жизни предприятий, чел.')
    return fig

a2 = DjangoDash("Ex2",
                serve_locally=True)

a2.layout = html.Div([
    dcc.RadioItems(id="dropdown-one",
                   options=[{'label':i, 'value':j} for i, j in [("O2", "Oxygen"),
                                                                ("N2", "Nitrogen"),
                                                                ("CO2", "Carbon Dioxide")]],
                   value="Oxygen"),
    html.Div(id="output-one")
    ])

@a2.expanded_callback(
    dash.dependencies.Output('output-one', 'children'),
    [dash.dependencies.Input('dropdown-one', 'value')]
    )
def callback_c(*args, **kwargs):
    'Update the output following a change of the input selection'
    #da = kwargs['dash_app']

    session_state = kwargs['session_state']

    calls_so_far = session_state.get('calls_so_far', 0)
    session_state['calls_so_far'] = calls_so_far + 1

    user_counts = session_state.get('user_counts', None)
    user_name = str(kwargs['user'])
    if user_counts is None:
        user_counts = {user_name:1}
        session_state['user_counts'] = user_counts
    else:
        user_counts[user_name] = user_counts.get(user_name, 0) + 1

    return "Args are [%s] and kwargs are %s" %(",".join(args), str(kwargs))

liveIn = DjangoDash("LiveInput",
                    serve_locally=True,
                    add_bootstrap_links=True)

liveIn.layout = html.Div([
    html.Div([html.Button('Choose red. Press me!',
                          id="red-button",
                          className="btn btn-danger"),
              html.Button('Blue is best. Pick me!',
                          id="blue-button",
                          className="btn btn-primary"),
              html.Button('Time to go green!',
                          id="green-button",
                          className="btn btn-success"),
             ], className="btn-group"),
    html.Div(id='button_local_counter', children="Press any button to start"),
    ], className="")

#pylint: disable=too-many-arguments
@liveIn.expanded_callback(
    dash.dependencies.Output('button_local_counter', 'children'),
    [dash.dependencies.Input('red-button', 'n_clicks'),
     dash.dependencies.Input('blue-button', 'n_clicks'),
     dash.dependencies.Input('green-button', 'n_clicks'),
     dash.dependencies.Input('red-button', 'n_clicks_timestamp'),
     dash.dependencies.Input('blue-button', 'n_clicks_timestamp'),
     dash.dependencies.Input('green-button', 'n_clicks_timestamp'),
    ],
    )
def callback_liveIn_button_press(red_clicks, blue_clicks, green_clicks,
                                 rc_timestamp, bc_timestamp, gc_timestamp, **kwargs): # pylint: disable=unused-argument
    'Input app button pressed, so do something interesting'

    if not rc_timestamp:
        rc_timestamp = 0
    if not bc_timestamp:
        bc_timestamp = 0
    if not gc_timestamp:
        gc_timestamp = 0

    if (rc_timestamp + bc_timestamp + gc_timestamp) < 1:
        change_col = None
        timestamp = 0
    else:
        if rc_timestamp > bc_timestamp:
            change_col = "red"
            timestamp = rc_timestamp
        else:
            change_col = "blue"
            timestamp = bc_timestamp

        if gc_timestamp > timestamp:
            timestamp = gc_timestamp
            change_col = "green"

        value = {'red_clicks':red_clicks,
                 'blue_clicks':blue_clicks,
                 'green_clicks':green_clicks,
                 'click_colour':change_col,
                 'click_timestamp':timestamp,
                 'user':str(kwargs.get('user', 'UNKNOWN'))}

        send_to_pipe_channel(channel_name="live_button_counter",
                             label="named_counts",
                             value=value)
    return "Number of local clicks so far is %s red and %s blue; last change is %s at %s" % (red_clicks,
                                                                                             blue_clicks,
                                                                                             change_col,
                                                                                             datetime.fromtimestamp(0.001*timestamp))

liveOut = DjangoDash("LiveOutput")

def _get_cache_key(state_uid):
    return "demo-liveout-s6-%s" % state_uid

def generate_liveOut_layout():
    'Generate the layout per-app, generating each tine a new uuid for the state_uid argument'
    return html.Div([
        dpd.Pipe(id="named_count_pipe",
                 value=None,
                 label="named_counts",
                 channel_name="live_button_counter"),
        html.Div(id="internal_state",
                 children="No state has been computed yet",
                 style={'display':'none'}),
        dcc.Graph(id="timeseries_plot"),
        dcc.Input(value=str(uuid.uuid4()),
                  id="state_uid",
                  style={'display':'none'},
                 )
        ])

liveOut.layout = generate_liveOut_layout

#pylint: disable=unused-argument
#@liveOut.expanded_callback(
@liveOut.callback(
    dash.dependencies.Output('internal_state', 'children'),
    [dash.dependencies.Input('named_count_pipe', 'value'),
     dash.dependencies.Input('state_uid', 'value'),],
    )
def callback_liveOut_pipe_in(named_count, state_uid, **kwargs):
    'Handle something changing the value of the input pipe or the associated state uid'

    cache_key = _get_cache_key(state_uid)
    state = cache.get(cache_key)

    # If nothing in cache, prepopulate
    if not state:
        state = {}

    # Guard against missing input on startup
    if not named_count:
        named_count = {}

    # extract incoming info from the message and update the internal state
    user = named_count.get('user', None)
    click_colour = named_count.get('click_colour', None)
    click_timestamp = named_count.get('click_timestamp', 0)

    if click_colour:
        colour_set = state.get(click_colour, None)

        if not colour_set:
            colour_set = [(None, 0, 100) for i in range(5)]

        _, last_ts, prev = colour_set[-1]

        # Loop over all existing timestamps and find the latest one
        if not click_timestamp or click_timestamp < 1:
            click_timestamp = 0

            for _, the_colour_set in state.items():
                _, lts, _ = the_colour_set[-1]
                if lts > click_timestamp:
                    click_timestamp = lts

            click_timestamp = click_timestamp + 1000

        if click_timestamp > last_ts:
            colour_set.append((user, click_timestamp, prev * random.lognormvariate(0.0, 0.1)),)
            colour_set = colour_set[-100:]

        state[click_colour] = colour_set
        cache.set(cache_key, state, 3600)

    return "(%s,%s)" % (cache_key, click_timestamp)

@liveOut.callback(
    dash.dependencies.Output('timeseries_plot', 'figure'),
    [dash.dependencies.Input('internal_state', 'children'),
     dash.dependencies.Input('state_uid', 'value'),],
    )
def callback_show_timeseries(internal_state_string, state_uid, **kwargs):
    'Build a timeseries from the internal state'

    cache_key = _get_cache_key(state_uid)
    state = cache.get(cache_key)

    # If nothing in cache, prepopulate
    if not state:
        state = {}

    colour_series = {}

    colors = {'red':'#FF0000',
              'blue':'#0000FF',
              'green':'#00FF00',
              'yellow': '#FFFF00',
              'cyan': '#00FFFF',
              'magenta': '#FF00FF',
              'black' : '#000000',
             }

    for colour, values in state.items():
        timestamps = [datetime.fromtimestamp(int(0.001*ts)) for _, ts, _ in values if ts > 0]
        #users = [user for user, ts, _ in values if ts > 0]
        levels = [level for _, ts, level in values if ts > 0]
        if colour in colors:
            colour_series[colour] = pd.Series(levels, index=timestamps).groupby(level=0).first()

    df = pd.DataFrame(colour_series).fillna(method="ffill").reset_index()[-25:]

    traces = [go.Scatter(y=df[colour],
                         x=df['index'],
                         name=colour,
                         line=dict(color=colors.get(colour, '#000000')),
                        ) for colour in colour_series]

    return {'data':traces,
            #'layout': go.Layout
           }

localState = DjangoDash("LocalState",
                        serve_locally=True)

localState.layout = html.Div([html.Img(src=localState.get_asset_url('image_one.png')),
                              html.Img(src='assets/image_two.png'),
                              ])

multiple_callbacks = DjangoDash("MultipleCallbackValues")

multiple_callbacks.layout = html.Div([
    html.Button("Press Me",
                id="button"),
    dcc.RadioItems(id='dropdown-color',
                   options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
                   value='red'
                   ),
    html.Div(id="output-one"),
    html.Div(id="output-two"),
    html.Div(id="output-three")
    ])

@multiple_callbacks.callback(
    [dash.dependencies.Output('output-one', 'children'),
     dash.dependencies.Output('output-two', 'children'),
     dash.dependencies.Output('output-three', 'children')
     ],
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('dropdown-color', 'value'),
     ])
def multiple_callbacks_one(button_clicks, color_choice):
    return ("Output 1: %s %s %s" % (button_clicks, color_choice, dash.callback_context.triggered),
            "Output 2: %s %s" % (color_choice, button_clicks),
            "Output 3: %s %s" % (button_clicks, color_choice),
            )


multiple_callbacks = DjangoDash("MultipleCallbackValuesExpanded")

multiple_callbacks.layout = html.Div([
    html.Button("Press Me",
                id="button"),
    dcc.RadioItems(id='dropdown-color',
                   options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
                   value='red'
                   ),
    html.Div(id="output-one"),
    html.Div(id="output-two"),
    html.Div(id="output-three")
    ])

@multiple_callbacks.expanded_callback(
    [dash.dependencies.Output('output-one', 'children'),
     dash.dependencies.Output('output-two', 'children'),
     dash.dependencies.Output('output-three', 'children')
     ],
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('dropdown-color', 'value'),
     ])
def multiple_callbacks_two(button_clicks, color_choice, **kwargs):
    if color_choice == 'green':
        raise PreventUpdate
    return ["Output 1: %s %s %s" % (button_clicks, color_choice, dash.callback_context.triggered),
            "Output 2: %s %s %s" % (button_clicks, color_choice, kwargs['callback_context'].triggered),
            "Output 3: %s %s [%s]" % (button_clicks, color_choice, kwargs)
            ]



external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
external_scripts_stylesheets = DjangoDash("ExternalScriptStylesheets",
                                          external_stylesheets=external_stylesheets,
                                          external_scripts=external_scripts)

external_scripts_stylesheets.layout = html.Div()

flexible_expanded_callbacks = DjangoDash("FlexibleExpandedCallbacks")

flexible_expanded_callbacks.layout = html.Div([
    html.Button("Press Me",
                id="button"),
    dcc.RadioItems(id='dropdown-color',
                   options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
                   value='red'
                   ),
    html.Div(id="output-one"),
    html.Div(id="output-two"),
    html.Div(id="output-three")
    ])

@flexible_expanded_callbacks.expanded_callback(
    dash.dependencies.Output('output-one', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def exp_callback_kwargs(button_clicks, **kwargs):
    return str(kwargs)


@flexible_expanded_callbacks.expanded_callback(
    dash.dependencies.Output('output-two', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def exp_callback_standard(button_clicks):
    return "ok"

@flexible_expanded_callbacks.expanded_callback(
    dash.dependencies.Output('output-three', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def exp_callback_dash_app_id(button_clicks, dash_app_id):
    return dash_app_id


pattern_state_callbacks = DjangoDash("PatternStateCallbacks")

pattern_state_callbacks.layout = html.Div([
    html.Div(id={"_id": "output-one", "_type": "divo"}),
    html.Div(id={"_id": "output-two", "_type": "div"}),
    html.Div(id={"_id": "output-three", "_type": "div"})
])


@pattern_state_callbacks.callback(
    dash.dependencies.Output({"_type": "div", "_id": MATCH}, 'children'),
    [dash.dependencies.Input({"_type": "div", "_id": MATCH}, 'n_clicks')])
def pattern_match(values):
    return str(values)


@pattern_state_callbacks.callback(
    dash.dependencies.Output({"_type": "divo", "_id": "output-one"}, 'children'),
    [dash.dependencies.Input({"_type": "div", "_id": ALL}, 'children')])
def pattern_all(values):
    return str(values)


