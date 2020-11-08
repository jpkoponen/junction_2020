# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data_interface import DataInterface

CUSTOMER_ID = 189

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

di = DataInterface()
di.load_transactions()

print(di.neighbours_pie_data.dtypes)
my_pie = px.pie(di.my_pie_data, names='names', values='values',
                        color_discrete_map=di.my_pie_colors, color='names', title="Your expenditure")
neighbours_pie = px.pie(di.neighbours_pie_data, names='names', values='values', labels='names',
                        color_discrete_map=di.neighbours_pie_colors, color='names', title="Peers' expenditure")
# my_pie = go.Figure(data=[go.Pie(labels=di.my_pie_data['names'], values=di.my_pie_data['values'], marker={'colors': di.my_pie_colors},
#                 title='Your expenditure')])
print(di.my_pie_colors)
print(di.neighbours_pie_colors)
cat = 'Asuminen'
histogram_data, colors = di.to_histogram_data('Asuminen')
histogram = go.Figure(data=[go.Bar(x=histogram_data[1], y=histogram_data[0], marker_color=colors)],
                      layout={'title': cat, 'xaxis_title': '€ / month', 'yaxis_title': 'Number of peers', 'bargap': 0})
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[

    html.Div([
        html.Div([
            dcc.Graph(
                id='my_pie',
                figure=my_pie
            ),
        ], className="six columns"),

        html.Div([
            dcc.Graph(
                id='neighbours_pie',
                figure=neighbours_pie
            ),
        ], className="six columns"),
    ]),

    html.Div([
        html.Div('?'),
        dcc.Graph(
            id='histogram',
            figure=histogram
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=False)