import pandas as pd
import plotly.express as px
from dash import Dash, dcc, ctx, html, Input, Output

PATH = 'MoscowRegion2024.csv'

vot_pot = 'Число избирателей, включенных в список избирателей'
vot_uik = 'Число избирательных бюллетеней, выданных в помещении для голосования в день голосования'
vot_home = 'Число избирательных бюллетеней, выданных вне помещения для голосования в день голосования'
tik = 'ТИК'
abscissa = 'Явка'
ordinate = 'Путин Владимир Владимирович (%)'
graf_name = 'Московская область 2024. Метод Шпилькина'

def calc_prsnt(n):
    return (df[vot_uik][n] + df[vot_home][n]) / df[vot_pot][n] * 100

df = pd.read_csv(PATH)
df['Явка'] = [calc_prsnt(i) for i in range(len(df[vot_pot]))]

scale = 2
current_df = df

fig = px.scatter(current_df, x = abscissa, y = ordinate, title=graf_name)



app = Dash(__name__)
app.layout = html.Div([
    html.H4('Выборы Президента России. Данные - Иван Шукшин'),
    dcc.Graph(id="scatter-plot"),
    html.P("Размер точек"),
    dcc.Slider(
        id='slider',
        min=0, max=10, step=0.1,
        marks={0: '0', 1.0: '1.0', 2.0: '2.0', 10.0: '10.0'},
        value=scale
    ),
    dcc.Dropdown(
        ['all'] + sorted(list(set(df[tik]))),
        'all',
        id='dropdown'
    )
])

@app.callback(
    Output("scatter-plot", "figure"),
    Input("dropdown", "value"),
    Input("slider", "value"))
def update_output(b1, b2):
    global current_df, scale
    triggered_id = ctx.triggered_id
    if triggered_id == 'dropdown':
        current_df = update_tik(b1)
    elif triggered_id == 'slider':
        scale = update_bar_chart(b2)

    fig = px.scatter(current_df, x=abscissa, y=ordinate, title=graf_name)
    fig.update_traces(marker_size=scale)

    return fig

def update_tik(sort_param):
    if sort_param == 'all':
        return df
    return df[df[tik] == sort_param]
def update_bar_chart(slider_val):
    return slider_val


app.run_server(debug=True)