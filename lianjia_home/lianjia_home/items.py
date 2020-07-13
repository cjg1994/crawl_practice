# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    totalprice=scrapy.Field()
    singleprice=scrapy.Field()
    huxing=scrapy.Field()
    area=scrapy.Field()
    chaoxiang=scrapy.Field()
    zhuangxiu=scrapy.Field()
    dianti=scrapy.Field()
    years=scrapy.Field()
