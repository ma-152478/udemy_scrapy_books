# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UdemyScraperItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()



    
    