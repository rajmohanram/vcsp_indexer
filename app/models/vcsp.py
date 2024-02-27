from app.extensions import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime(timezone=True))
    bucket = db.Column(db.String(100), nullable=False)
    event = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Event "{self.title}">'