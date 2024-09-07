# Import required libraries
import streamlit as st
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os
os.chdir("C:\\Users\\Mario Torres\\Desktop\\Data_Science\\7.-Modelamiento_Data_Science")
import pandas as pd

# FASE 1: CARGA DE DATOS (dataframe df_ventas --> Pestaña "Detalle" / dataframe df_ventas_acum --> Pestaña "Acumulado")
df_ventas = pd.read_csv('Data//Corrosion.csv',delimiter = " ")
# Helper function to extract numeric values from the factor outputs
def extract_numeric_value(output):
    # Check if output is None or not a string
    if output is None or not isinstance(output, str):
        return None
    try:
        # Now we are sure output is a string, we can attempt to extract the number
        return int(output.split(': ')[-1])
    except (ValueError, IndexError):
        # If conversion to int fails or the string is not in the expected format
        return None
def assign_pof(total):
    if total <= 15:
        return 1
    elif 16 <= total <= 25:
        return 2
    elif 26 <= total <= 35:
        return 3
    elif 36 <= total <= 50:
        return 4
    elif total > 75:
        return 5
    else:
        return 'Value out of range'  # Adjust as necessary for other ranges
def extract1_numeric_value(output):
    # Check if output is None or not a string
    if output is None or not isinstance(output, str):
        return None
    try:
        # Now we are sure output is a string, we can attempt to extract the number
        return float(output.split(': ')[-1])
    except (ValueError, IndexError):
        # If conversion to int fails or the string is not in the expected format
        return None
def assign_cof(total):
    if total < 10:
        return 'A'
    elif 10 <= total <= 19:
        return 'B'
    elif 20 <= total <= 29:
        return 'C'
    elif 30 <= total <= 39:
        return 'D'
    elif total > 40:
        return 'E'
    else:
        return 'Value out of range'  # Adjust as necessary for other ranges
    
data_EF = {
    'Number': ['<20', '20≤ components <150', '≥150'],
    'Value': [0, 5, 15],
}
df_EF = pd.DataFrame(data_EF)

data_DF = {
    'Damage': ['Thinning', 'Cracking', 'Localized Corrosion'],
    'Value': [2, 5, 3],
}
df_DF = pd.DataFrame(data_DF)



data_IF = {
    'Piping Inspection Quality': ['Extensive', 'Visual and UT', 'No Inspection Plan'],
    'Total Asset Inspection Quality': ['All components', 'Individual components', 'No Inspection Plan'],
    'IF1': [-5, -2, 0],
    'IF2': [-5, -2, 0],
}
df_IF = pd.DataFrame(data_IF)


data_CCF = {
    'Housekeeping': ['Better than Industry Standards', 'About Industry Standards', 'Lower than Industry Standards'],
    'CCF1': [0, 2, 5],
    'Design and Construction': ['Better than Industry Standards', 'About Industry Standards', 'Lower than Industry Standards'],
    'CCF2': [0, 2, 5],
    'Predictive Maintenance, QA/QC, Fabrication': ['Better than Industry Standards', 'About Industry Standards', 'Lower than Industry Standards'],
    'CCF3': [0, 2, 5],
}
df_CCF = pd.DataFrame(data_CCF)

data_PF = {
    'Number of interruptions': ['0 - 1', '2 - 4', '5 - 8', '9 - 12', 'more than 12'],
    'PF1': [0, 1, 3, 4, 5],
    'Exceeding Key Process Variables': ['Process is Stable', 'Unusual Circumstances', 
                                         'If upset conditions can accelerate equipment damage', 
                                         'Inherent loss of the control', ''],
    'PF2': [0, 1, 3, 5, None],  # The last option does not have a corresponding PF2
    'Protection Devices': ['No plugging', 'Slight Fouling or Plugging', 'Significant Fouling or Plugging', 
                           'Protective devices impaired', ''],
    'PF3': [0, 1, 3, 5, None],  # The last option does not have a corresponding PF3
}
df_PF = pd.DataFrame(data_PF)
data_MDF = {
    'Equipment Design': ['Meets current codes', 'Code-compliant at construction', 'Non-code equipment'],
    'MDF1': [0, 2, 5],
    'Process Conditions': ['Normal', 'Extreme', ''],  # Assuming there's an empty option for the third one
    'MDF2': [0, 5, None]  # Assuming there's no value for the third option in MDF2
}
df_MDF = pd.DataFrame(data_MDF)

