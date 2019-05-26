from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Date, \
    String
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base, CASCADE


class Post(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='post_id_uc'),
                      UniqueConstraint('fc_id', 'thread_fc_id',
                                       name='post_thread_uc'),
                      UniqueConstraint('fc_id', 'user_fc_id',
                                       name='post_user_uc'))

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)

    thread_fc_id = Column(Integer,
                          ForeignKey("thread.fc_id", ondelete=CASCADE),
                          index=True, nullable=False,)
    # thread = relationship('Thread', foreign_keys=[thread_fc_id])

    posted_at = Column(Date,
                       index=True)

    user_fc_id = Column(Integer,
                        # ForeignKey("User.fc_id", ondelete=CASCADE)
                        )
    # user = relationship('User')

    content = Column(String)

    def __json__(self):
        return {
            'id': self.id,
            'fc_id': self.fc_id,
            'thread_fc_id': self.thread_fc_id,
            'user_fc_id': self.user_fc_id,
            'content': self.content
        }
