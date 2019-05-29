from sqlalchemy.exc import SQLAlchemyError

from fc_scrapper.items.user import UserItem
from fc_scrapper.models import User
from fc_scrapper.pipelines.base import BasePipeline


class UserPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            session = self.Session()
            user = User(**item)
            try:
                session.add(user)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
            finally:
                session.close()

        return item
