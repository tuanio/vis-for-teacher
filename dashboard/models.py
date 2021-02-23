from dashboard import db

class WebsiteTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnts = db.Column(db.Integer, default=0)

    def __repr__(self):
        return 'Counts: %d' % (self.cnts)