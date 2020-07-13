# -*- coding: utf-8 -*-
"""
测试抽取的代理ip的有效性,并将有效的ip写入Redis数据库
"""
import scrapy
from xici_procy.items import XiciProcyItem

class XiciproxySpider(scrapy.Spider):
    name = 'xiciproxy'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    #初始化函数的参数由命令行追加参数传入
    def __init__(self,url):#爬虫初始化还能传参
        self.testurl=url
        self.current_page=1
    def start_requests(self):
        url="https://www.xicidaili.com/nn"
        yield scrapy.Request(url,headers=self.headers)
    def parse(self, response):
        list_selector=response.xpath('//tr[@class="odd"]')
        for one_selector in list_selector:
            item=XiciProcyItem()
            ip=one_selector.xpath('td[2]/text()').extract()[0]
            port=one_selector.xpath('td[3]/text()').extract()[0]
            http=one_selector.xpath('td[6]/text()').extract()[0]
            url="{}://{}:{}".format(http.lower(),ip,port)#构造url字符串,带上端口
            item["url"]=url
            yield scrapy.Request(self.testurl,headers=self.headers,
                                meta={"proxy":url,"item":item},
                                callback=self.parse_xici,#访问成功才会执行回调函数
                                errback=self.error_back,#访问失败执行错误处理函数
                                dont_filter=True)#该参数时必须的,因为对同一个网站self.testurl发起了
                                #因为每个item中的url都是用self.testurl来进行测试的

        # if self.current_page<5:                                        #多次请求,爬虫是会过滤掉的,所以要将这个参数设置为True,默认是False
        #     next=response.xpath('//a[@class="next_page"]/@href').extract()[0]
        #     new_url="https://www.xicidaili.com{}".format(next)
        #     self.current_page+=1
        #     yield scrapy.Request(new_url,headers=self.headers)
    def parse_xici(self,response):
        #如何测试一个网站是否访问成功呢,不需要下面的if测试,因为只有成功访问才会执行回调函数
        yield response.meta["item"]#这行代码是什么用的 如果成功了会输出{'url': 'http://182.35.82.3:9999'}
        #request的meta参数主要用来传递数据    数据可以传递给对应的response的
        #比如,item中有一个字段url,你需要对url发起请求,获取其中的数据再存到先前的item中，这就需要从Request传递到response传递item
    def error_back(self,failure):
        #打印错误日志信息
        self.logger.error(repr(failure),"*"*60)#错误输出方法 不是在控制台输出的
