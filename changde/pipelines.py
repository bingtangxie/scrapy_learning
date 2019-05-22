# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class ChangdePipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        # tablename = settings["MONGODB_TABLENAME"]
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.db = mydb

    def process_item(self, item, spider):
        if spider.name == 'caigou':
            data = dict(item)
            # return item
            # print(self.post)
            self.db[spider.name].insert(data)
        if spider.name == 'htgg':
            data = dict(item)
            self.db[spider.name].insert(data)
