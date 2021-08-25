import requests

import plotly.graph_objects as go
import plotly.io as pio

fig = go.Figure()

url = 'https://api.spacexdata.com/v4/launches/past'
r = requests.get(url)
past_launches_dict = r.json()

url = 'https://api.spacexdata.com/v4/launches/upcoming'
r = requests.get(url)
upcoming_launches_dict = r.json()

def addTrace(launches_dict):
    if launches_dict == past_launches_dict:
        name = 'Past'
        line_color = '#22272B'
        marker_color = '#4BB543'
    elif launches_dict == upcoming_launches_dict:
        name = 'Upcoming'
        line_color = '#22272B'
        marker_color = '#FFFFFF'
    else:
        name = 'Undefined'
        line_color = '#000000'
        marker_color = '#FFFFFF'

    print('Adding ' + name + ' launches')

    launch_date, launch_flight_number, launch_labels = [], [], []
    for launch_dict in launches_dict:
        launch_date.append(launch_dict['date_utc'])
        launch_flight_number.append(launch_dict['flight_number'])
        launch_name = launch_dict['name']
        launch_label = f"{launch_name}<br />Flight Number: {launch_dict['flight_number']}<br />Date: {launch_dict['date_utc']}"
        launch_labels.append(launch_label)
    fig.add_trace(
        go.Scatter(name=name, x=launch_date, y=launch_flight_number, hovertext=launch_labels, mode='markers',
                   marker=dict(
                       color=marker_color,
                       size=12,
                       line=dict(
                           color=line_color,
                           width=2
                       )
                   ), ))

addTrace(past_launches_dict)
addTrace(upcoming_launches_dict)

fig.update_layout(template='plotly_white', title="SpaceX Launches", xaxis_title="Launch Date",
    yaxis_title="Flight Number",)


pio.write_html(fig, file='spacex_launch_report.html', auto_open=True)
