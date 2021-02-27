from dashboard.datas import *
import dashboard.datas as datas
import numpy as np
from dashboard import db
from dashboard.models import User, Note

datas.init()

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

def generate_note(user_id, student):
    ''' generate default note '''
    return Note.query.filter_by(author_id=user_id, student_name=student).all()

def get_time_format(time):
    '''
        return formated time
    '''
    return str('%02d:%02d %02d/%02d/%04d'%(time.hour, time.minute, time.day, time.month, time.year))