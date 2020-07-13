# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html\
"""
我猜测,开启一个爬虫的时候,当抽取的数据被yield的时候，数据会经过pipes,也就是经过这里的管道,
每个管道类都会创建一个实例,优先级高的走完走优先级低的,item进入管道都是执行的item方法,每个管道类
中定义的__init__()应该都只会执行一次,之后对于每个经过的item都是调用同一个管道类实例的process_item(self,item,spider)来处理
open_spider(item,spider)方法在爬虫开启(爬取数据之前)就会执行
close_spider(item,spider)方法在爬虫关闭,所有数据爬取完毕的时候执行
"""
from scrapy.exceptions import DropItem
#其实这几个管道的功能都能写到一个管道类里,好像都不会出现矛盾，但是
#一个管道类最好只负责一个功能,遵循那个什么原则
class QidianHotPipeline(object):
    #管道处理item
    def process_item(self, item, spider):
        if item['form']=='连载':
            item['form']="LZ"
        else:
            item["form"]="WJ"
        return item
class DuplicatesPipeline(object):
    def __init__(self):
        self.author_set=set()#空集合不能{},必须是set()
    def process_item(self, item, spider):
        if item["author"] in self.author_set:
            raise DropItem("重复---------------") #会直接抛弃掉item,后面的管道也不会去走
        else:
            self.author_set.add(item["author"])
        return item
class SaveToTxtPipeLine(object):
    filename='hot.txt'
    file=None
    def open_spider(self,spider):
        self.file=open(self.filename,'a',encoding='utf-8')
    def process_item(self,item,spider):

        book=item['name']+','+item['author']+','+item['type']+','+item['form']+'\n'
        self.file.write(book)
        return item
    def close_spider(self,spider):
        self.file.close()
