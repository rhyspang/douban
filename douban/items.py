# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()
    stars = scrapy.Field()
    types = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    runtime = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
