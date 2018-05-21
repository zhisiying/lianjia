# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class LianjiaPipeline(object):
    def process_item(self, item, spider):
        return item

class MongolPipeline(object):
    def __init__(self,mongo_url,mongo_db):#初始化 mongo 配置
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),#调用 settings 写好的的配置
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        #建立连接
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        # if self.db[name].find_one({'url':item['url']}): #去重
        #     print('重复')
        # else:
        #     self.db[name].insert(dict(item))#存储
    def close_spider(self,spider):
        self.client.close()#关闭连接
