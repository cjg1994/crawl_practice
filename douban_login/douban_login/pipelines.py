# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
scrapy crawl login -o doulist.csv 这个命令行方法可以把item一行一行地写到scv文件中,而不需要这里构造csv文件写的对象
也可以将爬虫抽取的数据写入一个文件
但是自己编写的可以控制字段的排序
也就是可以决定"title","author","publishing_house"哪个写在前面,哪个写在后面
"""
import csv

class DoubanLoginPipeline(object):
    filename='doubanbook.csv'
    def open_spider(self,spider):
        self.file=open(self.filename,'w',encoding='utf-8')
        #csv还有一个读取csv文件的方法csv.DictReader 
        self.writer=csv.DictWriter(self.file,fieldnames=["title","author","publishing_house"])
        self.writer.writeheader()
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
    def close_spider(self,spider):
        self.file.close()
