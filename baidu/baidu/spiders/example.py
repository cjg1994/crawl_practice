# -*- coding: utf-8 -*-
# from selenium import webdriver #这里的webdriver是小写的
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC #上面三行基本上都是一起导入的
                                    #主要测试WebDriverWait().until(EC.presence_of_element_located())是否返回对应的元素
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # def __init__(self):
    #     self.driver=webdriver.PhantomJS(r'C:\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    #执行爬虫的时候会先执行一次这个方法,原来是继承父类的,这里重写了这个方法,自己发送了请求
    def start_requests(self):
        url="http://baidu.com/"
        # self.driver.get(url)
        #url="http://baisssdu.com/"#对三个错误进行单独的测试,说明errback参数只有在请求超时请求不到的时候才会回调函数
        # print(1/0)
        # page=self.driver.page_source
        # res=HtmlResponse(url=url,encoding='utf-8',body=page)
        # yield res
        yield scrapy.Request(url,callback=self.parse_my,errback=self.parse_myerror)  #只能是yield,不能是return
    def parse_my(self, response):
        # print(1/0)#这里故意抛出一个错误 观察会不会调用回调函数errback
        print(response.body.decode())#reponse.text
    def parse_myerror(self,failure):
        print("-"*100)
