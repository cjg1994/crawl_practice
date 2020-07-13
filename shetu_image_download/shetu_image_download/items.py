# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShetuImageDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls=scrapy.Field()
    images=scrapy.Field()  #前面两个变量名的名字是固定的
    title=scrapy.Field() #这个是下载图片时额外要获取的数据,可以自定义名字
