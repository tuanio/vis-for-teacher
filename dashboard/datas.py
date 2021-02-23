import pandas as pd
pd.options.mode.chained_assignment = None # default 'warn'
import os

color = '#499167'

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

def init():
    global size_big, size_medium, size_plot

    # size of plot for screen >= 1536 x 864
    size_plot = size_big = {
        'boxplot': (710, 330),
        'bar_xeploai': (550, 330)
    }

    # size of plot for screen 1366 x 768
    size_medium = {
        'boxplot': (600, 300),
        'bar_xeploai': (480, 300)
    }

df = pd.read_csv('dashboard/csv_files/cleaned_data.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)
xeploai_df = pd.read_csv('dashboard/csv_files/xeploai.csv')
tin_chi_df = pd.read_csv('dashboard/csv_files/tin_chi.csv')

subjects = list(df.columns[5:-6])
classmate = list(df['Họ và tên'])



