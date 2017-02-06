# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    email = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    tags = scrapy.Field()

