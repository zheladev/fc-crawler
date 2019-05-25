import scrapy
from scrapy.spiders import CrawlSpider


class ThreadSpider(CrawlSpider):
    name = 'fc_thread_spider'
    allowed_domains = ['forocoches.es']
    start_urls = [

    ]
    def start_requests(self):
        urls = [
            'https://www.forocoches.com/foro/showthread.php?t=7203162'
        ]
        return [scrapy.Request(url=url, callback=self.parse)
                for url in urls]

    def parse(self, response):
        url = response.url
        id_ = url.split('=')[-1:][0]
        title = response.css(f'span.cmega::text').extract_first()
        print(f'id: {id_}, title: {title}', end='\n\n\n')
