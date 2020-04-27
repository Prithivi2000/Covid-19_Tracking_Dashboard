import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import folium
from dash.dependencies import Input,Output
import requests
from io import StringIO
import plotly.offline as pyo
#from IPython.display import Image
#import cv2



external_stylesheets=[
    {
        'href':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
        'rel':'stylesheet' ,
        'integrity':'sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh',
        'crossorigin' :'anonymous'
    }
]
headers={'User-Agent':'Mozilla/5.0(Windows NT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url="https://www.grainmart.in/news/coronavirus-covd-19-live-cases-tracker-john-hopkins/"
s=requests.get(url, headers= headers).text


df1=pd.read_html(StringIO(s))
a=df1[0]
total_india=a[1][36]
active_india= a[2][36]
death_india = a[3][36]
recover_india = a[4][36]



url="https://www.grainmart.in/news/coronavirus-covd-19-live-cases-tracker-john-hopkins/"
v=requests.get(url, headers= headers).text


df2=pd.read_html(StringIO(v))
b=df2[0]
state_india = b[0][2:]
active_cases_column = b[2][2:]
death_cases_column = b[3][2:]


url="https://www.worldometers.info/coronavirus/"
s=requests.get(url, headers= headers).text
df=pd.read_html(StringIO(s))


url="https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/"
l=requests.get(url, headers= headers).text
df3=pd.read_html(StringIO(l))
c=df3[0]
death_share = c[2][1:]
age_share= c[0][1:]
trace_age = go.Bar(x = age_share,y = death_share, marker={'color':'#00ff00'})
data_age = [trace_age]
layout1 = go.Layout(title='Age-Wise Death Rate',
                xaxis={'title':'Age'},
                yaxis={'title':'Death-Rate'})


df4=pd.read_html(StringIO(l))
d=df4[1]
sex_cal_death=d[2][1:]
sex_cal_death_gender=d[0][1:]


trace_sex = go.Pie(labels= ['Male', 'Female'], values = ['61.8','38.2'], pull= [0.2, 0], textposition = 'inside', textfont_size= 14,
                   marker = dict(line = dict(color = '#000000', width=2)))
data_death_gender = [trace_sex]
layout2 = go.Layout(title='Gender Wise Death Rate')
fig6 = go.Figure(data = data_death_gender, layout= layout2)


active_cases=df[0]['ActiveCases']
recover_cases=df[0]['TotalRecovered']
death_cases = df[0]['TotalDeaths']
tests = df[0]['TotalTests']
options=[
        {'label':'Active Cases', 'value':'ActiveCases'},
        {'label':'Total Recovered', 'value':'TotalRecovered'},
        {'label':'Total Deaths', 'value':'TotalDeaths'},
        {'label':'Total Tests', 'value':'TotalTests'}
        ]

app= dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout= html.Div([
                html.H1('Corona Virus Pandemic',style={ 'color':'white', 'text-align':'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Total Cases', className='text-light'),
                                html.H4(total_india, className='text-light')
                            ], className='card-body bg-danger')
                        ], className='card')
                    ], className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Active Cases', className='text-light'),
                                html.H4(active_india, className='text-light')
                            ], className='card-body bg-info')
                        ], className='card')
                    ], className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Recoveries', className='text-light'),
                                html.H4(recover_india, className='text-light')
                            ], className='card-body bg-warning')
                        ], className='card')
                    ], className='col-md-3'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3('Deaths', className='text-light'),
                                html.H4(death_india, className='text-light')
                            ], className='card-body bg-success')
                        ], className='card')
                    ], className='col-md-3')
                ], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
