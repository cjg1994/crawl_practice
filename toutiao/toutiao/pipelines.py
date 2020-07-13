# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class ToutiaoPipeline(object):
    filename="toutiao.csv"
    def open_spider(self,spider):
        self.file=open(self.filename,'a',encoding='utf-8')
        self.writer=csv.DictWriter(self.file,fieldnames=["title","source","comment"])
        self.writer.writeheader()
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
    def close_spider(self,spider):
        self.file.close()#这一步感觉也是需要的,关闭文件,让缓冲区的数据写入文件.
