from os import environ

class Config:

    # FIXME: Local sqlite DB will be used for testing
    DATABASE_URI = "sqlite:///site.db"

    # General
    TESTING = environ.get("TESTING")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')