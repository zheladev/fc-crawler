from sqlalchemy import *
from sqlalchemy.engine import Engine
from sqlalchemy.orm import configure_mappers

from fc_scrapper import settings
from fc_scrapper.models.base import Base
from fc_scrapper.models.post import Post  # noqa
from fc_scrapper.models.thread import Thread  # noqa
from fc_scrapper.models.user import User  # noqa

configure_mappers()


def get_engine(s) -> Engine:
    """
    Performs a database connection using specified settings
    :return: SQLAlchemy engine instance
    """
    return create_engine(s)


def db_connect() -> Engine:
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return get_engine(settings.DATABASE)


def init_db():
    Base.metadata.create_all(db_connect())