data_TQF = {
    'Material Released': ['<1000 pounds', '1K - 10K pounds', '10K - 100K pounds', '>1 million pounds'],
    'Toxicity Factor': ['1', '2', '3', '4'],
    'TQF1': [15, 20, 27, 35],
    'TQF2': [-20, -10, 0, 20],
}
df_TQF = pd.DataFrame(data_TQF)

data_DIF = {
    'Boiling Point': ['<30', '30 - 80', '80 - 140', '140 - 200', '200 - 300', '>300'],
    'Value': [1, 0.5 , 0.3, 0.1, 0.05, 0.03],
}
df_DIF = pd.DataFrame(data_DIF)

data_CRF = {
    'Leak Detectors': ['Detect 50% or more of incipient leaks', 'No Detectors', '', ''],
    'CRF1': [-1, 0, None, None],
    'Isolation': ['Automatic with Detector Reading', 'Remote Isolation with Manual Activation', 'Manual Isolation with Manual Activation', 'No Isolation System'],
    'CRF2': [-1, -5, -25, 0],
    'Mitigation': ['Mitigate at least 90%', 'No Mitigation System', '', ''],
    'CRF3': [-5, 0, None, None],
}
df_CRF = pd.DataFrame(data_CRF)

data_PPF = {
    'Number of People': ['<10', '10 - 100', '100 - 1000', '1000-10000'],
    'Value': [0, 7, 15, 20],
}
df_PPF = pd.DataFrame(data_PPF)

# Initialize the app
app = dash.Dash(__name__)
mapbox_access_token = "pk.eyJ1IjoicmVzdGV2ZXM5OSIsImEiOiJja2hjcG5tOGUwMzJpMnh0OW4wa2s0a3N2In0.6N59idkWgjoWYkQoeYIO8Q"

# DEFINIR FIGURA ESTÁTICA PARA VENTAS GEOGRÁFICAS
#fig_mapa = go.Figure(go.Scattermapbox(
#        lon = df_ventas_acum['Longitud'],
#        lat = df_ventas_acum['Latitud'],
 #       mode='markers',
  #      text= df_ventas_acum['Suma Ingresos'],
   #     marker=go.scattermapbox.Marker(
    #        size=df_ventas_acum['Suma Ingresos']/50000,
#            color=df_ventas_acum['Suma Ingresos']/50000
#        )
 #   ))

#fig_mapa.update_layout(
 #   autosize=True,
 #   hovermode='closest',
 #   mapbox=dict(
 #       accesstoken=mapbox_access_token,
 #       bearing=0,
  #      center=dict(
  #          lat=40.41,
#            lon=-3.7
#        ),
#        pitch=0,
#        zoom=2
#    ),
#)#


app.config.suppress_callback_exceptions = True

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Pipeline Integrity', href='/'),
        html.Br(),
        dcc.Link('Prediccion', href='/prediccion'),
    ], className="row"),
    html.Div(id='page-content')
])

# Index page
colors = {
    'text': '#007bff',  # You can change the color code to whatever you like
    'background': ''  # Background color for the content area
}

index_page = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '0 20px'}, children=[
        html.Div([
                html.Img(src=app.get_asset_url('KIT.jpg'), style={'height': '100px'})
            ], style={'flex': '1', 'padding': '0 20px', 'display': 'flex', 'justifyContent': 'left'}),
             html.Div([
                html.H1(children='Pipeline Integrity', style={
                    'textAlign': 'center',
                    'color': colors['text']
                }),
                html.H2(children='Total Risk', style={
                    'textAlign': 'center',
                    'color': colors['text']
                })
            ], style={'flex': '1', 'padding': '0 20px', 'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'center'}),
        
              html.Div([
                html.Img(src=app.get_asset_url('VULCAN.jpg'), style={'height': '100px'})
            ], style={'flex': '1', 'padding': '0 20px', 'display': 'flex', 'justifyContent': 'right'}),
        ]),
 
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        html.Div(style={'width': '50%'}, children=[
            html.H3('Probability of Failure (PoF)', style={'textAlign': 'center', 'color': colors['text']}),  # Title for the left half
            # Equipment Factor
     
       html.Div([html.H3('1.-Equipment Factor'),
        dcc.Dropdown(
            id='number-dropdown',
            options=[{'label': label, 'value': value} for label, value in zip(df_EF['Number'], df_EF['Value'])],
            multi=False,
            placeholder="Select Number of Components"
        ),
        html.Button('Calculate EF', id='calculate-ef', n_clicks=0),
        html.Div(id='ef-output', children='Select number of components and calculate EF')
    ], style={'width': '33%', 'float': 'left', 'display': 'inline-block'}), 
    
    html.Div([html.H3('2.-Damage Factor'),
    dcc.Dropdown(
        id='damage-dropdown',
        options=[{'label': damage, 'value': value} for damage, value in zip(df_DF['Damage'], df_DF['Value'])],
        multi=True,
        placeholder="Select damage types"
    ),
    html.Button('Calculate DF', id='calculate-df', n_clicks=0),  
    html.Div(id='df-output', children='Select damages and calculate DF')
    ], style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),        
   
    html.Div([html.H3('3.-Inspection IF'),
        dcc.Dropdown(
            id='if1-dropdown',
            options=[{'label': f"{row['Piping Inspection Quality']} ", 'value': row['IF1']} 
                     for index, row in df_IF.iterrows()],
            placeholder="Select Piping Inspection Quality"
        ),
        dcc.Dropdown(
            id='if2-dropdown',
            options=[{'label': f"{row['Total Asset Inspection Quality']} ", 'value': row['IF2']} 
                     for index, row in df_IF.iterrows()],
            placeholder="Select Total Asset Inspection Quality"
        ),
        html.Button('Calculate IF', id='calculate-if', n_clicks=0),
        html.Div(id='if-output', children='Select inspection factors and calculate IF')
    ], style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
    
   
   
    
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}, children=[
    html.Div([html.H3('4.-Condition Factor (CCF)'),
    dcc.Dropdown(
        id='ccf1-dropdown',
        options=[{'label': row['Housekeeping'], 'value': row['CCF1']} 
                 for index, row in df_CCF.iterrows()],
        placeholder="Select Housekeeping Standard"
    ),
    dcc.Dropdown(
        id='ccf2-dropdown',
        options=[{'label': row['Design and Construction'], 'value': row['CCF2']} 
                 for index, row in df_CCF.iterrows()],
        placeholder="Select Design and Construction Standard"
    ),
    dcc.Dropdown(
        id='ccf3-dropdown',
        options=[{'label': row['Predictive Maintenance, QA/QC, Fabrication'], 'value': row['CCF3']} 
                 for index, row in df_CCF.iterrows()],
        placeholder="Select Predictive Maintenance Standard"
    ), 
    html.Button('Calculate CCF', id='calculate-ccf', n_clicks=0),  # Button to trigger the calculation
    html.Div(id='ccf-output')  # Placeholder where the result will be displayed
], style={'flex': '1', 'alignItems': 'flex-start'}),
    
    
    html.Div([html.H3('5.-Process Factor (PF)'),
    dcc.Dropdown(
        id='pf1-dropdown',
        options=[{'label': ni, 'value': pf1} for ni, pf1 in zip(data_PF['Number of interruptions'], data_PF['PF1'])],
        placeholder="Select Number of Interruptions"
    ),
    dcc.Dropdown(
        id='pf2-dropdown',
        options=[{'label': ekpv, 'value': pf2} for ekpv, pf2 in zip(data_PF['Exceeding Key Process Variables'], data_PF['PF2']) if pf2 is not None],
        placeholder="Select Exceeding Key Process Variables"
    ),
    dcc.Dropdown(
        id='pf3-dropdown',
        options=[{'label': pd, 'value': pf3} for pd, pf3 in zip(data_PF['Protection Devices'], data_PF['PF3']) if pf3 is not None],
        placeholder="Select Protection Devices"
    ),
    html.Button('Calculate PF', id='calculate-pf', n_clicks=0),
    html.Div(id='pf-output'
    )]
, style={'flex': '1', 'alignItems': 'center'}),
        html.Div([
        html.H3('6.-Mechanical Design Factor (MDF)'),
        dcc.Dropdown(
            id='mdf1-dropdown',
            options=[{'label': ed, 'value': mdf1} for ed, mdf1 in zip(data_MDF['Equipment Design'], data_MDF['MDF1'])],
            placeholder="Select Equipment Design"
        ),
        dcc.Dropdown(
            id='mdf2-dropdown',
            options=[{'label': pc, 'value': mdf2} for pc, mdf2 in zip(data_MDF['Process Conditions'], data_MDF['MDF2']) if mdf2 is not None],
            placeholder="Select Process Conditions"
        ),
        html.Button('Calculate MDF', id='calculate-mdf', n_clicks=0),
        html.Div(id='mdf-output')
    ], style={'flex': '1',  'alignItems': 'flex-end'})
        ]),
    
    html.Div([
    html.Button('Calculate PoF', id='calculate-pof', n_clicks=0),
    
    # Add a div to display the Probability of Failure
    html.Div(id='pof-output', children='The calculated Probability of Failure (PoF) will be shown here after calculation.')                
 # ... rest of your layout for index page
], style={'width': '100%', 'marginTop': '20px', 'textAlign': 'center'})
       
    ]),

         
