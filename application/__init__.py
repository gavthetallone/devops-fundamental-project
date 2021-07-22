from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.update(
    # SQLALCHEMY_DATABASE_URI = "sqlite:///data.db",
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:squareroot@35.230.137.217/data",
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SECRET_KEY=str(os.urandom(16))
)

db = SQLAlchemy(app)

from . import routes