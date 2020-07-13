# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['su.lianjia.com']
    start_urls = ['http://su.lianjia.com/']

    def parse(self, response):
        pass
