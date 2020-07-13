# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from toutiao.items import ToutiaoItem
import re
import lxml.html
class NewsSpider(scrapy.Spider):
    name = 'news'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    # allowed_domains = ['toutiao.com']
    # start_urls = ['http://toutiao.com/']
    def __init__(self):
        #PhantomJS没有图形界面
        #这里是绝对路径,如果是相对路径的话要把这个文件放在工程的主目录下 toutiao\phantomjs.exe
        self.driver=webdriver.PhantomJS(r'C:\PhantomJS\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    def start_requests(self):
        url='https://www.toutiao.com/ch/news_hot/'
        yield scrapy.Request(url,headers=self.headers)
    def parse(self, response):
        #这里的response好像不是中间件中返回的HtmlResponse???看下一行
        #经过测试,中间件返回的HtmlResponse会传到这里的解析函数parse中
        #之前测试一直错误是因为中间件中xpath书写错误导致并没有返回HtmlResponse,而是print('错误消息')
        #说明是返回的None,说明并没有截断请求,response还是原页面的源代码,原页面是通过AJAX加载的,所以一直获取不到元素
        selector_list=response.xpath('//div[@class="wcommonFeed"]/ul/li')
        # print(selector_list,'*'*100)
        # print(len(response.text),'*'*100)
        for li in selector_list:
            try:
                item=ToutiaoItem()
                item["title"]=li.xpath('.//a[@class="link title"]/text()').extract()[0].strip()
                item["source"]=li.xpath('.//a[@class="lbtn source"]/text()').extract()[0].strip('·').strip()#这里的点号一直没去掉,可以尝试从源代码中把那个点复制粘贴出来试试
                comment=li.xpath('.//a[@class="lbtn comment"]/text()').extract()[0].strip()
                item["comment"]=re.findall('(\d+?)评论',comment)[0]
                yield item
            except:
                continue#如果出错了,就跳过这个item,继续下一个item的抽取
                        #每次抓取元素写入item的时候都可以这样做
