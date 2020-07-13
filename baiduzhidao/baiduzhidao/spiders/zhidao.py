# -*- coding: utf-8 -*-
"""
遇到最大的坑是scrapy.Request()中的cookies必须通过cookies传递，不像requests可以直接放在headers中
当我们使用requests的时候，一般可以直接把Cookies放在Headers里面，随着请求一并提交，
但是，如果使用Scrapy的时候需要Cookies，就不能把Cookies放在Headers里面。在Scrapy发起请求的时候，有一个单独的参数来设置Cookies：
并且， cookies参数的值为一个字典，需要把原来Chrome中的字符串Cookies，先按分号分为不同的段，每一段再根据等号拆分为key和value。
settings中的COOKIES_ENABLED参数默认是被注释的，说明不启用cookies,解除注释并且设置为Flase,说明开启cookie,但是不用scrapy内置的cookie,自己在
DEFAULT_REQUEST_HEADERS中设置的Cookie才会生效。如果设为True,则失败，不知道设为True有什么用
"""
import scrapy
from baiduzhidao.items import BaiduzhidaoItem

class ZhidaoSpider(scrapy.Spider):
    name = 'zhidao'
    # allowed_domains = ['www.zhidao.baidu.com']
    # start_urls = ['http://www.zhidao.baidu.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    def start_requests(self):
        url="https://zhidao.baidu.com/list?fr=daohang"
        yield scrapy.Request(url)
        # cookies='BIDUPSID=E815020B2450FB2C5A2A883D52C36950; PSTM=1534739412; BAIDUID=6C1F5B57817225D5683A81001322601C:FG=1; shitong_key_id=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; H_PS_PSSID=1444_21105_30210_18560_26350; PSINO=5; ZD_ENTRY=baidu; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1576134017,1576304600; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1576304603; shitong_data=fb93080e6adce017f657e0ac08cbe25e60e50f648057e4ed0cbf0c937382bc9ada75d54602143a25296db1947076de41a52a1b073f5753b85a1922f018747c57870191529937f0878becf1516b06b859a257d596477e9dde37d573ed84c1afcf8596ec0873bdf7742153361067a890dcc72ba37ecf6c2173f1617b36d916a7c4; shitong_sign=4c046287'
        # #cookies参数是一个字典或者列表，还需要自己构造
        # mycookies={}
        # for c in cookies.split(';'):
        #     mycookies[c.split('=')[0].strip()]=c.split('=')[1].strip()
        # yield scrapy.Request(url,cookies=mycookies,callback=self.parse)

    def parse(self, response):
        #主要问题还是response.text的问题
        # print(response,'*'*100)
        # print(response.text.find("question-list-item"),'*'*100)
        # ques_list=response.xpath('//ul[@class="question-list-ul"]/li[@class="question-list-item"]')
        ques_list=response.xpath('//ul[@class="question-list-ul"]/li[@class="question-list-item"]') #为什么抓不到元素
        # print(ques_list,'*'*100)
        # print(ques_list,'*'*100)
        item=BaiduzhidaoItem()
        for ques in ques_list:
            # print('*'*100)
            item["TitleName"]=ques.xpath('div[1]/div//a/text()').extract()[0]
            yield item  #因为是yield item ,才会一个个返回抓取的问题，如果是return 那么只返回第一个就结束了
