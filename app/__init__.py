from flask import Flask

app = Flask(__name__)

from db import db
from app import path_mapping
from app import schedule_task