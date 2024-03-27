import pandas as pd
import plotly.express as px
from dash import Dash, dcc, ctx, html, Input, Output
import dash_bootstrap_components as dbc

PATH = 'MoscowRegion2024.csv'

vot_pot = 'Число избирателей, включенных в список избирателей'
vot_uik = 'Число избирательных бюллетеней, выданных в помещении для голосования в день голосования'
vot_home = 'Число избирательных бюллетеней, выданных вне помещения для голосования в день голосования'
vot_real_uik = 'Число бюллетеней в стационарных ящиках для голосования'
vot_real_home = 'Число избирательных бюллетеней в переносных ящиках для голосования'
noone = 'Число недействительных избирательных бюллетеней'
davankov = 'Даванков Владислав Андреевич'
putin = 'Путин Владимир Владимирович'
ldpr = 'Слуцкий Леонид Эдуардович'
kprf = 'Харитонов Николай Михайлович'

tik = 'ТИК'
abscissa = 'Явка'
ordinate = 'Путин Владимир Владимирович (%)'
graf_name = 'Московская область 2024. Собянина-Суховольского'

koib_name = 'koib.txt'
koib_row = 'КОИБ'

color_row = koib_row

def calc_prsnt(n):
    return (df[vot_uik][n] + df[vot_home][n]) / df[vot_pot][n] * 100

def get_uik_nom(s):
    start = len('УИК №')
    return int(s[start::])



df = pd.read_csv(PATH)
df['Явка'] = [calc_prsnt(i) for i in range(len(df[vot_pot]))]
df[color_row] = [get_uik_nom(df['УИК'][i]) in koib for i in range(len(df[vot_pot]))]

df.to_csv('МосковскаяОбласть2024.csv')

scale = 2
current_df = df
pt_color = None

fig = px.scatter(current_df, x=abscissa, y=ordinate,
                 title=graf_name, hover_name='УИК', color=pt_color,
                 range_x=[40, 100], range_y=[40, 100],
                 width=800, height=800)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row(html.H4('Выборы Президента России. Данные - Иван Шукшин'), style={'textAlign': 'center', 'margin-top': '40px'}),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="scatter-plot")
        ]),
        dbc.Col([
            html.Div(className='column', style={'textAlign': 'center', 'margin-top': '100px'}, children=[
                html.P("Территориальная комиссия"),
                dcc.Dropdown(
                    ['all'] + sorted(list(set(df[tik]))),
                    'all',
                    id='dropdown'
                ),
                dcc.Checklist(
                    [' Обозначить КОИБ'],
                    id='checkbox',
                    style={'margin-top' : '10px', 'margin-bottom' : '10px'}
                ),
                html.P("Размер точек"),
                dcc.Slider(
                    id='slider',
                    min=0, max=10, step=0.1,
                    marks={0: '0', 1.0: '1.0', 2.0: '2.0', 10.0: '10.0'},
                    value=scale
                )
            ])
        ])
    ])
])

@app.callback(
    Output("scatter-plot", "figure"),
    Input("dropdown", "value"),
    Input("slider", "value"),
    Input("checkbox", "value"))
def update_output(b1, b2, b3):
    global current_df, scale, pt_color
    triggered_id = ctx.triggered_id
    if triggered_id == 'dropdown':
        current_df = update_tik(b1)
    elif triggered_id == 'slider':
        scale = update_bar_chart(b2)
    elif triggered_id == 'checkbox':
        pt_color = koib_check(b3)

    fig = px.scatter(current_df, x=abscissa, y=ordinate,
                     title=graf_name, hover_name='УИК', color=pt_color,
                     range_x = [40, 100], range_y=[40, 100],
                     width=800, height=800
                     # size=vot_pot, size_max=10.0
                     )
    fig.update_traces(marker_size=scale)

    return fig

def update_tik(sort_param):
    if sort_param == 'all':
        return df
    return df[df[tik] == sort_param]
def update_bar_chart(slider_val):
    return slider_val
def koib_check(koib_val):
    if koib_val:
        return color_row
    else:
        return None


app.run_server(debug=True)
