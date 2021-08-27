import requests

import plotly.graph_objects as go
import plotly.io as pio
import textwrap

fig = go.Figure()

url = 'https://api.spacexdata.com/v4/launchpads'
r = requests.get(url)
launchpads_dict = r.json()

def addTrace(launchpads_dict):
    print('Generating map of launchpads..')

    launchpad_labels, launchpad_status, launchpad_longitude, launchpad_latitude = [], [], [], []
    for launchpad_dict in launchpads_dict:
        launchpad_status.append(launchpad_dict['status'])
        launchpad_longitude.append(launchpad_dict['longitude'])
        launchpad_latitude.append(launchpad_dict['latitude'])
        launchpad_name = launchpad_dict['name']
        launchpad_label = f"{launchpad_name}<br />{launchpad_dict['full_name']}"
        launchpad_labels.append(launchpad_label)

    fig.add_trace(
        go.Scattergeo(
            lon=launchpad_longitude,
            lat=launchpad_latitude,
            text=launchpad_status,
            mode='markers',
            hovertext=launchpad_labels,
            marker=dict(
                color='#4BB543',
                size=12,
                line=dict(
                    color='#000000',
                    width=2
                )
            ),
        )
    )

print(launchpads_dict)
addTrace(launchpads_dict)

fig.update_layout(
    title='SpaceX Launchpads',
    geo_scope='world',
)
fig.show()

pio.write_html(fig, file='spacex_launch_report.html', auto_open=True)
