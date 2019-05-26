from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from fc_scrapper.models import db_connect


class BasePipeline:
    # Use a singleton?
    Session = sessionmaker(bind=db_connect())
