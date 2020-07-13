# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class XiciProcyPipeline(object):
    def open_spider(self,spider):
        if spider.name=="xiciproxy":#如果有多个爬虫,每一个管道要加一个if测试
            host=spider.settings.get("REDIS_HOST")#获取设置文件中的REDIS_HOST
            port=spider.settings.get("REDIS_PORT")#获取设置文件中的REDIS_PORT
            db_index=spider.settings.get("REDIS_DB_INDEX")#获取设置文件中的REDIS_DB_INDEX
            self.db_conn=redis.StrictRedis(host=host,port=port,db=db_index,decode_responses=True)
            self.db_conn.delete("ip")
    def process_item(self, item, spider):
        if spider.name=="xiciproxy":
            #redis数据库对象的sadd方法
            self.db_conn.sadd("ip",dict(item)["url"])#直接写item["url"]可以吗,难道item[key]=value赋值的时候像字典,取值的时候
                                                    #先转换成字典吗
        return item
    def close_spider(self,spider):
        pass
