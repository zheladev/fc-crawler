from sqlalchemy.exc import SQLAlchemyError

from fc_scrapper.items.thread import ThreadItem
from fc_scrapper.models.thread import Thread
from fc_scrapper.pipelines.base import BasePipeline


class ThreadPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, ThreadItem):
            session = self.Session()
            thread = Thread(**item)
            try:
                session.add(thread)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
            finally:
                session.close()

        return item
