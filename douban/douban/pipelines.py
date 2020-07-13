# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class DoubanPipeline(object):
    filename="douban.csv"
    #爬虫打开的时候这个方法会执行
    def open_spider(self,spider):
        #构造一个csv文件对象准备用来写
        self.file=open(self.filename,'a',encoding="utf-8")
        self.writer=csv.DictWriter(self.file,fieldnames=["title","directors","casts","rate"])
        self.writer.writeheader()
    def process_item(self, item, spider):
        #这个方法用来处理item的
        self.writer.writerow(dict(item))#写一行的方法
        return item#还要返回item
    def close_spider(self,spider):
        #爬虫关闭的时候会执行这个方法, 需要把打开的文件对象关闭
        #self.writer其实是根据self.file创建的并对这个文件进行操作,所以只需要关闭self.file
        self.file.close()
