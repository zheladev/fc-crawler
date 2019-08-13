import re
from datetime import date

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fc_scrapper.items.thread import ThreadItem

FORUM_THREADS_AREA_XPATH = './/div[@class="pagenav"]'
FORUM_THREADS_RE = r'(.+)(f=[0-9]+)((&page=[0-9]{2})|())?'

THREAD_LIST_XPATH = '//tbody[contains(@id, "threadbits_forum_")]/tr'

THREAD_ITEM_XPATH_FIELDS = {
    'fc_id':
        './td[contains(@id, "td_threadtitle_")]/@id',
    'user_fc_id':
        './/span[contains(@onclick, "member.php?")]/@onclick',
    'posted_at':
        './/span[@class="time"]/..',
    'title':
        './/a[contains(@id, "thread_title_")]/text()'
}


class ForumSpider(CrawlSpider):
    """
    Crawls a subforum for threads and returns all posts
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._threads_to_crawl = kwargs.get('threads')

    name = 'fc_forum_spider'
    allowed_domains = ['forocoches.com']

    start_urls = ['https://www.forocoches.com/foro/forumdisplay.php?f=2']

    rules = [
        Rule(
            link_extractor=LinkExtractor(
                allow=FORUM_THREADS_RE,
                restrict_xpaths=FORUM_THREADS_AREA_XPATH),
            callback='parse_thread', follow=True),
    ]

    def parse_thread(self, response):
        selector = response.selector
        print(f'Crawling: {response.url}')

        for item in selector.xpath(THREAD_LIST_XPATH):
            thread = ThreadItem()
            for attr, xpath in THREAD_ITEM_XPATH_FIELDS.items():
                thread[attr] = get_attr(attr, item.xpath(xpath))

            self._threads_to_crawl.append(
                f"https://www.forocoches.com/foro/"
                f"showthread.php?t={thread['fc_id']}")
            yield thread


def get_attr(attr, xpath):
    _lambdas = {
        'fc_id':
            lambda x: x.get().replace('td_threadtitle_', ''),
        'user_fc_id':
            lambda x: re.search(r'member\.php\?u=([0-9]+)', x.get()).group(1),
        'posted_at':
            lambda x: str(date.today()),  # TODO: get actual date
        'title':
            lambda x: x.get()
    }

    return _lambdas[attr](xpath)
