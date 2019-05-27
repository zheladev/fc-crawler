from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from fc_scrapper import settings
from fc_scrapper.spiders.thread import ThreadSpider


def main():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(ThreadSpider)
    process.start()
