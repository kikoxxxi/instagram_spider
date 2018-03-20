# -*- coding: utf-8 -*-
import pymongo
from scrapy import log


class MongodbOperations:
    def __init__(self, stat):
        log.msg('Init MongoDB %s connection!!!!!!!!' %
                stat, log.INFO)
        self.client = pymongo.MongoClient()  # 连接数据库，默认localhost，port 27017
        self.db = self.client.spiders  # 选择数据库名字，不存在会自动创建
        self.collections = self.db.jacobbix  # 选择集合，不存在会自动创建

    # 集合中查询指定的url，不存在返回None
    def find_one(self, values):
        return self.collections.find_one({"original_url": values})

    # 插入数据
    def insert(self, values):
        self.collections.insert(values)
