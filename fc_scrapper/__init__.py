from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor, defer

from fc_scrapper import settings
from fc_scrapper.spiders.forum import ForumSpider
from fc_scrapper.spiders.thread import ThreadSpider


def main():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    runner = CrawlerRunner(settings=crawler_settings)

    @defer.inlineCallbacks
    def crawl():
        threads_to_crawl = []
        print('Crawling forum for threads...')
        yield runner.crawl(ForumSpider, threads=threads_to_crawl)
        print('Crawling threads for posts...')
        yield runner.crawl(ThreadSpider, start_urls=threads_to_crawl)
        reactor.stop()

    crawl()
    reactor.run()
