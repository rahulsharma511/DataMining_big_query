from turtle import width
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from datetime import date

import plotly.express as px
import pandas as pd
from google.oauth2 import service_account  # pip install google-auth
import pandas_gbq  # pip install pandas-gbq

credentials = service_account.Credentials.from_service_account_file('C:\\Users\\RahulSharma\\OneDrive\\Desktop\\data_mining\\assets\\key.json')
project_id = 'datamining101-364621'  # make sure to change this with your own project ID

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Chicage Taxi Data Visualization", style={'textAlign':'center'}),
    html.Div(id='graph-content'),
    html.Div([
        dcc.Dropdown(id='dropdown1', options=[{'label':x, 'value': x} for x in range(1999, 2022)], style={'width':'25%'}),
        dcc.Dropdown(id='dropdown2', options=[{'label':x, 'value': x} for x in range(1999, 2022)], style={'width':'25%'})]
    ),
    html.Button(id='enter', children=['Submit']),
    html.Div(id = 'heat-map'),
    html.Div(id = 'company-fig'),
    html.Div(
        dcc.Dropdown(id='dropdown3', options=[{'label':x, 'value': x} for x in range(2013, 2022)], style={'width':'25%'})
    )
])


@app.callback(
    Output('graph-content', 'children'),
    Output('heat-map', 'children'),
    Output('company-fig', "children"),
    Input('enter','n_clicks'),
    Input('dropdown3', 'value'),
    State('dropdown1', 'value'),
    State('dropdown2', 'value')
    
)
def create_graph(n,dropdown3, dropdown1, dropdown2):
    print(dropdown3)
    print(dropdown1)
    print(dropdown2)
    # I recommend running the SQL in Good Cloud to make sure it works
    # before running it here in your Dash App.
    df_sql = f"""select * from `datamining101-364621.taxidataset.taxi`
    """
    df_sql2 = f"""select * from `datamining101-364621.taxidataset.latlong`
    """
    df = pd.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
    df = df.sort_values(by = 'year')
    print('length of the df received is:' +str(len(df)))
    #df.to_csv("first_sample.csv")
    # dff = df.groupby('boroname')[['diameter']].mean()
    # dff.reset_index(inplace=True)
    # fig = px.bar(df, x='boroname', y='diameter')
    fig = px.line(df, x="year", y="total_count", title='Total rides every year')
    df_loc = pd.read_gbq(df_sql2, project_id=project_id, dialect='standard', credentials=credentials)
    fig2 = px.density_mapbox(df_loc, lat='pickup_latitude', lon='pickup_longitude', radius=10,
                        center=dict(lat=41.8, lon=-87.6), zoom=8.5, hover_name = 'count',
                        mapbox_style='stamen-terrain',
                        title="Heat Map for taxi pickup locations")
    df_sql3 = f""" select * from `datamining101-364621.taxidataset.companies` """ 
    df_company = pd.read_gbq(df_sql3, project_id = project_id, dialect = 'standard', credentials = credentials)
    df_company = df_company[df_company['year'] == dropdown3]
    fig3 = px.bar(df_company, x='company', y='total_count', title=f'Total count of taxi rides per company in year: {dropdown3}')
    return dcc.Graph(figure=fig), dcc.Graph(figure = fig2),dcc.Graph(figure = fig3)



if __name__=='__main__':
    app.run_server(debug=False)



    # SELECT
    # created_at,
    # boroname,
    # tree_dbh as diameter,
    # spc_common as type
    # FROM `bigquery-public-data.new_york_trees.tree_census_2015`
    # WHERE created_at < '{enddate}'
    # AND created_at > '{startdate}'
    # AND tree_dbh > {treediameter}
    # ORDER BY created_at DESC
    # LIMIT 1000