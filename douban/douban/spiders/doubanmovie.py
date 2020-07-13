# -*- coding: utf-8 -*-

"""
url是根据start=0 每次加20变化的
记得判定是否还继续爬取要用len判断字典中是否还有数据,而不能是根据是否还存在这个url,
因为即使把start改成很大的值,发现url是能访问的,只是movie_dict["data"]中没有数据了
"""
import scrapy
import json
from douban.items import DoubanItem

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    # allowed_domains = ['movie.douban.com']
    # start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86']
    count=1
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    def start_requests(self):
        yield scrapy.Request('https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=0&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86',headers=self.headers)

    def parse(self, response):
        #返回的是一个json数据 将其转换为python对象字典后进行操作
        movie_dict=json.loads(response.text)
        if len(movie_dict["data"])==0:
            return #可以停止爬虫
        for movie in movie_dict["data"]:
            item=DoubanItem()
            item["title"]=movie["title"]
            item["directors"]='-'.join(movie["directors"])
            item["casts"]='-'.join(movie["casts"])
            item["rate"]=movie["rate"]
            yield item
        next_page='https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86'.format(self.count*20)
        self.count+=1
        yield scrapy.Request(url=next_page,headers=self.headers)
