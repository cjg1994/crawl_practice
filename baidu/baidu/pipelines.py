# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
#导入的scrapy.conf在哪?

class BaiduPipeline(object):
    # def open_spider(self,spider):
    #     print("open"+"*"*100)
    def __init__(self):
        #导入settings模块就可以以字典的形式载入其中的变量
        host=settings['MONGODB_HOST']
        port=settings['MONGODB_PORT']
        db_name=settings['MONGODB_DBNAME']
        client=pymongo.MongoClient(host=host,port=port)
        db=client[db_name]
        self.post=db[settings['MONGODB_DOCNAME']]  #这里就是为了构造一个self.post?这是什么用的?是一个集合名?
#__init__就是为了构造数据库中的一个集合? 这是为了一个链接mongodb数据库的对象,而且指定了数据库中的一个集合
    def process_item(self, item, spider):
        person_info=dict(item)
        self.post.insert(person_info) #调用insert方法插入一条字典数据
        return item
