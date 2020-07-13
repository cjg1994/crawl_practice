# -*- coding: utf-8 -*-
import scrapy
from baidu.items import PersonInfoItem
#因为爬虫都是在工程名这个目录下执行的,所以导入的时候是baidu.items,此处的baidu是目录结构里的第二个baidu

class Exercise113Spider(scrapy.Spider):
    name = 'exercise11_3'
    allowed_domains = ['exercise.kingname.info']
    start_urls = ['http://exercise.kingname.info/exercise_xpath_3.html']

    def parse(self, response):
        elem_table=response.xpath('//div[@class="person_table"]/table')[0]
        tbody_tr_list=elem_table.xpath('tbody/tr')#这两行可以写成一行
        for elem in tbody_tr_list:
            item=PersonInfoItem()#类似一个字典结构数据
            text=elem.xpath('td/text()').extract()
            item['name']=text[0]
            item['age']=text[1]
            item['salary']=text[2]
            item['phone']=text[3]
            yield item #由parse解析函数返回item,会自动传到管道那里再进行处理
