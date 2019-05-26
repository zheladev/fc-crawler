from sqlalchemy import Column, Integer, UniqueConstraint, Date, \
    String
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base


class Thread(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='thread_id_uc'),
                      UniqueConstraint('fc_id', 'user_fc_id',
                                       name='thread_user_uc'))

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)
    posted_at = Column(Date,
                       index=True, nullable=True)

    # user = relationship('User')
    user_fc_id = Column(Integer,
                        # ForeignKey("User.fc_id", ondelete=CASCADE)
                        )

    title = Column(String, nullable=True)  # remove nullable
    # posts = relationship('Post', backref="Thread")

    def __json__(self):
        return {
            'id': self.id,
            'fc_id': self.fc_id,
            'user_fc_id': self.user_fc_id,
            'title': self.title
        }
