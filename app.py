# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 20:37:09 2020

@author: KIIT
"""


import dash
import pandas as pd
import dash_html_components as html
import webbrowser
from dash.dependencies import Input,State,Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

def load_data():
    dataset_name='global_terror.csv'
    
    global df
    df=pd.read_csv(dataset_name)
    temp_list=sorted(df['country_txt'].unique().tolist())
    global country_list
    country_list=[{'label':str(i), 'value':str(i)} for i in temp_list]
    months={'January':0,
            'February':1,
            'March':2,
            'April':3,
            'May':4,
            'June':5,
            'July':6,
            'August':7,
            'September':8,
            'October':9,
            'November':10,
            'December':11}
    global month_list
    month_list=[{'label':key, 'value':value} for key,value in months.items()]
    global day_list
    day_list=[{'label':str(i), 'value':i} for i in range(1,32)]
    global region_list
    region_list=[{'label':str(i),'value':str(i)} for i in (sorted(df['region_txt'].unique().tolist()))]
    global provstate_list
    provstate_list=[{'label':str(i),'value':str(i)} for i in (df['provstate'].unique().tolist())]
    global city_list
    city_list = [{'label':str(i),'value':str(i)} for i in (df['city'].unique().tolist())]
    global attack_list
    attack_list = [{'label':str(i),'value':str(i)} for i in (df['attacktype1_txt'].unique().tolist())]
    global year_list
    year_list=sorted(df['iyear'].unique().tolist())
    global year_dict
    year_dict={str(year): {'label':str(year),'style': {'color': '#f50'}} for year in year_list}
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt',
                             "Country Attacked":'country_txt'
                          }
    chart_dropdown_values=[{'label':str(key),'value':str(value)} for key, value in chart_dropdown_values.items()]
    
    
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    
def create_app_ui():
    main_layout=html.Div(
        [
            html.Div([
                html.H1(id='Main_title',children='Terrorism Analysis with Insights',className='h1'),
                html.Img(src='/assets/icon-kazi.png'),
                html.Img(src='/assets/icon-forsk.png')
                ],className='banner'),
            dcc.Tabs(id='Tabs', value='tab-1', children=[
                dcc.Tab(label='Map Tool', id='Map-tool', value='tab-1', children=[
                    dcc.Tabs(id='subtabs',value='tab-1', children=[
                        dcc.Tab(label='World Map Tool',
                                id='World',
                                value='tab-1'),   
                        dcc.Tab(label='India Map Tool', id='India',value='tab-2')],colors={"border": "black","primary": "blue"}
                    ),
                    html.Div([
                        html.Br(),
                        html.Div([
                            html.Div([
                                dcc.Dropdown(id='month-dropdown',
                                             
                                             multi=True,
                                             searchable=True,
                                             options=month_list,
                                             style={'border-radius':'40px'},
                                             placeholder='Select Month')
                                
                                ],className='five columns offset-by-one column'),
                            
                            html.Div([
                                
                                dcc.Dropdown(id='day-dropdown',
                                             multi=True,
                                             searchable=True,
                                             options=day_list,
                                             style={'border-radius':'40px'},
                                             placeholder='Select Day')
                                ],className=' five columns offset-by-one column')],
                            className='row'),
                        html.Br(),
                        html.Div([
                            html.Div([
                                dcc.Dropdown(id='region-dropdown',
                                             multi=True,
                                             searchable=True,
                                             style={'border-radius':'40px'},
                                             options=region_list,
                                             placeholder='Select Region')
                                ],className='five columns offset-by-one column'),
                            html.Div([
                                dcc.Dropdown(id='country-dropdown',
                                         multi=True,
                                         searchable=True,
                                         style={'border-radius':'40px'},
                                         options=country_list,
                                         placeholder='Select Country')
                            ],className='five columns offset-by-one column'),
                            
                            ],className='row'),
                        html.Br(),
                    html.Div([
                        html.Div([
                            dcc.Dropdown(id='provstate-dropdown',
                                         multi=True,
                                         searchable=True,
                                         options=provstate_list,
                                         style={'border-radius':'40px'},
                                         placeholder='Select Province or State')
                            ],className='five columns offset-by-one column'),
                        html.Div([
                            dcc.Dropdown(id='city-dropdown',
                                         multi=True,
                                         searchable=True,
                                         options=city_list,
                                         style={'border-radius':'40px'},
                                         placeholder='Select City')
                            ],className='five columns offset-by-one column'),
                    ],className='row'),
                    html.Br(),
                    html.Div([
                        dcc.Dropdown(id='attacktype-dropdown',
                                     multi=True,
                                     searchable=True,
                                     options=attack_list,
                                     style={'border-radius':'40px'},
                                     placeholder='Select Attack Type')
                        ],className='one-third column offset-by-one-third columns'),
                    html.Br(),
                    html.Br(),
                    html.H6(children='Select The Year',className='h6',style={'color':'Black'}),
                    dcc.RangeSlider(id='year-slider',
                                    min=min(year_list),
                                    max=max(year_list),
                                    allowCross=False,                                    
                                    value=[min(year_list),max(year_list)],
                                    marks=year_dict)]
                        ,style={'background-image':'url("/assets/back-image - Copy.jpg")','background-repeat': 'no-repeat','background-size': '100% 100%'})]),
                dcc.Tab(label='Chart Tool', id='chart Tool', value='Chart', children=[
                    dcc.Tabs(id='subtabs2', value='tab-1', children=[
                        dcc.Tab(label='World Chart Tool', id='WorldC', value='tab-1', children=[html.Div()]),
                        dcc.Tab(label='India Chart Tool', id='IndiaC', value='tab-2', children=[html.Div()])
                        ],colors={"border": "black","primary": "blue"}),
                    
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.H6(children='Incidents Per Year Grouped By:')
                            
                            ],className='offset-by-one column four columns'),
                        html.Div([
                            dcc.Dropdown(id='Chart_Dropdown',
                                     options=chart_dropdown_values,
                                     placeholder='Select Option',
                                     style={'border-radius':'40px'},
                                     value='region_txt'),
                            ],className='five columns')
                        ],className='row'),
                    html.Br(),
                    html.Hr(),
                    html.Div([
                        html.Div([
                            html.H6(id='search-text',children='Filter With Name of Region')],
                            className='offset-by-one column four columns'),
                        html.Div([
                    dcc.Input(id='search',placeholder='Search Filter',style={'width':'70%','border-radius': '40px'},autoFocus=True),
                    ],className='seven columns'),
                    ],className='row'),
                    html.Hr()])
                ],colors={"border": "black","primary": "blue"}),
            html.Br(),
            dcc.Loading(children=[dcc.Graph(id='graph-object')],type='graph')
            ]
        
        )
    
    return main_layout

@app.callback(
    Output('search-text','children'),
    [
     Input('Chart_Dropdown', 'value')
     ]
    )
def update_search_text_ui(chart_dp_value):
    
    inci=''
    for item in chart_dropdown_values:
        if(item.get('value')==chart_dp_value):
            inci=item.get('label')
    print(inci)
    inci='Filter With Name of '+inci+':'
    return inci

@app.callback(
    dash.dependencies.Output('graph-object','figure'),
    [
     dash.dependencies.Input('Tabs','value'),
     dash.dependencies.Input('month-dropdown','value'),
     dash.dependencies.Input('day-dropdown','value'),
     dash.dependencies.Input('region-dropdown','value'),
     dash.dependencies.Input('country-dropdown','value'),
     dash.dependencies.Input('provstate-dropdown','value'),
     dash.dependencies.Input('city-dropdown','value'),                
     dash.dependencies.Input('attacktype-dropdown','value'),
     dash.dependencies.Input('year-slider','value'),
     dash.dependencies.Input('Chart_Dropdown','value'),
     dash.dependencies.Input('search','value'),
     dash.dependencies.Input('subtabs2','value')
     ]
    )
def update_map_ui(tab,month,day,region,country,provstate,city,
                  attacktype,year,chart_dp_value,search_value,subtabs2_value):
    df1=df
    print('worldmap')
    figure=None
    if tab=='tab-1':
        year_range=range(year[0],year[1]+1)
        df1=df1[df1['iyear'].isin(year_range)]
        if(month is None or month==[]):
            pass
        else:
            df1=df1[df1['imonth'].isin(month)]
            if(day is None or day==[]):
                pass
            else:
                df1=df1[df1['iday'].isin(day)]
        
        if(region is None or region==[]):
            pass
        else:
            df1=df[df['region_txt'].isin(region)]
            if(country is None or country==[]):
                pass
            else:
                df1=df1[df1['country_txt'].isin(country)]
                if(provstate is None or provstate==[]):
                    pass
                else:
                    df1=df1[df1['provstate'].isin(provstate)]
                    if(city is None or city==[]):
                        pass
                    else:
                        df1=df1[df1['city'].isin(city)]
        
        if(attacktype is None or attacktype ==[]):
            pass
        else:
            df1=df1[df1['attacktype1_txt'].isin(attacktype)]
        if(df1.shape[0]):
            pass
        else:
            df1=pd.DataFrame(columns=['iyear','imonth','iday','region_txt','country_txt','provstate','city','latitude','longitude','nkill','attacktype1_txt'])
            df1.loc[0]=[0,0,0,None,None,None,None,None,None,None,None]
                            
        figure=go.Figure()
        figure=px.scatter_mapbox(df1,
                                 lat='latitude',
                                 lon='longitude',
                                 color='attacktype1_txt',
                                 hover_data=['region_txt','country_txt','provstate','city','attacktype1_txt','nkill','iyear'],
                                 zoom=1,
                                 title='World Map Plot'
                                 )
        figure.update_layout(mapbox_style='open-street-map',
                             autosize=True,
                             margin=dict(l=0,r=0,t=25,b=20)
                             )
    elif tab=='Chart':
        print(subtabs2_value)
        chart_df=df
        if subtabs2_value == "tab-1":
            if chart_dp_value is not None:
                if search_value is not None: 
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search_value, case = False)]
                else:
                    chart_df = df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
                    
            else:
                raise PreventUpdate
            
        
        elif subtabs2_value=='tab-2':
            if chart_dp_value is not None:
                chart_df=chart_df[chart_df['region_txt']=='South Asia']
                chart_df=chart_df[chart_df['country_txt']=='India']
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                if search_value is not None:
                    chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search_value, case = False)]
            else:
                raise PreventUpdate
        
        title='Area Chart-Incidents Per Year Grouped By:'
        inci=''
        for item in chart_dropdown_values:
            if(item.get('value')==chart_dp_value):
                inci=item.get('label')
        title=title+inci
                
            
        chartFigure = px.area(chart_df,
                              x= "iyear",
                              y ="count",
                              color = chart_dp_value,
                              title=title)
        figure = chartFigure
            
    else:
        return None
    return figure



@app.callback([
    Output('region-dropdown','value'),
    Output('region-dropdown','disabled'),
    Output('country-dropdown','value'),
    Output('country-dropdown','disabled')
    ],
    [
     Input('subtabs','value')
     ]
    )
def update_india_map(tab):
    region=None
    country=None
    region_D=None
    country_D=None
    if tab=='tab-1':
        region=[]
        country=[]
        region_D=False
        country_D=False
        return region,region_D,country,country_D
    elif tab=='tab-2':
        region=['South Asia']
        country=['India']
        region_D=True
        country_D=True
        return region, region_D,country,country_D


    

@app.callback(
    dash.dependencies.Output('city-dropdown','options'),
    [
     dash.dependencies.Input('provstate-dropdown','value')
     ]
    )
def update_city_ui(provstate):
    if(provstate is None or provstate==[]):
        return [{'label':'Select Province/State First','value':'-1','disabled':True}]
    else:
        return[{'label':str(i),'value':str(i)} for i in df[df['provstate'].isin(provstate)]['city'].unique().tolist()]

        

@app.callback(
    dash.dependencies.Output('provstate-dropdown', 'options'),
    [
     dash.dependencies.Input('country-dropdown','value')
     ]
    )
def update_state_ui(country):
    if(country is None):
        PreventUpdate
    else:
        if(country is None or country==[]):
            return[{'label':'Select Country First','value':'-1','disabled':True }]
        else:
            return[{'label':str(i),'value':str(i)} for i in df[df['country_txt'].isin(country)]['provstate'].unique().tolist()]
        

@app.callback(
    dash.dependencies.Output('country-dropdown', 'options'), 
    [
     dash.dependencies.Input('region-dropdown', 'value')
     ]
    )
def update_country_ui(region):
    if(region is None):
        PreventUpdate
    else:
        if(region is None or region==[]):
            return[{'label':'Choose Region First','value':'-1','disabled': True }]
        else:
            return [{'label':str(i),'value':str(i)} for i in df[df['region_txt'].isin(region)]['country_txt'].unique().tolist()]
    

@app.callback(
    dash.dependencies.Output('day-dropdown','options'),
    [
     dash.dependencies.Input('month-dropdown','value')
     ]
    )
def update_day_ui(month):
    date_list=range(1,31)
    #print(month)
    if(month is None or month==[]):
        return [{'label':'Select Month First','value':-1,'disabled':True}]
    else:    
        return [{'label':str(item),'value':item} for item in date_list]
        '''if(all(item in [1] for item in month)):
            return [{'label':str(item),'value':item} for item in date_list[:-2]]
        elif(item in month for item in [3,5,8,10]):
            return [{'label':str(item),'value':item} for item in date_list[:-1]]
        elif(item in month for item in [0,2,4,6,7,9,11]):
            return [{'label':str(item),'value':item} for item in date_list]'''
        
        
           


def main():
    print("Welcome to project of Terrorism Analysis")
    load_data()
    global app
    app.layout=create_app_ui()
    app.title='Forsk Terrorism Analysis'
    app.css.append_css(
        {'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})
    open_browser()
    app.run_server()
    
if __name__=='__main__':
    main()


