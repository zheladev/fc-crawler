from sqlalchemy.exc import SQLAlchemyError

from fc_scrapper.items.thread import ThreadItem
from fc_scrapper.models.thread import Thread
from fc_scrapper.pipelines.base import BasePipeline


class ThreadPipeline(BasePipeline):
    def process_item(self, item, spider):
        session = self.Session()
        if isinstance(item, ThreadItem):
            print('hi')
            thread = Thread(**item)
            print(f'created item {thread}')
            try:
                print('adding thread...  ', end='')
                session.add(thread)
                session.commit()
                print('thread added!')
            except SQLAlchemyError:
                print('failed.')
                session.rollback()
            finally:
                session.close()

        return item
