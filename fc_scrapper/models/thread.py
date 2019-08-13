from sqlalchemy import Column, Integer, UniqueConstraint, Date, \
    String, ForeignKey
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base, CASCADE


class Thread(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='thread_id_uc'),
                      UniqueConstraint('fc_id', 'user_fc_id',
                                       name='thread_user_uc'))

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)
    posted_at = Column(Date,
                       index=True, nullable=True)

    user_fc_id = Column(Integer,
                        ForeignKey("user.fc_id", ondelete=CASCADE)
                        )

    title = Column(String, nullable=True)  # remove nullable
    posts = relationship('Post', backref="thread")
