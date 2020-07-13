# -*- coding: utf-8 -*-
import scrapy
from seaborn_file_download.items import SeabornFileDownloadItem

class SeabornfileSpider(scrapy.Spider):
    name = 'seabornfile'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    def start_requests(self):
        url="http://seaborn.pydata.org/examples/index.html"
        yield scrapy.Request(url=url,headers=self.headers,callback=self.first_parse)
    def first_parse(self, response):
        selector_list=response.xpath('//div[@class="figure align-center"]')
        for selector in selector_list:
            link=selector.xpath('a/@href').extract()[0]
            #获得的link是相对地址
            new_url=response.urljoin(link)#response的url和link拼接,后者会根据它的./或者../对response的url进行拼接 一个表示当前文件夹,一个表示向上一层
            # print("new_url**************:",new_url)
            yield scrapy.Request(url=new_url,headers=self.headers,callback=self.second_parse)
    def second_parse(self,response):
        item=SeabornFileDownloadItem()
        file_link=response.xpath('//a[@class="reference download internal"]/@href').extract()[0]
        new_file_link=response.urljoin(file_link)
        # print("文件地址是*************:",new_file_link)
        item["file_urls"]=[new_file_link]#这里返回的要是一个列表形式,一个列表里可以有很多个url,
        yield item          #
                                        #传到管道的时候,文件管道会自动下载每一个url
