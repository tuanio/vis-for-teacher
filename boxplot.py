import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('cleaned_data.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

app = dash.Dash(__name__)

subjects = list(df.columns[5:-6])

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                html.Label(
                    ['Môn học'],
                    className='div-label'
                ),
            ),
            dcc.Dropdown(
                id='name_dropdown',
                options=[{'label': subject, 'value': subject} for subject in subjects],
                multi=False,
                searchable=True,
                placeholder='Tìm môn học...',
                value='Toán cao cấp 1',
                className='dropdown'
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='boxplot'
                    ),
                ],
                className='boxplot_class'
            )
        ],
        id='dropdown-menu'
    ),
    html.Div(
        [
            html.Label('Xuất danh sách sinh viên có điểm '),
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in ['>', '<', '>=', '<=', '!=', '=']],
                multi=False,
                searchable=False,
                style={'width': '200px', 'font-weight': 'bold'},
                id='input_op'
            ),
            dcc.Input(
                type='number',
                id='input_score'
            ),
            html.Div(['Số lượng sinh viên: '], id='len_test', ),
            html.Div(id='output_test')
        ],
        id='list_sv'
    )
])

@app.callback(
    Output('boxplot', 'figure'),
    [Input('name_dropdown', 'value')]
)
def generate_chart(name_dropdown):
    fig = px.box(
        df[subjects + ['Họ và tên']],
        y=name_dropdown,
        hover_data={'Họ và tên': True},
        title=name_dropdown,
        points='all'
    )
    return fig

@app.callback(
    Output('output_test', 'children'),
    Output('len_test', 'children'),
    [Input('input_op', 'value'), Input('input_score', 'value')]
)
def score(input_op, input_score):
    if (input_score == None):
        input_score = 0
    if (input_op == None):
        input_op = '>'
    ret = None
    dff = df[['Điểm 4', 'Họ và tên']]
    if (input_op == '>'):
        ret = dff[dff['Điểm 4'] > input_score]
    elif (input_op == '<'):
        ret = dff[dff['Điểm 4'] < input_score]
    elif (input_op == '>='):
        ret = dff[dff['Điểm 4'] >= input_score]
    elif (input_op == '<='):
        ret = dff[dff['Điểm 4'] <= input_score]
    elif (input_op == '='):
        ret = dff[dff['Điểm 4'] == input_score]
    elif (input_op == '!='):
        ret = dff[dff['Điểm 4'] != input_score]
    ans = []
    for i in ret.values:
        ans += [html.P('{}: {}'.format(i[1], i[0]))]
    return ans, [
            html.Label('Số lượng sinh viên có điểm tổng kết '),
            html.B(input_op),
            html.B(' ' + str(input_score)),
            html.Label(': ' + str(len(ans)))
        ]

if __name__ == '__main__':
    # ...
    app.run_server(debug=True)