from app import db, WebsiteTrack
db.drop_all()
db.create_all()
foo = WebsiteTrack(cnts=0)
db.session.add(foo)
db.session.commit()
