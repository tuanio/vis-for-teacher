import pandas as pd
pd.options.mode.chained_assignment = None # default = 'warn'

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from functools import cmp_to_key
from flask import Flask, send_from_directory
from plotly.tools import mpl_to_plotly
import mplcursors # matplotlib hover
matplotlib.use('Agg')
from math import *

op = {
    '=': 'bang',
    '≠': 'khac',
    '≥': 'lon_hon_bang',
    '>': 'lon_hon',
    '<': 'nho_hon',
    '≤': 'nho_hon_bang'
}


diem_xeploai = {
    (9, 10) : ['A+', 'Xuất sắc'],
    (8.5, 8.9) : ['A', 'Giỏi'],
    (8, 8.4) : ['B+', 'Khá'],
    (7, 7.9) : ['B', 'Khá'],
    (6, 6.9) : ['C+', 'Trung bình'],
    (5.5, 5.9) : ['C', 'Trung bình'],
    (5, 5.4) : ['D+', 'Trung bình yếu'],
    (4, 4.9) : ['D', 'Trung bình yếu'],
    (0, 3.9) : ['F', 'Kém']
}

diem_he4 = {
    'A+': 4, 'A': 3.8,
    'B+': 3.5, 'B': 3,
    'C+': 2.5, 'C': 2,
    'D+': 1.5, 'D': 1,
    'F': 0
}

