# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
csv_file="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(csv_file)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites=['CCAFS LC-40','VAFB SLC-4E','KSC LC-39A','CCAFS SLC-40']

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'All Sites'},
                                                                         {'label': launch_sites[0], 'value': launch_sites[0]},
                                                                         {'label': launch_sites[1], 'value': launch_sites[1]},
                                                                         {'label': launch_sites[2], 'value': launch_sites[2]},
                                                                         {'label': launch_sites[3], 'value': launch_sites[3]},
                                                                         ],value='All Sites',placeholder='Select a Launch Site'), 
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (1000 Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=min_payload, max=max_payload, value=[min_payload, max_payload], id='payload-slider'),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def update_input_container(launch_site_selection):
    if (launch_site_selection == 'All Sites'):
        pie_df=spacex_df.groupby('Launch Site')[['class']].sum().reset_index()
        labels=pie_df['Launch Site'].tolist()
        fig=px.pie(pie_df,values='class',names=labels,labels={'label':'Launch Site','class': 'Successful Landings'},title="Percentage of Successful Landings per Launch Site")
        return fig
    else: 
        pie_df=spacex_df.loc[spacex_df['Launch Site'] == launch_site_selection].groupby('class')['class'].count().reset_index(name='count')
        fig=px.pie(pie_df,values='count',names=pie_df['class'].tolist(),title="Percentage of Successful Landings from {}".format(launch_site_selection))
        return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')])

def dickbutt(launch_site_selection,slider_value):
    print(launch_site_selection,slider_value)
    if (launch_site_selection == 'All Sites'):
        mass_df=spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= slider_value[0]) & (spacex_df['Payload Mass (kg)'] <= slider_value[1])]
        fig=px.scatter(data_frame=mass_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation Between Payload Mass and Success for All Sites')
        return fig
    else: 
        mass_df=spacex_df.loc[(spacex_df['Payload Mass (kg)'] >= slider_value[0]) & (spacex_df['Payload Mass (kg)'] <= slider_value[1]) & (spacex_df['Launch Site'] == launch_site_selection)]
        fig=px.scatter(data_frame=mass_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation Between Payload Mass and Success for {}'.format(launch_site_selection))
        return fig
    return
# Run the app
PORT=8080
ADDRESS="192.168.0.13"
if __name__ == '__main__':
    app.run(host=ADDRESS,port=PORT)
    app.run_server(debug=True)