html.Div(style={'width': '48%', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
           
    html.H3('Consequence of Failure (CoF)', style={'textAlign': 'center', 'color': colors['text']}),  # Title for the left half
       html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        
        html.Div([
            
            html.H3('1.-Toxic Quantity Factor TQF'),
            dcc.Dropdown(
                id='tqf1-dropdown',
                options=[{'label': f"{row['Material Released']} ", 'value': row['TQF1']} 
                         for index, row in df_TQF.iterrows()],
                placeholder="Select Material Released [pounds]"
            ),
            dcc.Dropdown(
                id='tqf2-dropdown',
                options=[{'label': f"{row['Toxicity Factor']} ", 'value': row['TQF2']} 
                         for index, row in df_TQF.iterrows()],
                placeholder="Select Toxicity Factor"
            ),
            html.Button('Calculate TQF', id='calculate-tqf', n_clicks=0),
            html.Div(id='tqf-output', children='Select inspection factors and calculate TQF')
        ], style={'flex': '1', 'alignItems': 'flex-start'}),
        
        html.Div([html.H3('2.-Dispersibility Factor (DIF)'),
         dcc.Dropdown(
             id='dif-dropdown',
             options=[{'label': label, 'value': value} for label, value in zip(df_DIF['Boiling Point'], df_DIF['Value'])],
             multi=False,
             placeholder="Select Boiling Point"
         ),
         html.Button('Calculate DIF', id='calculate-dif', n_clicks=0),
         html.Div(id='dif-output', children='Select Boiling Point and calculate DIF')
     ], style={'flex': '1', 'alignItems': 'flex-end'}),
        ]),
        
        
        html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        html.Div([html.H3('3.-Credit Factor (CRF)'),
        dcc.Dropdown(
            id='crf1-dropdown',
            options=[{'label': row['Leak Detectors'], 'value': row['CRF1']} 
                     for index, row in df_CRF.iterrows()],
            placeholder="Select Detection System"
        ),
        dcc.Dropdown(
            id='crf2-dropdown',
            options=[{'label': row['Isolation'], 'value': row['CRF2']} 
                     for index, row in df_CRF.iterrows()],
            placeholder="Select Isolation System"
        ),
        dcc.Dropdown(
            id='crf3-dropdown',
            options=[{'label': row['Mitigation'], 'value': row['CRF3']} 
                     for index, row in df_CRF.iterrows()],
            placeholder="Select Mitigation"
        ), 
        html.Button('Calculate CRF', id='calculate-crf', n_clicks=0),  # Button to trigger the calculation
        html.Div(id='crf-output')  # Placeholder where the result will be displayed
    ], style={'flex': '1', 'alignItems': 'flex-start'}),
        
        html.Div([html.H3('4.-Population Factor  PPF'),
         dcc.Dropdown(
             id='people-dropdown',
             options=[{'label': label, 'value': value} for label, value in zip(df_PPF['Number of People'], df_PPF['Value'])],
             multi=False,
             placeholder="Select Number of People"
         ),
         html.Button('Calculate PPF', id='calculate-ppf', n_clicks=0),
         html.Div(id='ppf-output', children='Select number of people and calculate PPF')
     ], style={'flex': '1',  'alignItems': 'flex-end'})
         ]), 
        
         
    html.Div([
    html.Button('Calculate CoF', id='calculate-cof', n_clicks=0),
    
    # Add a div to display the Probability of Failure
    html.Div(id='cof-output', children='The calculated Consequence of Failure (CoF) will be shown here after calculation.')                
 # ... rest of your layout for index page
]),
    ]),
])
])
# Page 2 layout
page_2_layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'padding': '0 20px'}, children=[
        
        html.Div([
            html.Img(src=app.get_asset_url('KIT.jpg'), style={'height': '100px'})
        ], style={'flex': 'none', 'order': '1'}),
        # This div contains the title and subtitle
            html.Div([
            html.H1(children='Corrosion Model', style={
                'textAlign': 'center',
                'color': colors['text']
            }),
            html.H2(children='Total Risk', style={
                'textAlign': 'center',
                'color': colors['text']
            })
        ], style={'flex': 'none', 'order': '2'}),
        
        # This div contains the image
        html.Div([
            html.Img(src=app.get_asset_url('VULCAN.jpg'), style={'height': '100px'})
        ], style={'flex': 'none', 'order': '3'}),
    ]),
    # Selectors div
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px 0'}, children=[
        html.Div([
            html.Label('Insert a number:'),
            dcc.Input(id='number-input', type='number', min=0, max=100, step=1, value=50)
        ], style={'width': '30%', 'display': 'flex', 'flexDirection': 'column'}),

         
        html.Div([
            html.Label('Probability of Failure (PoF)'),
            dcc.Dropdown(id='selector1', 
                         options=[{'label': i, 'value': i} for i in df_ventas['ct(C)'].unique()],
                         value='')
        ], style={'width': '30%', 'display': 'flex', 'flexDirection': 'column'}),
        
        html.Div([
            html.Label('Consequence of Failure (CoF)'),
            dcc.Dropdown(id='selector2',
                         options=[{'label': i, 'value': i} for i in df_ventas['ct(C)'].unique()],
                         value='')
        ], style={'width': '30%', 'display': 'flex', 'flexDirection': 'column'}),
        
        html.Div([
            html.Label('Total Risk'),
            dcc.Dropdown(id='selector3',
                         options=[{'label': i, 'value': i} for i in df_ventas['ct(C)'].unique()],
                         value='')
        ], style={'width': '30%', 'display': 'flex', 'flexDirection': 'column'}),
    ]),
    html.Div([
    dcc.Graph(id='barplot_ventas_seg')
    ],style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
    dcc.Graph(id='barplot_beneficio_cat')
    ],style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

    html.Div([
    dcc.Graph(id='lineplot_cantidad')
    ],style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),
    
    
    
             
             
             
             
    html.Div([
   # dcc.Graph(id='mapa_ventas', figure=fig_mapa)
    ],style={'width': '100%'})
    ])
    # ... rest of your layout for page_2_layout


