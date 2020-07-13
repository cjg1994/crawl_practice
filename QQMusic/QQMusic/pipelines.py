# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class QqmusicPipeline(object):
    filename="qqmusic.csv"
    def open_spider(self,spider):
        self.file=open(self.filename,'a',encoding="utf-8")
        self.writer=csv.DictWriter(self.file,fieldnames=["song_name","album_name","singer_name","interval"])
        self.writer.writeheader()
    def process_item(self, item, spider):
        info=dict(item)
        self.writer.writerow(info)
        return item
    def close_spider(self,spider):
        self.file.close()
