# -*- coding: utf-8 -*-
"""
通过browsercookie可以获取chrome浏览器存在本地的各个网站的cookie对象,< Cookie key=value domain>
构造一个cookie字典,通过请求发送实现自动登录
"""

import scrapy
import browsercookie #browsercookie库的使用
from qidian_login.items import QidianLoginItem
cookie='Cookie: _csrfToken=W3JqtsH9COGyqaCjsvl3TgJe8E6YbrpcA2CAWen3; newstatisticUUID=1571035550_1737766613; ywkey=ywzElAb4Jnjy; ywguid=851000542593; ywopenid=A47F8ADC20F3492F392A7F56C0DBF5DB; e1=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22qd_M194%22%2C%22l3%22%3A1%2C%22l2%22%3A2%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22qd_M194%22%2C%22l3%22%3A1%2C%22l2%22%3A2%2C%22l1%22%3A3%7D'
class BookshelfSpider(scrapy.Spider):
    name = 'bookshelf'

    def __init__(self):
        cookiejar=browsercookie.chrome()#调用chrome方法,返回的是一个cookiejar.Cookiejar类
        self.cookie_dict={}
        for cookie in cookiejar:#cookiejar可以直接遍历,里面是一个个形如 <Cookie key=value domain>的cookie对象
                                #访问该对象的属性cookie.name cookie.value cookie.value
            if cookie.domain==".qidian.com":
                if cookie.name in ["_csrfToken",
                                "newstatisticUUID",
                                "ywkey",
                                "ywguid",
                                "ywopenid",
                                "e1",
                                "e2"] :
                    self.cookie_dict[cookie.name]=cookie.value
    def start_requests(self):
        url="https://my.qidian.com/bookcase?targetTab=tabTarget1" #个人书架的网址
        yield scrapy.Request(url,cookies=self.cookie_dict)
    def parse(self, response):
        book_list=response.xpath('//table[@id="shelfTable"]/tbody/tr')
        for book in book_list:
            item=QidianLoginItem()
            item["category"]=book.xpath('td[2]/span/b/a/text()').extract()[0]
            item["title"]=book.xpath('td[2]/span/b/a/text()').extract()[1]
            item["update"]=book.xpath('td[3]/text()').extract()[0]
            item["author"]=book.xpath('td[4]/a/text()').extract()[0]
            yield item