# Include 'selectors' where you want in your layout





# Update the page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/prediccion':
        return page_2_layout
    elif pathname == '/':
        return index_page
    else:
        return '404'
# FASE 4: Callback para actualizar gráfico de beneficio de categorías en función del dropdown de País y según selector de fechas
@app.callback(Output('barplot_beneficio_cat', 'figure'),
              [Input('selector_fecha', 'start_date'),Input('selector_fecha', 'end_date'),Input('selector', 'value'),Input('barplot_ventas_seg', 'hoverData')])
def actualizar_graph_cat(fecha_min, fecha_max, seleccion,hoverData):
# FASE 5: Interactividad inter-gráfico hoverData
    v_index = hoverData['points'][0]['x']
    filtered_df = df_ventas[(df_ventas["Fecha compra"]>=fecha_min) & (df_ventas["Fecha compra"]<=fecha_max) & (df_ventas["País"]==seleccion) & (df_ventas["Segmento"]==v_index)]

# FASE 2: CREACIÓN DE GRÁFICOS Y GROUPBY
    df_agrupado = filtered_df.groupby("Categoría")["Beneficio"].agg("sum").to_frame(name = "Beneficio").reset_index()

    return{
        'data': [go.Bar(x=df_agrupado["Categoría"],
                            y=df_agrupado["Beneficio"]
                            )],
        'layout': go.Layout(
            title="¿Cuáles han sido los beneficios de cada categoría?",
            xaxis={'title': "Categoría"},
            yaxis={'title': "Beneficios totales"},
            hovermode='closest')}


