from scrapy.spiders import CrawlSpider

from fc_scrapper.items.thread import ThreadItem


class ThreadSpider(CrawlSpider):
    """
    Crawls a thread from first to last page and returns all posts
    """
    name = 'fc_thread_spider'

    allowed_domains = ['forocoches.es']

    posts_list_xpath = "//div[@id='posts']/div/div/div/div/table[@id]"

    post_item_fields = {
        'fc_id': '',
        'thread': '',
        'user_id': '',
        'posted_at': '',
        'content': ''
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

        print('\n\n\n\n\n\n\n\n\n\n')
        # import pdb; pdb.set_trace()
        for item in selector.xpath(self.posts_list_xpath):
            print(item)
