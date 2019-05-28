from math import ceil

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
        def _crawl_threads(thread_list):
            print('foo')
            i = list(map(list,
                         zip(*[iter(thread_list)] * ceil(
                             len(thread_list) / 6))))
            print('bar')
            for zipped_threads in i:
                print('starting runner...')
                runner.crawl(ThreadSpider, start_urls=zipped_threads)
            runner.join()

        threads_to_crawl = []
        print('Crawling forum for threads...')
        forum_spider = runner.crawl(ForumSpider, threads=threads_to_crawl)
        forum_spider.addCallback(
            lambda x: _crawl_threads(threads_to_crawl))
        reactor.run()
        reactor.stop()

    crawl()
