# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GstservicesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    sub_title = scrapy.Field()
    description = scrapy.Field()
    sac_code = scrapy.Field()
    rate = scrapy.Field()
    id = scrapy.Field()
