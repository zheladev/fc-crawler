import re

from scrapy.spiders import CrawlSpider

from fc_scrapper.items.post import PostItem
from fc_scrapper.items.thread import ThreadItem


class ThreadSpider(CrawlSpider):
    """
    Crawls a thread from first to last page and returns all posts
    """
    name = 'fc_thread_spider'

    allowed_domains = ['forocoches.es']

    posts_list_xpath = "//div[@id='posts']/div/div/div/div/table[@id]"

    post_item_fields = {
        'id_':
            './@id',
        'user_id':
            './/a[@class="bigusername"]/@href',
        'posted_at':
            './tr/td/a[contains(@name, "post")]/following-sibling::text()',
        'content':
            './/td[contains(@id, "td_post_")]/div[@id="HOTWordsTxt"]/..'
    }

    start_urls = [
        'https://www.forocoches.com/foro/showthread.php?t=7203803'
    ]

    # rules = [
    #     Rule(
    #         link_extractor=LinkExtractor(
    #             allow='(.+)(t=[0-9]+)((&page=[0-9]+)|())'),
    #         callback='parse', follow=True),
    # ]

    def parse(self, response):
        selector = response.selector

        thread = ThreadItem()
        thread['id_'] = response.url.split('=')[-1:][0]
        thread['title'] = response.css(f'span.cmega::text').extract_first()
        thread['user_id'] = 'placeholder'

        yield thread

        for item in selector.xpath(self.posts_list_xpath):
            post = PostItem()
            print('NEW POST')
            post['thread_id'] = thread['id_']
            for attr, xpath in self.post_item_fields.items():
                post[attr] = get_attr(attr, item.xpath(xpath))
            yield post


def get_attr(attr, xpath):
    _lambdas = {
        'id_': lambda x: x.get()[4:],
        'user_id': lambda x: x.get().split('=')[-1:][0],
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
    garbage_filter = re.compile('(\n|\r|\t)+')

    # FIXME: Probably breaks if quote is found
    #        in between two bodies of text
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

    # print('raw data: \n', content.extract())
    # print("quotes without text(): \n",
    #       content.xpath('./div[contains(@style, ":") and not(@id)]')
    #       .extract())
    # print("\nquotes with text(): \n", clean_quotes)
    # print("clean_message_lines \n", message_lines)
    # print("\nmessage content: \n", content.xpath(
    #     './div[contains(@id, "post_message_")]'
    #     '/following-sibling::text()').extract())

    # !! if quote and quote has a href to another post then there's no need
    # to save said quote, look into having relationships in between
    # comments
    return {
        'quotes': clean_quotes,
        'message_lines': message_lines
    }
