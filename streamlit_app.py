from typing import Container
import numpy as np
import pandas as pd
import streamlit as st
# from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import plotly.express as px  # an API for creating figures 
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)


# ----------------------------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv(r'data/intro_bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

    
# ----------------------------------------------------------------------------------------------------
app.layout = html.Div([
    
html.H1("Web Application Dashboards with Dash", style={'text-align':'center'}),
    
   dcc.Dropdown(id="slct_year",
                 options=[
                    {"label":"2015", "value":2015},
                    {"label":"2016", "value":2016},
                    {"label":"2017", "value":2017},
                    {"label":"2016", "value":2016}],
                multi=False,
                value=2015,
                 style={'width':"40%"}
    ),


    html.Div(id='output_container', children=[]),    
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


    #  ----------------------------------------------------------------------------------------------------------------------------
    #  Connect the plotly graphs with Dash Components
    #  ----------------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output(component_id='output_container', component_property='children')],
    [Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was:  {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State','Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={'Pct of Colonies Impacted': '% of Bee colonies'},
        template='plotly_dark'
    )

    # # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff['Pct of COlonies Impacted'].astype(float),
    #         colorscale='Reds',
    #     )]
    # )

    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig




    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
   
if __name__ == '__main__':
     app.run_server(debug=True)

    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
    #  ----------------------------------------------------------------------------------------------------------------------------
    


