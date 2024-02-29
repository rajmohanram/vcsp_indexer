from app.extensions import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventTime = db.Column(db.String(100), nullable=False)
    userid = db.Column(db.String(100), nullable=False)
    eventName = db.Column(db.String(100), nullable=False)
    bucket = db.Column(db.String(100), nullable=False)
    object = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Event "{self.eventName}">'