# FASE 4: Callback para actualizar gráfico de evolución cantidad de pedido en función del dropdown de País y según selector de fechas
@app.callback(Output('lineplot_cantidad', 'figure'),
              [Input('selector_fecha', 'start_date'),Input('selector_fecha', 'end_date'),Input('selector', 'value'),Input('barplot_ventas_seg', 'hoverData')])
def actualizar_graph_cat(fecha_min, fecha_max, seleccion,hoverData):
# FASE 5: Interactividad inter-gráfico hoverData
    v_index = hoverData['points'][0]['x']
    filtered_df = df_ventas[(df_ventas["Fecha compra"]>=fecha_min) & (df_ventas["Fecha compra"]<=fecha_max) & (df_ventas["País"]==seleccion) & (df_ventas["Segmento"]==v_index)]

# FASE 2: CREACIÓN DE GRÁFICOS Y GROUPBY
    df_agrupado = filtered_df.groupby("Fecha compra")["Cantidad"].agg("sum").to_frame(name = "Cantidad").reset_index()

    return{
        'data': [go.Scatter(x=df_agrupado["Fecha compra"],
                            y=df_agrupado["Cantidad"],
                            mode="lines+markers"
                            )],
        'layout': go.Layout(
            title="¿Cuál es la evolución de la cantidad de pedidos solicitados?",
            xaxis={'title': "Fecha"},
            yaxis={'title': "Cantidad"},
            hovermode='closest')}

@app.callback(
    Output('ef-output', 'children'),
    [Input('calculate-ef', 'n_clicks')],
    [State('number-dropdown', 'value')]
)
def update_ef(n_clicks, selected_value):
    if n_clicks > 0:
        if selected_value is not None:
            return f"The calculated Equipment Factor (EF) is: {selected_value}"
        else:
            return 'Please select a number of components range.'
    return 'Select number of components range and calculate EF'
        
