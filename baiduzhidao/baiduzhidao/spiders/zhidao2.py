# -*- coding: utf-8 -*-
"""
创建爬虫的时候 命令行加上-t crawl 自动创建模板
scrapy.contrib.spiders中的CrawlSpider  会自动从start_requests中返回的数据中提取符合自定义规则的url,并且对这些url发起请求，
对一类请求的回调函数callback需进行设置
使用与那种需要二次请求提取数据的情况

"""
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from baiduzhidao.items import BaiduzhidaoItem
class Zhidao2Spider(CrawlSpider):
    name = 'zhidao2'
    rules=(
        Rule(LinkExtractor(allow=r'zhidao.baidu.com/question/'), callback='parse_item'),
        )
    # allowed_domains = ['www.zhidao.baidu.com']
    # start_urls = ['https://zhidao.baidu.com/list?fr=daohang']
    def start_requests(self):
        url="https://zhidao.baidu.com/list?fr=daohang"
        cookies='BIDUPSID=E815020B2450FB2C5A2A883D52C36950; PSTM=1534739412; BAIDUID=6C1F5B57817225D5683A81001322601C:FG=1; shitong_key_id=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1444_21105_30210_18560_26350; PSINO=5; ZD_ENTRY=baidu; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1576134017,1576304600; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1576304603; shitong_data=fb93080e6adce017f657e0ac08cbe25e60e50f648057e4ed0cbf0c937382bc9ada75d54602143a25296db1947076de41a52a1b073f5753b85a1922f018747c57870191529937f0878becf1516b06b859a257d596477e9dde37d573ed84c1afcf8596ec0873bdf7742153361067a890dcc72ba37ecf6c2173f1617b36d916a7c4; shitong_sign=4c046287'
        mycookies={}
        # print('*'*100)#到这里都是没错的
        for c in cookies.split(';'):
            mycookies[c.split('=')[0].strip()]=c.split('=')[1].strip()
        yield scrapy.Request(url,cookies=mycookies)

    def parse_item(self, response):
        print('-'*100)#并没有进入这个方法
        #改动rules后进入了这个方法，但是提取元素出错，猜测还是自动发起的那一系列请求没有携带cookies
        #改动设置文件可以设置默认cookie，继续测试  发现还是找不到元素 但是确实是根据rules的规则提取的url发起了二次请求
        name=response.xpath('//h1[@accuse="qTitle"]/span[@class="ask-title"]/text()').extract()[0]
        item=BaiduzhidaoItem()
        item['TitleName']=name
        yield item
