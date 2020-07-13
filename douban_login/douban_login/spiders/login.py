# -*- coding: utf-8 -*-
"""
遇到的主要问题是个人主页界面是登录以后才可以访问的,而我为了测试xpath的正确与否,直接拿了个人主页的url进行测试,
一直获取不到元素,并不是因为写错了xpath,而是因为必须要登录以后才能访问,没登录就测试是错误的.
后来补充:也就是你获取某些网页的时候是必需登录之后才能获取的,如果没登录直接获取URL的话,Response会是一个标明了403的错误
"""
import scrapy
import json

from douban_login.items import  DoubanLoginItem
class LoginSpider(scrapy.Spider):
    name = 'login'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    def start_requests(self):
        url='https://accounts.douban.com/j/mobile/login/basic'
        #表单数据传递的是什么就要写,像下面的空值也是要传递的
        data={
            "ck": "",
            "name": "15757116151",
            "password": "",
            "remember": "true",
            "ticket": ""
        }
        #这里Request的类型是FormRequest,formdata参数传递表单数据data
        yield scrapy.FormRequest(url,formdata=data,method="POST",headers=self.headers)
    def parse(self, response):
        #返回的reponse是一个json数据,用来表示是否成功
        result=json.loads(response.text)
        if result["status"]=="success":
            url='https://www.douban.com/doulist/120579697/'
            #需要自己做一个跳转 发送请求, 表明了解析函数
            yield scrapy.Request(url,callback=self.parse_doulist,headers=self.headers)
        else:
            self.logger.info("用户名或密码错误")#这个方法是输出错误信息吗

    def parse_doulist(self,response):
        books=response.xpath('//div[@class="article"]/div[@class="doulist-item"]')
        #item实例可以放在for循环中,放在外面也行,相当于不重新构建实例，只是每次改变实例的属性
        item=DoubanLoginItem()
        for book in books:
            item["title"]=book.xpath('div/div/div[@class="title"]/a/text()').extract()[0].strip()
            info_list=book.xpath('div/div/div[@class="abstract"]/text()').extract()#<br>标签把div下的文本分成了3个文本节点
            #上一行的表述其实不是特别准确,只是如果没有br 则是一个单独的文本节点
            #文本中包含了<br>标签的情况,说明<br>标签也是一个子节点,和文本节点并列
            item["author"]=info_list[0].strip().replace('作者:','')
            item["publishing_house"]=info_list[1].strip().replace('出版社:','')
            # re.findall('作者:(.*?)')
            # print(author)
            yield item
