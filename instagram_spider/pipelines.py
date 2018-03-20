# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .mongodb import mongodb_operations
from .mongodb.mongodb_operations import MongodbOperations


class InstagramSpiderPipeline(object):
    def __init__(self):
        self.mongodb = MongodbOperations("Insert")

    def process_item(self, item, spider):
        items = dict(item)
        self.mongodb.insert(items)
