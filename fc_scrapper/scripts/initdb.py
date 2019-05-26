from sqlalchemy.orm import configure_mappers

import config

from sqlalchemy import MetaData

from fc_scrapper.models import create_engine
from fc_scrapper.models.post import Post  # noqa
from fc_scrapper.models.thread import Thread  # noqa
from fc_scrapper.models.user import User  # noqa


def main():
    configure_mappers()

    engine = create_engine(config.DATABASE)
    metadata = MetaData()
    metadata.create_all(engine)
