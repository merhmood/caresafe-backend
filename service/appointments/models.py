from sqlalchemy.dialects.postgresql import UUID
from service.routes import db
import uuid


class Appointments(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    appointments = db.Column(db.PickleType)  # store arbitrary data

    user = db.relationship('User', backref=db.backref('appointments', lazy=True))

    def __init__(self, user_id, appointments):
        self.user_id = user_id
        self.appointments = appointments