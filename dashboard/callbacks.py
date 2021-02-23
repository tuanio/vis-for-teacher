from dash.dependencies import Output, Input
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from math import ceil
from functools import cmp_to_key
import matplotlib
import matplotlib.pyplot as plt
import os

pd.options.mode.chained_assignment = None # default 'warn'
matplotlib.use('Agg')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dashboard import app
import dashboard.datas as datas
from dashboard.datas import *
from dashboard.tools import *

datas.init()

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
        points='all',
        width=datas.size_plot['boxplot'][0],
        height=datas.size_plot['boxplot'][1],
        color_discrete_sequence=[color]
    )

    fig_boxplot.update_layout(
        title='Tổng quát điểm, thứ tự sinh viên',
        xaxis_title=name_dropdown,
        yaxis_title='Thang điểm',
    )

    # center the title
    fig_boxplot.update_layout(title_x=0.5)
    fig_boxplot.update_layout(hovermode="closest")

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
        title='Số lượng mỗi xếp loại',
        width=datas.size_plot['bar_xeploai'][0],
        height=datas.size_plot['bar_xeploai'][1],
        color_discrete_sequence=[color]
    )

    # center the title
    fig_bar.update_layout(title_x=0.5)
    # fig_bar.update_layout(hovermode="y")

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
    filename = 'dashboard/csv_files/list_student.xlsx'

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
    bar = [146 - i for i in foo]

    width = 0.5
    ind = np.arange(2)

    fig, ax = plt.subplots(figsize=(4, 4))

    bar1 = plt.bar(ind, foo, width, label='Đã học', edgecolor='black', color=color)
    bar2 = plt.bar(ind, bar, width, bottom=foo, label='Chưa học', edgecolor='black', color='#FFFFFF')

    # Thêm chữ cho bar chart
    def auto_label(rects, flag):
        for x, rect in enumerate(rects):
            if (flag):
                data = foo
                y = (rect.get_y() + rect.get_height()) / 2
            else:
                data = bar
                y = (rect.get_y() + 142) / 2
            ax.text(
                x, y,
                data[x],
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
    cwd = os.getcwd()
    fig.savefig('dashboard/assets/stacked_barchart/{}.png'.format(input_name))
    plt.close()
    ret =  app.get_asset_url('stacked_barchart/{}.png'.format(input_name))
    return ret