import os
import psycopg2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# DONE IMPLEMENT DATABASE URL
# postgresql+psycopg2://user:password@host:port/dbname
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:0000@localhost:5432/fyyur'

# Connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
