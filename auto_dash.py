import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px 
import dash 
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State
from dash import no_update

#Create App
app = dash.Dash(__name__)

#Clear the layout and do not display exceptions till callback gets executed
app.config.suppress_callback_exceptions = True 

#Reading Data provided on Automobile prices and car features
auto_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv',
    encoding = 'ISO-8859-1')

#Layout Section of Dash
app.layout = html.Div(children = 
    [html.H1('Car Automobile Components', style = {'textAlign': '#503D36', 'font-size': 24}),
    html.Div([ 
        html.Div( 
            html.H2('Drive Wheels Type: ', style = {'margin-right': '2em'}),),
            dcc.Dropdown(id = 'wheel-dropdown', 
                options = [{'label': 'Rear Wheel Drive', 'value': 'rwd'}, 
                {'label': 'Front Wheel Drive', 'value': 'fwd'}, 
                {'label': 'Four Wheel Drive', 'value': '4wd'}], 
                value = 'rwd'), #Drop down Menu
        html.Div([
            html.Div([dcc.Graph(id = 'plot1') ]), 
            html.Div([dcc.Graph(id = 'plot2') ],)
        ], style = {'display':'flex'}) # Allows graph to be side by side
    ])
])

#App Callback Decorator
@app.callback(
    [Output('plot1', 'figure'),
    Output('plot2', 'figure')],
    Input('wheel-dropdown', 'value')
    )

#Defining the callback function
def display_selected_drive_charts(value): 
    filtered_df = auto_data[auto_data['drive-wheels']==value].groupby(['drive-wheels', 'body-style'], as_index = False).mean()
    pie_fig = px.pie(filtered_df, values = 'price', names = 'body-style', title = 'Pie Chart')
    bar_fig = px.bar(filtered_df, x = 'body-style', y = 'price', title = 'Bar Chart')

    return pie_fig, bar_fig


if __name__ == '__main__': 
    app.run_server()