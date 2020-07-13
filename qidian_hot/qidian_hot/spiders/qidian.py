# -*- coding: utf-8 -*-
import scrapy
from qidian_hot.items import QidianHotItem
from qidian_hot import settings
import redis  #类似pymongo,python用来操作redis的库,redis数据库有16个数据库db0,db1...db15 需要指明使用的是哪个数据库
class QidianSpider(scrapy.Spider):
    name = 'qidian'


    count=1
    #重写父类的__init__方法
    def __init__(self):
        #这里又通过.属性的方法调用settings文件里的变量,其实也可以用settings[""]的方式
        host=settings.REDIS_HOST
        port=settings.REDIS_PORT
        db_index=settings.REDIS_DB_INDEX
        #链接redis,这个服务必须开启,decode_responses参数我记得设置成True后读取的时候读取出来的就是字符串
        self.db_conn=redis.StrictRedis(host=host,port=port,db=db_index,decode_responses=True)

    def start_requests(self):
        url="https://www.qidian.com/rank/hotsales?page=1"
        #从数据库中产生一个随机ip
        #redis数据库 应该是从名称为 ip 的这个集合中随机取出一个值
        proxy=self.db_conn.srandmember("ip")
        print("随机代理:",proxy)
        #对request的meta属性的键proxy赋值实现代理,设置超时时间10秒,其实10秒没连上也说明这个代理ip有问题了
        #errback参数指明错误处理函数,如果请求超时了就会调用这个函数 疑问 爬虫出错会调用这个函数吗 等下测试一下 不会 只有请求超时
        yield scrapy.Request(url,meta={"proxy":proxy,"download_timeout":10},callback=self.parse,errback=self.error_parse)
    def parse(self, response):
        books=response.xpath('//div[@class="rank-body"]/div/div/ul/li')

        for book in books:
            item=QidianHotItem()
            name=book.xpath('div[2]/h4/a/text()').extract()[0]
            author=book.xpath('div[2]/p[1]/a/text()').extract()[0]
            type=book.xpath('div[2]/p[1]/a/text()').extract()[1]
            form=book.xpath('div[2]/p[1]/span/text()').extract()[0]
            item['name']=name
            item['author']=author
            item['type']=type
            item['form']=form
            yield item

        self.count+=1
        if self.count<=2:
            next_page='https://www.qidian.com/rank/hotsales?page={}'.format(self.count)
            proxy=self.db_conn.srandmember("ip")
            yield scrapy.Request(url=next_page,meta={"proxy":proxy,"download_timeout":10},callback=self.parse,errback=self.error_parse)
    #错误回调函数的参数 failure对象
    def error_parse(self,failure):
        #输出错误信息
        self.logger.error(repr(failure))
        #通过failure对象可以得到超时请求的url
        request=failure.request
        self.db_conn.srem("ip",request.meta["proxy"])#通过meta属性获取代理的url
        proxy=self.db_conn.srandmember("ip")#再重新选取一个代理ip
        #dont_filter参数需要设置,因为如果多个代理ip无效的话,这个请求会多次对同一url发起请求,所以要设置该参数
        #说明发起过请求的url会被忽略
        yield scrapy.Request(request.url,meta={"proxy":proxy,"download_timeout":10},callback=self.parse,errback=self.error_parse,dont_filter=True)
