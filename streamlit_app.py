import numpy as np
import pandas as pd
import streamlit as st
# from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import plotly.express as px

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Web App Title
st.markdown('''
# **OVC Data Visualization App**
App built using `PYTHON` & `STREAMLIT` by [Daniel Maina]
---
''')



# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
    Please download the **example file here** to a local folder then load it into this platform for data visualization:
[Example CSV input file](https://raw.githubusercontent.com/dmainagithub/my_datasets/main/viral_load_results.csv)
""")
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}    
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})    

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
    
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

    dcc.Graph(
        id='my_bee_map', 
        figure=fig
    )

])

if __name__ == '__main__':
     app.run_server(debug=True)
    
    


# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()
    # pr = ProfileReport(df, explorative=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    # st_profile_report(pr)
    

    
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Example data
        @st.cache
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)
