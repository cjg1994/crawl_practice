# -*- coding: utf-8 -*-
import scrapy
from shetu_image_download.items import ShetuImageDownloadItem

class ShetuSpider(scrapy.Spider):
    name = 'shetu'

    def start_requests(self):
        url="http://699pic.com/photo/"
        yield scrapy.Request(url)
    def parse(self, response):
        selector_list=response.xpath('//div[@class="pl-list"]')
        for selector in selector_list:
            href=selector.xpath('a[1]/@href').extract()[0]
            yield scrapy.Request(href,callback=self.parse_image)
            break#单元测试
    def parse_image(self,response):
        # url_list=response.xpath('//ul[@class="swipeboxEx clearfix"]/li/a/img/@src').extract()#用src属性获取不到是为什么
        url_list=response.xpath('//ul[@class="swipeboxEx clearfix"]/li/a/img/@data-original').extract()
        if url_list:#因为上面循环中的url中内容结构并非一个模板,有些获取不到url_list的，所以这里要用if
                #这应该是是第一次爬取遇到错误才发现的
            item=ShetuImageDownloadItem()
            item["image_urls"]=url_list #这里就是一个列表,里面有很多元素,不同于之前下载文件,只有一个url,但也要写成列表
            item["title"]=response.xpath('//ul[@class="swipeboxEx clearfix"]/li/a/img/@title').extract_first()
            #.extract_first()代替了.extract()[0]
            #一个item["title"]对应一个item["image_urls"],也就是对应了很多个url,管道中设置文件目录时会用到
            yield item
