# -*- coding: utf-8 -*-
import scrapy
from cnblogSpider.items import CnblogspiderItem
import re
class CnblogsSpiderSpider(scrapy.Spider):
    name = 'cnblogs_spider'
    allowed_domains = ['cnblogs.com']
    start_urls = ['http://cnblogs.com/qiyeboy/default.html?page=1']

    def parse(self, response):
        #首先抽取每篇文章的一大块,这种抽取方法较好,不像那种把每个抽取对象单独抽取成一个列表之后再整理

        papers=response.xpath('//div[@class="day"]')
        for paper in papers:
            url=paper.xpath('div[@class="postTitle"]/a/@href').extract()[0]
            title=paper.xpath('div[@class="postTitle"]/a/text()').extract()[0]
            time=paper.xpath('div[@class="dayTitle"]/a/text()').extract()[0]
            content=paper.xpath('div[@class="postCon"]/div/text()').extract()[0]
            # print(url,title,time,content)
            #item的另一种构造方法
            item=CnblogspiderItem(url=url,title=title,time=time,content=content)#也可以item=CnblogspiderItem(),再按照字典键的方法添加
            yield item
        # print(response.text.find('下一页'))
        #re.S不是必要的 使
        # *是匹配一次或者多次 用“a”去匹配"  aab"得到的是'' 因为匹配到的空格也是满足条件的  很少这样用吧
        #\s 匹配空字符
        #\S 匹配非空字符
        #可以用scrapy shell url 单独测试xpath等匹配是否正确
        next_page=re.search('<a href="(\S*?)">\s*下一页\s*</a>',response.text,re.S).group(1)

        # print('='*80)
        #会自动爬取后面的url
        #判定如果还有页面需要爬取
        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse)
