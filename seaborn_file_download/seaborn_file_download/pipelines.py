# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline

class SeabornFileDownloadPipeline(object):
    def process_item(self, item, spider):
        return item

#保存文件的管道,需要在settings文件中注明FILES_STORE变量
#下面自定义了文件名 这一个个文件保存的都是什么数据 item吗  保存的是一个个url所对应的文件
#结合items.py文件,item["file_urls"]是一个url列表,可能是一个值,可能有多个值,这个项目里一个值,但也要写成列表形式
#每一个url对应的文件都会由下面的管道进行下载
class SaveFilePipeline(FilesPipeline):
    #重写这个方法自定义文件名(自定义的目录/自定义文件名),原来是在./examples/full/下下载文件的,重写这个方法之后是在设置的./examples下下载文件
    #没有了full文件夹,说明父类中此方法默认是创建了full目录
    def file_path(self,request,response=None,info=None):#这里的request是对item["file_urls"]中的url发起的请求
        # name=request.url.split('/')[-1]
        file_name=request.url.split('/')[-1]
        foleder_name=file_name.split('.')[0]
        return foleder_name+'/'+file_name
