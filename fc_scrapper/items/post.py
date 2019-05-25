import scrapy

from fc_scrapper.items.base import BaseItem


class PostItem(BaseItem):
    id_ = scrapy.Field()  # post id: table id="'post'+ int"
    thread_id = scrapy.Field()  # id of post's parent: int
    post_count = scrapy.Field()  # sequence number within thread: int
    posted_at = scrapy.Field()  # unparsed post date: String

    # postmenu_{id_} > a.class{bigusername} > innerHTML
    user_name = scrapy.Field()  # name of user: String

    # postmenu_{id_} > a.class{href} -> member.php?u=1231212
    user_id = scrapy.Field()  # id of user: int

    # id="post_message_{id_}"
    content = scrapy.Field()




