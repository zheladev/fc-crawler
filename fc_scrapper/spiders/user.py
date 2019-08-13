import re
import datetime

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
    name = 'fc_user_spider'
    allowed_domains = ['forocoches.com']

    def parse(self, response):
        selector = response.selector
        print(f'Crawling: {response.url}')

        user = UserItem()
        user['fc_id'] = re.search('u=([0-9]+).*', response.url).group(1)

        if selector.xpath(THREAD_ITEM_XPATH_FIELDS['name']).get() is not None:
            for attr, xpath in THREAD_ITEM_XPATH_FIELDS.items():
                user[attr] = get_attr(attr, selector.xpath(xpath))
            yield user
        else:
            user['name'] = "DESACTIVADO O INACTIVO"
            user['created_at'] = datetime.date(1900, 1, 1)
            user['status'] = ""
            yield user


def get_attr(attr, xpath):
    _lambdas = {
        'name':
            lambda x: x.get()[:-1],
        'created_at':
            lambda x: get_date(x.get()),  # TODO: convert to proper date
        'status':
            lambda x: x.get(),
    }

    return _lambdas[attr](xpath)


def get_date(datestr: str):
    months = {
        'ene': 1,
        'feb': 2,
        'mar': 3,
        'abr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dic': 12,
    }
    d, m, y = datestr.split("-")
    return datetime.date(int(y), months[m], int(d))
