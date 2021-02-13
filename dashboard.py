import pandas as pd
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

df = pd.read_csv('cleaned_data.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

xeploai_df = pd.read_csv('xeploai.csv')

tin_chi_df = pd.read_csv('tin_chi.csv')

# nguồn script ở ngoài thư mục assets
external_scripts = [
    {
        'src': 'https://kit.fontawesome.com/cab3a28685.js',
        'crossorigin': 'anonymous'
    },
]

server = Flask(__name__)

app = dash.Dash(server=server, external_scripts=external_scripts)

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
            ok = ['Tiếng anh 2']
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
            tin_chi += tin_chi_df[i[0]].values[0]
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
                placeholder='Toán cao cấp 1',
                value='Toán cao cấp 1',
                className='dropdown',
                persistence=True,
                persistence_type='session'
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
                                persistence=True,
                                persistence_type='session'
                            ),
                            html.Div(style={'width': '10px'}),
                            dcc.Input(
                                type='number',
                                id='input_score',
                                placeholder='0',
                                className='form-control',
                                style={'width': '70px'},
                                persistence=True,
                                persistence_type='session'
                            ),
                            html.Div(style={'width': '10px'}),
                            html.Div(id='download-btn')
                        ],
                        style={'display': 'flex', 'padding': '7px 0px'}
                    ),
                    html.Div(style={'height': '10px'}),
                    html.Div(id='output_test')
                ],
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
                                value='Nguyễn Văn Anh Tuấn',
                                placeholder='Nguyễn Văn Anh Tuấn',
                                clearable=False,
                                id='input_name',
                                persistence=True,
                                persistence_type='session'
                            ),
                        ],
                        className='btn',
                        style={'width': '400px'}
                    ),
                    html.Div(style={'height': '10px'}),
                    html.Img(id='bar_chart', alt='ok')
                ],
                style={'width': '400px'}
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
    Output('download-btn', 'children'),
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
                            html.Th(i, scope='row'),
                            html.Td(j[0]),
                            html.Td(j[1]),
                            html.Td(j[2])
                        ]) for i, j in zip(range(len(ret.values)), ret.values)
                    ],
                ),
            ],
            className='table table-sm table-hover',
        )
    
    # filename = 'csv_files/danhsach_sv_{}_{}.xlsx'.format(op[input_op], input_score)
    filename = 'list_student.xlsx'

    ret_df.to_excel(filename)

    download_list_link = html.A(
                            [html.I(className='fas fa-file-download')], 
                            href='/download/{}'.format(filename), 
                            className='btn btn-outline-success',
                        )
    return ans, download_list_link

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

    bar1 = plt.bar(ind, foo, width, label='Đã học', edgecolor='black', color='#F1FFFA')
    bar2 = plt.bar(ind, bar, width, bottom=foo, label='Chưa học', edgecolor='black', color='#D5C7BC')

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

    plt.xticks(ind, [input_name, 'Trung bình lớp K15DS'], fontsize=9)
    fig.suptitle('Số tín chỉ đã học của ' + input_name, fontsize=11)
    plt.legend(loc='upper center')
    fig.savefig('assets/stacked_barchart/{}.png'.format(input_name))
    plt.close()
    return app.get_asset_url('stacked_barchart/{}.png'.format(input_name))

if __name__ == '__main__':
    app.run_server(debug=True)