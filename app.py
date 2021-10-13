import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import dribbleanalysis as da




app = dash.Dash(__name__,external_stylesheets =[dbc.themes.BOOTSTRAP])
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

jumbotron = dbc.Jumbotron(
    [
        html.H1("Dribble Lab", className="display-3"),
        html.P(
            "Keep your dribble and basketball skills in check!",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            "Jumbotrons use utility classes for typography and "
            "spacing to suit the larger container."
        ),
        #html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ]
)



app.layout = html.Div(children=[
    jumbotron,
    dcc.Upload(id='upload_video',children=[dbc.Button('Upload video')]),
    dbc.Card(
        dbc.CardBody([
            html.Video(id='video',src=r'assets/videos/bball14.mp4', controls=True,className = "mx-30"),
            html.Div(children='''
                Dash: A web application framework for Python.
            '''),
            dcc.Graph(
                id='graph'
            )
        ]), className = "mx-2"
    
    )
    #dbc.Card(
    #    dbc.CardBody([
    #        dcc.Graph(
    #            id='graph'
    #        )
    #    ]), className= "mx-2"

    #)

])


@app.callback([Output('video','src'),               #Change1
            Output('graph','figure')],
              [Input('upload_video', 'filename')],
              )
def update_output(file):
    if(file==None):
        raise dash.exceptions.PreventUpdate
    videos=r'assets/videos/'+ file               #get functions from da here
    print (videos)  
    points=da.videoCapture(videos)
    plots=da.plotting(points)                                #return the temp video from assets file
    temp='assets/videos/temp.mp4'
    #print (temp)  
    return videos , plots                  #Changed videos to tmep


if __name__ == '__main__':
    app.run_server(debug=False)