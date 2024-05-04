from flask import Flask
import signal 
from flask_cors import CORS 
from os import environ
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase 
from flask_socketio import SocketIO 
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "https://omnihale.com", "https://business.omnihale.com"], supports_credentials=True)
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

# Create the tables
with app.app_context():
    db.create_all()

socketio = SocketIO(app, cors_allowed_origins=["http://localhost:3000", "http://localhost:3001", "https://omnihale.com", "https://business.omnihale.com"])


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on_error()  # Handles all socket errors
def handle_socket_error(e):
    print('Socket error occurred:', e)

def handle_shutdown(signum, frame):
    print('Shutting down...')
    socketio.close_room('/')  # Close all connections
    exit(0)

signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)




if __name__ == '__main__':
  socketio.run(app)

from service import routes