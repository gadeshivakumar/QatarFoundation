import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False