df = pd.read_csv('csv_files/cleaned_data.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

xeploai_df = pd.read_csv('csv_files/xeploai.csv')

tin_chi_df = pd.read_csv('csv_files/tin_chi.csv')

# nguồn script ở ngoài thư mục assets
external_scripts = [
    {
        'src': 'https://kit.fontawesome.com/cab3a28685.js',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js',
        'crossorigin': 'anonymous',
        'integrity':"sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0",
    }
]

external_stylesheets = [
    {
        'href':"https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css",
        'rel':"stylesheet",
        'integrity':"sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl",
        'crossorigin':"anonymous"
    }
]

server = Flask(__name__)

app = dash.Dash(server=server, external_scripts=external_scripts, external_stylesheets=external_stylesheets)

subjects = list(df.columns[5:-6])
classmate = list(df['Họ và tên'])


@server.route('/download/<path:path>')
def download(path):
    return send_from_directory('', path, as_attachment=True)

def get_xeploai(diem):
    for i in diem_xeploai.items():
        if (i[0][0] <= diem <= i[0][1]):
            return i[1]
    ok = ['NO']
    if (diem >= 250):
        ok = ['Tiếng anh 1']
        if (diem >= 350):
            ok += ['Tiếng anh 2']
        # kk and kk is like "lorem ipsum"
        ok += ['kk', 'kk']
    return ok

# số tín chỉ của sinh viên có tên là name
def so_tin_chi_sv(name):
    tin_chi = 0
    for i in df.loc[df['Họ và tên'] == name, subjects].items():
        if np.isnan(i[1].values[0]):
            continue
        xeploai = get_xeploai(i[1].values[0])
        if (xeploai[0] not in ['NO', 'F']):
            flag = True
            if (len(xeploai) >= 3):
                flag = i[0] in xeploai
            tin_chi += tin_chi_df[i[0]].values[0] * flag
    return int(tin_chi)

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
                clearable=False,
                placeholder=subjects[0],
                value=subjects[0],
                className='dropdown',
                persistence="true",
                persistence_type='session'
            ),
            html.Div(style={'height': '10px'}),
            html.Div(
                [
                    html.Button(
                        [html.I(className='fas fa-question')],
                        id='boxplot_helper',
                        type='button',
                        className='btn btn-primary dropdown-toggle',
                        **{
                            'data-bs-toggle': 'dropdown',
                            'aria-expanded': 'false'
                        }
                    ),
                    html.Div(
                        [
                            html.H4(
                                ['Các tham số'],
                                style={'textAlign': 'center'},
                            ),
                            html.Hr(className='dropdown-divider'),
                            html.P(
                                [html.B('max'), ' điểm cao nhất trong lớp'],
                            ),
                            html.P(
                                [html.B('min'), ' điểm thấp nhất trong lớp'],
                            ),
                            html.P(
                                [html.B('median(điểm giữa)'), ' mức điểm chia điểm của lớp thành 2 nửa'],
                            ),
                            html.P(
                                [html.B('q1 (tứ phân vị dưới)'), ' 75% điểm của lớp nằm dưới mức điểm này'],
                            ),
                            html.P(
                                [html.B('q3 (tứ phân vị trên)'), ' 25% điểm của lớp nằm dưới mức điểm này'],
                            ),
                            html.P(
                                [html.B('xếp thứ tự'), ' thứ tự của sinh viên trong danh sách điểm của lớp'],
                            ),
                            html.Hr(className='dropdown-divider'),
                            html.H6('IQR là độ trải giữa, phần lớn điểm tập trung ở miền này'),
                            html.H6('lower/upper fence là hàng rào để loại bỏ ngoại lệ khỏi phần lớn dữ liệu'),
                            html.P(
                                [
                                    html.Img(src='assets/imgs/iqr_formula.png')
                                ],
                            ),
                            html.P(
                                [
                                    html.Img(src='assets/imgs/lower_fence_formula.png')
                                ],
                            ),
                            html.P(
                                [
                                    html.Img(src='assets/imgs/upper_fence_formula.png')
                                ],
                            ),
                        ],
                        className='dropdown-menu p-4',
                        style={
                            'fontSize': '14px', 
                            'max-width': '320px', 
                            'overflowWrap': 'break-word', 
                            'boxShadow': '2px 2px 5px 0 #585959'
                        },
                        **{'aria-labelledby': 'boxplot_helper'},
                    )
                ],
                className='dropdown'
            ),
            html.Div(style={'height': '5px'}),
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
                    html.Div(
                        [
                            html.Div(
                                'Danh sách sinh viên có điểm', 
                                style={
                                    'paddingTop': '5px',
                                    'fontWeight': 'bold'
                                }
                            ),
                            html.Div(style={'width': '10px'}),
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in ['>', '<', '≥', '≤', '≠', '=']],
                                multi=False,
                                searchable=False,
                                value='≥',
                                placeholder='≥',
                                clearable=False,
                                id='input_op',
                                persistence="true",
                                persistence_type='session'
                            ),
                            html.Div(style={'width': '10px'}),
                            dcc.Input(
                                type='number',
                                id='input_score',
                                placeholder='0',
                                className='form-control',
                                style={'width': '70px'},
                                persistence="true",
                                persistence_type='session',
                                min='1',
                                max='10'
                            ),
                            html.Div(style={'width': '10px'}),
                            html.Div(id='download-btn')
                        ],
                        style={
                            'display': 'flex',
                            'padding': '7px 0px'
                        }
                    ),
                    html.Div(style={'height': '10px'}),
                    html.Div('',id='percent_of_class'),
                    html.Div(style={'height': '10px'}),
                    html.Div(id='output_test')
                ],
                className='show-table',
                style={'width': '40%'}
            ),
            html.Div(style={'width': '10px'}),
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                options=[{'label': i, 'value': i} for i in classmate],
                                multi=False,
                                searchable=True,
                                value=classmate[0],
                                placeholder=classmate[0],
                                clearable=False,
                                id='input_name',
                                persistence="true",
                                persistence_type='session'
                            ),
                        ],
                        className='btn',
                        style={'width': '400px'}
                    ),
                    html.Div(style={'height': '10px'}),
                    html.Img(id='bar_chart', alt='ok')
                ],
                style={
                    'width': '410px', 
                }
            )
        ],
        style={"display": "flex"},
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

    # dropdown_chart = df[subjects + ['Họ và tên']]
    dropdown_chart = df[subjects + ['Họ và tên']].sort_values(by=name_dropdown, ascending=False).reset_index().copy()
    dropdown_chart['Xếp thứ tự'] = np.arange(1, len(dropdown_chart) + 1)
    for i in range(1, len(dropdown_chart)):
        if (dropdown_chart.loc[i - 1, name_dropdown] == dropdown_chart.loc[i, name_dropdown]):
            dropdown_chart['Xếp thứ tự'][i] = dropdown_chart['Xếp thứ tự'][i - 1]

