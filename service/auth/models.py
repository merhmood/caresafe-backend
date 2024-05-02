from sqlalchemy.dialects.postgresql import UUID
import uuid
from service.routes import db


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    state = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, state, address, email, password):
        self.name = name
        self.address = address
        self.state = state
        self.email = email
        self.password = password