dcc.Graph(id='Scatter', figure={
                                                                    'data':[
                                                                            go.Scatter(
                                                                                        x= state_india,
                                                                                        y= active_cases_column,
                                                                                        mode='lines+markers'
                                                                                        )
                                                                            ],
                                                                    'layout': go.Layout(title='STATE-WISE ACTIVE CASES IN INDIA')

                                                                })
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
dcc.Graph(id='Scatter-line', figure={
                                                                    'data':[
                                                                            go.Scatter(
                                                                                        x= state_india,
                                                                                        y=death_cases_column,
                                                                                        mode='lines+markers'
                                                                                        )
                                                                            ],
                                                                    'layout': go.Layout(title='STATE-WISE DEATH CASES IN INDIA')

                                                                })
                ],className='card-body')
            ],className='card')
        ],className='col-md-6')
    ],className='row'),
                html.Div([
                    html.Div([
                            html.Div([
                                html.Div([
                                    dcc.Dropdown(id='picker',options=options,value='ActiveCases'),
                                    dcc.Graph(id='choropleth')
                                ], className='card-body')
                            ],className='card')
                    ],className='col-md-12')
                ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Now Check Your Probability of Getting Affected', style={'color': 'white', 'text-align':'center'})
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-12')
    ],className='row'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Graph(id='Bar-Gender', figure= fig6)
                            ],className='card-body')
                        ],className='card')
                    ],className='col-md-12')
                ],className='row'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    dcc.Graph(id='Bar_age', figure={
                                        'data': data_age,
                                        'layout': layout1

                                    })

                                ],className='card-body')
                            ],className='card')
                        ],className='col-md-12')
                    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('COVID19 SYMPTOMS', style={'color':'white', 'text-align':'center'})
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5('COVID-19 affects different people in different ways. Most infected people will develop mild to moderate symptoms.'),
                    html.H5('Common Symptoms:'),
                    html.H5('1. Fever'),
                    html.H5('2. Tiredness'),
                    html.H5('3. Dry Cough'),
                    html.H5('Some people may experience:'),
                    html.H5('1. Aches and Pain'),
                    html.H5('2. Nasal Congestion'),
                    html.H5('3. Runny Nose and Sore Throat'),
                    html.H5('4. Diarrhoea'),
                    html.H5('On an average it takes 5-6 days from when someone is infected with the virus for symptoms to show, however it can take upto 14 days.')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Prevention is Better Than Cure', style={'text-align':'center'}),
                    html.H2('See Below The preventive measures you should take', style={'text-align':'center'})
                ],className='card-body')
            ],className='card bg-success')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5('1. STAY home'),
                    html.H5('2. KEEP a safe distance'),
                    html.H5('3. WASH hands often'),
                    html.H5('4. COVER your cough'),
                    html.H5('5. SICK? Call the helpine numbers given below....')
                ], className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H2('Govt. Help-Line Numbers', style={'color':'white', 'text_align': 'center'})
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H5('Andhra Pradesh:    0866-2410978'),
                    html.H5('Arunachal Pradesh: 9436055743'),
                    html.H5('Assam:             6913347770'),
                    html.H5('Bihar:             104'),
                    html.H5('Chattisgarh:       104'),
                    html.H5('Gujarat:           104'),
                    html.H5('Goa:               104'),
                    html.H5('Haryana:           8558893911'),
                    html.H5('Himachal Pradesh:  104'),
                    html.H5('Jharkhand:         104'),
                    html.H5('Karnataka:         104'),
                    html.H5('Kerala:            0471-2552056'),
                    html.H5('Madhya Pradesh:    104'),
                    html.H5('Maharashtra:       020-26127394'),
                    html.H5('Manipur:           3852411668'),
                    html.H5('Meghalaya:         108'),
                    html.H5('Mizoram:           102'),
                    html.H5('Nagaland:          7005539653'),
                    html.H5('Odisha:            9439994859'),
                    html.H5('Punjab:            104'),
                    html.H5('Rajasthan:         0141-2225624'),
                    html.H5('Sikkim:            104'),
                    html.H5('Tamil Nadu:        044-29510500'),
                    html.H5('Telangana:         104'),
                    html.H5('Tripura:           0381-2315879'),
                    html.H5('Uttarakhand:       104'),
                    html.H5('Uttar Pradesh:     18001805145'),
                    html.H5('West Bengal:       1800313444222, 033-2341-2600'),
                    html.H5('Andaman and Nicobar Island: 03192-232102'),
                    html.H5('Chandigarh:  9779558282'),
                    html.H5('Dadra and Nagar Haveli and Daman and Diu: 104'),
                    html.H5('Delhi:  011-22307145'),
                    html.H5('Jammu & Kashmir:  01912520982, 0194-2440283'),
                    html.H5('Ladakh:   01982256462'),
                    html.H5('Lakshadweep:  104'),
                    html.H5('Puducherry:  104')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row'),



                html.Div([
                   html.Div([
                       html.Div([
                           html.Div([
                                html.H6('@TROUBLESHOOTERS TECHNOLOGICAL SOLUTIONS@', style={ 'color':'grey', 'text-align':'center'}),
                                html.H6('STAY HOME, STAY SAFE', style={ 'color':'grey', 'text-align':'center'}),
                                html.H6('#INDIAFIGHTSCORONA', style={ 'color':'grey', 'text-align':'center'})


                           ], className='card-body')
                       ], className='card')
                   ], className='col-md-12')
                ], className='row')

], className='container')

