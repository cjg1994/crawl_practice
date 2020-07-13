# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
"""
如果要下载文件,下面的file_urls和files是固定写法
"""

import scrapy


class SeabornFileDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls=scrapy.Field()#要下载的文件的url
    files=scrapy.Field() #这两个变量名是固定的,会自动下载url对应的文件
