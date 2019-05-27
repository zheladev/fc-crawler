# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from functools import reduce

from sqlalchemy.exc import SQLAlchemyError

from fc_scrapper.items.post import PostItem
from fc_scrapper.models import Post
from fc_scrapper.pipelines.base import BasePipeline


class PostPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            session = self.Session()
            item['content'] = process_content(item['content'])
            post = Post(**item)
            try:
                session.add(post)
                session.commit()
            except SQLAlchemyError:
                session.rollback()
            finally:
                session.close()
            pass

        return item


def process_content(content):
    message = reduce(lambda x, y: x + y, content['message_lines'])
    return message
