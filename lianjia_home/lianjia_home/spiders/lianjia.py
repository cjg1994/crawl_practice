# -*- coding: utf-8 -*-
"""
房屋名称 户型 面积 朝向 装修情况 有无电梯 房屋总价 房屋单价 房屋产权
"""

import scrapy
#要记住运行爬虫的主目录是在工程目录之下,工程目录下还有一个和工程名一样名字的文件夹
from lianjia_home.items import LianjiaHomeItem

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['su.lianjia.com']
    start_urls = ['http://su.lianjia.com/ershoufang/']

    def parse(self, response):
        url_list=response.xpath('//ul[@class="sellListContent"]/li/div/div[@class="title"]/a/@href').extract()
        #对每一个url都yield一个请求Request,然后执行对应的解析函数,完成一个url之后会回到这里,因为yield
        for url in url_list:
            yield scrapy.Request(url=url,callback=self.parse_new)
    def parse_new(self,response):
        #每个页面只抓取一个元素,并没有相同的元素,所以不像以往那样还有for循环
        item=LianjiaHomeItem()
        name=response.xpath('//div[@class="communityName"]/a[1]/text()').extract()[0]
        totalprice=response.xpath('//div[@class="overview"]/div[@class="content"]/div[@class="price "]/span[@class="total"]/text()').extract()[0]
        singleprice=response.xpath('//div[@class="overview"]/div[@class="content"]/div[@class="price "]/div/div/span/text()').extract()[0]
            infolist=response.xpath('//div[@class="introContent"]/div/div/ul/li/text()').extract()
        huxing=infolist[0]
        area=infolist[2]
        chaoxiang=infolist[6]
        zhuangxiu=infolist[8]
        dianti=infolist[10]
        years=infolist[11]
        #这里有个问题,有些房子信息部分指标是直接没有写(并没有写暂无数据,而是直接没有那一项),上面的定位可能会定位错信息
        item['name']=name
        item['totalprice']=totalprice
        item['singleprice']=singleprice
        item['huxing']=huxing
        item['area']=area
        item['chaoxiang']=chaoxiang
        item['zhuangxiu']=zhuangxiu
        item['dianti']=dianti
        item['years']=years
        yield item
