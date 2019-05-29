from sqlalchemy import Column, Integer, UniqueConstraint, Date, \
    String

from fc_scrapper.models.base import BaseModel, Base


class User(Base, BaseModel):
    __table_args__ = (UniqueConstraint('fc_id',
                                       name='user_id_uc'),)

    fc_id = Column(Integer,
                   index=True, unique=True, nullable=False)

    created_at = Column(String,
                           index=True)
    name = Column(String)
    status = Column(String)

    def __json__(self):
        return {
            'id': self.id,
            'fc_id': self.fc_id,
            'creation_date': self.creation_date,
            'name': self.name
        }
