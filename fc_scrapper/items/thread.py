import scrapy

from fc_scrapper.items.base import BaseItem


class ThreadItem(BaseItem):
    # thread list, td > #td_threadtitle_{id_}

    fc_id = scrapy.Field()

    # id="td_threadtitle_{id_}" >>
    # span{onClick='window.open('member.php?u=user_id')}
    user_fc_id = scrapy.Field()
    posted_at = scrapy.Field()
    # id="thread_title_{id_}" > innerHTML
    title = scrapy.Field()


