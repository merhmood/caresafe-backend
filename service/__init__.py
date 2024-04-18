from flask import Flask
from flask_cors import CORS
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Adinoyi2@localhost:5432/dev"
# initialize the app with the extension
db.init_app(app)

from service import routes