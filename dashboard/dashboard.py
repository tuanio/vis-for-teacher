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
                                    className='img-thumbneil float-left logo-img logo-img-iuh'
                                ),
                                id='logo-iuh',
                                className='logo'
                            ),
                            html.Div(
                                html.Img(
                                    src='assets/imgs/logo_k15ds.png',
                                    className='img-thumbneil float-left logo-img logo-img-k15ds'
                                ),
                                id='logo-k15ds',
                                className='logo'
                            ),
                            html.Div(
                                html.Img(
                                    src="assets/imgs/logo_vft.png",
                                    className='img-thumbneil logo-img logo-img-vft'
                                ),
                                id='logo-vft',
                                className='logo'
                            ),
                            html.Div(
                                [
                                    html.Div(html.Button('Sign Up', id='btn-sign-up'), className='sign-up'),
                                    html.Div(html.Button('Login', id='btn-login'), className='login')
                                ],
                                className='form-login'
                            ),
                            html.Div(
                                [
                                    html.Img(
                                        src="assets/imgs/dark_mode.png",
                                        id='icon-dark-mode'
                                    ),
                                    html.Label(
                                        [
                                            dcc.Input(type='checkbox', id='checkbox'),
                                            html.Div(className='slider round')
                                        ],
                                        className='theme-switch',
                                        htmlFor='checkbox'
                                    )
                                ],
                                className='theme-switch-wrapper'
                            )
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
            html.Div(
                [
                    html.P(
                        [
                            html.I(className='fas fa-asterisk'),
                            ' Những môn học không có sinh viên nào học sẽ không được hiển thị lên trên thanh tìm kiếm'
                        ]
                    ),
                ],
                style={
                    'fontSize': 'small', 
                    'margin': '10px 0',
                    'color': 'gray'
                }
            ),
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
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(
                                        [
                                            html.I(className='fas fa-clipboard', style={'margin-right': '5px'}),
                                            html.Span('Ghi chú sinh viên'),
                                        ],
                                        style={
                                            'marginTop': '5px',
                                            'textAlign': 'center',
                                            'fontWeight': 'bold',
                                            'fontSize': 'large',
                                        },
                                    )
                                ],
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        dcc.Dropdown(
                                            options=[{'label': i, 'value': i} for i in classmate],
                                            multi=False,
                                            searchable=True,
                                            value=classmate[0],
                                            placeholder=classmate[0],
                                            clearable=False,
                                            id='dropdown_note',
                                            persistence='true',
                                            persistence_type='session',
                                        ),
                                        style={
                                            'width': '300px',
                                            'margin-right': '10px'
                                        },
                                    ),
                                    html.Div(
                                        html.A(
                                            [html.I(className='fas fa-comment-dots')],
                                            href='javascript:void(0);',
                                            className='btn btn-outline-success',
                                            id='show-note-btn-a'
                                        ),
                                        id='show-note-btn'
                                    ),
                                ],
                                style={'display': 'flex'},
                            ),
                        ],
                        style={
                            'height': '100px',
                            'width': '375px',
                            'padding': '5px',
                        },
                        className='graph'
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.A(
                                        [html.I(className='fas fa-plus')],
                                        href='javascript:void(0);',
                                        className='btn btn-outline-dark',
                                    ),
                                ],
                                id='add-note-btn'
                            ),
                            html.Div(
                                html.Div(id='show-note'),
                                style={'margin': '10px 0 0 0'}
                            ),
                        ],
                        **{'data-flag': '0'},
                        className='graph note-container',
                    ),

                    # template of edit note
                    html.Div(
                        [
                            html.Div(
                                html.P(
                                    'Cập nhật mới nhất: 17:51 26/02/2021',
                                    className='note-sm-label'
                                ) 
                            ),
                            html.Div(
                                dcc.Input(
                                    type='text',
                                    placeholder='Tiêu đề',
                                    className='form-control',
                                    id='note-edit-title-input'
                                ),
                                id='note-edit-title'
                            ),
                            html.Div(
                                dcc.Textarea(
                                    placeholder='Nội dung ghi chú',
                                    id='note-edit-txtarea',
                                    className='form-control'
                                ),
                                id='note-edit-content'
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        html.A(
                                            'Lưu thay đổi',
                                            href='javascript:void(0);',
                                            className='btn btn-outline-success'
                                        ),
                                        id='note-edit-save',
                                    ),
                                    html.Div(
                                        html.A(
                                            html.I(className='fas fa-trash'),
                                            href='javascript:void(0);',
                                            className='btn btn-outline-dark'
                                        ),
                                        id='note-edit-remove',
                                    )
                                ],
                                id='note-edit-tools'
                            ),
                        ],
                        **{'data-id': '0'},
                        id='edit-note',
                        className='graph note-container-edit'
                    )
                ],
                style={
                    'margin-left': '10px',
                },
            ),
            html.Div(id='template-note', style={'display': 'none'}),
            html.Div(id="data-note", style={'display': 'none'}),
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