@app.callback(Output('choropleth', 'figure'),[Input('picker','value')])
def update_graph(type):
    if type == 'ActiveCases':
        dff = df[0].groupby('Country,Other')['ActiveCases'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff['Country,Other'], z=dff['ActiveCases'], autocolorscale=False,
                                       locationmode='country names', colorscale='rainbow',
                                       marker={'line': {'color': 'rgb(180,180,180)', 'width': 0.5}},
                                       colorbar={'thickness': 15, 'len': 1., 'x': 0.9, 'y': 0.7,
                                                 'title': {'text': 'Active Cases', 'side': 'bottom'}})],
                'layout': go.Layout(title='Active Cases all over the world')}
    elif type == 'TotalRecovered':
        dff1 = df[0].groupby('Country,Other')['TotalRecovered'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff1['Country,Other'], z=dff1['TotalRecovered'], autocolorscale=False,
                                       locationmode='country names', colorscale='rainbow',
                                       marker={'line': {'color': 'rgb(255,255,255)', 'width': 0.5}},
                                       colorbar={'thickness': 15, 'len': 1, 'x': 0.9, 'y': 0.7,
                                                 'title': {'text': 'Total Recovered', 'side': 'bottom'}})],
                'layout': go.Layout(title='Recovered cases all over the world')}
    elif type == 'TotalTests':
        dff3 = df[0].groupby('Country,Other')['TotalTests'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff3['Country,Other'], z=dff3['TotalTests'], autocolorscale=False,
                                       locationmode='country names', colorscale='rainbow',
                                       marker={'line': {'color': 'rgb(255,255,255)', 'width': 0.5}},
                                       colorbar={'thickness': 15, 'len': 1, 'x': 0.9, 'y': 0.7,
                                                 'title': {'text': 'Total Tests', 'side': 'bottom'}})],
                'layout': go.Layout(title='Total Tests all over the world')}
    else:
        dff2 = df[0].groupby('Country,Other')['TotalDeaths'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff2['Country,Other'], z=dff2['TotalDeaths'], autocolorscale=False,
                                       locationmode='country names', colorscale='rainbow',
                                       marker={'line': {'color': 'rgb(255,255,255)', 'width': 0.5}},
                                       colorbar={'thickness': 15, 'len': 1, 'x': 0.9, 'y': 0.7,
                                                 'title': {'text': 'Total Deaths', 'side': 'bottom'}})],
                'layout': go.Layout(title='Total Death cases all over the world')}


if __name__=="__main__":
    app.run_server(debug=True)
