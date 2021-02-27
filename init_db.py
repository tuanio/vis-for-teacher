from app import *
db.drop_all()
db.create_all()
from dashboard.tools import *

db.session.add(WebsiteTrack(cnts=0))
db.session.add(User(username='tuanio', password='ok', note_id=0))
db.session.add(
    Note(
        author_id=0,
        title='Điểm toán cao cấp 1', 
        title_shorten='Điểm toán cao cấp 1',
        content='- Sinh viên đã làm rất tốt\n- Điểm cần được cập nhật\n- Sinh viên này làm lớp trưởng môn toán cao cấp 1',
        student_name='Phạm Thành Trung'
    )
)
db.session.add(
    Note(
        author_id=0,
        title='Điểm toán cao cấp 2', 
        title_shorten='Điểm toán cao cấp 2',
        content='',
        student_name='Phạm Thành Trung'
    )
)
db.session.add(
    Note(
        author_id=0,
        title='Điểm toán cao cấp 2', 
        title_shorten='Điểm toán cao cấp 2',
        content='- Được 10 điểm môn toán cao cấp 2',
        student_name='Huỳnh Minh Toàn'
    )
)
db.session.add(
    Note(
        author_id=0,
        title='Xem xét môn tiếng anh 1', 
        title_shorten='Xem xét môn tiếng an...',
        content='- Khi thi được 630 tiếng anh 1',
        student_name='Nguyễn Văn Anh Tuấn'
    )
)
db.session.commit()

# update the time format
notes = Note.query.all()
for note in notes:
    note.date_update_format = get_time_format(note.date_update)
db.session.commit()
