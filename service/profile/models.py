from sqlalchemy import PickleType
from sqlalchemy.dialects.postgresql import UUID
from service.routes import db
import uuid


class Profile(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    remote_appointments_threshold = db.Column(db.String(150), nullable=False)
    daily_appointments_threshold = db.Column(db.String(200), nullable=False)

    def __init__(self, user_id, name, address, remote_appointments_threshold, daily_appointments_threshold):
        self.user_id = user_id
        self.name = name
        self.address = address
        self.remote_appointments_threshold = remote_appointments_threshold
        self.daily_appointments_threshold = daily_appointments_threshold