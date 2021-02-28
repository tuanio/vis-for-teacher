from dashboard import db
from datetime import datetime
import pytz

class WebsiteTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnts = db.Column(db.Integer, default=0)

    def __repr__(self):
        '''
            print(cái WebsiteTrack sẽ hiển thị theo dạng dưới)
        '''
        return 'Counts: %d' % (self.cnts)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=0)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    note_id = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User({}, {}, {})>'.format(self.id, self.username, self.note_id)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date_update = db.Column(db.DateTime, default=datetime.now().astimezone(pytz.timezone('Asia/Ho_Chi_Minh')))
    title = db.Column(db.String(500))
    title_shorten = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    student_name = db.Column(db.String(100), nullable=False)
    date_update_format = db.Column(db.String(100), default='')

    def __repr__(self):
        return '<Note({}, {}, {}, {}, {}, {}, {}, {})>'.format(self.id, self.author_id, self.date_update, self.title, self.title_shorten, self.student_name, self.date_update_format, self.content)