import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None # default 'warn'

import dash
import dash_core_components as dcc
import dash_html_components as html

from dashboard import app
import dashboard.datas as datas
from dashboard.datas import *
from dashboard.tools import compare, so_tin_chi_sv

from dashboard.callbacks import *

datas.init()

app.layout = html.Div([
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                        
                            html.Div(
                                html.Img(
                                    src='assets/imgs/logo_iuh.png',
                                    className='img-thumbneil float-left logo-img logo-img-iuh',
                                ),
                                id='logo-iuh',
                                className='logo'
                            ),
                            html.Div(
                                html.Img(
                                    src='assets/imgs/logo_k15ds.png',
                                    className='img-thumbneil float-left logo-img logo-img-k15ds',
                                ),
                                id='logo-k15ds',
                                className='logo'
                            ),
                        ],
                        id='header'
                    ),
                    html.Marquee(
                        'Huỳnh Minh Toàn đang xếp thứ I trong lớp Lập trình phân tích dữ liệu\
                        Phạm Thành Trung đang đứng ở top đầu lớp Thống Kê máy tính và ứng dụng. Nguyễn Văn Anh Tuấn có tiềm năng thoát top 1 từ dưới lên',
                        className='btn btn-success'
                    ),
                ],
            ),
            html.Div(style={'height': '10px'}),
            html.Div(
                [
                    html.Div(
                        [
                            html.Button(
                                [html.I(className='fas fa-question')],
                                id='boxplot_helper',
                                type='button',
                                className='btn btn-success dropdown-toggle',
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
                                        [html.B('q1 (tứ phân vị dưới)'), ' 25% điểm của lớp nằm dưới mức điểm này'],
                                    ),
                                    html.P(
                                        [html.B('q3 (tứ phân vị trên)'), ' 75% điểm của lớp nằm dưới mức điểm này'],
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
                                    'maxWidth': '320px', 
                                    'overflowWrap': 'break-word', 
                                    'boxShadow': '2px 2px 5px 0 #585959'
                                },
                                **{'aria-labelledby': 'boxplot_helper'},
                            )
                        ],
                        className='dropdown'
                    ),
                    html.Div(style={'width': '10px'}),
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
                        persistence_type='session',
                        style={'width': '100%'},
                    ),
                ],
                style={'display': 'flex'}
            ),
            html.Div(style={'height': '10px'}),
            html.Div(style={'height': '5px'}),
            html.Div(
                [
                    html.Div(
                        dcc.Graph(
                            id='boxplot',
                            config={'modeBarButtonsToRemove': ['pan2d', "select2d", "lasso2d", "zoomIn2d",
                                "zoomOut2d", "autoScale2d", 'toggleSpikelines'],
                                "scrollZoom": True,
                                "displaylogo": False
                            }
                        ),
                        id='div-boxplot',
                        className='graph-1 graph-boxplot graph'
                    ),
                    html.Div(
                        dcc.Graph(
                            id='bar_xeploai',
                            config={'modeBarButtonsToRemove': ['pan2d', "select2d", "lasso2d", "zoomIn2d",
                                "zoomOut2d", "autoScale2d", 'toggleSpikelines', 'hoverCompareCartesian'],
                                "displaylogo": False
                            }
                        ),
                        id='div-bar-xeploai',
                        className='graph-1 graph-bar-xeploai graph'
                    )
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
                className='show-table graph',
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
                },
                className='graph'
            )
        ],
        style={"display": "flex"},
        id='second-layer'
    ),
    html.Div(
        [
            html.P(['Made by 3T Team and the respected teacher from IUH with ', html.I(className='fas fa-heart')]),
        ],
        className='footer graph'
    )
], className='container')