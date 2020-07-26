from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


from db import db
from app import path_mapping
from app import schedule_task