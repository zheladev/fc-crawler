from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Date, \
    String
from sqlalchemy.orm import relationship

from fc_scrapper.models.base import BaseModel, Base, CASCADE


class Thread(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='id_uc'),
                      UniqueConstraint('fc_id', 'user_fc_id',
                                       name='post_user_uc'))

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)
    posted_at = Column(Date,
                       index=True)

    user = relationship('User')
    user_fc_id = Column(Integer,
                        ForeignKey("User.fc_id", ondelete=CASCADE))

    title = Column(String)

    def __json__(self):
        return {
            'id': self.id,
            'fc_id': self.fc_id,
            'user_fc_id': self.user_fc_id,
            'title': self.title
        }
