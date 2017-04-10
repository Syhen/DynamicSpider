# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import time


class DynamicPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.today = time.strftime('%Y-%m-%d')

    @classmethod
    def from_crawler(cls, crawler):
        """
        1.这个方法是什么作用？
        2.应该有一个库存储的管理类（比如我想存在多个库里，存在多个表里，每个表的内容还可能不一样）
        3.历史数据，再添加一个pipline吧  ##### ok #####
        （写一个middlewares，判断往pipline里面发送什么数据）"""
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('MONGO_INFO_COLLECTION')
        )

    def open_spider(self, spider):
        self.con = pymongo.MongoClient(self.mongo_uri)
        self.db = self.con[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.mongo_collection].update({'_id': item['id']}, {'$set': item}, True)
        return item

    def close_spider(self, spider):
        self.con.close()


class DynamicHistoryPipeline(DynamicPipeline):
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        super(DynamicHistoryPipeline, self).__init__(mongo_uri, mongo_db, mongo_collection)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('MONGO_HISTORY_COLLECTION')
        )

    def process_item(self, item, spider):
        """how to just add one line from Parent function?"""
        item['id'] = item['id'] + '_' + self.today
        self.db[self.mongo_collection].update({'_id': item['id']}, {'$set': item}, True)
        return item
