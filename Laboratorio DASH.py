import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pandas as pd
import dash_daq as daq


app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor':'lavender'},
    children=
    [   html.H1(
            children='Laboratorio GMG 2020',
            style={'textAlign': 'center','fontFamily':'Calibri Light','margin-bottom':-10}
        ),
        html.H2(
            children='Panel de visualización de sensores',
            style={'textAlign': 'center','fontFamily':'Calibri Light','margin-bottom':0}
        ),
        html.H3(children='Control para la actualización',style={'textAlign': 'left','fontFamily':'Calibri Light','margin-bottom':0}),
        html.Button('Detener', id='detener', n_clicks=0,style={'margin-left':50,'margin-top':10}),
        html.Button('Iniciar', id='iniciar', n_clicks=0,style={'margin-top':10}),
        html.H3(children='Gráfica de Masa vs Tiempo',style={'textAlign':'center','fontFamily':'Calibri Light'}),
        dcc.Graph(id='graf 1', animate=False, style={'margin-bottom':100}),
        dcc.Interval(
            id='detonador',
            interval=200,
            n_intervals = 0
        ),
        daq.LEDDisplay(
            id='medidorhumedad',
            label="Humedad",
            backgroundColor='mediumblue',
            color='azure',
            style={'margin-bottom':-200,'margin-left':400,'fontFamily':'Calibri Light','fontSize':20},
            labelPosition='bottom'
            ),
        daq.Gauge(id='medidoraguja',
            min=0,
            max=40,
            showCurrentValue=True,
            label=' ',
            style={'margin-right':400},
            units='°C',
            color={'gradient':True,"ranges":{"blue":[0,30],"red":[30,40]
            }}),
        dcc.Graph(id='zoom', animate=False, style={'margin-bottom':100}
        ),
        daq.NumericInput(id='numeric',
            label='Escala de tiempo',
            min=0,
            max=60,
            value=20,
            style={'margin-top':-100,'fontFamily':'Calibri Light','fontSize':20}
        ) 
    ])

##### Medidor de humedad
@app.callback(Output('medidorhumedad','value'),
        [Input('detonador', 'n_intervals')])

def marc_humedad(n):
    df = pd.read_csv('prueba.dat',delimiter='	',encoding='utf_16',header=None,names=['tiempo','temperatura','humedad','masa'])
    H = df.iloc[-1,2]

    return int(H)

##### medidor de temperatura con aguja
@app.callback(Output('medidoraguja','value'),
        [Input('detonador', 'n_intervals')])

def update_graph_scatter(n):
    df = pd.read_csv('prueba.dat',delimiter='	',encoding='utf_16',header=None,names=['tiempo','temperatura','humedad','masa'])
    T = df.iloc[-1,1]

    return int(T)

##### Callback para actualizar la gráfica
@app.callback(Output('graf 1', 'figure'),
        [Input('detonador', 'n_intervals')])

def update_graph_scatter(n):
    df = pd.read_csv('prueba.dat',delimiter='	',encoding='utf_16',header=None,names=['tiempo','temperatura','humedad','masa'])
    X = df['tiempo']
    Y = df['masa']
    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [data],'layout' : go.Layout(xaxis={'title': 'Tiempo'},
                                                yaxis={'title': 'Masa'},
                                                height=500,
                                                plot_bgcolor='white',
                                                paper_bgcolor='lavender',
                                                font_color='black',
                                                )}

##### callback para pausar e iniciar la actualización
@app.callback(
    Output('detonador','max_intervals'),
    [Input('detener', 'n_clicks'),
    Input('iniciar', 'n_clicks')
    ])

def stop_interval(btn1,btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'iniciar' in changed_id:
        max_intervals = -1
    elif 'detener' in changed_id:
        max_intervals = 0
    else:
        max_intervals = 0
    return (max_intervals)

##### Callback para actualizar la gráfica Con ZOOM
@app.callback(Output('zoom', 'figure'),
        [Input('detonador', 'n_intervals'),Input('numeric','value')])

def update_graph_scatter(n,value):
    df = pd.read_csv('prueba.dat',delimiter='	',encoding='utf_16',header=None,names=['tiempo','temperatura','humedad','masa'])
    X = df['tiempo']
    Y = df['masa']
    Z = df.iloc[-1,0]
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines'
            )

    return {'data': [data],'layout' : go.Layout(xaxis={'title': 'Tiempo','range':[float(Z)-int(value),float(Z)]},
                                                yaxis={'title': 'masa'},
                                                title={'text':'Gráfica ampliada','xanchor':'center','font.size':20,'font.family':"arial"},
                                                height=500,
                                                plot_bgcolor='white',
                                                paper_bgcolor='lavender',
                                                font_color='black',
                                                )}

if __name__ == '__main__':
    app.run_server(debug=True)