@app.callback(
    Output('df-output', 'children'),
    [Input('calculate-df', 'n_clicks')],
    [State('damage-dropdown', 'value')]
)
def update_df(n_clicks, selected_values):
    # The selected_values now are the numeric values corresponding to the damages
    if n_clicks > 0 and selected_values:
        total_df = sum(selected_values)
        return f"The calculated Damage Factor (DF) is: {total_df}"
    else:
        return 'Select damages and calculate DF'
@app.callback(
    Output('if-output', 'children'),
    [Input('calculate-if', 'n_clicks')],
    [State('if1-dropdown', 'value'), State('if2-dropdown', 'value')]
)
def update_if(n_clicks, if1_value, if2_value):
    if n_clicks > 0:
        # Ensure that both dropdowns have selections
        if if1_value is not None and if2_value is not None:
            total_if = if1_value + if2_value
            return f"The calculated Inspection Factor (IF) is: {total_if}"
        else:
            return 'Please select values from both dropdowns to calculate IF.'
    return 'Select inspection factors and calculate IF'  
@app.callback(
    Output('tqf-output', 'children'),
    [Input('calculate-tqf', 'n_clicks')],
    [State('tqf1-dropdown', 'value'), State('tqf2-dropdown', 'value')]
)
def update_tqf(n_clicks, tqf1_value, tqf2_value):
    if n_clicks > 0:
        # Ensure that both dropdowns have selections
        if tqf1_value is not None and tqf2_value is not None:
            total_tqf = tqf1_value + tqf2_value
            return f"The calculated Toxicity Factor (TQF) is: {total_tqf}"
        else:
            return 'Please select values from both dropdowns to calculate TQF.'
    return 'Select Toxicity Factor and calculate TQF' 
@app.callback(
    Output('ppf-output', 'children'),
    [Input('calculate-ppf', 'n_clicks')],
    [State('people-dropdown', 'value')]
)
def update_ppf(n_clicks, selected_value):
    if n_clicks > 0:
        if selected_value is not None:
            return f"The calculated Population Factor (PPF) is: {selected_value}"
        else:
            return 'Please select a number of people.'
    return 'Select number of people and calculate PPF'

@app.callback(
    Output('dif-output', 'children'),
    [Input('calculate-dif', 'n_clicks')],
    [State('dif-dropdown', 'value')]
)
def update_dif(n_clicks, selected_value):
    if n_clicks > 0:
        if selected_value is not None:
            return f"The calculated Dispersibility Factor (DIF) is: {selected_value}"
        else:
            return 'Please select a Boiling Point.'
    return 'Select Boiling Point and calculate DIF'
@app.callback(
    Output('crf-output', 'children'),
    [Input('calculate-crf', 'n_clicks')],
    [State('crf1-dropdown', 'value'), State('crf2-dropdown', 'value'), State('crf3-dropdown', 'value')]
)
def update_crf(n_clicks, crf1_value, crf2_value, crf3_value):
    if n_clicks > 0:
        # Ensure that all dropdowns have selections
        if crf1_value is not None and crf2_value is not None and crf3_value is not None:
            total_crf = crf1_value + crf2_value + crf3_value
            return f"The calculated Credit Factor (CRF) is: {total_crf}"
        else:
            return 'Please select values from all dropdowns to calculate CRF.'
    return 'Select credit factors and calculate CRF'
     
@app.callback(
    Output('ccf-output', 'children'),
    [Input('calculate-ccf', 'n_clicks')],
    [State('ccf1-dropdown', 'value'), State('ccf2-dropdown', 'value'), State('ccf3-dropdown', 'value')]
)
def update_ccf(n_clicks, ccf1_value, ccf2_value, ccf3_value):
    if n_clicks > 0:
        # Ensure that all dropdowns have selections
        if ccf1_value is not None and ccf2_value is not None and ccf3_value is not None:
            total_ccf = ccf1_value + ccf2_value + ccf3_value
            return f"The calculated Condition Factor (CCF) is: {total_ccf}"
        else:
            return 'Please select values from all dropdowns to calculate CCF.'
    return 'Select condition factors and calculate CCF'

