# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# TODO: decide on naming convention, thread spider calls posts pipeline
from fc_scrapper.items.post import PostItem
from fc_scrapper.pipelines.base import BasePipeline


class PostPipeline(BasePipeline):
    def process_item(self, item, spider):
        if isinstance(item, PostItem):
            pass

        return item
