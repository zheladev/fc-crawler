import sys
from math import ceil

from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from twisted.internet import reactor

from fc_scrapper import settings
from fc_scrapper.models import db_connect, User
from fc_scrapper.spiders.forum import ForumSpider
from fc_scrapper.spiders.thread import ThreadSpider
from fc_scrapper.spiders.user import UserSpider


def main(argv=sys.argv):
    opt = 'all'
    if len(argv) >= 2:
        opt = argv[1]
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    runner = CrawlerRunner(settings=crawler_settings)

    if opt == 'threads' or opt == 'all':
        crawl_threads(runner)
    if opt == 'users' or opt == 'all':
        crawl_users(runner)
    else:
        exit(1)

    d = runner.join()
    d.addCallback(lambda _: reactor.stop())
    reactor.run()


def crawl_threads(runner):
    def _crawl_threads(thread_list):
        i = list(map(list,
                     zip(*[iter(thread_list)] * ceil(
                         len(thread_list) / 6))))
        for zipped_threads in i:
            print('starting thread crawlers...')
            runner.crawl(ThreadSpider, start_urls=zipped_threads)

    threads_to_crawl = []
    print('Crawling forum for threads...')
    forum_spider = runner.crawl(ForumSpider, threads=threads_to_crawl)
    forum_spider.addCallback(
        lambda x: _crawl_threads(threads_to_crawl))


def crawl_users(runner):
    s = sessionmaker(bind=db_connect())()
    max_id = s.query(
        func.max(User.fc_id)).one_or_none()[0]
    if not max_id:
        max_id = 0

    user_urls = [f'https://www.forocoches.com/foro/member.php?u={uid}'
                 for uid in range(max_id + 1, max_id + 10001)]
    print('starting user crawler...')
    runner.crawl(UserSpider, start_urls=user_urls)