#    Trực quan cái boxplot
    fig_boxplot = px.box(
        dropdown_chart,
        y=name_dropdown,
        hover_data={'Họ và tên': True, 'Xếp thứ tự': True},
        title='Tổng quát điểm, thứ tự sinh viên',
        points='all'
    )

    # center the title
    fig_boxplot.update_layout(title_x=0.5)

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
        title='Số lượng mỗi xếp loại'
    )

    # center the title
    fig_bar.update_layout(title_x=0.5)

    # Trả về 1 tuple có 2 phần tử là 2 output
    return fig_boxplot, fig_bar

@app.callback(
    Output('output_test', 'children'),
    Output('download-btn', 'children'),
    Output('percent_of_class', 'children'),
    [Input('input_op', 'value'), Input('input_score', 'value')]
)
def score(input_op, input_score):
    if (input_score == None):
        input_score = 0
    if (input_op == None):
        input_op = '>'
    ret = None
    dff = df[['Mã sinh viên', 'Họ và tên', 'Điểm 4']]
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

    ret_df = pd.DataFrame(columns=['Mã SV', 'Họ và tên', 'Điểm tổng kết 3 kỳ'])

    for i in ret.values:
        ret_df = pd.concat([ret_df, pd.DataFrame({'Mã SV': i[0], 'Họ và tên': i[1], 'Điểm tổng kết 3 kỳ': i[2]}, index=[0])], ignore_index=True)

    percent = ''

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
                            ) for i in ['#', 'Mã SV', 'Họ và tên', 'Điểm tổng kết 3 kỳ']
                        ],
                    ) 
                ]),   
                html.Tbody(
                    [
                        html.Tr([
                            html.Td(i + 1),
                            html.Td(j[0]),
                            html.Td(j[1]),
                            html.Td(j[2])
                        ]) for i, j in zip(range(len(ret.values)), ret.values)
                    ],
                ),
            ],
            className='table table-sm table-hover',
        )
    
    percent = 'Tỉ lệ sinh viên thỏa truy vấn so với lớp: {}%'.format(round(len(ret.values) / len(classmate) * 100, 2))
    
    # filename = 'csv_files/danhsach_sv_{}_{}.xlsx'.format(op[input_op], input_score)
    filename = 'csv_files/list_student.xlsx'

    ret_df.to_excel(filename)

    download_list_link = html.A(
                            [html.I(className='fas fa-file-download')], 
                            href='/download/{}'.format(filename), 
                            className='btn btn-outline-success',
                        )
    return ans, download_list_link, percent

@app.callback(
    Output('bar_chart', 'src'),
    [Input('input_name', 'value')]
)
def stacked_bar(input_name):

    tin_chi_tb_lop_ds = ceil(np.array([so_tin_chi_sv(i) for i in classmate]).mean())

    foo = [so_tin_chi_sv(input_name), tin_chi_tb_lop_ds]
    bar = [142 - i for i in foo]

    width = 0.5
    ind = np.arange(2)

    fig, ax = plt.subplots(figsize=(4, 5))

    bar1 = plt.bar(ind, foo, width, label='Đã học', edgecolor='black', color='#06BEE1')
    bar2 = plt.bar(ind, bar, width, bottom=foo, label='Chưa học', edgecolor='black', color='#FFFFFF')

    # Thêm chữ cho bar chart
    def auto_label(rects, flag):
        for idx, rect in enumerate(rects):
            height = rect.get_height()
            x = idx
            if (flag):
                data = foo
                y = (rect.get_y() + rect.get_height()) / 2
            else:
                data = bar
                y = (rect.get_y() + 142) / 2
            ax.text(
                x, y,
                data[idx],
                ha='center',
                va='bottom',
                fontsize=12
            )

    auto_label(bar1, True)
    auto_label(bar2, False)

    plt.xticks(ind, [input_name, 'Trung bình lớp K15DS'], fontsize=10)
    fig.suptitle('Số tín chỉ đã tích lũy của ' + input_name, fontsize=12)
    plt.legend(loc='upper center')
    input_name = input_name.replace(' ', '')
    fig.savefig('assets/stacked_barchart/{}.png'.format(input_name))
    plt.close()
    ret =  app.get_asset_url('stacked_barchart/{}.png'.format(input_name))
    return ret

if __name__ == '__main__':
    app.run()