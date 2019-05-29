import re
from datetime import date

from scrapy.spiders import CrawlSpider

from fc_scrapper.items.user import UserItem

THREAD_ITEM_XPATH_FIELDS = {
    'name':
        './/td[@id="username_box"]/h1/text()',
    'created_at':
        './/td[@id="profile_box"]//span[@class="smallfont"]/strong/text()',
    'status':
        './/td[@id="username_box"]/h2/text()'
}


class UserSpider(CrawlSpider):
    """
    Crawls all users
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._threads_to_crawl = kwargs.get('threads')

    name = 'fc_user_spider'
    allowed_domains = ['forocoches.com']

    # TODO: make script to feed start_urls and run several in parallel
    start_urls = [f'https://www.forocoches.com/foro/member.php?u={uid}'
                  for uid in range(1, 1000000)]

    def parse(self, response):
        selector = response.selector
        print(f'Crawling: {response.url}')

        user = UserItem()
        user['fc_id'] = re.search('u=([0-9]+).*', response.url).group(1)

        if selector.xpath(THREAD_ITEM_XPATH_FIELDS['name']).get() is not None:
            for attr, xpath in THREAD_ITEM_XPATH_FIELDS.items():
                user[attr] = get_attr(attr, selector.xpath(xpath))
        else:
            user['name'] = "DEACTIVATED_USER"
            user['created_at'] = "DEACTIVATED_USER"
            user['status'] = "DEACTIVATED_USER"
        yield user


def get_attr(attr, xpath):
    _lambdas = {
        'name':
            lambda x: x.get()[:-1],
        'created_at':
            lambda x: x.get(),  # TODO: convert to proper date
        'status':
            lambda x: x.get(),
    }

    return _lambdas[attr](xpath)
