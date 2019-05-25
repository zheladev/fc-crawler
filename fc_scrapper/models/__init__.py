from sqlalchemy import *
from sqlalchemy.engine.url import URL

from fc_scrapper import settings


def get_engine():
    """
    Performs a database connection using specified settings
    :return: SQLAlchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """

