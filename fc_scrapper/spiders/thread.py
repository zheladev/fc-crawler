import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from fc_scrapper.items.post import PostItem

THREAD_PAGES_AREA_XPATH = './/div[@class="pagenav"]'
THREAD_PAGES_RE = r'(.+)(t=[0-9]+)((&page=[0-9]+)|())?'

POSTS_LIST_XPATH = "//div[@id='posts']/div/div/div/div/table[@id]"

POST_ITEM_XPATH_FIELDS = {
    'fc_id':
        './@id',
    'user_fc_id':
        './/a[@class="bigusername"]/@href',
    'posted_at':
        './tr/td/a[contains(@name, "post")]/following-sibling::text()',
    'content':
        './/td[contains(@id, "td_post_")]/div[@id="HOTWordsTxt"]/..'
}


class ThreadSpider(CrawlSpider):
    """
    Crawls a subforum for threads and returns all posts
    """
    name = 'fc_thread_spider'
    allowed_domains = ['forocoches.com']

    rules = Rule(
        link_extractor=LinkExtractor(
            allow=THREAD_PAGES_RE,
            restrict_xpaths=THREAD_PAGES_AREA_XPATH),
        callback='parse_items', follow=True),

    def parse_items(self, response):
        selector = response.selector
        print(f'Crawling: {response.url}')

        thread_url = response.url
        thread_id = re.search('t=([0-9]+).*', thread_url).group(1)

        for item in selector.xpath(POSTS_LIST_XPATH):
            post = PostItem()
            post['thread_fc_id'] = thread_id
            for attr, xpath in POST_ITEM_XPATH_FIELDS.items():
                post[attr] = get_attr(attr, item.xpath(xpath))
            yield post


def get_attr(attr, xpath):
    _lambdas = {
        'fc_id': lambda x: x.get()[4:],
        'user_fc_id': lambda x: x.get().split('=')[-1:][0],
        'posted_at': lambda x: x.get()[5:-10],
        'content': lambda x: get_content(x)
    }
    return _lambdas[attr](xpath)


def get_content(content):
    # TODO: handle all possible cases
    #   [x] 1: Only text without breaks
    #   [x] 2: Only text with breaks
    #   [x] 3: Quote & text w/o breaks
    #   [x] 4: Quote & text w/ breaks
    #   [ ] 5: Text with quote(s) in between

    # TODO: save quotes as references instead of value
    #       check if quote contains reference to other post
    #       if post, save reference
    #       else, save contents in message itself

    # TODO: save emoticons (images) and their position within the message

    # TODO: save quote position within message

    # FIXME: raw_message_lines may break if quote is found
    #        in between two bodies of text
    garbage_filter = re.compile('(\n|\r|\t)+')

    raw_message_lines = content.xpath(
        './div[contains(@id, "post_message_")]'
        '/following-sibling::text()').extract()

    raw_quotes = content.xpath(
        './div[contains(@style, ":") and not(@id)]//text()').extract()
    clean_quotes = list(filter(lambda x: not garbage_filter.search(x),
                               raw_quotes))

    message_lines = list(filter(bool,
                                (map(lambda m: garbage_filter.sub('', m),
                                     raw_message_lines))))
    return {
        'quotes': clean_quotes,
        'message_lines': message_lines
    }
