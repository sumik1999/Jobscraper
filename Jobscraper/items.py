# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinscraperItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()


class CompanyscraperItem(scrapy.Item):
    description = scrapy.Field()
    location = scrapy.Field()
    number_employees = scrapy.Field()


class JobscraperItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    subcategory = scrapy.Field()
    job_detail = scrapy.Field()
    company_detail = scrapy.Field()
