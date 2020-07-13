from scrapy.spiders import Spider
from scrapy import Request
import re
import os

class SitesSpider(Spider):
    name="sites"

    def start_requests(self):
        url="https://www.12306.cn/index/script/core/common/station_name_v10043.js"
        yield Request(url)

    def parse(self,response):
        sites=re.findall(r"([\u4e00-\u9fa5]+)\|([A-Z]+)",response.text)
        if(os.path.exists("sites.txt")):
            os.remove("sites.txt")
        with open("sites.txt","a",encoding="utf-8") as f:
            for site_name,site_code in sites:
                f.write(site_name+":"+site_code+"\n")#write函数传入一个\n实现换行
