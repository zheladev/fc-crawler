from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Date, \
    String
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base, CASCADE


class Post(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='id_uc'),
                      UniqueConstraint('fc_id', 'thread_fc_id',
                                       name='post_thread_uc'),
                      UniqueConstraint('fc_id', 'user_fc_id',
                                       name='post_user_uc'))

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)

    thread = relationship('Thread')
    thread_fc_id = Column(Integer,
                          ForeignKey("Thread.fc_id", ondelete=CASCADE),
                          index=True, nullable=False)

    posted_at = Column(Date,
                       index=True)

    user = relationship('User')
    user_fc_id = Column(Integer,
                        ForeignKey("User.fc_id", ondelete=CASCADE))

    content = Column(String)

    def __json__(self):
        return {
            'id': self.id,
            'fc_id': self.fc_id,
            'thread_fc_id': self.thread_fc_id,
            'user_fc_id': self.user_fc_id,
            'content': self.content
        }
