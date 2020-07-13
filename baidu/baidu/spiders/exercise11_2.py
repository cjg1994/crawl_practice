# -*- coding: utf-8 -*-
import scrapy


class Exercise112Spider(scrapy.Spider):
    name = 'exercise11_2'
    allowed_domains = ['exercise.kingname.info']
    start_urls = ['http://exercise.kingname.info/exercise_xpath_2.html',"http://exercise.kingname.info/exercise_xpath_1.html","http://baidu.com/"]

    def parse(self, response):
        # print("---"*30)
        shangpin_list=response.xpath('//ul[@class="item"]')
        for elem in shangpin_list:
            # print(type(elem.xpath('li[@class="name"]/text()')))
            name=elem.xpath('li[@class="name"]/text()').extract()
            price=elem.xpath('li[@class="price"]/text()').extract()
            name=name[0] if name else 'N/A'
            price=price[0] if price else 'N/A'
            print('名称:{}  价格:{}'.format(name,price))
