import scrapy

from fc_scrapper.items.base import BaseItem


class PostItem(BaseItem):
    fc_id = scrapy.Field()  # post id: table id="'post'+ int"
    thread_fc_id = scrapy.Field()  # id of post's parent: int
    posted_at = scrapy.Field()  # unparsed post date: String

    # postmenu_{id_} > a.class{href} -> member.php?u=1231212
    user_fc_id = scrapy.Field()  # id of user: int

    # id="post_message_{id_}"
    content = scrapy.Field()




