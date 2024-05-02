from sqlalchemy import PickleType
from sqlalchemy.dialects.postgresql import UUID
from service.routes import db
import uuid

class ConfigureAppointments(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    appointment_fields = db.Column(PickleType)

    user = db.relationship('User', backref=db.backref('appointment_fields', lazy=True))

    def __init__(self, user_id, appointment_fields):
        self.user_id = user_id
        self.appointment_fields = appointment_fields