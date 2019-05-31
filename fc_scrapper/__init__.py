import sys
import time
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

USER_NUMBER = 100000


def main(argv=sys.argv):
    opt = 'all'
    if len(argv) >= 2:
        opt = argv[1]
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    runner = CrawlerRunner(settings=crawler_settings)

    if opt not in ['users', 'all', 'threads']:
        exit(1)
    if opt in ['users', 'all']:
        crawl_users_parallel(runner)
    if opt in ['threads', 'all']:
        crawl_threads(runner)

    start = time.time()
    d = runner.join()
    d.addCallback(lambda _: reactor.stop())
    reactor.run()
    end = time.time()
    print(f"Crawl time: {end - start} seconds.")
    with open("times.txt", "a") as f:
        f.write(f"Crawl time: {end - start} seconds.\n")


def crawl_threads(runner):
    def _crawl_threads(thread_list):
        i = list(map(list,
                     zip(*[iter(thread_list)] * ceil(
                         len(thread_list) / 6))))
        for zipped_threads in i:
            print('starting thread crawler...')
            runner.crawl(ThreadSpider, start_urls=zipped_threads)

    threads_to_crawl = []
    print('Crawling forum for threads...')
    runner.crawl(ForumSpider, threads=threads_to_crawl).addCallback(
        lambda x: _crawl_threads(threads_to_crawl)
    )


# SLOWER
def crawl_users(runner):
    s = sessionmaker(bind=db_connect())()
    max_id = s.query(
        func.max(User.fc_id)).one_or_none()[0]
    if not max_id:
        max_id = 0

    user_urls = [f'https://www.forocoches.com/foro/member.php?u={uid}'
                 for uid in range(max_id + 1, max_id + 1 + USER_NUMBER)]
    # print('starting user crawler...')
    runner.crawl(UserSpider, start_urls=user_urls)


def crawl_users_parallel(runner):
    s = sessionmaker(bind=db_connect())()
    max_id = s.query(
        func.max(User.fc_id)).one_or_none()[0]
    if not max_id:
        max_id = 0

    user_urls = [f'https://www.forocoches.com/foro/member.php?u={uid}'
                 for uid in range(max_id + 1, max_id + 1 + USER_NUMBER)]
    i = list(map(list,
                 zip(*[iter(user_urls)] * ceil(
                     len(user_urls) / 12))))
    for test in i:
        print('starting user crawler...')
        runner.crawl(UserSpider, start_urls=test)
