from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_ui as dui
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

app = Dash()
app.config['suppress_callback_exceptions'] = True
my_css_urls = [
  "https://codepen.io/rmarren1/pen/mLqGRg.css",
]

for url in my_css_urls:
    app.css.append_css({
        "external_url": url
    })

controlpanel = dui.ControlPanel(_id="controlpanel")
controlpanel.create_group(
    group="State",
    group_title="Change the selected State."
)
state_select = dcc.Dropdown(
    id="state-dropdown",
    options=[{
        'label': x.title(),
        'value': x
        } for x in df["state"].tolist()
    ],
    value=df["state"].tolist()[0]
)
controlpanel.add_element(state_select, "State")

controlpanel.create_group(
    group="Another",
    group_title="Another option group."
)
another = dcc.Dropdown(
    id="another-element",
    options=[{
        'label': "example",
        'value': "show"
        }
    ],
    value="show"
)
controlpanel.add_element(html.P("Here is another group"), "Another")
controlpanel.add_element(another, "Another")

controlpanel.create_group(
    group="Third",
    group_title="A third option group"
)
third = dcc.RadioItems(
    id="third-element",
    options=[
        {
            'label': "example",
            'value': "show"
        },
        {
            'label': "example2",
            'value': "show2"
        },
    ],
    value="show2"
)
controlpanel.add_element(third, "Third")

grid = dui.Grid(
    _id="grid",
    num_rows=12,
    num_cols=12,
    grid_padding=10
)


grid.add_graph(col=1, row=1, width=12, height=4, graph_id="all-bar")
grid.add_graph(col=1, row=5, width=12, height=4, graph_id="total-exports-bar")

grid.add_graph(col=1, row=9, width=4, height=4, graph_id="all-pie")
grid.add_graph(col=5, row=9, width=4, height=4, graph_id="produce-pie")
grid.add_graph(col=9, row=9, width=4, height=4, graph_id="animal-pie")


app.layout = dui.Layout(
    grid=grid,
    controlpanel=controlpanel
)


@app.callback(Output('total-exports-pie', 'figure'),
              [Input('state-dropdown', 'value')])
def create_total_exports_pie(state):
    trace = go.Pie(
        labels=df['state'],
        values=df['total exports'],
        textinfo='none',
        marker=dict(
            colors=['red' if x == state else 'grey' for x in df['state']]
        ))
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'title':
        "{:s}'s proportion of total US agriculture exports".format(state)
    })


@app.callback(Output('total-exports-bar', 'figure'),
              [Input('state-dropdown', 'value')])
def create_total_exports_bar(state):
    my_df = df.sort_values('total exports', ascending=False)
    trace = go.Bar(
        x=my_df['state'],
        y=my_df['total exports'],
        marker=dict(
            color=['red' if x == state else 'grey' for x in my_df['state']]
        ))
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'autosize': True,
        'title':
        "{:s}'s agriculture exports vs. other states".format(state)
    })


@app.callback(Output('produce-pie', 'figure'),
              [Input('state-dropdown', 'value')])
def create_produce_pie(state):
    produce_vars = ["total fruits", "total veggies", "corn", "wheat"]
    row = df[df["state"] == state].iloc[0]
    trace = go.Pie(
        labels=produce_vars,
        textinfo="label+percent",
        values=[row[v] for v in produce_vars])
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'title':
        "{:s}'s produce distribution".format(state)
    })


@app.callback(Output('animal-pie', 'figure'),
              [Input('state-dropdown', 'value')])
def create_animal_pie(state):
    animal_vars = ["beef", "pork", "poultry", "dairy"]
    row = df[df["state"] == state].iloc[0]
    trace = go.Pie(
        labels=animal_vars,
        textinfo="label+percent",
        values=[row[v] for v in animal_vars])
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'title':
        "{:s}'s animal product distribution".format(state),
    })


@app.callback(Output('all-pie', 'figure'),
              [Input('state-dropdown', 'value')])
def create_all_pie(state):
    vs = list(set(df.columns) - {"Unnamed: 0", "total exports", "state"})
    row = df[df["state"] == state].iloc[0]
    trace = go.Pie(
        labels=vs,
        textinfo="label+percent",
        values=[row[v] for v in vs])
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'title':
        "{:s}'s agriculture distribution".format(state)
    })


@app.callback(Output('all-bar', 'figure'),
              [Input('state-dropdown', 'value')])
def create_all_bar(state):
    vs = list(set(df.columns) - {"Unnamed: 0", "total exports", "state"})
    row = df[df["state"] == state].iloc[0]
    trace = go.Bar(
        x=vs,
        y=[row[v] for v in vs])
    return go.Figure(data=[trace], layout={
        'showlegend': False,
        'title':
        "{:s}'s agriculture distribution".format(state)
    })
if __name__ == "__main__":
    app.run_server(debug=True)
