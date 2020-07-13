# -*- coding: utf-8 -*-
import scrapy


class Exercise111Spider(scrapy.Spider):
    name = 'exercise11_1'
    #allowed_domains只会爬取这个域名下的url  可以删除
    allowed_domains = ['exercise.kingname.info']#注释掉这行
    #这个参数也测试过,如果有多个url需要爬取,可以写到这个列表里,但是爬取的顺序还有待确定,基本不用这个变量,都是在回调函数中再发起请求
    start_urls = ['http://exercise.kingname.info/exercise_xpath_1.html']

    def parse(self, response):

        url="http://baidu.com/"
        name_list=response.xpath('//li[@class="name"]/text()').extract()
        price_list=response.xpath('//li[@class="price"]/text()').extract()

        for x,y in zip(name_list,price_list):
            print('名称:{}  价格:{}'.format(x,y))
            print("-"*100)
        print("-"*50,self.count)

        yield scrapy.Request(url,callback=self.parse_my)#因为allowed_domains的存在这个请求会被过滤,
                                                #如果去掉allowed_domains,那么百度网页也可以爬去下来
    def parse_my(self,response):
        print(response.text)
