from dashboard.models import WebsiteTrack
from dashboard import server
from flask import render_template, url_for, redirect, send_from_directory
from dashboard import db
from dashboard.datas import *
import dashboard.datas as datas

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

    return redirect('/')

@server.route('/track')
def track():
    '''
        - Page to show how many times the website was loaded
    '''
    return 'Passengers: ' + str(WebsiteTrack.query.one().cnts)