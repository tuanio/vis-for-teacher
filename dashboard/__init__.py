import dash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

server = Flask(__name__)
app = dash.Dash(server=server, update_title=None, url_base_pathname='/')

# env = 'dev'
env = 'production'

if (env == 'dev'):
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_db/vis.db'
    server.debug = True
    app.debug = True
else:
    server.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nvajiwnacldrjc:8feb48b666b3b52f969d07231dc98f16fbb8eb40330b6471c672b2cfb4cdc823@ec2-3-213-85-90.compute-1.amazonaws.com:5432/d85fqrf0s08b3d'
    server.debug = False
    app.debug = False    

server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta charset="utf-8">
        <title>Vis for teacher</title>
        <link rel="icon" href="http://iuh.edu.vn/templates/images/icon.ico" type="image/x-icon" sizes="16x16">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <script src="https://kit.fontawesome.com/cab3a28685.js" crossorigin="anonymous"></script>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

from dashboard.datas import *
import dashboard.datas as datas
from dashboard.models import *
from dashboard.tools import * 
from dashboard.routes import *
from dashboard.dashboard import *
from dashboard.callbacks import *

datas.init()