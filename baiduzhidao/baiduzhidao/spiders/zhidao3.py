# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from baiduzhidao.items import BaiduzhidaoItem

class Zhidao3Spider(CrawlSpider):
    name = 'zhidao3'
    # allowed_domains = ['www.zhidao.baidu.com'] #域名别加www.加了出现了错误
    allowed_domains = ['zhidao.baidu.com']
    start_urls = ['https://zhidao.baidu.com/list?fr=daohang']

    rules = (
        Rule(LinkExtractor(allow=r'zhidao.baidu.com/question/'), callback='parse_item', follow=None),#这里的follow表示是否对符合这个规则提取到的url再进行提取，类似递归
    )

    def parse_item(self, response):
        print('-'*100)#并没有进入这个方法
        #后来测试是抓取元素失败  h1并不是class属性为qTitle 而是accuse属性
        name=response.xpath('//h1[@accuse="qTitle"]/span[@class="ask-title"]/text()').extract()[0]
        item=BaiduzhidaoItem()
        item['TitleName']=name
        yield item
