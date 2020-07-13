# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy.http import HtmlResponse#而不是scrapy.Response,不存在scrapy.Response,scrapy.Request其实也是<class 'scrapy.http.request.Request'>
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #上面三行基本上都是一起导入的
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from scrapy import signals


class ToutiaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ToutiaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        if spider.name=="news":
            # print('*'*100)
            #这个函数可以处理爬虫发送的request,可以在这一步中请求对应的url,返回一个response,类似充当代理的角色
            #webdriver这里最大的作用就是执行一段JS代码并且获取源代码
            spider.driver.get(request.url)
            try:
                wait=WebDriverWait(spider.driver,10)
                #自己编写的时候一直获取不到数据,经过测试是因为此处的xpath书写错误,导致下一行代码出错,而直接跳转至错误处理了
                myres=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="wcommonFeed"]')))#注意这里的参数是元祖,可能能传入多个条件
                # print("*"*60)
                # print(myres.xpath("div/@mwidth"))#错误
                print("*"*60,type(myres))#myres是selenium中的一个WebElement对象,没有xpath属性,有send_keys方法
                                        #如果要对元素进行其他操作,需要
                # print('*'*100)
                # for i in range(5):
                #     #driver可以执行JS代码,把JS代码写成一个字符串就行了
                #     spider.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')#滚动至底部
                #     time.sleep(5)#每次鼠标移到最下面时会加载页面,等待5秒让页面加载完成
                #通过driver对象的page_source属性可以获取页面源代码
                origin_code=spider.driver.page_source
                #返回一个response给爬虫的parse函数,HtmlResponse的参数body传递源代码
                res=HtmlResponse(url=request.url,encoding='utf-8',body=origin_code,request=request)#针对这次请求返回一个响应response
                # print('*'*100)
                return res
            except TimeoutException:
                print("time out")
            except NoSuchElementException:
                print("no such element")
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None#如果爬虫名字不是news,返回None说明不操作这个请求,继续这个请求

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
