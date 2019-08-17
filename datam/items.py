# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:class relatedItem(scrapy.Item)
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class datamItem(scrapy.Item):
    title = scrapy.Field()
    usern = scrapy.Field()
    body = scrapy.Field()
    contact = scrapy.Field()
    city = scrapy.Field()
    #related = scrapy.Field()
    relatedtext = scrapy.Field()
    tags = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    date = scrapy.Field()
    pass

#class datamItem2(scrapy.Item):
#    related = scrapy.Field()
#    pass