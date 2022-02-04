from Jobscraper.spiders.linkedin_spider import LinkedInSpider
from Jobscraper.spiders.careerguide_spider import CareerguideSpider
from twisted.internet import task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import scrapy
from scrapy.crawler import CrawlerProcess


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(CareerguideSpider)
    process.start()
