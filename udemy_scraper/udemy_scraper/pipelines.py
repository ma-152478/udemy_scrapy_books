# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



class UdemyScraperPipeline(object):
    def process_item(self, item, spider):
        if item['availability'][0].startswith("In stock"):
            item['availability'] = "yes"
        else:
            item['availability'] = "no" 
        return item
