# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
scrapy中有下载文件和下载图片的管道类
"""
from scrapy.pipelines.images import ImagesPipeline
import scrapy
class ShetuImageDownloadPipeline(object):
    def process_item(self, item, spider):
        return item
class SaveImagePipeline(ImagesPipeline):
    #重写了下面这个方法从item["image_urls"]中下载一张张图片,同一个item中每张图片对应的title都是相同的
    def get_media_requests(self,item,info):#这个方法貌似可以return一个列表,列表元素是所有的请求,而不用这里的for循环
        for url in item["image_urls"]:      #重写这个方法我觉得主要是为了传递item["title"]
            yield scrapy.Request(url,meta={"title":item["title"]})
    #设置文件名(或者是 目录/文件名),默认是一个哈希值,这些都是在settings文件的IMAGES_STORE设置的目录下的
    def file_path(self,request,response=None,info=None):
        title=request.meta["title"]#前面的下载文件项目中文件名是从request.url中抽取的，所以不需要重写上面那个方法传递item["title"]
        image_name=request.url.split("/")[-1]
        return "%s/%s"%(title,image_name)
    #设置缩略图的路径,也是衔接在settings文件的IMAGES_STORE设置的目录下的,thumb_id与settings文件中IMAGES_THUMBS对应
    def thumb_path(self,request,thumb_id,response=None,info=None):
        title=request.meta["title"]
        image_name=request.url.split("/")[-1]
        return "%s/%s/%s"%(title,thumb_id,image_name)
