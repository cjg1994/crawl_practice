# -*- coding: utf-8 -*-
import scrapy
import json
from QQMusic.items import QqmusicItem

class QqmusicSpider(scrapy.Spider):
    name = 'qqmusic'
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
    def start_requests(self):
        url="https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI40323794911615374&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A4%2C%22offset%22%3A0%2C%22num%22%3A20%2C%22period%22%3A%222019-10-16%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
        yield scrapy.Request(url=url,headers=self.headers)

    def parse(self, response):
        songs_dict=json.loads(response.text)
        songs_list=songs_dict["detail"]["data"]["songInfoList"]
        for song in songs_list:
            item=QqmusicItem()
            item["song_name"]=song["name"]
            item["singer_name"]=song["singer"][0]["name"]
            item["album_name"]=song["album"]["name"]
            item["interval"]=song["interval"]
            yield item
