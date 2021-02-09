import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from functools import cmp_to_key
import numpy as np

df = pd.read_csv('cleaned_data.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

xeploai_df = pd.read_csv('xeploai.csv')

# nguồn script ở ngoài thư mục assets
external_scripts = [
    {
        'src': 'https://kit.fontawesome.com/cab3a28685.js',
        'crossorigin': 'anonymous'
    },
]

app = dash.Dash(__name__, external_scripts=external_scripts)

subjects = list(df.columns[5:-6])

app.layout = html.Div([
    html.Div(
        [
            html.Marquee(
                'Huỳnh Minh Toàn đang xếp thứ I trong lớp Lập trình phân tích dữ liệu\
                Phạm Thành Trung đang đứng ở top đầu lớp Thống Kê máy tính và ứng dụng. Nguyễn Văn Anh Tuấn có tiềm năng thoát top 1 từ dưới lên',
                className='btn btn-warning'
            ),
            html.Div(style={'height': '10px'}),
            dcc.Dropdown(
                id='name_dropdown',
                options=[{'label': subject, 'value': subject} for subject in subjects],
                multi=False,
                searchable=True,
                placeholder='Toán cao cấp 1',
                value='Toán cao cấp 1',
                className='dropdown'
            ),
            html.Div(style={'height': '10px'}),
            html.Div(
                [
                    dcc.Graph(id='boxplot'),
                    dcc.Graph(id='bar_xeploai')
                ],
                style={'display': 'flex'},
                className='boxplot_class'
            )
        ],
        id='dropdown-menu'
    ),
    html.Div(
        [
            html.Div(
                [
                    html.Div('Danh sách sinh viên có điểm', style={'padding-top': '5px'}),
                    html.Div(style={'width': '10px'}),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in ['>', '<', '≥', '≤', '≠', '=']],
                        multi=False,
                        searchable=False,
                        value='≥',
                        placeholder='≥',
                        clearable=False,
                        id='input_op',
                    ),
                    html.Div(style={'width': '10px'}),
                    dcc.Input(
                        type='number',
                        id='input_score',
                        placeholder='0',
                        className='form-control',
                        style={'width': '70px'}
                    ),
                    html.Div(style={'width': '10px'}),
                    html.A(
                        [html.I(className='fas fa-file-download')], 
                        href='xeploai.csv', 
                        className='btn btn-outline-success',
                    )
                ],
                style={'display': 'flex', 'padding': '7px 0px'}
            ),
            html.Div(style={'height': '10px'}),
            html.Div(id='output_test', style={'width': '40%'})
        ],
        id='list_sv'
    )
], className='container')

# Hàm compare dùng để sắp xếp
# -1 if o1 < o2
# 1 if o1 > o2
# 0 if o1 == o2
def compare(o1, o2):
    o1 = o1[0]
    o2 = o2[0]
    try:
        o1[0]
        o2[0]
    except:
        return 0
    if (o1[0] == o2[0]):
        return [1, -1][len(o1) == 2]
    return [1, -1][o1[0] < o2[0]]

@app.callback(
    Output('boxplot', 'figure'),
    Output('bar_xeploai', 'figure'),
    [Input('name_dropdown', 'value')]
)
def generate_chart(name_dropdown):

    # Trực quan cái boxplot
    fig_boxplot = px.box(
        df[subjects + ['Họ và tên']],
        y=name_dropdown,
        hover_data={'Họ và tên': True},
        title=name_dropdown,
        points='all'
    )

    # Đếm
    data_score = Counter(xeploai_df[name_dropdown])
    
    # Loại bỏ nan khỏi data sau khi đếm
    if np.nan in data_score:
        data_score.pop(np.nan)

    # Sắp xếp giảm dần theo key
    data_score = {i[0] : i[1] for i in sorted(Counter(xeploai_df[name_dropdown]).items(), key=cmp_to_key(compare)) if i[0] != np.nan}
    
    # Chuyển dữ liệu đếm thành một dataframe
    data_score_df = pd.DataFrame({
        'Xếp loại': data_score.keys(),
        'Số lượng': data_score.values()
    })

    data_score_df = data_score_df[data_score_df['Xếp loại'] != np.nan]

    # Trực quan hóa
    fig_bar = px.bar(
        data_frame=data_score_df,
        x='Xếp loại',
        y='Số lượng',
    )

    # Trả về 1 tuple có 2 phần tử là 2 output
    return fig_boxplot, fig_bar

@app.callback(
    Output('output_test', 'children'),
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
    elif (input_op == '≥'):
        ret = dff[dff['Điểm 4'] >= input_score]
    elif (input_op == '≤'):
        ret = dff[dff['Điểm 4'] <= input_score]
    elif (input_op == '='):
        ret = dff[dff['Điểm 4'] == input_score]
    elif (input_op == '≠'):
        ret = dff[dff['Điểm 4'] != input_score]
    if (len(ret.values) == 0):
        ans = html.Div(
            ['Không có sinh viên nào thỏa truy vấn!'],
            role='alert',
            className='alert alert-warning'
        ) 
    else:
        ans = html.Table([
                html.Thead([
                    html.Tr(
                        [
                            html.Th(
                                [i],
                                scope='row',
                            ) for i in ['#', 'Họ và tên', 'Điểm tổng kết 3 kỳ']
                        ],
                    ) 
                ]),   
                html.Tbody(
                    [
                        html.Tr([
                            html.Th(i, scope='row'),
                            html.Td(j[1]),
                            html.Td(j[0])
                        ]) for i, j in zip(range(len(ret.values)), ret.values)
                    ],
                ),
            ],
            className='table table-sm table-hover',
        )
    return ans

if __name__ == '__main__':
    # ...
    app.run_server(debug=True)