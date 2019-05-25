import scrapy

from fc_scrapper.items.base import BaseItem


class UserItem(BaseItem):
    id_ = scrapy.Field()
    name = scrapy.Field()
    created_at = scrapy.Field()
    status = scrapy.Field()
