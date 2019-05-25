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
            './/div[contains(@id, "post_message_")]/following-sibling::text()'
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
            post['thread_id'] = thread['id_']
            for attr, xpath in self.post_item_fields.items():
                post[attr] = self.get_attr(attr, item.xpath(xpath))
            yield post

    def get_attr(self, attr, xpath):
        _lambdas = {
            'id_': lambda x: x.get()[4:],
            'user_id': lambda x: x.get().split('=')[-1:][0],
            'posted_at': lambda x: x.get()[5:-10],
            'content': lambda x: x.get()[4:]
        }

        return _lambdas[attr](xpath)

    def get_content(self, attr, content):
        #TODO: get HOTWordsTxt (citas)
        #TODO: get text
        pass