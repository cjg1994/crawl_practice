# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import csv

class LianjiaHomePipeline(object):
    def process_item(self, item, spider):
        #这个函数处理item,item可以当做是一个字典
        #下一步遍历字典的键
        for i in item:
            if item[i] =="暂无数据":
                raise DropItem("is N/A") #抛出DropItem,会丢弃掉这个item,下面的管道就不会执行了
        return item

#自己创建的一个管道类,需要在settings里启用
#如果上面那个管道没有丢弃item,就会执行下面的管道,写入文件.
class SaveToCsvPipeLine(object):
    filename="home.csv"

    def open_spider(self,spider):
        self.file=open(self.filename,'a',encoding='utf-8')
        self.writer=csv.DictWriter(self.file,fieldnames=["name","totalprice","singleprice","huxing","area","chaoxiang","zhuangxiu","dianti","years"])
        self.writer.writeheader()
    def process_item(self,item,spider):
        self.writer.writerow(item)
        return item
    def close_spider(self,spider):
        self.file.close()
