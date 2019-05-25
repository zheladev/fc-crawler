from datetime import datetime
from enum import Enum
import uuid

from sqlalchemy import Column, DateTime, UniqueConstraint, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.schema import MetaData
# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
from fc_scrapper.lib.string_formatting import to_snake_case

CASCADE = 'cascade'

ON_DELETE_OPTIONS = [
    CASCADE,
]

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)  # inherit on models


class TableMixin:
    """Generic metadata on database entries."""

    @declared_attr
    def __tablename__(self):
        """table_name returns a name by using the class name."""
        return to_snake_case(self.__name__)


class BaseModel(TableMixin):
    def __init__(self, *args, **kwargs):
        """ Shell init to avoid keyword warning in linters """

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated = Column(
        DateTime(timezone=True), onupdate=datetime.utcnow())
    deleted = Column(DateTime(timezone=True))
