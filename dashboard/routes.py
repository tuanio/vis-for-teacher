from dashboard.models import WebsiteTrack
from dashboard import server
from flask import render_template, url_for, redirect, send_from_directory, jsonify, request
from dashboard import db
from dashboard.datas import *
import dashboard.datas as datas
from dashboard.models import *
from dashboard.tools import *
from dashboard.callbacks import * 
import json
import pytz

datas.init()

@server.route('/download/<path:path>')
def download(path):
    return send_from_directory('', path, as_attachment=True)

@server.route('/onload/<int:width>/<int:height>')
def onload(width, height):
    '''
        - This function use to count how many times the website was loaded
        - Load the screen of website
    '''
    cnts = WebsiteTrack.query.one()
    cnts.cnts = cnts.cnts + 1
    db.session.commit()

    # print('Width: {}, Height: {}'.format(width, height))

    # Reference to global variable first

    if (width <= 1366):
        datas.size_plot = datas.size_medium
    else:
        datas.size_plot = datas.size_big

    return jsonify(width=width, height=height)

@server.route('/track')
def track():
    '''
        - Page to show how many times the website was loaded
    '''
    return 'Passengers: ' + str(WebsiteTrack.query.one().cnts)

@server.route('/add-note/<string:student_name>')
def add_note(student_name):
    '''
        Dùng user_id mặc định là 0, sau này sửa lại sau
    '''
    user_id = 0
    new_note = Note(
        author_id=user_id,
        title='Tiêu đề ghi chú',
        title_shorten='Tiêu đề ghi chú...',
        content='',
        student_name=student_name
    )

    db.session.add(new_note)
    db.session.commit()

    new_note = Note.query.all()[-1]
    new_note.date_update_format = get_time_format(new_note.date_update)

    db.session.commit()

    # turn back to dashboard
    return jsonify(
        id=new_note.id,
        date_update_format=new_note.date_update_format,
        title_shorten=new_note.title_shorten
    )

@server.route('/view-note/<int:id>')
def view_note(id):
    try:
        data = Note.query.filter_by(id=id).one()
        return jsonify(
            id=data.id,
            author_id=data.author_id,
            date_update=data.date_update,
            title=data.title,
            title_shorten=data.title_shorten,
            content=data.content,
            student_name=data.student_name,
            date_update_format=data.date_update_format
        )
    except:
        ...
    return {'view-note' : 'failed'}


@server.route('/save-note', methods=['GETS', 'POST'])
def save_note():
    if (request.method == 'POST'):

        data = [i for i in request.form.keys()][0]
        data = json.loads(data)

        # update the note to the database
        note = Note.query.filter_by(id=data['id']).one()
        note.title = data['title']

        note.title_shorten = data['title'][:min(25, len(data['title']))]
        if (data['title'] != note.title_shorten):
            note.title_shorten += '...'
        
        note.content = data['content']
        note.date_update = datetime.now().astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
        note.date_update_format = get_time_format(note.date_update)

        # commit changes
        db.session.commit()

        # return a json
        return jsonify(title_shorten=note.title_shorten, student=note.student_name, date_update_format=note.date_update_format)
    return {'err': 'err'}

@server.route('/delete-note/<int:id>')
def delete_note(id):
    try:
        Note.query.filter_by(id=id).delete()
        db.session.commit()
        return {'delete': 'ok'}
    except:
        ...
    return {'delete': 'fail'}