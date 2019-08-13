from sqlalchemy import Column, Integer, UniqueConstraint, String, Date
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base


class User(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='user_id_uc'),)

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)

    created_at = Column(Date,
                        index=True)
    name = Column(String)
    status = Column(String)
    threads = relationship('Thread', backref="user")
    posts = relationship('Post', backref="user")