@app.callback(
    Output('pf-output', 'children'),
    [Input('calculate-pf', 'n_clicks')],
    [State('pf1-dropdown', 'value'), State('pf2-dropdown', 'value'), State('pf3-dropdown', 'value')]
)
def calculate_pf(n_clicks, pf1_value, pf2_value, pf3_value):
    if n_clicks > 0:
        total_pf = sum(filter(None, [pf1_value, pf2_value, pf3_value]))  # Sums up all non-None values
        return f"Total Process Factor (PF): {total_pf}"
    return "Select all factors and calculate PF"
@app.callback(
    Output('mdf-output', 'children'),
    [Input('calculate-mdf', 'n_clicks')],
    [State('mdf1-dropdown', 'value'), State('mdf2-dropdown', 'value')]
)
def calculate_mdf(n_clicks, mdf1_value, mdf2_value):
    if n_clicks > 0:
        total_mdf = sum(filter(None, [mdf1_value, mdf2_value]))  # Sums up all non-None values
        return f"Total Mechanical Design Factor (MDF): {total_mdf}"
    return "Select all factors and calculate MDF"

# Callback for updating the PoF output
@app.callback(
    Output('pof-output', 'children'),
    [Input('calculate-pof', 'n_clicks')],
    [State('ef-output', 'children'),
     State('df-output', 'children'),
     State('if-output', 'children'),
     State('ccf-output', 'children'),
     State('pf-output', 'children'),
     State('mdf-output', 'children')]
)
def calculate_pof(n_clicks, ef, df, if_factor, ccf, pf, mdf):
    if n_clicks > 0:
        try:
            # Parse the outputs to extract numeric values
            ef_val = extract_numeric_value(ef)
            df_val = extract_numeric_value(df)
            if_val = extract_numeric_value(if_factor)
            ccf_val = extract_numeric_value(ccf)
            pf_val = extract_numeric_value(pf)
            mdf_val = extract_numeric_value(mdf)

            # Check if any of the values were not parsed successfully
            if None in (ef_val, df_val, if_val, ccf_val, pf_val, mdf_val):
                return 'Not all factors have been calculated. Please calculate all factors before determining PoF.'

            # Sum the values to get the total PoF
            total = sum(filter(None, (ef_val, df_val, if_val, ccf_val, pf_val, mdf_val)))
            pof = assign_pof(total)  # You'd need to define assign_pof based on the PoF ranges
            return f"Probability of Failure (PoF) is: {pof}"

        except Exception as e:
            print(f"Error calculating PoF: {e}")
            return f"Error calculating PoF: {e}"

    return dash.no_update  # If button wasn't clicked, don't update the output


@app.callback(
    Output('cof-output', 'children'),
    [Input('calculate-cof', 'n_clicks')],
    [State('tqf-output', 'children'),
     State('dif-output', 'children'),
     State('crf-output', 'children'),
     State('ppf-output', 'children')]
)

def calculate_cof(n_clicks, tqf, dif, crf, ppf):
    if n_clicks > 0:
        try:
            # Parse the outputs to extract numeric values
            tqf_val = extract1_numeric_value(tqf)
            dif_val = extract1_numeric_value(dif)
            crf_val = extract1_numeric_value(crf)
            ppf_val = extract1_numeric_value(ppf)
            
            # Check if any of the values were not parsed successfully
            if None in (tqf_val, dif_val, crf_val, ppf_val):
                return 'Not all factors have been calculated. Please calculate all factors before determining CoF.'

            # Sum the values to get the total PoF
            total = sum(filter(None, (tqf_val, dif_val, crf_val, ppf_val)))
            cof = assign_cof(total)  # You'd need to define assign_pof based on the CoF ranges
            return f"Consequence of Failure (CoF) is: {cof}"

        except Exception as e:
            print(f"Error calculating CoF: {e}")
            return f"Error calculating CoF: {e}"

    return dash.no_update 
# Run the app
if __name__ == '__main__':
    app.run_server(port=8000)
